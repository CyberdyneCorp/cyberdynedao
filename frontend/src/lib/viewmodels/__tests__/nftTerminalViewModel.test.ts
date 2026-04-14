import { describe, it, expect } from 'vitest';
import {
	buildNFTUrl,
	truncateWalletAddress,
	listActiveTraitLabels
} from '../nftTerminalViewModel';
import type { NFTTraits } from '$lib/web3/contracts';

const traits: NFTTraits = {
	Learning: true,
	Frontend: false,
	Backend: true,
	'Blog Creator': true,
	Admin: false,
	Marketplace: false
};

describe('nftTerminalViewModel', () => {
	it('truncateWalletAddress', () => {
		expect(truncateWalletAddress(null)).toBe('unknown');
		expect(truncateWalletAddress('')).toBe('unknown');
		expect(truncateWalletAddress('0x1234567890abcdef1234567890abcdef12345678')).toBe('0x1234...5678');
	});
	it('buildNFTUrl default when missing wallet or traits', () => {
		expect(buildNFTUrl(null, '0xabc')).toContain('cyberdyne_nft_enhanced.svg');
		expect(buildNFTUrl(traits, '')).toContain('cyberdyne_nft_enhanced.svg');
	});
	it('buildNFTUrl includes params for wallet + traits', () => {
		const url = buildNFTUrl(traits, '0xabc', new Date('2024-01-15T00:00:00Z'));
		expect(url).toContain('learning=1');
		expect(url).toContain('frontend=0');
		expect(url).toContain('backend=1');
		expect(url).toContain('blog=1');
		expect(url).toContain('admin=0');
		expect(url).toContain('market=0');
		expect(url).toContain('wallet=0xabc');
		expect(url).toContain('issued=2024-01-15');
	});
	it('listActiveTraitLabels', () => {
		expect(listActiveTraitLabels(null)).toEqual([]);
		const labels = listActiveTraitLabels(traits);
		expect(labels).toContain('Blog Creator');
		expect(labels).toContain('LEARNING');
		expect(labels).toContain('BACKEND');
	});
});
