import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
	MatlabApiError,
	check,
	downloadArtifact,
	plot,
	repl,
	whoami
} from '../matlabApi';
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

function mockBlobOnce(status: number, size: number, contentType: string): void {
	// Use a string body — jsdom's Response constructor handles strings
	// reliably; Uint8Array/Blob inputs hit jsdom's missing `stream()`.
	const body = 'x'.repeat(size);
	(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(
		new Response(body, {
			status,
			headers: { 'content-type': contentType }
		})
	);
}

beforeEach(() => {
	globalThis.fetch = vi.fn() as unknown as typeof fetch;
	// Always override — jsdom ships a nodedata: implementation that
	// produces non-deterministic URLs we can't assert on.
	URL.createObjectURL = vi.fn(() => 'blob:mock://1') as typeof URL.createObjectURL;
	URL.revokeObjectURL = vi.fn() as typeof URL.revokeObjectURL;
});

afterEach(() => {
	clearAuthToken();
	vi.restoreAllMocks();
});

describe('matlabApi', () => {
	it('repl posts to /api/matlab/v1/repl with stateful=true by default', async () => {
		setAuthToken('tok');
		mockJsonOnce(200, {
			ok: true,
			stdout: '2\n',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: []
		});
		const res = await repl({ source: 'disp(1+1)', session_id: 'sess-1' });
		expect(res.stdout).toBe('2\n');
		const [url, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(url).toBe('/api/matlab/v1/repl');
		expect(init.method).toBe('POST');
		const body = JSON.parse(init.body as string);
		expect(body.source).toBe('disp(1+1)');
		expect(body.session_id).toBe('sess-1');
		expect(body.stateful).toBe(true);
		const headers = init.headers as Headers;
		expect(headers.get('authorization')).toBe('Bearer tok');
		expect(headers.get('content-type')).toBe('application/json');
	});

	it('plot defaults format to png', async () => {
		setAuthToken('tok');
		mockJsonOnce(200, {
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: ['/var/lib/m/abc.png']
		});
		await plot({ source: 'plot([1 2 3])', session_id: 's' });
		const [, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		const body = JSON.parse(init.body as string);
		expect(body.format).toBe('png');
	});

	it('check posts to /v1/check', async () => {
		mockJsonOnce(200, { ok: true, diagnostics: [], stdout: '', stderr: '' });
		const res = await check({ source: 'x = 1' });
		expect(res.ok).toBe(true);
		const [url] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(url).toBe('/api/matlab/v1/check');
	});

	it('whoami hits /v1/auth/whoami GET with bearer', async () => {
		setAuthToken('tok');
		mockJsonOnce(200, { authenticated: true, mode: 'user', id: 'u', email: 'e@x' });
		const r = await whoami();
		expect(r.authenticated).toBe(true);
		const [url, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(url).toBe('/api/matlab/v1/auth/whoami');
		expect(init.method).toBe('GET');
		expect((init.headers as Headers).get('authorization')).toBe('Bearer tok');
	});

	it('downloadArtifact strips leading slashes and returns an object URL', async () => {
		setAuthToken('tok');
		mockBlobOnce(200, 16, 'image/png');
		const out = await downloadArtifact('/srv/matlab/figs/x.png');
		expect(out.url).toBe('blob:mock://1');
		expect(out.contentType).toBe('image/png');
		expect(out.bytes).toBe(16);
		const [url] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		// Leading slash stripped, then URL-encoded.
		expect(url).toBe(`/api/matlab/v1/files/${encodeURIComponent('srv/matlab/figs/x.png')}`);
	});

	it('throws MatlabApiError with the server detail on non-2xx', async () => {
		mockJsonOnce(401, { detail: 'missing bearer token' });
		await expect(repl({ source: 'x' })).rejects.toMatchObject({
			name: 'MatlabApiError',
			status: 401,
			message: 'missing bearer token'
		});
	});

	it('joins 422 array-shaped validation errors', async () => {
		mockJsonOnce(422, {
			detail: [
				{ msg: 'source is required' },
				{ msg: 'session_id must be a string' }
			]
		});
		await expect(repl({ source: '' })).rejects.toThrow(/source is required/);
	});

	it('falls back to HTTP <status> if the body is not JSON-shaped', async () => {
		(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(
			new Response('not json', { status: 500 })
		);
		try {
			await whoami();
		} catch (e) {
			expect(e).toBeInstanceOf(MatlabApiError);
			expect((e as MatlabApiError).status).toBe(500);
			expect((e as MatlabApiError).message).toBe('HTTP 500');
		}
	});
});
