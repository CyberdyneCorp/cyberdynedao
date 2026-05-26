import { describe, expect, it, beforeEach, afterEach, vi } from 'vitest';
import {
	AuthHttpError,
	getProfile,
	login,
	logout,
	oauthAuthorizationUrl,
	refresh,
	walletChallenge,
	walletVerify
} from '../cyberdyneAuthService';
import { setAuthToken, clearAuthToken } from '../authToken';

type FetchMock = ReturnType<typeof vi.fn>;

function mockFetchOnce(status: number, body: unknown): void {
	(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(
		new Response(JSON.stringify(body), {
			status,
			headers: { 'content-type': 'application/json' }
		})
	);
}

beforeEach(() => {
	globalThis.fetch = vi.fn() as unknown as typeof fetch;
});

afterEach(() => {
	clearAuthToken();
	vi.restoreAllMocks();
});

describe('cyberdyneAuthService', () => {
	it('login posts to /auth/login and returns the token shape', async () => {
		mockFetchOnce(200, {
			access_token: 'a',
			refresh_token: 'r',
			token_type: 'bearer'
		});
		const res = await login('x@y.z', 'pw');
		expect(res.access_token).toBe('a');
		expect(res.refresh_token).toBe('r');
		const fetchMock = globalThis.fetch as unknown as FetchMock;
		const [url, init] = fetchMock.mock.calls[0];
		expect(url).toBe('/api/auth/api/v1/auth/login');
		expect(init.method).toBe('POST');
		expect(JSON.parse(init.body as string)).toEqual({ email: 'x@y.z', password: 'pw' });
	});

	it('login throws AuthHttpError with the server detail on 401', async () => {
		mockFetchOnce(401, { detail: 'Invalid credentials' });
		await expect(login('x@y.z', 'bad')).rejects.toMatchObject({
			name: 'AuthHttpError',
			status: 401,
			message: 'Invalid credentials'
		});
	});

	it('login surfaces array-shaped 422 validation errors as a joined string', async () => {
		mockFetchOnce(422, {
			detail: [
				{ loc: ['body', 'email'], msg: 'value is not a valid email address' },
				{ loc: ['body', 'password'], msg: 'too short' }
			]
		});
		await expect(login('not-an-email', 'x')).rejects.toThrow(/not a valid email/);
	});

	it('refresh posts the refresh_token', async () => {
		mockFetchOnce(200, { access_token: 'a2', refresh_token: 'r2', token_type: 'bearer' });
		const res = await refresh('r-old');
		expect(res.access_token).toBe('a2');
		const [, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(JSON.parse(init.body as string)).toEqual({ refresh_token: 'r-old' });
	});

	it('logout posts and swallows errors (best-effort)', async () => {
		mockFetchOnce(500, { detail: 'down' });
		await expect(logout('r')).resolves.toBeUndefined();
	});

	it('logout is a no-op when no refresh token is given', async () => {
		await logout(null);
		expect(globalThis.fetch).not.toHaveBeenCalled();
	});

	it('getProfile attaches the bearer token via withAuth', async () => {
		setAuthToken('mytoken');
		mockFetchOnce(200, { id: 'u-1', email: 'x@y.z' });
		const user = await getProfile();
		expect(user.id).toBe('u-1');
		const [, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		const headers = init.headers as Headers;
		expect(headers.get('authorization')).toBe('Bearer mytoken');
	});

	it('oauthAuthorizationUrl encodes the redirect + fragment mode', async () => {
		mockFetchOnce(200, { authorization_url: 'https://accounts.google.com/...' });
		const res = await oauthAuthorizationUrl('google', 'https://app.example/auth/callback');
		expect(res.authorization_url).toContain('https://accounts.google.com');
		const [url] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(url).toContain('/api/auth/api/v1/auth/oauth/google?');
		expect(url).toContain('frontend_redirect=https');
		expect(url).toContain('return_mode=fragment');
	});

	it('walletChallenge posts wallet_address + chain_id', async () => {
		mockFetchOnce(201, {
			challenge_id: 'ch-1',
			message: 'sign this',
			nonce: 'nnn',
			expires_in_seconds: 300
		});
		const res = await walletChallenge('0xabc', 8453);
		expect(res.challenge_id).toBe('ch-1');
		const [url, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(url).toBe('/api/auth/api/v1/auth/wallet/challenge');
		expect(JSON.parse(init.body as string)).toEqual({ wallet_address: '0xabc', chain_id: 8453 });
	});

	it('walletVerify posts challenge_id + signature', async () => {
		mockFetchOnce(200, {
			access_token: 'a',
			refresh_token: 'r',
			token_type: 'bearer',
			is_new_user: false,
			wallet_address: '0xabc'
		});
		const res = await walletVerify('ch-1', '0xsig');
		expect(res.wallet_address).toBe('0xabc');
		const [url, init] = (globalThis.fetch as unknown as FetchMock).mock.calls[0];
		expect(url).toBe('/api/auth/api/v1/auth/wallet/verify');
		expect(JSON.parse(init.body as string)).toEqual({
			challenge_id: 'ch-1',
			signature: '0xsig'
		});
	});

	it('AuthHttpError carries the status', async () => {
		mockFetchOnce(403, { detail: 'forbidden' });
		try {
			await getProfile();
		} catch (e) {
			expect(e).toBeInstanceOf(AuthHttpError);
			expect((e as AuthHttpError).status).toBe(403);
		}
	});
});
