import { writable, derived, get, type Readable } from 'svelte/store';
import { browser } from '$app/environment';
import { CyberdyneAccessNFTManager, type NFTTraits, type UserNFTData } from '$lib/web3/contracts';
import { CONTRACT_ADDRESSES } from '$lib/web3/config';
import { walletAddress, isConnected } from './web3Store';

// NFT Access Manager instance - lazy initialization to avoid errors
let nftManager: CyberdyneAccessNFTManager | null = null;

function getNFTManager(): CyberdyneAccessNFTManager {
	if (!nftManager) {
		try {
			console.log('🏗️ AccessNFTStore: Initializing CyberdyneAccessNFTManager');
			console.log('📋 CONTRACT_ADDRESSES:', CONTRACT_ADDRESSES);
			console.log('📍 CYBERDYNE_ACCESS_NFT address:', CONTRACT_ADDRESSES.CYBERDYNE_ACCESS_NFT);
			
			if (!CONTRACT_ADDRESSES.CYBERDYNE_ACCESS_NFT) {
				throw new Error('CYBERDYNE_ACCESS_NFT contract address is not configured');
			}
			
			nftManager = new CyberdyneAccessNFTManager(CONTRACT_ADDRESSES.CYBERDYNE_ACCESS_NFT);
			console.log('✅ AccessNFTStore: NFT Manager created successfully');
		} catch (error) {
			console.error('❌ Failed to initialize NFT Manager:', error);
			throw error;
		}
	}
	return nftManager;
}

// Store state
export const userTraits = writable<NFTTraits | null>(null);
export const userNFTData = writable<UserNFTData | null>(null);
export const hasAccessNFT = writable<boolean>(false);
export const isLoadingTraits = writable<boolean>(false);
export const traitsError = writable<string | null>(null);

// Derived stores for specific access types
export const hasLearningAccess: Readable<boolean> = derived(
	userTraits,
	($traits) => $traits?.Learning ?? false
);

export const hasFrontendAccess: Readable<boolean> = derived(
	userTraits,
	($traits) => $traits?.Frontend ?? false
);

export const hasBackendAccess: Readable<boolean> = derived(
	userTraits,
	($traits) => $traits?.Backend ?? false
);

export const hasBlogCreatorAccess: Readable<boolean> = derived(
	userTraits,
	($traits) => $traits?.['Blog Creator'] ?? false
);

export const hasAdminAccess: Readable<boolean> = derived(
	userTraits,
	($traits) => $traits?.Admin ?? false
);

export const hasMarketplaceAccess: Readable<boolean> = derived(
	userTraits,
	($traits) => $traits?.Marketplace ?? false
);

// Derived store for checking if user has any access
export const hasAnyAccess: Readable<boolean> = derived(
	userTraits,
	($traits) => {
		if (!$traits) return false;
		return Object.values($traits).some(access => access === true);
	}
);

