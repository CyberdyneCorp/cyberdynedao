/**
 * Python interpreter remote backend client.
 *
 * All calls go through a **same-origin proxy** at `/api/interpreter/*` —
 * the proxy block lives in `frontend/Dockerfile` (prod nginx) and
 * `vite.config.ts` (dev). Same rationale as the MATLAB proxy.
 *
 * Auth: the user's CyberdyneAuth bearer is injected via `withAuth()`.
 * Every execution/file/config endpoint is `HTTPBearer`-gated upstream.
 *
 * Wire format mirrors the upstream OpenAPI exactly.
 */

import { withAuth } from '$lib/auth/authToken';

const INTERPRETER_BASE = '/api/interpreter';

/** Metadata for a file in the session workspace. */
export interface FileMeta {
	name: string;
	size_bytes: number;
	modified_at: number; // epoch seconds
}

/**
 * An auto-captured renderable output from an execution — a matplotlib
 * figure, an HTML table, a JSON repr, etc. The backend captures these
 * without the code having to save a file explicitly.
 *
 * - `artifact` points at a workspace file to download (set for binary
 *   outputs like `image/png`); fetch it through the authed proxy.
 * - `text` carries inline content for `text/*` and `application/json`
 *   (no file to download).
 */
export interface RichOutputModel {
	mime_type: string;
	artifact?: string | null;
	text?: string | null;
}

/** True for a rich output the UI can render as an inline image. */
export function isImageRichOutput(o: RichOutputModel): boolean {
	return o.mime_type.startsWith('image/') && !!o.artifact;
}

export interface ExecuteRequest {
	code: string;
	/** Run under the RestrictedPython sandbox (upstream default: true). */
	restricted?: boolean;
	session_id?: string;
}

export interface ExecuteResponse {
	success: boolean;
	result?: string | null;
	stdout: string;
	stderr: string;
	error?: string | null;
	truncated?: boolean;
	/** Files in the session workspace after execution. */
	artifacts: FileMeta[];
	/** Auto-captured renderable outputs (figures, HTML, JSON). */
	rich_outputs?: RichOutputModel[];
}

export interface SessionResponse {
	session_id: string;
}

export interface UploadResponse {
	session_id: string;
	file: FileMeta;
}

export interface FileListResponse {
	session_id: string;
	files: FileMeta[];
}

// ── Kernels (stateful execution) ────────────────────────────────────
// A kernel keeps a live Python process so variables/imports persist
// across executions — unlike `/execute`, which is stateless. Kernels may
// be disabled per deployment (see CapabilitiesResponse.kernels.enabled);
// callers fall back to `/execute` when they are.

export interface KernelResponse {
	id: string;
	session_id: string;
	created_at: number;
	last_active_at: number;
	execution_count: number;
	idle_expires_at: number;
	hard_expires_at: number;
	/** False once the kernel has been killed (idle/hard timeout). */
	alive: boolean;
}

export interface KernelExecuteResponse {
	kernel_id: string;
	/** False if a timeout killed the kernel during/before this run. */
	alive: boolean;
	execution_count: number;
	success: boolean;
	result?: string | null;
	stdout: string;
	stderr: string;
	error?: string | null;
	truncated?: boolean;
	artifacts: FileMeta[];
	rich_outputs?: RichOutputModel[];
}

// ── Capabilities / config (what this deployment supports) ───────────

export interface LibraryInfo {
	module: string;
	version?: string | null;
}

export interface ExecutionLimits {
	timeout_seconds: number;
	max_memory_mb: number;
	max_output_length: number;
	max_code_size: number;
}

export interface WorkspaceCapabilities {
	enabled: boolean;
	max_file_mb: number;
	max_session_mb: number;
	max_files: number;
}

export interface ManimCapabilities {
	enabled: boolean;
	formats: string[];
	qualities: string[];
	timeout_seconds: number;
	max_file_mb: number;
}

export interface KernelCapabilities {
	enabled: boolean;
	idle_ttl_seconds: number;
	max_ttl_seconds: number;
	max_sessions: number;
}

export interface CapabilitiesResponse {
	service_version: string;
	python_version: string;
	restricted_by_default: boolean;
	allow_unrestricted: boolean;
	libraries: LibraryInfo[];
	algorithms: string[];
	limits: ExecutionLimits;
	workspace: WorkspaceCapabilities;
	manim: ManimCapabilities;
	kernels: KernelCapabilities;
}

/** A built-in server-side algorithm result. `result` is algorithm-specific. */
export interface AlgorithmResponse {
	name: string;
	result: unknown;
}

export class InterpreterApiError extends Error {
	constructor(
		public readonly status: number,
		message: string
	) {
		super(message);
		this.name = 'InterpreterApiError';
	}
}

