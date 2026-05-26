<script lang="ts">
	import { onMount } from 'svelte';
	import {
		LiquidityPositionCard,
		StatCard,
		PixelScrollArea,
		PixelButton,
		type StatCardRow
	} from '@cyberdynecorp/svelte-ui-core';
	import {
		createInvestmentsViewModel,
		computePoolStats,
		formatInvestmentPrice as formatPrice
	} from '$lib/viewmodels/investmentsViewModel';
	import type { LiquidityPosition } from '$lib/data/investments';
	import { fetchDaoOverview } from '$lib/api/contentApi';

	const vm = createInvestmentsViewModel();

	// Stale-while-revalidate: static positions render first, the API
	// snapshot replaces them once it lands.
	let positions = $state<LiquidityPosition[]>(vm.positions);

	onMount(async () => {
		const overview = await fetchDaoOverview();
		if (!overview) return;
		positions = overview.snapshot.uniswapPositions.map((p, idx) => ({
			id: p.positionId,
			pair: `${p.token0Symbol}/${p.token1Symbol}`,
			token0: p.token0Symbol,
			token1: p.token1Symbol,
			token0Logo: '',
			token1Logo: '',
			totalValue: p.usdValue,
			minPrice: p.tickLower,
			maxPrice: p.tickUpper,
			currentPrice: (p.tickLower + p.tickUpper) / 2,
			feeAPY: p.feeTierBps / 100,
			pooledAssets: { token0Amount: p.token0Amount, token1Amount: p.token1Amount },
			totalPnL: 0,
			totalAPR: 0,
			uncollectedFees: p.uncollectedFeesUsd,
			status: p.inRange ? 'in-range' : 'out-of-range',
			compound: false,
			// Preserve sort stability if the DAO ships duplicate pool ids.
			...(idx === -1 ? {} : {})
		}));
	});

	const poolStats = $derived(computePoolStats(positions));

	const overviewRows = $derived([
		{ label: 'Total Value', value: formatPrice(poolStats.totalValueLocked) },
		{
			label: 'Total P&L',
			value: `${poolStats.totalPnL >= 0 ? '+' : ''}${formatPrice(poolStats.totalPnL)}`,
			accent: poolStats.totalPnL >= 0 ? 'success' : 'danger'
		},
		{ label: 'Active', value: `${poolStats.activePositions}/${positions.length}` },
		{ label: 'Avg APY', value: `${poolStats.averageAPY.toFixed(1)}%` }
	] as StatCardRow[]);

	const statusRows = $derived(positions.map((p) => ({
		label: p.pair,
		value: formatPrice(p.totalValue),
		accent: p.status === 'in-range' ? 'success' : 'danger'
	})) as StatCardRow[]);
</script>

<div class="investments-view flex flex-col h-full bg-white">
	<header class="px-3 py-2 border-b-2 border-black bg-gradient-to-r from-blue-600 to-indigo-600">
		<h1 class="text-sm sm:text-base font-bold font-mono flex items-center gap-2 text-white">
			<span>💎</span> CYBERDYNE DAO INVESTMENTS
		</h1>
		<p class="font-mono text-xs text-white/80">Uniswap V3 Liquidity Positions</p>
	</header>

	<div class="flex-1 grid grid-cols-1 md:grid-cols-[1fr_260px] gap-2 p-2 overflow-hidden">
		<PixelScrollArea maxHeight="100%" ariaLabel="Liquidity positions">
			<div class="flex flex-col gap-2 pr-2">
				{#each positions as p (p.pair)}
					<LiquidityPositionCard
						tokenA={p.pair.split('/')[0]}
						tokenB={p.pair.split('/')[1]}
						value={p.totalValue}
						pnl={p.totalPnL}
						currency="USD"
						range={{
							min: p.minPrice,
							max: p.maxPrice,
							lower: p.minPrice,
							upper: p.maxPrice,
							current: p.currentPrice
						}}
						feeApyPct={p.feeAPY}
						uncollected={Number(p.uncollectedFees) || 0}
					/>
				{/each}
			</div>
		</PixelScrollArea>

		<aside class="flex flex-col gap-2 min-w-0">
			<StatCard title="Portfolio Overview" icon="💎" rows={overviewRows} />
			<StatCard title="Position Status" icon="📊" rows={statusRows} />
			<div class="border-2 border-black bg-white p-2">
				<h3 class="font-mono font-bold text-xs mb-2">⚡ Quick Actions</h3>
				<PixelButton variant="outline" size="sm" fullWidth>📊 View Analytics</PixelButton>
			</div>
		</aside>
	</div>
</div>

<style>
	.investments-view {
		min-height: 100%;
	}
	@media (max-width: 768px) {
		.investments-view :global(aside) {
			order: -1;
		}
	}
</style>
