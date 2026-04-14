import type { NFTTraits } from '$lib/web3/contracts';

const DEFAULT_NFT_URL = '/assets/cyberdyne_nft_enhanced.svg';

export function truncateWalletAddress(address: string | undefined | null): string {
	if (!address) return 'unknown';
	return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

export function buildNFTUrl(
	traits: NFTTraits | null,
	walletAddress: string,
	today: Date = new Date()
): string {
	if (!traits || !walletAddress) return DEFAULT_NFT_URL;
	const issued = today.toISOString().split('T')[0];
	const params = new URLSearchParams({
		learning: traits.Learning ? '1' : '0',
		frontend: traits.Frontend ? '1' : '0',
		backend: traits.Backend ? '1' : '0',
		blog: traits['Blog Creator'] ? '1' : '0',
		admin: traits.Admin ? '1' : '0',
		market: traits.Marketplace ? '1' : '0',
		issued,
		wallet: walletAddress
	});
	return `${DEFAULT_NFT_URL}?${params.toString()}`;
}

export function listActiveTraitLabels(traits: NFTTraits | null): string[] {
	if (!traits) return [];
	return Object.entries(traits)
		.filter(([, value]) => value)
		.map(([key]) => (key === 'Blog Creator' ? 'Blog Creator' : key.toUpperCase()));
}
