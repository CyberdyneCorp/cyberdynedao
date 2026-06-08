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

/**
 * Public Cyberflies MCP (Model Context Protocol) endpoint.
 *
 * External LLM clients (Claude, Claude Code, ChatGPT) connect here **directly**
 * — NOT through the same-origin proxy — and authenticate with a personal API
 * key as the Bearer token. The server resolves the owner from the key and
 * scopes its read-only tools (list/search/get recordings) to that user.
 *
 * Override at build time with `VITE_CYBERFLIES_MCP_URL` if the domain changes.
 */
export const CYBERFLIES_MCP_URL: string =
	import.meta.env.VITE_CYBERFLIES_MCP_URL ??
	'https://cyberflies.mcp.coolify.cyberdynecorp.ai/mcp';

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

async function patchJson<T>(path: string, body: unknown): Promise<T> {
	const res = await fetch(`${CYBERFLIES_BASE}${path}`, {
		method: 'PATCH',
		headers: withAuth({ 'content-type': 'application/json', accept: 'application/json' }),
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new CyberfliesApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

/** POST with no body that returns 204 (no content). */
async function postEmpty(path: string): Promise<void> {
	const res = await fetch(`${CYBERFLIES_BASE}${path}`, {
		method: 'POST',
		headers: withAuth({ accept: 'application/json' })
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

// ── Channel rename ──────────────────────────────────────────────────

/** Rename / re-describe a channel. */
export function updateChannel(
	channelId: string,
	patch: { name?: string; description?: string | null }
): Promise<ChannelResponse> {
	return patchJson<ChannelResponse>(`/api/v1/channels/${encodeURIComponent(channelId)}`, patch);
}

// ── MCP servers (the meeting agent's tools) ─────────────────────────

export interface McpServer {
	id: string;
	name: string;
	url: string;
	enabled: boolean;
	has_auth_token: boolean;
}

export interface McpServerListResponse {
	items: McpServer[];
}

export function listMcpServers(): Promise<McpServerListResponse> {
	return getJson<McpServerListResponse>('/api/v1/mcp-servers');
}

export function createMcpServer(body: {
	name: string;
	url: string;
	auth_token?: string | null;
	enabled?: boolean;
}): Promise<McpServer> {
	return postJson<McpServer>('/api/v1/mcp-servers', body);
}

/** Enable / disable a registered MCP server. */
export function setMcpServerEnabled(serverId: string, enabled: boolean): Promise<McpServer> {
	return patchJson<McpServer>(`/api/v1/mcp-servers/${encodeURIComponent(serverId)}`, { enabled });
}

export function deleteMcpServer(serverId: string): Promise<void> {
	return del(`/api/v1/mcp-servers/${encodeURIComponent(serverId)}`);
}

// ── API keys (inbound MCP + programmatic access) ────────────────────

/**
 * A personal API key as listed back. The raw secret is **never** returned
 * after creation — only its `prefix` (the leading, non-secret characters)
 * is shown so the user can tell keys apart.
 */
export interface ApiKey {
	id: string;
	name: string;
	prefix: string;
	created_at: string;
	last_used_at?: string | null;
	revoked: boolean;
}

/** Returned once, on creation. `token` is the full secret — shown a single
 *  time and never recoverable afterwards. */
export interface ApiKeyCreated extends ApiKey {
	token: string;
}

export interface ApiKeyListResponse {
	items: ApiKey[];
}

export function listApiKeys(): Promise<ApiKeyListResponse> {
	return getJson<ApiKeyListResponse>('/api/v1/api-keys');
}

/** Create a personal API key. The response includes the one-time `token`. */
export function createApiKey(name: string): Promise<ApiKeyCreated> {
	return postJson<ApiKeyCreated>('/api/v1/api-keys', { name });
}

/** Revoke (delete) an API key. 204. */
export function revokeApiKey(apiKeyId: string): Promise<void> {
	return del(`/api/v1/api-keys/${encodeURIComponent(apiKeyId)}`);
}

// ── Presigned media: direct large-file upload + playback URLs ───────

export interface UploadUrlResponse {
	recording_id: string;
	upload_url: string;
	storage_key: string;
	expires_in: number;
	status: string;
}

export interface PresignedUrlResponse {
	url: string;
	expires_seconds: number;
}

/** Ask the backend for a presigned URL to upload a large file directly to
 *  storage (skips the API proxy). */
export function requestUploadUrl(
	filename: string,
	sizeBytes: number,
	capturedAt?: string
): Promise<UploadUrlResponse> {
	return postJson<UploadUrlResponse>('/api/v1/recordings/upload-url', {
		filename,
		size_bytes: sizeBytes,
		captured_at: capturedAt ?? null
	});
}

/** PUT the file bytes straight to the presigned storage URL (no auth header —
 *  the signature is in the URL; cross-origin to the storage host). */
export async function putToPresignedUrl(uploadUrl: string, file: File): Promise<void> {
	const res = await fetch(uploadUrl, {
		method: 'PUT',
		headers: { 'content-type': file.type || 'application/octet-stream' },
		body: file
	});
	if (!res.ok) throw new CyberfliesApiError(res.status, `storage upload failed (${res.status})`);
}

/** Confirm a direct upload finished — kicks off transcription/summarization. */
export function completeUpload(recordingId: string): Promise<void> {
	return postEmpty(`/api/v1/recordings/${encodeURIComponent(recordingId)}/complete-upload`);
}

/** Presigned URL to stream/download a recording's original media. */
export function recordingMediaUrl(recordingId: string): Promise<PresignedUrlResponse> {
	return getJson<PresignedUrlResponse>(
		`/api/v1/recordings/${encodeURIComponent(recordingId)}/media`
	);
}
