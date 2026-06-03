/**
 * CyberdyneAuth session view-model.
 *
 * Single source of truth for the logged-in user across the app. Three
 * entry points all converge on `installSession(access, refresh, user?)`:
 *
 *   - Email + password  → service.login → installSession
 *   - Google OAuth      → /auth/callback parses #hash → installSession
 *   - Wallet SIWE       → AppKit connect → service.walletChallenge →
 *                         wallet personal_sign → service.walletVerify →
 *                         installSession
 *
 * Persistence: sessionStorage under `cyberdyne.auth.v1`. Cleared on
 * tab close on purpose — refresh-on-tab-close is the geo_dashboard
 * pattern and avoids stale tokens lingering on shared devices.
 *
 * Proactive refresh: scheduled at 75 % of remaining JWT lifetime via
 * the `exp` claim. If the refresh roundtrip fails, the session clears
 * and the user is forced to re-auth — no silent half-state.
 */

import {
	getProfile,
	login as svcLogin,
	logout as svcLogout,
	refresh as svcRefresh,
	walletChallenge,
	walletVerify,
	type AuthUser
} from './cyberdyneAuthService';
import { clearAuthToken, setAuthToken } from './authToken';

const STORAGE_KEY = 'cyberdyne.auth.v1';
const REFRESH_LEAD_FRACTION = 0.75; // refresh at 75 % of remaining lifetime
const MIN_REFRESH_DELAY_MS = 30_000;

interface PersistedSession {
	token: string;
	refreshToken: string;
	user: AuthUser | null;
	expiresAt: number; // epoch ms; 0 if unknown
}

function decodeJwtExpMs(token: string): number {
	// Best-effort JWT exp decode. If anything fails we return 0 and rely
	// on the server to 401, which the next call's catch handles.
	try {
		const payload = token.split('.')[1];
		if (!payload) return 0;
		const json = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
		const claims = JSON.parse(json) as { exp?: number };
		return typeof claims.exp === 'number' ? claims.exp * 1000 : 0;
	} catch {
		return 0;
	}
}

function readPersisted(): PersistedSession | null {
	if (typeof sessionStorage === 'undefined') return null;
	try {
		const raw = sessionStorage.getItem(STORAGE_KEY);
		if (!raw) return null;
		const parsed = JSON.parse(raw) as PersistedSession;
		if (typeof parsed.token !== 'string' || typeof parsed.refreshToken !== 'string') {
			return null;
		}
		return parsed;
	} catch {
		return null;
	}
}

function writePersisted(s: PersistedSession): void {
	if (typeof sessionStorage === 'undefined') return;
	try {
		sessionStorage.setItem(STORAGE_KEY, JSON.stringify(s));
	} catch {
		/* quota / private-mode — non-fatal */
	}
}

function wipePersisted(): void {
	if (typeof sessionStorage === 'undefined') return;
	try {
		sessionStorage.removeItem(STORAGE_KEY);
	} catch {
		/* ignore */
	}
}

export interface AuthViewModel {
	// Reactive state.
	readonly token: string | null;
	readonly refreshToken: string | null;
	readonly user: AuthUser | null;
	readonly expiresAt: number;
	readonly isAuthenticated: boolean;
	/** True when the signed-in user carries the `editor` scope — gates
	 * the admin authoring surface (course/lesson/quiz CMS). */
	readonly isEditor: boolean;
	/** True when CyberdyneAuth marks the user as an admin. Admins reach
	 * the authoring surface even without the `editor` scope, which the
	 * (currently disabled) on-chain policy engine would otherwise grant. */
	readonly isAdmin: boolean;
	readonly isRestored: boolean;
	readonly loading: boolean;
	readonly error: string | null;

	// Lifecycle.
	restore(): Promise<void>;
	login(email: string, password: string): Promise<void>;
	logout(): Promise<void>;
	refreshAccessToken(): Promise<void>;
	installSession(
		accessToken: string,
		refreshToken: string,
		preloadedUser?: AuthUser | null
	): Promise<void>;

	/**
	 * SIWE — caller provides a `sign` callback that hands the message
	 * to the connected wallet and returns the signature. The VM owns
	 * the challenge / verify roundtrip + session install.
	 */
	loginWithWallet(opts: {
		walletAddress: string;
		chainId: number;
		sign: (message: string) => Promise<string>;
	}): Promise<void>;

	clearError(): void;
}

