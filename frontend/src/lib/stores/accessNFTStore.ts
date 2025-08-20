import { writable, derived, type Readable } from 'svelte/store';
import { browser } from '$app/environment';
import { CyberdyneAccessNFTManager, type NFTTraits, type UserNFTData } from '$lib/web3/contracts';
import { CONTRACT_ADDRESSES } from '$lib/web3/config';
import { walletAddress, isConnected } from './web3Store';

// NFT Access Manager instance
const nftManager = new CyberdyneAccessNFTManager(CONTRACT_ADDRESSES.CYBERDYNE_ACCESS_NFT);

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
		if (!browser) return;
		if (!CONTRACT_ADDRESSES.CYBERDYNE_ACCESS_NFT) {
			console.warn('CyberdyneAccessNFT contract address not configured');
			return;
		}

		const userAddress = address || walletAddress.get();
		if (!userAddress) {
			accessNFTActions.clearTraits();
			return;
		}

		isLoadingTraits.set(true);
		traitsError.set(null);

		try {
			// Check if user has any access NFTs
			const hasAccess = await nftManager.hasAnyAccess(userAddress);
			hasAccessNFT.set(hasAccess);

			if (hasAccess) {
				// Load user traits and NFT data
				const [traits, nftData] = await Promise.all([
					nftManager.getUserTraits(userAddress),
					nftManager.getUserPermissions(userAddress)
				]);

				userTraits.set(traits);
				userNFTData.set(nftData);
			} else {
				userTraits.set(null);
				userNFTData.set(null);
			}
		} catch (error) {
			console.error('Error loading user traits:', error);
			traitsError.set(error instanceof Error ? error.message : 'Failed to load access data');
			accessNFTActions.clearTraits();
		} finally {
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
		const address = walletAddress.get();
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
			const traits = await nftManager.getUserTraits(address);
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
	}
};

// Auto-load traits when wallet connects/disconnects
if (browser) {
	// Subscribe to wallet address changes
	walletAddress.subscribe((address) => {
		if (address) {
			accessNFTActions.loadUserTraits(address);
		} else {
			accessNFTActions.clearTraits();
		}
	});

	// Subscribe to connection status changes
	isConnected.subscribe((connected) => {
		if (!connected) {
			accessNFTActions.clearTraits();
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