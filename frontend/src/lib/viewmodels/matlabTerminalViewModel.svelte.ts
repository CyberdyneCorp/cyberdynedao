/**
 * MATLAB REPL terminal view-model.
 *
 * Owns the cell history (each Run / Plot click pushes one cell) and
 * orchestrates the API call → artifact download → cell update flow.
 *
 * Session strategy:
 *   - One random `session_id` per VM instance so two open MATLAB
 *     windows have isolated workspaces.
 *   - `stateful: true` on every REPL call so `x = 1; disp(x)` works
 *     across cells.
 *
 * Plot artifacts come back as server-side paths; we GET them through
 * `/api/matlab/v1/files/{path}` and stash an `URL.createObjectURL`
 * blob URL per artifact, surfaced inline in the cell. When a cell is
 * cleared (or the VM destroyed) we `URL.revokeObjectURL` to release
 * memory — long REPL sessions otherwise accumulate megabytes of
 * forgotten PNGs in the browser.
 */

import { downloadArtifact, plot as runPlot, repl as runRepl, MatlabApiError } from '$lib/api/matlabApi';

export interface MatlabPlot {
	url: string;
	contentType: string;
	bytes: number;
}

export type CellStatus = 'running' | 'ok' | 'error';

export interface MatlabCell {
	id: number;
	mode: 'repl' | 'plot';
	/** True when the cell was a Run that auto-fell-back to /v1/plot. */
	plotFallback: boolean;
	source: string;
	status: CellStatus;
	stdout: string;
	stderr: string;
	error: string | null;
	plots: MatlabPlot[];
	/** Non-empty when one or more artifact downloads failed; surfaced
	 *  in the cell so the user knows why the plot is missing. */
	artifactErrors: string[];
	timedOut: boolean;
	truncated: boolean;
	startedAt: number;
	finishedAt: number | null;
}

/**
 * Heuristic: does this MATLAB source look like it's trying to draw?
 * Matches the common 2D/3D plotting verbs at the start of an expression
 * or after a newline / semicolon. Used to auto-route Run → Plot so the
 * user doesn't have to know which endpoint to call.
 */