async function readError(res: Response): Promise<string> {
	try {
		const body = (await res.json()) as { detail?: unknown };
		if (typeof body.detail === 'string') return body.detail;
		if (Array.isArray(body.detail)) {
			return body.detail
				.map((d) =>
					typeof d === 'object' && d && 'msg' in d
						? String((d as { msg: unknown }).msg)
						: JSON.stringify(d)
				)
				.join('; ');
		}
		return `HTTP ${res.status}`;
	} catch {
		return `HTTP ${res.status}`;
	}
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
	const headers = withAuth({ 'content-type': 'application/json', accept: 'application/json' });
	const res = await fetch(`${INTERPRETER_BASE}${path}`, {
		method: 'POST',
		headers,
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new InterpreterApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

/** Execute Python in the sandbox. `restricted` defaults to `true` (the
 *  upstream default): this backend disables unrestricted execution by
 *  policy and returns 403 otherwise. Callers can still pass `restricted`
 *  explicitly if a deployment allows it. */
export function execute(req: ExecuteRequest): Promise<ExecuteResponse> {
	return postJson<ExecuteResponse>('/execute', { restricted: true, ...req });
}

export function createSession(): Promise<SessionResponse> {
	return postJson<SessionResponse>('/sessions', {});
}

export async function listFiles(sessionId: string): Promise<FileMeta[]> {
	const qs = `?session_id=${encodeURIComponent(sessionId)}`;
	const res = await fetch(`${INTERPRETER_BASE}/files${qs}`, {
		method: 'GET',
		headers: withAuth({ accept: 'application/json' })
	});
	if (!res.ok) throw new InterpreterApiError(res.status, await readError(res));
	const body = (await res.json()) as FileListResponse;
	return body.files ?? [];
}

/**
 * Multipart upload into the session workspace. Don't set content-type —
 * fetch + FormData generate the multipart boundary automatically.
 */
export async function uploadFile(
	file: File | Blob,
	filename: string,
	sessionId?: string
): Promise<UploadResponse> {
	const qs = sessionId ? `?session_id=${encodeURIComponent(sessionId)}` : '';
	const form = new FormData();
	form.append('file', file, filename);
	const res = await fetch(`${INTERPRETER_BASE}/files${qs}`, {
		method: 'POST',
		headers: withAuth({ accept: 'application/json' }),
		body: form
	});
	if (!res.ok) throw new InterpreterApiError(res.status, await readError(res));
	return (await res.json()) as UploadResponse;
}

/**
 * Download a workspace file/artifact as an object URL ready to drop into
 * an `<img src>` or an `<a download>`. Caller owns the URL — revoke with
 * `URL.revokeObjectURL` when it scrolls out of view.
 */
export async function downloadFile(
	sessionId: string,
	filename: string
): Promise<{ url: string; contentType: string; bytes: number }> {
	const res = await fetch(
		`${INTERPRETER_BASE}/files/${encodeURIComponent(sessionId)}/${encodeURIComponent(filename)}`,
		{ method: 'GET', headers: withAuth() }
	);
	if (!res.ok) throw new InterpreterApiError(res.status, await readError(res));
	const blob = await res.blob();
	return {
		url: URL.createObjectURL(blob),
		contentType: res.headers.get('content-type') ?? blob.type ?? 'application/octet-stream',
		bytes: blob.size
	};
}

async function getJson<T>(path: string): Promise<T> {
	const res = await fetch(`${INTERPRETER_BASE}${path}`, {
		method: 'GET',
		headers: withAuth({ accept: 'application/json' })
	});
	if (!res.ok) throw new InterpreterApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function del(path: string): Promise<void> {
	const res = await fetch(`${INTERPRETER_BASE}${path}`, {
		method: 'DELETE',
		headers: withAuth({ accept: 'application/json' })
	});
	if (!res.ok) throw new InterpreterApiError(res.status, await readError(res));
}

// ── Kernels ─────────────────────────────────────────────────────────

/** Spin up a stateful kernel. Pass an existing `sessionId` to mount that
 *  workspace; omit it to let the server create a fresh one. */
export function createKernel(sessionId?: string): Promise<KernelResponse> {
	return postJson<KernelResponse>('/kernels', sessionId ? { session_id: sessionId } : {});
}

/** Run code in a live kernel; variables/imports persist between calls. */
export function executeInKernel(kernelId: string, code: string): Promise<KernelExecuteResponse> {
	return postJson<KernelExecuteResponse>(
		`/kernels/${encodeURIComponent(kernelId)}/execute`,
		{ code }
	);
}

export function getKernel(kernelId: string): Promise<KernelResponse> {
	return getJson<KernelResponse>(`/kernels/${encodeURIComponent(kernelId)}`);
}

/** Tear down a kernel (frees the live process). 204. */
export function deleteKernel(kernelId: string): Promise<void> {
	return del(`/kernels/${encodeURIComponent(kernelId)}`);
}

// ── Capabilities / config ───────────────────────────────────────────

export function getCapabilities(): Promise<CapabilitiesResponse> {
	return getJson<CapabilitiesResponse>('/capabilities');
}

// ── Built-in algorithms ─────────────────────────────────────────────

export function fibonacci(n: number): Promise<AlgorithmResponse> {
	return postJson<AlgorithmResponse>('/algorithms/fibonacci', { n });
}

export function factorial(n: number): Promise<AlgorithmResponse> {
	return postJson<AlgorithmResponse>('/algorithms/factorial', { n });
}

export function isPrime(n: number): Promise<AlgorithmResponse> {
	return postJson<AlgorithmResponse>('/algorithms/is-prime', { n });
}

export function sumList(numbers: number[]): Promise<AlgorithmResponse> {
	return postJson<AlgorithmResponse>('/algorithms/sum-list', { numbers });
}
