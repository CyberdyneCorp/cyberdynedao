/**
 * Cyberflies (meetings) remote backend client.
 *
 * All calls go through a **same-origin proxy** at `/api/cyberflies/*` —
 * the proxy block lives in `frontend/Dockerfile` (prod nginx) and
 * `vite.config.ts` (dev). Same reason as the MATLAB/CyberdyneAuth
 * proxies: no CORS preflight, no upstream URL leaking into the bundle.
 *
 * Auth: the user's CyberdyneAuth bearer is injected via `withAuth()`.
 * Every endpoint here is `HTTPBearer`-gated upstream.
 *
 * Wire format mirrors the upstream OpenAPI exactly.
 */

import { withAuth } from '$lib/auth/authToken';

const CYBERFLIES_BASE = '/api/cyberflies';

/** Transcription produced by the backend after a recording is processed. */
export interface TranscriptionSchema {
	text: string;
	language?: string | null;
	duration_seconds?: number | null;
	word_count: number;
}

/** AI summary — shared shape between a single recording and a channel recap. */
export interface SummarySchema {
	headline: string;
	abstract: string;
	bullets: string[];
}

/**
 * A single uploaded meeting recording. `status` is a free-form string
 * upstream (no enum); we treat `completed`/`failed` as terminal and
 * anything else as still-processing — see {@link isTerminalStatus}.
 */
export interface RecordingResponse {
	id: string;
	owner_id: string;
	status: string;
	audio_format: string;
	size_bytes: number;
	device?: string | null;
	captured_at?: string | null;
	created_at: string;
	updated_at: string;
	transcription?: TranscriptionSchema | null;
	summary?: SummarySchema | null;
	error?: string | null;
}

export interface RecordingListResponse {
	items: RecordingResponse[];
	limit: number;
	offset: number;
}

export interface PresignedUrlResponse {
	url: string;
	expires_seconds: number;
}

export interface ChannelResponse {
	id: string;
	owner_id: string;
	name: string;
	description?: string | null;
	recap?: SummarySchema | null;
	created_at: string;
	updated_at: string;
}

export interface ChannelListResponse {
	items: ChannelResponse[];
	limit: number;
	offset: number;
}

export interface ChatMessage {
	role: 'user' | 'assistant';
	content: string;
}

export interface ChatReplyResponse {
	reply: string;
	used_tools: string[];
}

/** Returns true when the backend is done processing this recording. */
export function isTerminalStatus(status: string): boolean {
	const s = status.toLowerCase();
	return s === 'completed' || s === 'failed' || s === 'error';
}

export class CyberfliesApiError extends Error {
	constructor(
		public readonly status: number,
		message: string
	) {
		super(message);
		this.name = 'CyberfliesApiError';
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
	const res = await fetch(`${CYBERFLIES_BASE}${path}`, {
		method: 'POST',
		headers,
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new CyberfliesApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function getJson<T>(path: string): Promise<T> {
	const res = await fetch(`${CYBERFLIES_BASE}${path}`, {
		method: 'GET',
		headers: withAuth({ accept: 'application/json' })
	});
	if (!res.ok) throw new CyberfliesApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

/** DELETE returning 204 (no body). */
async function del(path: string): Promise<void> {
	const res = await fetch(`${CYBERFLIES_BASE}${path}`, {
		method: 'DELETE',
		headers: withAuth({ accept: 'application/json' })
	});
	if (!res.ok) throw new CyberfliesApiError(res.status, await readError(res));
}

/** POST with a JSON body that returns 204 (no body to parse). */
async function postNoContent(path: string, body: unknown): Promise<void> {
	const res = await fetch(`${CYBERFLIES_BASE}${path}`, {
		method: 'POST',
		headers: withAuth({ 'content-type': 'application/json', accept: 'application/json' }),
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new CyberfliesApiError(res.status, await readError(res));
}

// ── Recordings ──────────────────────────────────────────────────────

export function listRecordings(limit = 50, offset = 0): Promise<RecordingListResponse> {
	const qs = `?limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}`;
	return getJson<RecordingListResponse>(`/api/v1/recordings${qs}`);
}

export function getRecording(recordingId: string): Promise<RecordingResponse> {
	return getJson<RecordingResponse>(`/api/v1/recordings/${encodeURIComponent(recordingId)}`);
}

/** Delete a recording (audio, transcript and channel membership). 204. */
export function deleteRecording(recordingId: string): Promise<void> {
	return del(`/api/v1/recordings/${encodeURIComponent(recordingId)}`);
}

/**
 * Multipart upload of a captured audio file. The backend returns 202
 * with a `pending` recording immediately and transcribes asynchronously;
 * poll {@link getRecording} until the status is terminal.
 *
 * Don't set content-type — fetch + FormData generate the multipart
 * boundary automatically.
 */
export async function uploadRecording(
	file: File | Blob,
	options?: { device?: string; capturedAt?: string; filename?: string }
): Promise<RecordingResponse> {
	const form = new FormData();
	form.append('file', file, options?.filename ?? (file instanceof File ? file.name : 'audio'));
	if (options?.device) form.append('device', options.device);
	if (options?.capturedAt) form.append('captured_at', options.capturedAt);
	const headers = withAuth({ accept: 'application/json' });
	const res = await fetch(`${CYBERFLIES_BASE}/api/v1/recordings`, {
		method: 'POST',
		headers,
		body: form
	});
	if (!res.ok) throw new CyberfliesApiError(res.status, await readError(res));
	return (await res.json()) as RecordingResponse;
}

/** Temporary signed URL to download/stream the original audio. */
export function getAudioUrl(
	recordingId: string,
	expiresSeconds = 3600
): Promise<PresignedUrlResponse> {
	const qs = `?expires_seconds=${encodeURIComponent(expiresSeconds)}`;
	return getJson<PresignedUrlResponse>(
		`/api/v1/recordings/${encodeURIComponent(recordingId)}/audio-url${qs}`
	);
}

// ── Channels ────────────────────────────────────────────────────────

export function listChannels(limit = 50, offset = 0): Promise<ChannelListResponse> {
	const qs = `?limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}`;
	return getJson<ChannelListResponse>(`/api/v1/channels${qs}`);
}

/** Create a channel. 201. */
export function createChannel(name: string, description?: string): Promise<ChannelResponse> {
	return postJson<ChannelResponse>('/api/v1/channels', { name, description });
}

/** Add a recording to a channel. 204. */
export function addRecordingToChannel(channelId: string, recordingId: string): Promise<void> {
	return postNoContent(
		`/api/v1/channels/${encodeURIComponent(channelId)}/recordings`,
		{ recording_id: recordingId }
	);
}

// ── Chat ────────────────────────────────────────────────────────────

/** Chat across all of the user's meetings knowledge. */
export function chat(messages: ChatMessage[]): Promise<ChatReplyResponse> {
	return postJson<ChatReplyResponse>('/api/v1/chat', { messages });
}

/** Chat scoped to a single channel's meetings. */
export function chatInChannel(
	channelId: string,
	messages: ChatMessage[]
): Promise<ChatReplyResponse> {
	return postJson<ChatReplyResponse>(
		`/api/v1/channels/${encodeURIComponent(channelId)}/chat`,
		{ messages }
	);
}
