/**
 * CyberdyneAuth HTTP client.
 *
 * Talks to the upstream `auth.backend.coolify.cyberdynecorp.ai` via a
 * **same-origin reverse proxy** (`/api/auth/api/v1/*`). In prod the
 * proxy is an nginx `location` block in the frontend container; in dev
 * it's a Vite proxy entry. Same-origin means:
 *
 *  - No CORS preflight on every request.
 *  - The auth host never appears in `import.meta.env.VITE_*`, so a
 *    Coolify env-var typo can't accidentally break login.
 *  - We can serve `<a href="/api/auth/api/v1/auth/oauth/google?...">`
 *    style redirects without leaking the upstream URL to the page.
 *
 * Wire format mirrors the upstream OpenAPI verbatim — `LoginRequest`,
 * `TokenResponse`, `WalletChallengeRequest`, etc. If we ever need to
 * change shape, fix it on the auth server, don't shim it here.
 */

import { withAuth } from './authToken';

const AUTH_BASE = '/api/auth/api/v1';

export interface TokenResponse {
	access_token: string;
	refresh_token: string;
	token_type: string; // always "bearer"
}

/** Server-side user profile. Fields beyond `id` + `email` are best-effort. */
export interface AuthUser {
	id: string;
	email: string;
	wallet_address?: string | null;
	is_active?: boolean;
	scopes?: string[];
	/** CyberdyneAuth admin flag. Surfaced under one of these keys
	 * depending on the auth-server version; any truthy one grants the
	 * authoring surface (see `authVM.isAdmin`). */
	is_superuser?: boolean;
	is_admin?: boolean;
	is_staff?: boolean;
	[k: string]: unknown;
}

export interface WalletChallengeResponse {
	challenge_id: string;
	message: string; // EIP-4361 SIWE message — sign this with personal_sign
	nonce: string;
	expires_in_seconds: number;
}

export interface WalletTokenResponse extends TokenResponse {
	is_new_user: boolean;
	wallet_address: string;
}

export interface OAuthAuthorizationUrlResponse {
	authorization_url: string;
}

class AuthHttpError extends Error {
	constructor(public readonly status: number, message: string) {
		super(message);
		this.name = 'AuthHttpError';
	}
}

async function readError(res: Response): Promise<string> {
	try {
		const body = (await res.json()) as { detail?: unknown };
		if (typeof body.detail === 'string') return body.detail;
		if (Array.isArray(body.detail)) {
			return body.detail
				.map((d: unknown) => (typeof d === 'object' && d && 'msg' in d ? String((d as { msg: unknown }).msg) : JSON.stringify(d)))
				.join('; ');
		}
		return `HTTP ${res.status}`;
	} catch {
		return `HTTP ${res.status}`;
	}
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
	const res = await fetch(`${AUTH_BASE}${path}`, {
		method: 'POST',
		headers: { 'content-type': 'application/json' },
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new AuthHttpError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function getJson<T>(path: string, opts: { withBearer?: boolean } = {}): Promise<T> {
	const headers = opts.withBearer ? withAuth() : new Headers();
	const res = await fetch(`${AUTH_BASE}${path}`, { method: 'GET', headers });
	if (!res.ok) throw new AuthHttpError(res.status, await readError(res));
	return (await res.json()) as T;
}

// ── Email + password ─────────────────────────────────────────────────

export function login(email: string, password: string): Promise<TokenResponse> {
	return postJson<TokenResponse>('/auth/login', { email, password });
}

export function refresh(refreshToken: string): Promise<TokenResponse> {
	return postJson<TokenResponse>('/auth/refresh', { refresh_token: refreshToken });
}

export async function logout(refreshToken: string | null): Promise<void> {
	// Best-effort. We always clear local state regardless of upstream.
	if (!refreshToken) return;
	try {
		await postJson('/auth/logout', { refresh_token: refreshToken });
	} catch {
		/* swallow — local logout already happened */
	}
}

// ── Profile (used by callback to validate + hydrate) ─────────────────

export function getProfile(): Promise<AuthUser> {
	return getJson<AuthUser>('/users/me', { withBearer: true });
}

// ── OAuth (Google) ───────────────────────────────────────────────────

/**
 * Asks the auth server for the provider's authorization URL. Caller
 * should `window.location.assign(authorization_url)` — Google sends the
 * user back to `frontend_redirect` with tokens in the URL fragment.
 *
 * `return_mode=fragment` keeps tokens out of server access logs.
 */
export function oauthAuthorizationUrl(
	provider: 'google',
	frontendRedirect: string
): Promise<OAuthAuthorizationUrlResponse> {
	const qs = new URLSearchParams({
		frontend_redirect: frontendRedirect,
		return_mode: 'fragment'
	});
	return getJson<OAuthAuthorizationUrlResponse>(`/auth/oauth/${provider}?${qs}`);
}

// ── Wallet (SIWE) ────────────────────────────────────────────────────

export function walletChallenge(
	walletAddress: string,
	chainId: number
): Promise<WalletChallengeResponse> {
	return postJson<WalletChallengeResponse>('/auth/wallet/challenge', {
		wallet_address: walletAddress,
		chain_id: chainId
	});
}

export function walletVerify(
	challengeId: string,
	signature: string
): Promise<WalletTokenResponse> {
	return postJson<WalletTokenResponse>('/auth/wallet/verify', {
		challenge_id: challengeId,
		signature
	});
}

// Re-export the error for callers that want to inspect HTTP status.
export { AuthHttpError };
