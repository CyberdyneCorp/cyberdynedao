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
	createSession,
	createKernel,
	executeInKernel,
	getCapabilities,
	listFiles,
	uploadFile,
	downloadFile,
	isImageRichOutput,
	InterpreterApiError,
	type FileMeta,
	type RichOutputModel,
	type CapabilitiesResponse
} from '$lib/api/interpreterApi';

export type CellStatus = 'running' | 'ok' | 'error';

/** An inline image rendered from an auto-captured rich output. `url` is a
 *  blob URL the VM owns and revokes when the cell is cleared. */
export interface CellImage {
	name: string;
	mimeType: string;
	url: string;
}

/** Non-image rich output (text/plain, text/html, application/json) shown
 *  inline as text — never injected as HTML, to avoid XSS. */
export interface CellText {
	mimeType: string;
	text: string;
}

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
	/** Kernel execution counter (`In [n]`); null in stateless `/execute` mode. */
	executionCount: number | null;
	/** Auto-captured figures/images, resolved to blob URLs. */
	images: CellImage[];
	/** Auto-captured text/HTML/JSON outputs. */
	texts: CellText[];
	startedAt: number;
	finishedAt: number | null;
}

/** How the REPL runs code. `kernel` keeps state across cells; `stateless`
 *  is the per-call RestrictedPython sandbox (`/execute`). */
export type ExecutionMode = 'kernel' | 'stateless' | 'unknown';

export interface InterpreterViewModel {
	readonly cells: InterpreterCell[];
	readonly input: string;
	readonly running: boolean;
	/** Server-issued workspace session id, or null until the first
	 *  execute/refresh/upload lazily creates one via POST /sessions. The
	 *  interpreter rejects client-invented ids ("invalid session id"), so
	 *  we never fabricate one. */
	readonly sessionId: string | null;
	/** Files in the session workspace, refreshed from each /execute
	 *  response and on demand via {@link refreshFiles}. */
	readonly files: FileMeta[];
	readonly filesLoading: boolean;
	readonly error: string | null;
	/** How the REPL executes code — resolved from server capabilities on the
	 *  first run. `kernel` persists variables across cells. */
	readonly executionMode: ExecutionMode;
	/** Server capabilities (python version, libraries, limits), or null until
	 *  the first run fetches them. Drives the info panel + feature gating. */
	readonly capabilities: CapabilitiesResponse | null;

	setInput(value: string): void;
	runCode(): Promise<void>;
	clearCells(): void;
	resetSession(): void;
	refreshFiles(): Promise<void>;
	uploadWorkspaceFile(file: File): Promise<void>;
	downloadWorkspaceFile(name: string): Promise<void>;
	appendToInput(snippet: string): void;
	/** Revoke any outstanding blob URLs — call from the view's onDestroy. */
	destroy(): void;
}

