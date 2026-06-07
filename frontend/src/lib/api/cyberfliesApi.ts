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

/** One timestamped chunk of a transcript (seconds). */
export interface TranscriptSegmentSchema {
	start: number;
	end: number;
	text: string;
}

/** Transcription produced by the backend after a recording is processed. */
export interface TranscriptionSchema {
	text: string;
	language?: string | null;
	duration_seconds?: number | null;
	word_count: number;
	segments?: TranscriptSegmentSchema[];
}

/** A follow-up the AI extracted from the meeting. */
export interface ActionItemSchema {
	text: string;
	assignee?: string | null;
}

/** AI summary — shared shape between a single recording and a channel recap. */
export interface SummarySchema {
	headline: string;
	abstract: string;
	bullets: string[];
	action_items?: ActionItemSchema[];
}

/** Original-media metadata for a recording (audio vs video, availability). */
export interface MediaSchema {
	kind: string; // 'audio' | 'video'
	format: string;
	size_bytes: number;
	duration_seconds?: number | null;
	available: boolean;
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
	media?: MediaSchema | null;
	transcription?: TranscriptionSchema | null;
	summary?: SummarySchema | null;
	error?: string | null;
}

export interface RecordingListResponse {
	items: RecordingResponse[];
	limit: number;
	offset: number;
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

/** Platforms the capture bot can join. */
export type MeetingPlatform = 'google_meet' | 'microsoft_teams';

/** A meeting-capture bot session. `status` walks
 *  scheduled → joining → in_call → recording → uploading → completed,
 *  or → failed. On completion `recording_id` links the produced Recording. */
export interface MeetingSession {
	id: string;
	owner_id: string;
	platform: MeetingPlatform;
	meeting_url: string;
	status: string;
	bot_display_name?: string | null;
	consent_message?: string | null;
	recording_id?: string | null;
	started_at?: string | null;
	ended_at?: string | null;
	error?: string | null;
	created_at: string;
	updated_at: string;
}

export interface MeetingSessionListResponse {
	items: MeetingSession[];
	limit: number;
	offset: number;
}

export interface JoinMeetingRequest {
	platform: MeetingPlatform;
	meeting_url: string;
	bot_display_name?: string;
	consent_message?: string;
	/** Capture video as well as audio (the bot records the screen). */
	capture_video?: boolean;
}

/** True when the capture bot session has reached a terminal state. */
export function isTerminalMeetingStatus(status: string): boolean {
	const s = status.toLowerCase();
	return s === 'completed' || s === 'failed';
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

export interface AudioFile {
	blob: Blob;
	filename: string;
	contentType: string;
}

/** Extension for a media content-type, used as a download-filename fallback
 *  when the server doesn't send a Content-Disposition. */
function extForContentType(contentType: string): string {
	const map: Record<string, string> = {
		'audio/mp4': '.m4a',
		'audio/x-m4a': '.m4a',
		'audio/mpeg': '.mp3',
		'audio/wav': '.wav',
		'audio/x-wav': '.wav',
		'audio/x-caf': '.caf',
		'video/mp4': '.mp4',
		'video/quicktime': '.mov'
	};
	return map[contentType.split(';')[0].trim().toLowerCase()] ?? '';
}

/** Parse the download filename from a Content-Disposition header, handling
 *  both `filename="…"` and RFC 5987 `filename*=UTF-8''…`. */
export function filenameFromContentDisposition(header: string | null): string | null {
	if (!header) return null;
	const star = /filename\*\s*=\s*[^']*''([^;]+)/i.exec(header);
	if (star) {
		try {
			return decodeURIComponent(star[1].trim());
		} catch {
			/* fall through to the plain form */
		}
	}
	const plain = /filename\s*=\s*"?([^";]+)"?/i.exec(header);
	return plain ? plain[1].trim() : null;
}

/**
 * Stream the original audio/video through the API (same-origin proxy +
 * bearer). Replaces the deprecated `/audio-url` presigned endpoint, which
 * handed back an internal `minio:9000` URL unreachable from the browser.
 * The returned blob is ready to save via an `<a download>`.
 */
export async function fetchAudioFile(recordingId: string): Promise<AudioFile> {
	const res = await fetch(
		`${CYBERFLIES_BASE}/api/v1/recordings/${encodeURIComponent(recordingId)}/audio`,
		{ method: 'GET', headers: withAuth() }
	);
	if (!res.ok) throw new CyberfliesApiError(res.status, await readError(res));
	const blob = await res.blob();
	const contentType = res.headers.get('content-type') ?? blob.type ?? 'application/octet-stream';
	const filename =
		filenameFromContentDisposition(res.headers.get('content-disposition')) ??
		`recording-${recordingId}${extForContentType(contentType)}`;
	return { blob, filename, contentType };
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

/** Delete a channel (membership links are removed; recordings are kept). 204. */
export function deleteChannel(channelId: string): Promise<void> {
	return del(`/api/v1/channels/${encodeURIComponent(channelId)}`);
}

/** Add a recording to a channel. 204. */
export function addRecordingToChannel(channelId: string, recordingId: string): Promise<void> {
	return postNoContent(
		`/api/v1/channels/${encodeURIComponent(channelId)}/recordings`,
		{ recording_id: recordingId }
	);
}

/** Remove a recording from a channel (the recording itself is kept). 204. */
export function removeRecordingFromChannel(
	channelId: string,
	recordingId: string
): Promise<void> {
	return del(
		`/api/v1/channels/${encodeURIComponent(channelId)}/recordings/${encodeURIComponent(recordingId)}`
	);
}

/** List the meetings that belong to a channel. */
export function listChannelRecordings(channelId: string): Promise<RecordingListResponse> {
	return getJson<RecordingListResponse>(
		`/api/v1/channels/${encodeURIComponent(channelId)}/recordings`
	);
}

/** Generate an AI recap across all of a channel's meetings. */
export function generateChannelRecap(channelId: string): Promise<SummarySchema> {
	return postJson<SummarySchema>(`/api/v1/channels/${encodeURIComponent(channelId)}/recap`, {});
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

/** Chat scoped to a single meeting. */
export function chatInRecording(
	recordingId: string,
	messages: ChatMessage[]
): Promise<ChatReplyResponse> {
	return postJson<ChatReplyResponse>(
		`/api/v1/recordings/${encodeURIComponent(recordingId)}/chat`,
		{ messages }
	);
}

// ── Meeting-capture bot ─────────────────────────────────────────────

/** Dispatch the capture bot to join + record a live meeting. 202. */
export function joinMeeting(req: JoinMeetingRequest): Promise<MeetingSession> {
	return postJson<MeetingSession>('/api/v1/meetings', req);
}

export function listMeetingSessions(limit = 50, offset = 0): Promise<MeetingSessionListResponse> {
	const qs = `?limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}`;
	return getJson<MeetingSessionListResponse>(`/api/v1/meetings${qs}`);
}

export function getMeetingSession(sessionId: string): Promise<MeetingSession> {
	return getJson<MeetingSession>(`/api/v1/meetings/${encodeURIComponent(sessionId)}`);
}