export function createAuthVM(): AuthViewModel {
	let token = $state<string | null>(null);
	let refreshToken = $state<string | null>(null);
	let user = $state<AuthUser | null>(null);
	let expiresAt = $state<number>(0);
	let isRestored = $state<boolean>(false);
	let loading = $state<boolean>(false);
	let error = $state<string | null>(null);

	let refreshTimer: ReturnType<typeof setTimeout> | null = null;

	function clearTimer(): void {
		if (refreshTimer !== null) {
			clearTimeout(refreshTimer);
			refreshTimer = null;
		}
	}

	function scheduleRefresh(): void {
		clearTimer();
		if (!refreshToken || expiresAt <= 0) return;
		const remaining = expiresAt - Date.now();
		if (remaining <= 0) {
			// Already expired — fire immediately.
			void doRefresh();
			return;
		}
		const delay = Math.max(MIN_REFRESH_DELAY_MS, remaining * REFRESH_LEAD_FRACTION);
		refreshTimer = setTimeout(() => {
			void doRefresh();
		}, delay);
	}

	function setSession(t: string, r: string, u: AuthUser | null): void {
		token = t;
		refreshToken = r;
		user = u;
		expiresAt = decodeJwtExpMs(t);
		setAuthToken(t);
		writePersisted({ token: t, refreshToken: r, user: u, expiresAt });
		scheduleRefresh();
	}

	function clearLocal(): void {
		clearTimer();
		token = null;
		refreshToken = null;
		user = null;
		expiresAt = 0;
		clearAuthToken();
		wipePersisted();
	}

	async function doRefresh(): Promise<void> {
		const r = refreshToken;
		if (!r) return;
		try {
			const tok = await svcRefresh(r);
			// Refresh response may not carry the user; preserve current.
			setSession(tok.access_token, tok.refresh_token, user);
		} catch {
			clearLocal();
			error = 'Session expired. Please sign in again.';
		}
	}

	async function installSession(
		accessToken: string,
		newRefreshToken: string,
		preloadedUser: AuthUser | null = null
	): Promise<void> {
		// Set the token first so getProfile() picks it up via withAuth().
		setAuthToken(accessToken);
		let resolvedUser = preloadedUser;
		if (!resolvedUser) {
			try {
				resolvedUser = await getProfile();
			} catch {
				resolvedUser = null;
			}
		}
		setSession(accessToken, newRefreshToken, resolvedUser);
	}

	async function login(email: string, password: string): Promise<void> {
		loading = true;
		error = null;
		try {
			const tok = await svcLogin(email, password);
			await installSession(tok.access_token, tok.refresh_token);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Login failed.';
			throw e;
		} finally {
			loading = false;
		}
	}

	async function loginWithWallet(opts: {
		walletAddress: string;
		chainId: number;
		sign: (message: string) => Promise<string>;
	}): Promise<void> {
		loading = true;
		error = null;
		try {
			const challenge = await walletChallenge(opts.walletAddress, opts.chainId);
			const signature = await opts.sign(challenge.message);
			const tok = await walletVerify(challenge.challenge_id, signature);
			// Server tells us if this is the user's first sign-in via this wallet
			// — useful UX hook for a "Welcome" toast later.
			await installSession(tok.access_token, tok.refresh_token);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Wallet sign-in failed.';
			throw e;
		} finally {
			loading = false;
		}
	}

	async function logout(): Promise<void> {
		const r = refreshToken;
		clearLocal(); // local first — UI updates immediately
		await svcLogout(r);
	}

	async function restore(): Promise<void> {
		const persisted = readPersisted();
		if (!persisted) {
			isRestored = true;
			return;
		}
		setAuthToken(persisted.token);
		token = persisted.token;
		refreshToken = persisted.refreshToken;
		user = persisted.user;
		expiresAt = persisted.expiresAt;

		// Validate. If expired, try a refresh; if that fails, drop session.
		if (expiresAt > 0 && Date.now() >= expiresAt) {
			await doRefresh();
		} else {
			scheduleRefresh();
		}
		isRestored = true;
	}

	function clearError(): void {
		error = null;
	}

	return {
		get token() { return token; },
		get refreshToken() { return refreshToken; },
		get user() { return user; },
		get expiresAt() { return expiresAt; },
		get isAuthenticated() { return token !== null; },
		get isEditor() {
			return Array.isArray(user?.scopes) && user.scopes.includes('editor');
		},
		get isAdmin() {
			return Boolean(user?.is_superuser || user?.is_admin || user?.is_staff);
		},
		get isRestored() { return isRestored; },
		get loading() { return loading; },
		get error() { return error; },
		restore,
		login,
		logout,
		refreshAccessToken: doRefresh,
		installSession,
		loginWithWallet,
		clearError
	};
}

// Single shared instance for the whole app. Re-imported wherever the
// session needs to be read or mutated. Same shape as the geo_dashboard
// pattern of `vms.auth` passed through context — we use a module export
// because the app has a single root and no preview/SSR split.
export const authVM = createAuthVM();