export function createInterpreterVM(): InterpreterViewModel {
	let cells = $state<InterpreterCell[]>([]);
	let input = $state<string>('');
	let running = $state<boolean>(false);
	let sessionId = $state<string | null>(null);
	let files = $state<FileMeta[]>([]);
	let filesLoading = $state<boolean>(false);
	let error = $state<string | null>(null);
	let executionMode = $state<ExecutionMode>('unknown');
	let capabilities = $state<CapabilitiesResponse | null>(null);
	let nextCellId = 1;

	// Live kernel id (kernel mode only); null until created or after the
	// kernel is killed by an idle/hard timeout — the next run recreates it.
	let kernelId: string | null = null;

	// Every blob URL we mint for an inline image, so we can revoke them on
	// clear/reset/destroy — long sessions otherwise leak megabytes of PNGs.
	const objectUrls = new Set<string>();
	function trackUrl(url: string): string {
		objectUrls.add(url);
		return url;
	}
	function revokeAllUrls(): void {
		for (const url of objectUrls) URL.revokeObjectURL(url);
		objectUrls.clear();
	}

	// Lazily create one server-issued session and reuse it. Coalesce
	// concurrent callers so a burst of run/refresh/upload doesn't spawn
	// multiple workspaces.
	let sessionInflight: Promise<string> | null = null;
	async function ensureSession(): Promise<string> {
		if (sessionId) return sessionId;
		if (sessionInflight) return sessionInflight;
		sessionInflight = (async () => {
			try {
				const { session_id } = await createSession();
				sessionId = session_id;
				return session_id;
			} finally {
				sessionInflight = null;
			}
		})();
		return sessionInflight;
	}

	// Fetch server capabilities once. On any failure we leave them null and
	// the REPL falls back to the stateless /execute path — the capabilities
	// probe must never block running code.
	let capsInflight: Promise<CapabilitiesResponse | null> | null = null;
	async function ensureCapabilities(): Promise<CapabilitiesResponse | null> {
		if (capabilities) return capabilities;
		if (capsInflight) return capsInflight;
		capsInflight = (async () => {
			try {
				capabilities = await getCapabilities();
				return capabilities;
			} catch {
				return null;
			} finally {
				capsInflight = null;
			}
		})();
		return capsInflight;
	}

	// Decide how to run code and make sure the backing resource (kernel or
	// session) exists. Kernels persist variables across cells; we use one
	// when the deployment enables them, falling back to stateless /execute
	// otherwise. A kernel mounts the workspace session, so we adopt its
	// session_id for file ops.
	async function ensureExecutor(): Promise<ExecutionMode> {
		const caps = await ensureCapabilities();
		if (!caps?.kernels?.enabled) {
			executionMode = 'stateless';
			await ensureSession();
			return 'stateless';
		}
		if (!kernelId) {
			const kernel = await createKernel(sessionId ?? undefined);
			kernelId = kernel.id;
			sessionId = kernel.session_id;
		}
		executionMode = 'kernel';
		return 'kernel';
	}

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
			executionCount: null,
			images: [],
			texts: [],
			startedAt: Date.now(),
			finishedAt: null
		};
		cells = [...cells, cell];
		return cell;
	}

	// Resolve auto-captured rich outputs into render-ready cell fields:
	// image outputs become blob URLs (downloaded through the authed proxy),
	// everything else (text/html/json) is kept as inline text. A failed
	// image download is skipped rather than failing the whole cell.
	async function resolveRichOutputs(
		sid: string,
		outputs: RichOutputModel[] | undefined
	): Promise<{ images: CellImage[]; texts: CellText[] }> {
		const images: CellImage[] = [];
		const texts: CellText[] = [];
		for (const out of outputs ?? []) {
			if (isImageRichOutput(out) && out.artifact) {
				try {
					const { url } = await downloadFile(sid, out.artifact);
					images.push({ name: out.artifact, mimeType: out.mime_type, url: trackUrl(url) });
				} catch {
					/* skip an image we couldn't fetch */
				}
			} else if (typeof out.text === 'string' && out.text !== '') {
				texts.push({ mimeType: out.mime_type, text: out.text });
			}
		}
		return { images, texts };
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
			const mode = await ensureExecutor();
			// Shared response shape across both paths.
			let success: boolean;
			let stdout: string;
			let stderr: string;
			let result: string | null;
			let errorText: string | null;
			let truncated: boolean;
			let artifacts: FileMeta[];
			let richOutputs: RichOutputModel[] | undefined;
			let executionCount: number | null = null;
			let noticeText: string | null = null;

			if (mode === 'kernel' && kernelId) {
				let resp = await executeInKernel(kernelId, trimmed);
				// An idle/hard timeout kills the kernel — its state (variables,
				// imports) is gone. Spin up a fresh one and retry once so a long
				// pause between cells doesn't surface as a confusing error.
				if (!resp.alive) {
					kernelId = null;
					const restartedMode = await ensureExecutor();
					if (restartedMode === 'kernel' && kernelId) {
						noticeText = 'Kernel had expired and was restarted — earlier variables were cleared.';
						resp = await executeInKernel(kernelId, trimmed);
					}
				}
				success = resp.success;
				stdout = resp.stdout ?? '';
				stderr = resp.stderr ?? '';
				result = resp.result ?? null;
				errorText = resp.error ?? null;
				truncated = resp.truncated ?? false;
				artifacts = resp.artifacts ?? [];
				richOutputs = resp.rich_outputs;
				executionCount = resp.execution_count ?? null;
			} else {
				const sid = sessionId ?? (await ensureSession());
				const resp = await runExecute({ code: trimmed, session_id: sid });
				success = resp.success;
				stdout = resp.stdout ?? '';
				stderr = resp.stderr ?? '';
				result = resp.result ?? null;
				errorText = resp.error ?? null;
				truncated = resp.truncated ?? false;
				artifacts = resp.artifacts ?? [];
				richOutputs = resp.rich_outputs;
			}

			const sid = sessionId ?? '';
			const { images, texts } = await resolveRichOutputs(sid, richOutputs);
			patchCell(cell.id, {
				status: success ? 'ok' : 'error',
				stdout,
				stderr,
				result,
				error: errorText,
				truncated,
				executionCount,
				images,
				texts,
				finishedAt: Date.now()
			});
			if (noticeText) error = noticeText;
			// Both paths return the post-run workspace listing — adopt it so
			// the Files panel reflects anything the code wrote.
			if (Array.isArray(artifacts)) files = artifacts;
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
			const sid = await ensureSession();
			files = await listFiles(sid);
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
			const sid = await ensureSession();
			await uploadFile(file, file.name, sid);
			files = await listFiles(sid);
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			filesLoading = false;
		}
	}

	async function downloadWorkspaceFile(name: string): Promise<void> {
		try {
			const sid = await ensureSession();
			const { url } = await downloadFile(sid, name);
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
		get executionMode() {
			return executionMode;
		},
		get capabilities() {
			return capabilities;
		},
		setInput: (value) => {
			input = value;
		},
		runCode,
		clearCells: () => {
			revokeAllUrls();
			cells = [];
			nextCellId = 1;
		},
		resetSession: () => {
			revokeAllUrls();
			cells = [];
			nextCellId = 1;
			// Drop the session + kernel; the next run/refresh/upload creates a
			// fresh server-issued one. Capabilities are deployment-wide, so we
			// keep them cached.
			sessionId = null;
			sessionInflight = null;
			kernelId = null;
			executionMode = 'unknown';
			files = [];
			error = null;
		},
		refreshFiles,
		uploadWorkspaceFile,
		downloadWorkspaceFile,
		appendToInput: (snippet) => {
			const sep = input.length > 0 && !input.endsWith('\n') ? '\n' : '';
			input = `${input}${sep}${snippet}`;
		},
		destroy: () => {
			revokeAllUrls();
		}
	};
}
