/**
 * Cyberdyne chat agent client.
 *
 * Talks to the backend's `/api/v1/chat/*` endpoints. Bearer is auto-
 * injected via `withAuth()` (so the agent inherits the user's
 * CyberdyneAuth identity — anonymous sessions still work, the backend
 * just stores a null `user_id`).
 *
 * The backend's chat response is non-streaming today: one POST returns
 * the final assistant message after all tool rounds. We don't surface
 * intermediate tool calls live — they land in the message list when
 * the user fetches history.
 */

import { withAuth } from '$lib/auth/authToken';

const API_BASE = (import.meta.env.VITE_BACKEND_API_URL ?? '').replace(/\/+$/, '');

export interface AgentToolCall {
	id: string;
	name: string;
	argumentsJson: string;
	/** The tool's result content (a JSON string: `{ok, status, error, stderr,
	 *  ...}`). Absent on the live wire shape — the backend returns results as
	 *  separate `tool`-role messages — so the view model attaches it from the
	 *  matching result message once history is (re)loaded. Lets the UI show and
	 *  copy *why* a tool call failed, not just what was called. */
	resultJson?: string;
}

export interface AgentMessage {
	id: string;
	sessionId: string;
	role: 'user' | 'assistant' | 'tool' | 'system';
	content: string;
	toolCalls: AgentToolCall[];
	toolCallId: string | null;
	tokensIn: number;
	tokensOut: number;
	model: string | null;
	createdAt: string;
}

export interface AgentSessionStart {
	sessionId: string;
	createdAt: string;
}

export interface AgentHistory {
	sessionId: string;
	messages: AgentMessage[];
	/** Opaque token for the next (older) page when paged with `limit`;
	 *  null when the oldest message is already included or unpaged. */
	nextCursor: string | null;
}

export interface HistoryParams {
	/** Return the most-recent N messages (still chronological). */
	limit?: number;
	/** Opaque cursor (a prior `nextCursor`) to page into older history. */
	before?: string;
}

export class AgentApiError extends Error {
	constructor(public readonly status: number, message: string) {
		super(message);
		this.name = 'AgentApiError';
	}
}

async function readError(res: Response): Promise<string> {
	try {
		const body = (await res.json()) as { detail?: unknown };
		if (typeof body.detail === 'string') return body.detail;
		return `HTTP ${res.status}`;
	} catch {
		return `HTTP ${res.status}`;
	}
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
	if (!API_BASE) {
		throw new AgentApiError(0, 'VITE_BACKEND_API_URL is not configured');
	}
	const headers = withAuth({ 'content-type': 'application/json', accept: 'application/json' });
	const res = await fetch(`${API_BASE}${path}`, {
		method: 'POST',
		headers,
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new AgentApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function getJson<T>(path: string): Promise<T> {
	if (!API_BASE) throw new AgentApiError(0, 'VITE_BACKEND_API_URL is not configured');
	const res = await fetch(`${API_BASE}${path}`, {
		method: 'GET',
		headers: withAuth({ accept: 'application/json' })
	});
	if (!res.ok) throw new AgentApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

export function startSession(): Promise<AgentSessionStart> {
	return postJson<AgentSessionStart>('/api/v1/chat/sessions', {});
}

/** Files the user attached this turn: the interpreter session they were
 *  uploaded to, plus their filenames (so the agent knows what to read). */
export interface MessageAttachments {
	interpreterSessionId: string;
	filenames: string[];
}

export function sendMessage(
	sessionId: string,
	content: string,
	attachments?: MessageAttachments
): Promise<AgentMessage> {
	const body: Record<string, unknown> = { content };
	if (attachments && attachments.filenames.length > 0) {
		body.interpreterSessionId = attachments.interpreterSessionId;
		body.attachments = attachments.filenames;
	}
	return postJson<AgentMessage>(
		`/api/v1/chat/sessions/${encodeURIComponent(sessionId)}/messages`,
		body
	);
}

export function getHistory(sessionId: string, params: HistoryParams = {}): Promise<AgentHistory> {
	const q = new URLSearchParams();
	if (params.limit !== undefined) q.set('limit', String(params.limit));
	if (params.before) q.set('before', params.before);
	const qs = q.toString();
	return getJson<AgentHistory>(
		`/api/v1/chat/sessions/${encodeURIComponent(sessionId)}${qs ? `?${qs}` : ''}`
	);
}

/** Callbacks for the streamed turn. `onDone` carries the final persisted
 *  assistant message; `onError` fires for in-band stream errors. */
export interface StreamHandlers {
	onDelta(text: string): void;
	onStatus(tool: string): void;
	onDone(message: AgentMessage): void;
	onError(detail: string): void;
}

function dispatchSseEvent(evt: Record<string, unknown>, h: StreamHandlers): void {
	switch (evt.type) {
		case 'delta':
			if (typeof evt.text === 'string') h.onDelta(evt.text);
			break;
		case 'status':
			if (typeof evt.tool === 'string') h.onStatus(evt.tool);
			break;
		case 'done':
			if (evt.message) h.onDone(evt.message as AgentMessage);
			break;
		case 'error':
			h.onError(typeof evt.detail === 'string' ? evt.detail : 'stream error');
			break;
	}
}

/**
 * Stream a turn over Server-Sent Events. Reads the response body manually
 * (the bearer header rules out EventSource), splits on the SSE `\n\n`
 * delimiter, and routes each `data:` event to the handlers.
 */
export async function streamMessage(
	sessionId: string,
	content: string,
	handlers: StreamHandlers,
	attachments?: MessageAttachments
): Promise<void> {
	if (!API_BASE) throw new AgentApiError(0, 'VITE_BACKEND_API_URL is not configured');
	const body: Record<string, unknown> = { content };
	if (attachments && attachments.filenames.length > 0) {
		body.interpreterSessionId = attachments.interpreterSessionId;
		body.attachments = attachments.filenames;
	}
	const res = await fetch(
		`${API_BASE}/api/v1/chat/sessions/${encodeURIComponent(sessionId)}/messages/stream`,
		{
			method: 'POST',
			headers: withAuth({ 'content-type': 'application/json', accept: 'text/event-stream' }),
			body: JSON.stringify(body)
		}
	);
	if (!res.ok || !res.body) throw new AgentApiError(res.status, await readError(res));
	const reader = res.body.getReader();
	const decoder = new TextDecoder();
	let buffer = '';
	for (;;) {
		const { value, done } = await reader.read();
		if (done) break;
		buffer += decoder.decode(value, { stream: true });
		let sep: number;
		while ((sep = buffer.indexOf('\n\n')) !== -1) {
			const frame = buffer.slice(0, sep);
			buffer = buffer.slice(sep + 2);
			const dataLine = frame.split('\n').find((l) => l.startsWith('data:'));
			if (!dataLine) continue;
			const json = dataLine.slice('data:'.length).trim();
			if (!json) continue;
			try {
				dispatchSseEvent(JSON.parse(json) as Record<string, unknown>, handlers);
			} catch {
				/* ignore a malformed frame */
			}
		}
	}
}
