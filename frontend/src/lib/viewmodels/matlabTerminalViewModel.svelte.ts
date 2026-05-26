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
	source: string;
	status: CellStatus;
	stdout: string;
	stderr: string;
	error: string | null;
	plots: MatlabPlot[];
	timedOut: boolean;
	truncated: boolean;
	startedAt: number;
	finishedAt: number | null;
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
			source,
			status: 'running',
			stdout: '',
			stderr: '',
			error: null,
			plots: [],
			timedOut: false,
			truncated: false,
			startedAt: Date.now(),
			finishedAt: null
		};
		cells = [...cells, cell];
		return cell;
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

			// Download every artifact in parallel; collect plots that
			// actually decoded.
			const plots: MatlabPlot[] = [];
			if (response.artifacts && response.artifacts.length > 0) {
				const settled = await Promise.allSettled(
					response.artifacts.map((path) => downloadArtifact(path))
				);
				for (const r of settled) {
					if (r.status === 'fulfilled') plots.push(r.value);
				}
			}

			patchCell(cell.id, {
				status: response.ok ? 'ok' : 'error',
				stdout: response.stdout ?? '',
				stderr: response.stderr ?? '',
				plots,
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
