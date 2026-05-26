/**
 * MATLAB-LLVM remote backend client.
 *
 * All calls go through a **same-origin proxy** at `/api/matlab/*` —
 * the proxy block lives in `frontend/Dockerfile` (prod nginx) and
 * `vite.config.ts` (dev). Same reason as the CyberdyneAuth proxy:
 * no CORS preflight, no upstream URL leaking into the Vite bundle.
 *
 * Auth: the user's CyberdyneAuth bearer is injected via `withAuth()`.
 * The MATLAB backend's `/v1/auth/whoami` accepts the same JWT.
 *
 * Wire format mirrors the upstream OpenAPI exactly.
 */

import { withAuth } from '$lib/auth/authToken';

const MATLAB_BASE = '/api/matlab';

export interface ReplRequest {
	source: string;
	session_id?: string;
	user_id?: string;
	stateful?: boolean;
}

export interface ReplResponse {
	ok: boolean;
	stdout: string;
	stderr: string;
	timed_out: boolean;
	truncated: boolean;
	stateful: boolean;
	/** New figure/file paths — fetch each via `downloadArtifact()`. */
	artifacts: string[];
}

export interface PlotRequest {
	source: string;
	session_id?: string;
	user_id?: string;
	format?: 'png' | 'svg' | 'pdf';
}

export interface Diagnostic {
	severity?: string;
	line?: number;
	column?: number;
	message?: string;
	[k: string]: unknown;
}

export interface CheckResponse {
	ok: boolean;
	diagnostics: Diagnostic[];
	stdout: string;
	stderr: string;
}

export interface WhoAmIResponse {
	authenticated: boolean;
	mode: string;
	id?: string | null;
	email?: string | null;
	organization_id?: string | null;
}

export class MatlabApiError extends Error {
	constructor(public readonly status: number, message: string) {
		super(message);
		this.name = 'MatlabApiError';
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
	const headers = withAuth({ 'content-type': 'application/json' });
	const res = await fetch(`${MATLAB_BASE}${path}`, {
		method: 'POST',
		headers,
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new MatlabApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function getJson<T>(path: string): Promise<T> {
	const res = await fetch(`${MATLAB_BASE}${path}`, {
		method: 'GET',
		headers: withAuth()
	});
	if (!res.ok) throw new MatlabApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

export function whoami(): Promise<WhoAmIResponse> {
	return getJson<WhoAmIResponse>('/v1/auth/whoami');
}

export function repl(req: ReplRequest): Promise<ReplResponse> {
	return postJson<ReplResponse>('/v1/repl', { stateful: true, ...req });
}

export function plot(req: PlotRequest): Promise<ReplResponse> {
	return postJson<ReplResponse>('/v1/plot', { format: 'png', ...req });
}

export function check(req: ReplRequest): Promise<CheckResponse> {
	return postJson<CheckResponse>('/v1/check', req);
}

/**
 * Download an artifact (plot PNG/SVG/PDF) as an object URL ready to
 * drop into an `<img src>`. Caller owns the URL — revoke with
 * `URL.revokeObjectURL` when the cell scrolls out of view.
 *
 * The upstream's ``/v1/files/{path}`` route resolves the workspace
 * from ``session_id`` (plus the authenticated principal). Without it,
 * the file lookup falls back to the ``default`` workspace, which is
 * **not** the one our REPL writes to → 404. Always pass the same
 * ``sessionId`` you used for the REPL turn that produced the
 * artifact.
 */
export async function downloadArtifact(
	path: string,
	sessionId?: string
): Promise<{ url: string; contentType: string; bytes: number }> {
	// The upstream gives us paths relative to the workspace
	// (e.g. ``cd_plot_abc.png``). Strip any leading slashes
	// defensively — the proxy prefix already adds the right segment.
	const cleanPath = path.replace(/^\/+/, '');
	const qs = sessionId ? `?session_id=${encodeURIComponent(sessionId)}` : '';
	const headers = withAuth();
	const res = await fetch(`${MATLAB_BASE}/v1/files/${encodeURIComponent(cleanPath)}${qs}`, {
		method: 'GET',
		headers
	});
	if (!res.ok) throw new MatlabApiError(res.status, await readError(res));
	const blob = await res.blob();
	return {
		url: URL.createObjectURL(blob),
		contentType: res.headers.get('content-type') ?? blob.type ?? 'application/octet-stream',
		bytes: blob.size
	};
}
