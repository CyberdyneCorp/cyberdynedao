import { describe, it, expect } from 'vitest';
import { get } from 'svelte/store';
import {
	createInvestmentsViewModel,
	formatInvestmentPrice,
	formatInvestmentNumber,
	getPnLColor,
	getPositionStatusColor,
	computePoolStats,
	computePriceIndicator
} from '../investmentsViewModel';
import type { LiquidityPosition } from '$lib/data/investments';

const positions: LiquidityPosition[] = [
	{
		id: 'a', pair: 'A/B', token0: 'A', token1: 'B', token0Logo: '🔷', token1Logo: '💵',
		totalValue: 1500, minPrice: 1, maxPrice: 2, currentPrice: 1.5, feeAPY: 10,
		pooledAssets: { token0Amount: 1, token1Amount: 1 }, totalPnL: 100, totalAPR: 10,
		uncollectedFees: 1, status: 'in-range', compound: true
	},
	{
		id: 'b', pair: 'X/Y', token0: 'X', token1: 'Y', token0Logo: '🦄', token1Logo: '🔷',
		totalValue: 500, minPrice: 10, maxPrice: 20, currentPrice: 25, feeAPY: 20,
		pooledAssets: { token0Amount: 0, token1Amount: 0 }, totalPnL: -50, totalAPR: -5,
		uncollectedFees: 0, status: 'out-of-range', compound: false
	}
];

describe('investmentsViewModel helpers', () => {
	it('formatInvestmentPrice ranges', () => {
		expect(formatInvestmentPrice(5000)).toBe('$5.0k');
		expect(formatInvestmentPrice(50, 2)).toBe('$50.00');
	});
	it('formatInvestmentNumber ranges', () => {
		expect(formatInvestmentNumber(3000)).toBe('3.0k');
		expect(formatInvestmentNumber(1.2345, 2)).toBe('1.23');
	});
	it('getPnLColor', () => {
		expect(getPnLColor(10)).toContain('green');
		expect(getPnLColor(-5)).toContain('red');
	});
	it('getPositionStatusColor', () => {
		expect(getPositionStatusColor('in-range')).toContain('green');
		expect(getPositionStatusColor('out-of-range')).toContain('red');
	});
	it('computePoolStats for empty and populated', () => {
		expect(computePoolStats([])).toEqual({ totalValueLocked: 0, totalPnL: 0, averageAPY: 0, activePositions: 0 });
		const stats = computePoolStats(positions);
		expect(stats.totalValueLocked).toBe(2000);
		expect(stats.totalPnL).toBe(50);
		expect(stats.activePositions).toBe(1);
	});
	it('computePriceIndicator clamps and flags range', () => {
		const mid = computePriceIndicator(positions[0]);
		expect(mid.clamped).toBeCloseTo(50);
		expect(mid.inRange).toBe(true);
		const above = computePriceIndicator(positions[1]);
		expect(above.clamped).toBe(100);
		expect(above.inRange).toBe(false);
		const zeroSpan: LiquidityPosition = { ...positions[0], minPrice: 1, maxPrice: 1, currentPrice: 1 };
		expect(computePriceIndicator(zeroSpan).clamped).toBe(0);
	});
});

describe('investmentsViewModel factory', () => {
	it('initial state', () => {
		const vm = createInvestmentsViewModel(positions);
		expect(vm.positions).toHaveLength(2);
		expect(vm.poolStats.totalValueLocked).toBe(2000);
		expect(get(vm.activeTab)).toBe('positions');
		expect(get(vm.selectedPosition)).toBeNull();
	});
	it('setTab and selectPosition', () => {
		const vm = createInvestmentsViewModel(positions);
		vm.setTab('analytics');
		expect(get(vm.activeTab)).toBe('analytics');
		vm.selectPosition(positions[0]);
		expect(get(vm.selectedPosition)).toEqual(positions[0]);
		vm.selectPosition(null);
		expect(get(vm.selectedPosition)).toBeNull();
	});
	it('defaults to built-in positions', () => {
		const vm = createInvestmentsViewModel();
		expect(vm.positions.length).toBeGreaterThan(0);
	});
});
