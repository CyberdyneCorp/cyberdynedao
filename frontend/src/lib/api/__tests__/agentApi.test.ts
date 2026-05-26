import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
	AgentApiError,
	getHistory,
	sendMessage,
	startSession
} from '../agentApi';
import { clearAuthToken, setAuthToken } from '$lib/auth/authToken';

type FetchMock = ReturnType<typeof vi.fn>;

function mockJsonOnce(status: number, body: unknown): void {
	(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(
		new Response(JSON.stringify(body), {
			status,
			headers: { 'content-type': 'application/json' }
		})
	);
}

beforeEach(() => {
	globalThis.fetch = vi.fn() as unknown as typeof fetch;
	// VITE_BACKEND_API_URL is read at module-eval time via
	// import.meta.env; vitest's vite picks it up from the project env.
	// For these tests we rely on it being set to the real production URL
	// (the build-time default), which the API_BASE strips of trailing
	// slashes. Either way, our assertions are pattern-based.
});

afterEach(() => {
	clearAuthToken();
	vi.restoreAllMocks();
});

describe('agentApi', () => {
	it('startSession posts to /api/v1/chat/sessions with bearer', async () => {
		setAuthToken('tok');
		mockJsonOnce(201, { sessionId: 's-1', createdAt: '2026-05-26T09:00:00Z' });
		const s = await startSession();
		expect(s.sessionId).toBe('s-1');
		const [url, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(String(url)).toMatch(/\/api\/v1\/chat\/sessions$/);
		expect(init.method).toBe('POST');
		expect((init.headers as Headers).get('authorization')).toBe('Bearer tok');
	});

	it('sendMessage posts the content + URL-encodes the session id', async () => {
		mockJsonOnce(200, {
			id: 'm-1',
			sessionId: 's/1',
			role: 'assistant',
			content: 'hi',
			toolCalls: [],
			toolCallId: null,
			tokensIn: 5,
			tokensOut: 7,
			model: 'gpt-4o-mini',
			createdAt: '2026-05-26T09:00:01Z'
		});
		const reply = await sendMessage('s/1', 'hello');
		expect(reply.content).toBe('hi');
		const [url, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(String(url)).toMatch(/\/chat\/sessions\/s%2F1\/messages$/);
		expect(JSON.parse(init.body as string)).toEqual({ content: 'hello' });
	});

	it('getHistory returns the message list', async () => {
		mockJsonOnce(200, {
			sessionId: 's-1',
			messages: [
				{
					id: 'm-1',
					sessionId: 's-1',
					role: 'user',
					content: 'q',
					toolCalls: [],
					toolCallId: null,
					tokensIn: 0,
					tokensOut: 0,
					model: null,
					createdAt: '2026-05-26T09:00:00Z'
				}
			]
		});
		const h = await getHistory('s-1');
		expect(h.messages).toHaveLength(1);
		expect(h.messages[0].role).toBe('user');
	});

	it('throws AgentApiError on non-2xx with the detail field', async () => {
		mockJsonOnce(401, { detail: 'authentication required' });
		await expect(sendMessage('s', 'x')).rejects.toMatchObject({
			name: 'AgentApiError',
			status: 401,
			message: 'authentication required'
		});
	});

	it('falls back to HTTP <status> on non-JSON error bodies', async () => {
		(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(
			new Response('not json', { status: 502 })
		);
		try {
			await startSession();
		} catch (e) {
			expect(e).toBeInstanceOf(AgentApiError);
			expect((e as AgentApiError).status).toBe(502);
			expect((e as AgentApiError).message).toBe('HTTP 502');
		}
	});
});
