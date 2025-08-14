import { writable, derived, type Readable } from 'svelte/store';
import { browser } from '$app/environment';
import { walletManager, type WalletInfo } from '$lib/web3/wallet';
import { BASE_NETWORK } from '$lib/web3/config';

// Wallet connection state
export const walletInfo = writable<WalletInfo | null>(null);

// Connection status
export const isConnected: Readable<boolean> = derived(
	walletInfo,
	($walletInfo) => $walletInfo?.isConnected ?? false
);

// Wallet address
export const walletAddress: Readable<string> = derived(
	walletInfo,
	($walletInfo) => $walletInfo?.address ?? ''
);

// Wallet balance
export const walletBalance: Readable<string> = derived(
	walletInfo,
	($walletInfo) => $walletInfo?.balance ?? '0'
);

// Network info
export const currentChainId: Readable<number> = derived(
	walletInfo,
	($walletInfo) => $walletInfo?.chainId ?? BASE_NETWORK.chainId
);

// Check if on correct network
export const isCorrectNetwork: Readable<boolean> = derived(
	currentChainId,
	($chainId) => $chainId === BASE_NETWORK.chainId
);

// Loading states
export const isConnecting = writable<boolean>(false);
export const connectionError = writable<string | null>(null);

// Web3 Actions
export const web3Actions = {
	// Connect wallet
	async connectWallet() {
		if (!browser) return;
		
		isConnecting.set(true);
		connectionError.set(null);

		try {
			const info = await walletManager.connectWallet();
			walletInfo.set(info);
		} catch (error) {
			console.error('Failed to connect wallet:', error);
			connectionError.set(error instanceof Error ? error.message : 'Failed to connect wallet');
		} finally {
			isConnecting.set(false);
		}
	},

	// Disconnect wallet
	async disconnectWallet() {
		await walletManager.disconnectWallet();
		walletInfo.set(null);
		connectionError.set(null);
	},

	// Complete disconnect - clears all wallet state and storage
	async completeDisconnect() {
		console.log('Web3Store: Complete disconnect initiated');
		
		try {
			await walletManager.disconnectWallet();
		} catch (error) {
			console.warn('Web3Store: Error disconnecting wallet manager:', error);
		}
		
		// Reset all store state
		walletInfo.set(null);
		connectionError.set(null);
		isConnecting.set(false);
		
		console.log('Web3Store: All state reset');
	},

	// Refresh wallet info
	async refreshWalletInfo() {
		if (!browser) return;
		
		try {
			const info = await walletManager.getWalletInfo();
			walletInfo.set(info);
		} catch (error) {
			console.error('Failed to refresh wallet info:', error);
		}
	},

	// Switch to Base network
	async switchToBaseNetwork() {
		if (!browser) return;
		
		try {
			await walletManager.switchToBaseNetwork();
			// Refresh wallet info after network switch
			setTimeout(() => {
				web3Actions.refreshWalletInfo();
			}, 1000);
		} catch (error) {
			console.error('Failed to switch network:', error);
			connectionError.set('Failed to switch to Base network');
		}
	},

	// Clear error
	clearError() {
		connectionError.set(null);
	}
};

// Initialize wallet connection on page load (if previously connected)
if (browser) {
	// Check if wallet was previously connected
	const checkConnection = async () => {
		try {
			if (walletManager.isWalletAvailable()) {
				const info = await walletManager.getWalletInfo();
				if (info) {
					walletInfo.set(info);
				}
			}
		} catch (error) {
			// Silently fail - wallet might not be connected
		}
	};

	// Check connection when the page loads
	checkConnection();

	// Listen for wallet events
	if (typeof window !== 'undefined') {
		window.addEventListener('wallet:accountsChanged', (event: any) => {
			const accounts = event.detail;
			if (accounts.length === 0) {
				walletInfo.set(null);
			} else {
				web3Actions.refreshWalletInfo();
			}
		});

		window.addEventListener('wallet:chainChanged', () => {
			web3Actions.refreshWalletInfo();
		});

		window.addEventListener('wallet:disconnected', () => {
			walletInfo.set(null);
		});
	}
}

// Utility store for formatted address
export const shortAddress: Readable<string> = derived(
	walletAddress,
	($address) => {
		if (!$address) return '';
		return `${$address.slice(0, 6)}...${$address.slice(-4)}`;
	}
);