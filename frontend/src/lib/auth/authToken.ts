/**
 * Module-level holder for the current access token.
 *
 * Every fetch that hits a CyberdyneAuth-gated endpoint uses `withAuth()`
 * to inject `Authorization: Bearer <token>`. The auth view-model
 * updates the holder via {@link setAuthToken} on login / refresh /
 * restore / logout — never reach into module state from anywhere else.
 *
 * Why module-level (not a Svelte store): every downstream service
 * (`contentApi.ts`, the future chat client, the marketplace checkout
 * trigger) needs synchronous access to the token from arbitrary call
 * sites. A store would force every caller to `get()` it or subscribe.
 * The trade-off is that token rotation is invisible to reactive code —
 * which is fine, because nothing reactive should care about the token,
 * only whether the user is authenticated (that lives in the VM).
 */

let currentToken: string | null = null;

export function setAuthToken(token: string | null): void {
	currentToken = token;
}

export function getAuthToken(): string | null {
	return currentToken;
}

export function clearAuthToken(): void {
	currentToken = null;
}

/**
 * Returns a `Headers` instance with the bearer token attached if one is
 * set. Caller's headers win — only adds `Authorization` if the caller
 * didn't already set it. Safe to pass anywhere that accepts `HeadersInit`.
 */
export function withAuth(init?: HeadersInit): Headers {
	const headers = new Headers(init ?? {});
	if (currentToken && !headers.has('authorization')) {
		headers.set('Authorization', `Bearer ${currentToken}`);
	}
	return headers;
}
