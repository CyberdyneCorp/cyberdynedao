import { describe, it, expect, vi, afterEach } from 'vitest';
import { get } from 'svelte/store';
import {
	createDaoViewModel,
	formatCurrency,
	formatDecimals,
	formatDaoDate,
	getProposalStatusColor,
	getVotePercentage,
	computeCountdown,
	sumTreasury,
	acceptedProposalCount,
	successRate
} from '../daoViewModel';
import type { TreasuryAsset, DaoProposal, DividendInfo, OperationalData } from '$lib/types/dao';

const assets: TreasuryAsset[] = [
	{ symbol: 'ETH', name: 'Ethereum', balance: 1, usdValue: 100, change24h: 0 },
	{ symbol: 'USDC', name: 'USD Coin', balance: 50, usdValue: 50, change24h: 0 }
];
const proposals: DaoProposal[] = [
	{ id: 1, title: 't', description: '', proposer: 'p', status: 'accepted', votesFor: 100, votesAgainst: 50, totalVotes: 150, submittedDate: new Date(), endDate: new Date() },
	{ id: 2, title: 't', description: '', proposer: 'p', status: 'rejected', votesFor: 10, votesAgainst: 90, totalVotes: 100, submittedDate: new Date(), endDate: new Date() }
];
const dividend: DividendInfo = { nextDistribution: new Date(Date.now() + 1000 * 60 * 60 * 25), lastDistribution: new Date(), estimatedAmount: 10, totalHolders: 1000 };
const ops: OperationalData = { monthlyIncome: 1000, monthlyOperationalCosts: 500, netProfit: 500, profitMargin: 50 };

describe('daoViewModel helpers', () => {
	it('formatCurrency, formatDecimals, formatDaoDate', () => {
		expect(formatCurrency(1000)).toContain('1,000');
		expect(formatDecimals(1000, 2)).toBe('1,000.00');
		expect(formatDaoDate(new Date('2024-05-20T00:00:00Z'))).toMatch(/May/);
	});
	it('getProposalStatusColor all branches', () => {
		expect(getProposalStatusColor('accepted')).toContain('green');
		expect(getProposalStatusColor('rejected')).toContain('red');
		expect(getProposalStatusColor('pending')).toContain('yellow');
		expect(getProposalStatusColor('x')).toContain('gray');
	});
	it('getVotePercentage', () => {
		expect(getVotePercentage(50, 100)).toBe(50);
		expect(getVotePercentage(50, 0)).toBe(0);
	});
	it('computeCountdown future and past', () => {
		const future = new Date(Date.now() + 1000 * 60 * 60 * 25);
		expect(computeCountdown(future)).toMatch(/\d+d/);
		const past = new Date(Date.now() - 1000);
		expect(computeCountdown(past)).toMatch(/progress/);
	});
	it('sumTreasury', () => expect(sumTreasury(assets)).toBe(150));
	it('acceptedProposalCount', () => expect(acceptedProposalCount(proposals)).toBe(1));
	it('successRate', () => {
		expect(successRate(proposals)).toBe(50);
		expect(successRate([])).toBe(0);
	});
});

describe('daoViewModel factory', () => {
	afterEach(() => vi.useRealTimers());

	it('exposes data and initial countdown', () => {
		const vm = createDaoViewModel(assets, proposals, dividend, ops);
		expect(vm.totalTreasuryValue).toBe(150);
		expect(get(vm.timeUntilDividend)).toMatch(/d/);
	});

	it('tick updates countdown', () => {
		const vm = createDaoViewModel(assets, proposals, dividend, ops);
		const old = get(vm.timeUntilDividend);
		vm.tick(new Date(Date.now() + 1000 * 60 * 60 * 24));
		expect(get(vm.timeUntilDividend)).not.toBe(old);
	});

	it('startCountdown returns a cleanup that clears interval', () => {
		vi.useFakeTimers();
		const vm = createDaoViewModel(assets, proposals, dividend, ops);
		const cleanup = vm.startCountdown();
		vi.advanceTimersByTime(60001);
		cleanup();
	});

	it('defaults to built-in fixtures', () => {
		const vm = createDaoViewModel();
		expect(vm.treasuryAssets.length).toBeGreaterThan(0);
	});
});
