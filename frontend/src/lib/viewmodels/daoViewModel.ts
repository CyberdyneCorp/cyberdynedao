import { writable, derived, type Readable, type Writable } from 'svelte/store';
import type { TreasuryAsset, DaoProposal, DividendInfo, OperationalData } from '$lib/types/dao';
import {
	treasuryAssets as defaultTreasury,
	recentProposals as defaultProposals,
	dividendInfo as defaultDividend,
	operationalData as defaultOps
} from '$lib/constants/daoData';

export function formatCurrency(amount: number): string {
	return new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: 'USD',
		minimumFractionDigits: 2,
		maximumFractionDigits: 2
	}).format(amount);
}

export function formatDecimals(num: number, decimals = 2): string {
	return new Intl.NumberFormat('en-US', {
		minimumFractionDigits: decimals,
		maximumFractionDigits: decimals
	}).format(num);
}

export function formatDaoDate(date: Date): string {
	return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

export function getProposalStatusColor(status: string): string {
	switch (status) {
		case 'accepted': return 'text-green-600 bg-green-100';
		case 'rejected': return 'text-red-600 bg-red-100';
		case 'pending': return 'text-yellow-600 bg-yellow-100';
		default: return 'text-gray-600 bg-gray-100';
	}
}

export function getVotePercentage(votesFor: number, totalVotes: number): number {
	return totalVotes > 0 ? (votesFor / totalVotes) * 100 : 0;
}

export function computeCountdown(target: Date, now: Date = new Date()): string {
	const diff = target.getTime() - now.getTime();
	if (diff <= 0) return 'Distribution in progress...';
	const days = Math.floor(diff / (1000 * 60 * 60 * 24));
	const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
	return `${days}d ${hours}h ${minutes}m`;
}

export function sumTreasury(assets: TreasuryAsset[]): number {
	return assets.reduce((sum, a) => sum + a.usdValue, 0);
}

export function acceptedProposalCount(proposals: DaoProposal[]): number {
	return proposals.filter(p => p.status === 'accepted').length;
}

export function successRate(proposals: DaoProposal[]): number {
	if (proposals.length === 0) return 0;
	return (acceptedProposalCount(proposals) / proposals.length) * 100;
}

export interface DaoViewModel {
	treasuryAssets: TreasuryAsset[];
	recentProposals: DaoProposal[];
	dividendInfo: DividendInfo;
	operationalData: OperationalData;
	totalTreasuryValue: number;
	timeUntilDividend: Readable<string>;
	startCountdown: () => () => void;
	tick: (now?: Date) => void;
}

export function createDaoViewModel(
	assets: TreasuryAsset[] = defaultTreasury,
	proposals: DaoProposal[] = defaultProposals,
	dividend: DividendInfo = defaultDividend,
	ops: OperationalData = defaultOps
): DaoViewModel {
	const countdownStore: Writable<string> = writable(computeCountdown(dividend.nextDistribution));

	const tick = (now: Date = new Date()) => {
		countdownStore.set(computeCountdown(dividend.nextDistribution, now));
	};

	const startCountdown = () => {
		tick();
		const interval = setInterval(tick, 60000);
		return () => clearInterval(interval);
	};

	return {
		treasuryAssets: assets,
		recentProposals: proposals,
		dividendInfo: dividend,
		operationalData: ops,
		totalTreasuryValue: sumTreasury(assets),
		timeUntilDividend: derived(countdownStore, (v) => v),
		startCountdown,
		tick
	};
}
