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

import {
	downloadArtifact,
	listFiles,
	plot as runPlot,
	repl as runRepl,
	uploadFile,
	MatlabApiError,
	type FileInfo
} from '$lib/api/matlabApi';

export interface WorkspaceVariable {
	/** Variable name as it appears in the MATLAB workspace. */
	name: string;
	/** Human-readable shape — ``5x5``, ``1x1``, ``200x3`` etc. */
	size: string;
	/** Class label — ``double``, ``logical``, ``char``, ``struct`` … */
	klass: string;
}

/**
 * Parse the stdout of a MATLAB ``whos`` call. Format observed on
 * matlab-llvm (slightly leaner than classic MATLAB — no Bytes
 * column):
 *
 * ```
 *   Name             Size             Class
 *   A                5x5              double
 *   b                1x1              double
 * ```
 *
 * Lines outside that shape (errors / blank / header) are skipped.
 * Exported for unit testing.
 */
export function parseWhos(stdout: string): WorkspaceVariable[] {
	const rows: WorkspaceVariable[] = [];
	for (const raw of stdout.split('\n')) {
		const line = raw.trim();
		if (!line) continue;
		// Skip the column header line (case-insensitive).
		if (/^name\s+size\s+class/i.test(line)) continue;
		// 3+ whitespace-separated columns, name first.
		const parts = line.split(/\s+/);
		if (parts.length < 3) continue;
		const [name, size, klass, ...rest] = parts;
		// Defensive: skip lines that don't look like a MATLAB identifier.
		if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(name)) continue;
		rows.push({
			name,
			size,
			klass: [klass, ...rest].join(' ')
		});
	}
	return rows;
}

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
	/** Live MATLAB workspace — refreshed via ``whos`` after each
	 *  successful REPL turn, and on demand via ``refreshWorkspace()``. */
	readonly workspaceVariables: WorkspaceVariable[];
	/** Files in the session's workspace dir. Refreshed at the same
	 *  cadence as variables. */
	readonly workspaceFiles: FileInfo[];
	/** True while a workspace refresh is in flight (variables OR files). */
	readonly workspaceLoading: boolean;
	/** Non-empty when the most recent refresh failed; surfaced in the
	 *  side panel as a small banner. */
	readonly workspaceError: string | null;

	setInput(value: string): void;
	submitRepl(): Promise<void>;
	submitPlot(): Promise<void>;
	resetSession(): void;
	clearCells(): void;

	/** Refresh both variables (via ``whos``) and files (via
	 *  /v1/files) in parallel. Called automatically after each
	 *  successful turn; also exposed for an explicit refresh button. */
	refreshWorkspace(): Promise<void>;

	/** Insert ``snippet`` at the cursor in the prompt textarea. Used
	 *  by Variables-panel click handlers (``disp(name)``, etc.). */
	appendToInput(snippet: string): void;

	/** Download a workspace file into the user's browser. */
	downloadWorkspaceFile(path: string): Promise<void>;

	/** Upload a file from the user's machine into the workspace. */
	uploadWorkspaceFile(file: File): Promise<void>;
}

