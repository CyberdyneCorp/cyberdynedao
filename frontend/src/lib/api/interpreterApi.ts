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
