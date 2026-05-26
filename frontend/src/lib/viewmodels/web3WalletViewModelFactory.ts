/**
 * Default Web3Wallet VM wiring — keeps concrete service imports out of views.
 *
 * The component imports `createDefaultWeb3WalletViewModel()` and gets a fully
 * wired VM back, so Web3Wallet.svelte stays pure view code.
 *
 * Phase 7: Web3Auth is gone. All three sign-in paths (email, Google,
 * SIWE) route through CyberdyneAuth via the ``authVM`` + service layer.
 */
import { appKitService } from '$lib/web3/appKitService';
import { completeWalletDisconnect } from '$lib/utils/walletDisconnect';
import { walletInfo as web3WalletInfo } from '$lib/stores/web3Store';
import {
	createWeb3WalletViewModel,
	type CyberdyneUserLike,
	type Web3WalletViewModel
} from './web3WalletViewModel';
import { authVM } from '$lib/auth/authViewModel.svelte';
import { oauthAuthorizationUrl } from '$lib/auth/cyberdyneAuthService';

/** Fire-and-forget bootstrap. Initializes AppKit and restores any
 *  existing CyberdyneAuth session. Errors are intentionally swallowed
 *  so a missing VITE_REOWN_PROJECT_ID doesn't break the rest of the UI. */
export async function bootstrapWeb3Wallet(): Promise<void> {
	try {
		await Promise.allSettled([appKitService.initialize(), authVM.restore()]);
	} catch {
		/* non-fatal */
	}
}

function toCyberdyneUser(): CyberdyneUserLike | null {
	const u = authVM.user;
	if (!u) return null;
	const wallet = typeof u.wallet_address === 'string' ? u.wallet_address : null;
	const displayName =
		(typeof u.name === 'string' && u.name) ||
		(typeof u.full_name === 'string' && u.full_name) ||
		null;
	return {
		id: u.id,
		email: u.email,
		walletAddress: wallet,
		displayName
	};
}

export function createDefaultWeb3WalletViewModel(): Web3WalletViewModel {
	return createWeb3WalletViewModel({
		connectWalletConnect: async () => {
			const initialized = await appKitService.initialize();
			if (!initialized) throw new Error('Failed to initialize AppKit');
			await appKitService.openModal();
		},

		signPersonalMessage: async (message, address) =>
			appKitService.signPersonalMessage(message, address),

		loginWithEmail: async (email, password) => {
			await authVM.login(email, password);
			return toCyberdyneUser();
		},

		startGoogleOAuth: async () => {
			// Static adapter — no server to redirect through. Hit the
			// CyberdyneAuth ``/auth/oauth/google`` directly (via the
			// same-origin proxy) and navigate to whatever URL it returns.
			const callback = `${window.location.origin}/auth/callback`;
			const { authorization_url } = await oauthAuthorizationUrl('google', callback);
			window.location.assign(authorization_url);
		},

		loginWithWallet: async (opts) => {
			await authVM.loginWithWallet(opts);
			return toCyberdyneUser();
		},

		disconnect: async () => {
			try {
				await authVM.logout();
			} catch {
				/* best-effort — wallet teardown is still important */
			}
			return completeWalletDisconnect();
		},

		restoreSession: async () => {
			if (!authVM.isRestored) {
				await authVM.restore();
			}
			return toCyberdyneUser();
		},

		setGlobalWeb3Info: (info) => web3WalletInfo.set(info)
	});
}
