/**
 * Python interpreter REPL view-model.
 *
 * Owns the cell history (each Run pushes one cell) and the session
 * workspace file list. Mirrors the MATLAB terminal VM, but the
 * interpreter's `/execute` returns the full post-run workspace listing
 * in `artifacts`, so we use that to keep the Files panel current without
 * a separate listing round-trip.
 *
 * Session strategy: one random `session_id` per VM instance so two open
 * windows have isolated workspaces. The backend creates the workspace
 * lazily on first `/execute` (or `/files` upload) with that id.
 *
 * Image artifacts are fetched through `/api/interpreter/files/...` as
 * `URL.createObjectURL` blob URLs, surfaced in the Files panel. We
 * revoke those URLs when a fresh listing replaces them or the VM is
 * destroyed — long sessions otherwise leak megabytes of forgotten PNGs.
 */

import {
	execute as runExecute,
	listFiles,
	uploadFile,
	downloadFile,
	InterpreterApiError,
	type FileMeta
} from '$lib/api/interpreterApi';

export type CellStatus = 'running' | 'ok' | 'error';

export interface InterpreterCell {
	id: number;
	source: string;
	status: CellStatus;
	stdout: string;
	stderr: string;
	/** Value of the last expression, if the backend returned one. */
	result: string | null;
	error: string | null;
	truncated: boolean;
	startedAt: number;
	finishedAt: number | null;
}

function randomSessionId(): string {
	if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
		return `web-${crypto.randomUUID()}`;
	}
	return `web-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export interface InterpreterViewModel {
	readonly cells: InterpreterCell[];
	readonly input: string;
	readonly running: boolean;
	readonly sessionId: string;
	/** Files in the session workspace, refreshed from each /execute
	 *  response and on demand via {@link refreshFiles}. */
	readonly files: FileMeta[];
	readonly filesLoading: boolean;
	readonly error: string | null;

	setInput(value: string): void;
	runCode(): Promise<void>;
	clearCells(): void;
	resetSession(): void;
	refreshFiles(): Promise<void>;
	uploadWorkspaceFile(file: File): Promise<void>;
	downloadWorkspaceFile(name: string): Promise<void>;
	appendToInput(snippet: string): void;
}

export function createInterpreterVM(): InterpreterViewModel {
	let cells = $state<InterpreterCell[]>([]);
	let input = $state<string>('');
	let running = $state<boolean>(false);
	let sessionId = $state<string>(randomSessionId());
	let files = $state<FileMeta[]>([]);
	let filesLoading = $state<boolean>(false);
	let error = $state<string | null>(null);
	let nextCellId = 1;

	function appendCell(source: string): InterpreterCell {
		const cell: InterpreterCell = {
			id: nextCellId++,
			source,
			status: 'running',
			stdout: '',
			stderr: '',
			result: null,
			error: null,
			truncated: false,
			startedAt: Date.now(),
			finishedAt: null
		};
		cells = [...cells, cell];
		return cell;
	}

	function patchCell(id: number, patch: Partial<InterpreterCell>): void {
		cells = cells.map((c) => (c.id === id ? { ...c, ...patch } : c));
	}

	function toMessage(err: unknown): string {
		if (err instanceof InterpreterApiError) {
			return `${err.status === 401 ? 'Sign in required — ' : ''}${err.message}`;
		}
		return err instanceof Error ? err.message : String(err);
	}

	async function runCode(): Promise<void> {
		const trimmed = input.trim();
		if (trimmed === '' || running) return;
		running = true;
		input = '';
		const cell = appendCell(trimmed);
		try {
			const response = await runExecute({ code: trimmed, session_id: sessionId });
			patchCell(cell.id, {
				status: response.success ? 'ok' : 'error',
				stdout: response.stdout ?? '',
				stderr: response.stderr ?? '',
				result: response.result ?? null,
				error: response.error ?? null,
				truncated: response.truncated ?? false,
				finishedAt: Date.now()
			});
			// /execute returns the post-run workspace listing — adopt it so
			// the Files panel reflects anything the code wrote.
			if (Array.isArray(response.artifacts)) files = response.artifacts;
		} catch (err) {
			patchCell(cell.id, {
				status: 'error',
				error: toMessage(err),
				finishedAt: Date.now()
			});
		} finally {
			running = false;
		}
	}

	async function refreshFiles(): Promise<void> {
		filesLoading = true;
		try {
			files = await listFiles(sessionId);
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			filesLoading = false;
		}
	}

	async function uploadWorkspaceFile(file: File): Promise<void> {
		filesLoading = true;
		try {
			await uploadFile(file, file.name, sessionId);
			files = await listFiles(sessionId);
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			filesLoading = false;
		}
	}

	async function downloadWorkspaceFile(name: string): Promise<void> {
		try {
			const { url } = await downloadFile(sessionId, name);
			const anchor = document.createElement('a');
			anchor.href = url;
			anchor.download = name.split('/').pop() ?? name;
			document.body.appendChild(anchor);
			anchor.click();
			document.body.removeChild(anchor);
			setTimeout(() => URL.revokeObjectURL(url), 30_000);
		} catch (err) {
			error = toMessage(err);
		}
	}

	return {
		get cells() {
			return cells;
		},
		get input() {
			return input;
		},
		get running() {
			return running;
		},
		get sessionId() {
			return sessionId;
		},
		get files() {
			return files;
		},
		get filesLoading() {
			return filesLoading;
		},
		get error() {
			return error;
		},
		setInput: (value) => {
			input = value;
		},
		runCode,
		clearCells: () => {
			cells = [];
			nextCellId = 1;
		},
		resetSession: () => {
			cells = [];
			nextCellId = 1;
			sessionId = randomSessionId();
			files = [];
			error = null;
		},
		refreshFiles,
		uploadWorkspaceFile,
		downloadWorkspaceFile,
		appendToInput: (snippet) => {
			const sep = input.length > 0 && !input.endsWith('\n') ? '\n' : '';
			input = `${input}${sep}${snippet}`;
		}
	};
}
