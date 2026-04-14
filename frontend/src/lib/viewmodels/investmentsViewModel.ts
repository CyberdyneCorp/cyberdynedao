import { writable, type Writable } from 'svelte/store';
import type { LiquidityPosition } from '$lib/data/investments';
import { liquidityPositions as defaultPositions } from '$lib/data/investments';

export type InvestmentsTab = 'positions' | 'analytics';

export interface PoolStats {
	totalValueLocked: number;
	totalPnL: number;
	averageAPY: number;
	activePositions: number;
}

export function formatInvestmentPrice(price: number, decimals = 2): string {
	if (price >= 1000) return `$${(price / 1000).toFixed(1)}k`;
	return `$${price.toFixed(decimals)}`;
}

export function formatInvestmentNumber(num: number, decimals = 2): string {
	if (num >= 1000) return `${(num / 1000).toFixed(1)}k`;
	return num.toFixed(decimals);
}

export function getPnLColor(value: number): string {
	return value >= 0 ? 'text-green-500' : 'text-red-500';
}

export function getPositionStatusColor(status: string): string {
	return status === 'in-range' ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100';
}

export function computePoolStats(positions: LiquidityPosition[]): PoolStats {
	if (positions.length === 0) {
		return { totalValueLocked: 0, totalPnL: 0, averageAPY: 0, activePositions: 0 };
	}
	return {
		totalValueLocked: positions.reduce((sum, p) => sum + p.totalValue, 0),
		totalPnL: positions.reduce((sum, p) => sum + p.totalPnL, 0),
		averageAPY: positions.reduce((sum, p) => sum + p.feeAPY, 0) / positions.length,
		activePositions: positions.filter(p => p.status === 'in-range').length
	};
}

export function computePriceIndicator(position: LiquidityPosition): { clamped: number; inRange: boolean } {
	const span = position.maxPrice - position.minPrice;
	const ratio = span === 0 ? 0 : ((position.currentPrice - position.minPrice) / span) * 100;
	return {
		clamped: Math.min(Math.max(ratio, 0), 100),
		inRange: position.currentPrice >= position.minPrice && position.currentPrice <= position.maxPrice
	};
}

export interface InvestmentsViewModel {
	positions: LiquidityPosition[];
	poolStats: PoolStats;
	activeTab: Writable<InvestmentsTab>;
	selectedPosition: Writable<LiquidityPosition | null>;
	selectPosition: (p: LiquidityPosition | null) => void;
	setTab: (t: InvestmentsTab) => void;
}

export function createInvestmentsViewModel(
	positions: LiquidityPosition[] = defaultPositions
): InvestmentsViewModel {
	const activeTab = writable<InvestmentsTab>('positions');
	const selectedPosition = writable<LiquidityPosition | null>(null);
	return {
		positions,
		poolStats: computePoolStats(positions),
		activeTab,
		selectedPosition,
		selectPosition: (p) => selectedPosition.set(p),
		setTab: (t) => activeTab.set(t)
	};
}