export function createMatlabTerminalVM(): MatlabTerminalViewModel {
	let cells = $state<MatlabCell[]>([]);
	let input = $state<string>('');
	let running = $state<boolean>(false);
	let sessionId = $state<string>(randomSessionId());
	let workspaceVariables = $state<WorkspaceVariable[]>([]);
	let workspaceFiles = $state<FileInfo[]>([]);
	let workspaceLoading = $state<boolean>(false);
	let workspaceError = $state<string | null>(null);
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
		// Pass the active sessionId so the upstream resolves to the
		// right workspace (not the default one) when streaming the file.
		const settled = await Promise.allSettled(
			paths.map((p) => downloadArtifact(p, sessionId))
		);
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
			// Route to /v1/plot when the user explicitly asked for a plot,
			// or when their Run source clearly intends to draw — the
			// upstream endpoint owns saveas, so we don't need to inject
			// it. Otherwise stay on /v1/repl for ordinary REPL turns.
			// Both endpoints return the same JSON shape and share the
			// stateful workspace (matlab_llvm#55 + #56).
			const usePlot = mode === 'plot' || looksLikePlot(trimmed);
			const response = usePlot
				? await runPlot({ source: trimmed, session_id: sessionId, format: 'png' })
				: await runRepl({ source: trimmed, session_id: sessionId, stateful: true });

			const downloaded = await downloadAllArtifacts(response.artifacts ?? []);

			patchCell(cell.id, {
				status: response.ok ? 'ok' : 'error',
				stdout: response.stdout ?? '',
				stderr: response.stderr ?? '',
				plots: downloaded.plots,
				artifactErrors: downloaded.errors,
				// Surface "auto-plotted" when the user pressed Run but we
				// routed to /v1/plot — the UI shows a small "+plot" badge.
				plotFallback: mode === 'repl' && usePlot,
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
			// Auto-refresh workspace after a turn so the side panel
			// reflects new variables / files. Failures are silenced —
			// we surface them via workspaceError but don't block.
			void refreshWorkspace();
		}
	}

	/**
	 * Pull the current MATLAB workspace state in parallel:
	 *   - variables: a side ``whos`` call into the same session
	 *   - files: /v1/files listing for the same session_id
	 *
	 * Concurrent invocations are coalesced (only one in-flight refresh
	 * at a time) so a rapid string of REPL turns doesn't queue up
	 * redundant work.
	 */
	let refreshInflight: Promise<void> | null = null;
	async function refreshWorkspace(): Promise<void> {
		if (refreshInflight) return refreshInflight;
		refreshInflight = (async () => {
			workspaceLoading = true;
			try {
				const [whosResult, filesResult] = await Promise.allSettled([
					runRepl({ source: 'whos', session_id: sessionId, stateful: true }),
					listFiles(sessionId)
				]);

				const errs: string[] = [];

				if (whosResult.status === 'fulfilled') {
					workspaceVariables = parseWhos(whosResult.value.stdout ?? '');
				} else {
					errs.push(
						`whos: ${
							whosResult.reason instanceof Error
								? whosResult.reason.message
								: String(whosResult.reason)
						}`
					);
				}

				if (filesResult.status === 'fulfilled') {
					workspaceFiles = filesResult.value;
				} else {
					errs.push(
						`files: ${
							filesResult.reason instanceof Error
								? filesResult.reason.message
								: String(filesResult.reason)
						}`
					);
				}

				workspaceError = errs.length > 0 ? errs.join(' · ') : null;
			} finally {
				workspaceLoading = false;
				refreshInflight = null;
			}
		})();
		return refreshInflight;
	}

	async function downloadWorkspaceFile(path: string): Promise<void> {
		try {
			const { url, contentType: _ct, bytes: _b } = await downloadArtifact(path, sessionId);
			// Trigger a browser-side download via a hidden anchor.
			const anchor = document.createElement('a');
			anchor.href = url;
			anchor.download = path.split('/').pop() ?? path;
			document.body.appendChild(anchor);
			anchor.click();
			document.body.removeChild(anchor);
			// The blob URL stays alive long enough for the download to
			// initiate; revoke after a tick so subsequent clicks still
			// work if the browser hasn't started the transfer yet.
			setTimeout(() => URL.revokeObjectURL(url), 30_000);
		} catch (err) {
			workspaceError = err instanceof Error ? err.message : String(err);
		}
	}

	async function uploadWorkspaceFile(file: File): Promise<void> {
		try {
			workspaceLoading = true;
			await uploadFile(file, file.name, sessionId);
			// Re-list immediately so the new file appears in the panel.
			workspaceFiles = await listFiles(sessionId);
			workspaceError = null;
		} catch (err) {
			workspaceError = err instanceof Error ? err.message : String(err);
		} finally {
			workspaceLoading = false;
		}
	}

	return {
		get cells() { return cells; },
		get input() { return input; },
		get running() { return running; },
		get sessionId() { return sessionId; },
		get workspaceVariables() { return workspaceVariables; },
		get workspaceFiles() { return workspaceFiles; },
		get workspaceLoading() { return workspaceLoading; },
		get workspaceError() { return workspaceError; },
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
			workspaceVariables = [];
			workspaceFiles = [];
			workspaceError = null;
		},
		clearCells: () => {
			for (const c of cells) revokeCellPlots(c);
			cells = [];
			nextCellId = 1;
		},
		refreshWorkspace,
		appendToInput: (snippet) => {
			const sep = input.length > 0 && !input.endsWith('\n') ? '\n' : '';
			input = `${input}${sep}${snippet}`;
		},
		downloadWorkspaceFile,
		uploadWorkspaceFile
	};
}