// Access NFT Actions
export const accessNFTActions = {
	// Load user traits and NFT data
	async loadUserTraits(address?: string) {
		console.log('🚀 AccessNFTStore: loadUserTraits called');
		
		if (!browser) {
			console.log('❌ Not in browser environment, skipping');
			return;
		}
		
		// Check if wallet is connected first
		const connectionStatus = get(isConnected);
		console.log('🔗 Current connection status:', connectionStatus);
		
		if (!connectionStatus) {
			console.log('❌ Wallet not connected, aborting trait loading');
			accessNFTActions.clearTraits();
			return;
		}
		
		if (!CONTRACT_ADDRESSES.CYBERDYNE_ACCESS_NFT) {
			console.warn('❌ CyberdyneAccessNFT contract address not configured');
			console.warn('Current CONTRACT_ADDRESSES:', CONTRACT_ADDRESSES);
			console.warn('Please set VITE_CYBERDYNE_ACCESS_NFT_ADDRESS in your .env file');
			return;
		}

		const userAddress = address || get(walletAddress);
		console.log('👤 User address for trait loading:', userAddress);
		
		if (!userAddress) {
			console.log('❌ No user address available, clearing traits');
			accessNFTActions.clearTraits();
			return;
		}
		
		console.log('✅ All prerequisites met for trait loading:');
		console.log('  - Browser environment: ✅');
		console.log('  - Wallet connected: ✅');
		console.log('  - Contract address configured: ✅');
		console.log('  - User address available: ✅');
		console.log('  - Contract address:', CONTRACT_ADDRESSES.CYBERDYNE_ACCESS_NFT);
		console.log('  - User address:', userAddress);

		console.log('⏳ Starting trait loading process...');
		isLoadingTraits.set(true);
		traitsError.set(null);

		try {
			console.log('🔍 Step 1: Checking if user has any access NFTs...');
			const manager = getNFTManager();
			const hasAccess = await manager.hasAnyAccess(userAddress);
			console.log('✅ User has access NFTs:', hasAccess);
			hasAccessNFT.set(hasAccess);

			if (hasAccess) {
				console.log('📊 Step 2: Loading user traits and NFT data...');
				const [traits, nftData] = await Promise.all([
					manager.getUserTraits(userAddress),
					manager.getUserPermissions(userAddress)
				]);
				
				console.log('🎯 Raw traits from contract:', traits);
				console.log('📋 Raw NFT data from contract:', nftData);

				userTraits.set(traits);
				userNFTData.set(nftData);
				
				console.log('✅ Traits and NFT data successfully loaded and stored');
			} else {
				console.log('❌ User has no access NFTs, clearing data');
				userTraits.set(null);
				userNFTData.set(null);
			}
		} catch (error) {
			console.error('💥 Error loading user traits:', error);
			console.error('Error details:', {
				name: error instanceof Error ? error.name : 'Unknown',
				message: error instanceof Error ? error.message : String(error),
				stack: error instanceof Error ? error.stack : undefined
			});
			traitsError.set(error instanceof Error ? error.message : 'Failed to load access data');
			accessNFTActions.clearTraits();
		} finally {
			console.log('🏁 Trait loading process finished');
			isLoadingTraits.set(false);
		}
	},

	// Clear all traits data
	clearTraits() {
		userTraits.set(null);
		userNFTData.set(null);
		hasAccessNFT.set(false);
		traitsError.set(null);
		isLoadingTraits.set(false);
	},

	// Refresh traits data
	async refreshTraits() {
		const address = get(walletAddress);
		if (address) {
			await accessNFTActions.loadUserTraits(address);
		}
	},

	// Clear error
	clearError() {
		traitsError.set(null);
	},

	// Get specific access type
	async checkSpecificAccess(address: string, accessType: 'learning' | 'frontend' | 'backend' | 'blog' | 'admin' | 'marketplace'): Promise<boolean> {
		try {
			const manager = getNFTManager();
			const traits = await manager.getUserTraits(address);
			if (!traits) return false;

			switch (accessType) {
				case 'learning':
					return traits.Learning;
				case 'frontend':
					return traits.Frontend;
				case 'backend':
					return traits.Backend;
				case 'blog':
					return traits['Blog Creator'];
				case 'admin':
					return traits.Admin;
				case 'marketplace':
					return traits.Marketplace;
				default:
					return false;
			}
		} catch (error) {
			console.error(`Error checking ${accessType} access:`, error);
			return false;
		}
	},

	// Manual trigger for testing - call this from browser console
	async manualLoadTraits() {
		console.log('🧪 Manual trait loading triggered');
		const address = get(walletAddress);
		const connected = get(isConnected);
		
		console.log('🔍 Current state:');
		console.log('  - Connected:', connected);
		console.log('  - Address:', address);
		console.log('  - Contract Address:', CONTRACT_ADDRESSES.CYBERDYNE_ACCESS_NFT);
		
		if (!connected || !address) {
			console.warn('⚠️ Wallet not connected or no address available');
			return;
		}
		
		await accessNFTActions.loadUserTraits(address);
	}
};

// Expose for debugging in browser console
if (browser && typeof window !== 'undefined') {
	(window as any).accessNFTActions = accessNFTActions;
	console.log('🧪 AccessNFT actions exposed to window.accessNFTActions for debugging');
}

// Auto-load traits when wallet connects/disconnects
if (browser) {
	console.log('🔄 AccessNFTStore: Setting up wallet connection subscriptions');
	
	// We need to track both connection state and address to ensure complete authentication
	let currentAddress = '';
	let currentConnectionStatus = false;
	
	// Subscribe to connection status changes first
	isConnected.subscribe((connected) => {
		console.log('🔗 AccessNFTStore: Connection status changed:', connected);
		currentConnectionStatus = connected;
		
		if (!connected) {
			console.log('❌ Wallet disconnected, clearing traits...');
			currentAddress = '';
			accessNFTActions.clearTraits();
		} else {
			console.log('✅ Wallet connected, checking for address...');
			// If we're connected and have an address, load traits
			if (currentAddress) {
				console.log('🎯 Both connected and address available, loading traits for:', currentAddress);
				accessNFTActions.loadUserTraits(currentAddress);
			}
		}
	});
	
	// Subscribe to wallet address changes
	walletAddress.subscribe((address) => {
		console.log('👤 AccessNFTStore: Wallet address changed:', address);
		currentAddress = address;
		
		if (address && currentConnectionStatus) {
			console.log('✅ Both address and connection status confirmed, loading traits...');
			console.log('📊 Loading traits for authenticated user:', address);
			accessNFTActions.loadUserTraits(address);
		} else if (!address) {
			console.log('❌ No address available, clearing traits...');
			accessNFTActions.clearTraits();
		} else {
			console.log('⏳ Address available but wallet not fully connected yet, waiting...');
		}
	});
}

// Utility function to get trait display name
export function getTraitDisplayName(trait: keyof NFTTraits): string {
	const displayNames: Record<keyof NFTTraits, string> = {
		Learning: 'Learning Materials',
		Frontend: 'Frontend Servers',
		Backend: 'Backend Servers',
		'Blog Creator': 'Blog Creator',
		Admin: 'Administrator',
		Marketplace: 'Marketplace Seller'
	};
	
	return displayNames[trait];
}

// Utility function to get active traits list
export function getActiveTraits(traits: NFTTraits | null): string[] {
	if (!traits) return [];
	
	return Object.entries(traits)
		.filter(([_, hasAccess]) => hasAccess)
		.map(([trait, _]) => getTraitDisplayName(trait as keyof NFTTraits));
}