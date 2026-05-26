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

export function sendMessage(sessionId: string, content: string): Promise<AgentMessage> {
	return postJson<AgentMessage>(
		`/api/v1/chat/sessions/${encodeURIComponent(sessionId)}/messages`,
		{ content }
	);
}

export function getHistory(sessionId: string): Promise<AgentHistory> {
	return getJson<AgentHistory>(`/api/v1/chat/sessions/${encodeURIComponent(sessionId)}`);
}
