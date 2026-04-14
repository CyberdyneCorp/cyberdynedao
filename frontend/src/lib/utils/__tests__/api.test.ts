import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { api, ApiClient } from '../api';

describe('ApiClient', () => {
	let fetchSpy: ReturnType<typeof vi.spyOn>;

	beforeEach(() => {
		fetchSpy = vi.spyOn(globalThis, 'fetch');
	});
	afterEach(() => {
		fetchSpy.mockRestore();
	});

	function mockResponse(options: { ok: boolean; status: number; statusText?: string; body?: unknown; contentType?: string }) {
		const headers = new Map();
		headers.set('content-type', options.contentType ?? 'application/json');
		return {
			ok: options.ok,
			status: options.status,
			statusText: options.statusText ?? '',
			json: async () => options.body,
			text: async () => String(options.body ?? ''),
			headers: { get: (k: string) => headers.get(k) }
		} as unknown as Response;
	}

	it('get returns data on success', async () => {
		fetchSpy.mockResolvedValueOnce(mockResponse({ ok: true, status: 200, body: { ok: 1 } }));
		const res = await api.get<{ ok: number }>('/x');
		expect(res.data).toEqual({ ok: 1 });
		expect(res.status).toBe(200);
	});

	it('get returns error on non-ok response', async () => {
		fetchSpy.mockResolvedValueOnce(mockResponse({ ok: false, status: 500, statusText: 'fail' }));
		const res = await api.get('/x');
		expect(res.error).toContain('500');
		expect(res.status).toBe(500);
	});

	it('returns text when content-type not json', async () => {
		fetchSpy.mockResolvedValueOnce(mockResponse({ ok: true, status: 200, body: 'hello', contentType: 'text/plain' }));
		const res = await api.get<string>('/x');
		expect(res.data).toBe('hello');
	});

	it('post sends body', async () => {
		fetchSpy.mockResolvedValueOnce(mockResponse({ ok: true, status: 200, body: { ok: 1 } }));
		await api.post('/x', { a: 1 });
		expect(fetchSpy).toHaveBeenCalled();
		const args = fetchSpy.mock.calls[0][1] as RequestInit;
		expect(args.method).toBe('POST');
		expect(args.body).toBe(JSON.stringify({ a: 1 }));
	});

	it('post handles no body', async () => {
		fetchSpy.mockResolvedValueOnce(mockResponse({ ok: true, status: 200, body: {} }));
		await api.post('/x');
		const args = fetchSpy.mock.calls[0][1] as RequestInit;
		expect(args.body).toBeUndefined();
	});

	it('put and delete methods', async () => {
		fetchSpy.mockResolvedValue(mockResponse({ ok: true, status: 200, body: {} }));
		await api.put('/x', { a: 1 });
		await api.put('/y');
		await api.delete('/x');
		expect(fetchSpy).toHaveBeenCalledTimes(3);
	});

	it('handles timeout (AbortError)', async () => {
		fetchSpy.mockRejectedValueOnce(Object.assign(new Error('aborted'), { name: 'AbortError' }));
		const res = await api.get('/x');
		expect(res.status).toBe(408);
		expect(res.error).toMatch(/timeout/i);
	});

	it('handles generic errors', async () => {
		fetchSpy.mockRejectedValueOnce(new Error('network down'));
		const res = await api.get('/x');
		expect(res.status).toBe(0);
		expect(res.error).toMatch(/network down/);
	});

	it('handles non-Error rejection', async () => {
		fetchSpy.mockRejectedValueOnce('string failure');
		const res = await api.get('/x');
		expect(res.error).toMatch(/Unknown/);
	});

	it('custom ApiClient uses baseUrl and headers', async () => {
		fetchSpy.mockResolvedValueOnce(mockResponse({ ok: true, status: 200, body: {} }));
		const client = new ApiClient('https://api.test', { 'X-Custom': '1' });
		await client.get('/v1', { headers: { Authorization: 'Bearer abc' } });
		const [url, init] = fetchSpy.mock.calls[0];
		expect(url).toBe('https://api.test/v1');
		const headers = (init as RequestInit).headers as Record<string, string>;
		expect(headers['X-Custom']).toBe('1');
		expect(headers.Authorization).toBe('Bearer abc');
	});
});
