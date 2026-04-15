/**
 * Default Web3Wallet VM wiring — keeps concrete service imports out of views.
 *
 * The component imports `createDefaultWeb3WalletViewModel()` and gets a fully
 * wired VM back, so Web3Wallet.svelte stays pure view code.
 */
import { web3AuthService } from '$lib/web3/web3AuthService';
import { appKitService } from '$lib/web3/appKitService';
import { completeWalletDisconnect } from '$lib/utils/walletDisconnect';
import { walletInfo as web3WalletInfo } from '$lib/stores/web3Store';
import {
	createWeb3WalletViewModel,
	type Web3AuthUserLike,
	type Web3WalletViewModel
} from './web3WalletViewModel';

/**
 * Fire-and-forget initialization of the wallet services + polyfills.
 * Call from onMount. Errors are intentionally swallowed so UI doesn't break
 * when the user hasn't configured wallets.
 */
export async function bootstrapWeb3Wallet(): Promise<void> {
	try {
		const { polyfillsReady } = await import('$lib/polyfills');
		await polyfillsReady;
		appKitService.initialize().catch(() => {});
	} catch {
		// non-fatal
	}
}

export function createDefaultWeb3WalletViewModel(): Web3WalletViewModel {
	return createWeb3WalletViewModel({
		connectWalletConnect: async () => {
			const initialized = await appKitService.initialize();
			if (!initialized) throw new Error('Failed to initialize AppKit');
			await appKitService.openModal();
		},
		connectWeb3Auth: async () => {
			const { polyfillsReady } = await import('$lib/polyfills');
			await polyfillsReady;
			const user = await web3AuthService.loginWithGoogle();
			return user as Web3AuthUserLike | null;
		},
		disconnect: async () => completeWalletDisconnect(),
		checkAuthStatus: async () => {
			const user = await web3AuthService.checkAuthStatus();
			return user as Web3AuthUserLike | null;
		},
		setGlobalWeb3Info: (info) => web3WalletInfo.set(info)
	});
}