const PLOT_VERB = /(^|[\s;])(plot|plot3|figure|imshow|imagesc|surf|mesh|contour|contourf|histogram|bar|barh|scatter|scatter3|stem|stairs|loglog|semilogx|semilogy|polar|polarplot|pie|area|heatmap|fplot|fsurf|fmesh|quiver|quiver3|geoplot|geoscatter|plotmatrix|spy)\s*\(/i;
export function looksLikePlot(source: string): boolean {
	return PLOT_VERB.test(source);
}

function randomSessionId(): string {
	// crypto.randomUUID is available in jsdom + every browser we ship to.
	if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
		return `web-${crypto.randomUUID()}`;
	}
	return `web-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export interface MatlabTerminalViewModel {
	readonly cells: MatlabCell[];
	readonly input: string;
	readonly running: boolean;
	readonly sessionId: string;
	setInput(value: string): void;
	submitRepl(): Promise<void>;
	submitPlot(): Promise<void>;
	resetSession(): void;
	clearCells(): void;
}

export function createMatlabTerminalVM(): MatlabTerminalViewModel {
	let cells = $state<MatlabCell[]>([]);
	let input = $state<string>('');
	let running = $state<boolean>(false);
	let sessionId = $state<string>(randomSessionId());
	let nextCellId = 1;

	function appendCell(mode: 'repl' | 'plot', source: string): MatlabCell {
		const cell: MatlabCell = {
			id: nextCellId++,
			mode,
			plotFallback: false,
			source,
			status: 'running',
			stdout: '',
			stderr: '',
			error: null,
			plots: [],
			artifactErrors: [],
			timedOut: false,
			truncated: false,
			startedAt: Date.now(),
			finishedAt: null
		};
		cells = [...cells, cell];
		return cell;
	}

	async function downloadAllArtifacts(
		paths: string[]
	): Promise<{ plots: MatlabPlot[]; errors: string[] }> {
		const plots: MatlabPlot[] = [];
		const errors: string[] = [];
		if (paths.length === 0) return { plots, errors };
		const settled = await Promise.allSettled(paths.map((p) => downloadArtifact(p)));
		settled.forEach((r, i) => {
			if (r.status === 'fulfilled') {
				plots.push(r.value);
			} else {
				const reason = r.reason instanceof Error ? r.reason.message : String(r.reason);
				errors.push(`${paths[i]}: ${reason}`);
			}
		});
		return { plots, errors };
	}

	function patchCell(id: number, patch: Partial<MatlabCell>): void {
		cells = cells.map((c) => (c.id === id ? { ...c, ...patch } : c));
	}

	function revokeCellPlots(cell: MatlabCell): void {
		for (const p of cell.plots) {
			try {
				URL.revokeObjectURL(p.url);
			} catch {
				/* ignore */
			}
		}
	}

	async function runOne(mode: 'repl' | 'plot', source: string): Promise<void> {
		const trimmed = source.trim();
		if (trimmed === '' || running) return;
		running = true;
		input = '';
		const cell = appendCell(mode, trimmed);
		try {
			const fn = mode === 'plot' ? runPlot : runRepl;
			const response = await fn({ source: trimmed, session_id: sessionId, stateful: true });

			const downloaded = await downloadAllArtifacts(response.artifacts ?? []);
			let plots = downloaded.plots;
			const artifactErrors = [...downloaded.errors];
			let plotFallback = false;
			let extraStderr = '';

			// Auto-fallback: if Run produced no figure but the source
			// looks like a plot call, transparently retry through
			// /v1/plot in the same session. MATLAB's /v1/repl doesn't
			// auto-saveas — the user shouldn't have to know that.
			if (
				mode === 'repl' &&
				response.ok &&
				plots.length === 0 &&
				looksLikePlot(trimmed)
			) {
				try {
					const plotResponse = await runPlot({
						source: trimmed,
						session_id: sessionId,
						format: 'png'
					});
					const fallback = await downloadAllArtifacts(plotResponse.artifacts ?? []);
					if (fallback.plots.length > 0) {
						plots = fallback.plots;
						plotFallback = true;
					}
					artifactErrors.push(...fallback.errors);
					if (plotResponse.stderr) {
						extraStderr = plotResponse.stderr;
					}
				} catch (fallbackErr) {
					const msg =
						fallbackErr instanceof Error ? fallbackErr.message : String(fallbackErr);
					artifactErrors.push(`plot fallback failed: ${msg}`);
				}
			}

			patchCell(cell.id, {
				status: response.ok ? 'ok' : 'error',
				stdout: response.stdout ?? '',
				stderr: [response.stderr ?? '', extraStderr].filter(Boolean).join('\n').trim(),
				plots,
				artifactErrors,
				plotFallback,
				timedOut: response.timed_out ?? false,
				truncated: response.truncated ?? false,
				finishedAt: Date.now()
			});
		} catch (err) {
			const message =
				err instanceof MatlabApiError
					? `${err.status === 401 ? 'Sign in required — ' : ''}${err.message}`
					: err instanceof Error
						? err.message
						: String(err);
			patchCell(cell.id, {
				status: 'error',
				error: message,
				finishedAt: Date.now()
			});
		} finally {
			running = false;
		}
	}

	return {
		get cells() { return cells; },
		get input() { return input; },
		get running() { return running; },
		get sessionId() { return sessionId; },
		setInput: (value) => {
			input = value;
		},
		submitRepl: () => runOne('repl', input),
		submitPlot: () => runOne('plot', input),
		resetSession: () => {
			for (const c of cells) revokeCellPlots(c);
			cells = [];
			sessionId = randomSessionId();
			nextCellId = 1;
		},
		clearCells: () => {
			for (const c of cells) revokeCellPlots(c);
			cells = [];
			nextCellId = 1;
		}
	};
}
