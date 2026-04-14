<script lang="ts">
	import {
		createInvestmentsViewModel,
		formatInvestmentPrice as formatPrice,
		formatInvestmentNumber as formatNumber,
		getPnLColor,
		getPositionStatusColor as getStatusColor,
		computePriceIndicator
	} from '$lib/viewmodels/investmentsViewModel';

	const vm = createInvestmentsViewModel();
	const { positions: liquidityPositions, poolStats } = vm;
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-2 border-b-2 border-black">
		<h1 class="text-lg font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-xl">💎</span>
			CYBERDYNE DAO INVESTMENTS
		</h1>
		<p class="font-mono text-xs text-black">Uniswap V3 Liquidity Positions • Active Portfolio Management</p>
	</div>

	<div class="flex-1 flex">
		<div class="flex-1 overflow-y-auto">
			<div class="p-2 space-y-1 max-w-xs">
				{#each liquidityPositions as position}
					{@const indicator = computePriceIndicator(position)}
					<div
						class="border-2 rounded p-2 transition-all hover:shadow-md"
						class:bg-green-50={position.status === 'in-range'}
						class:border-green-400={position.status === 'in-range'}
						class:bg-red-50={position.status === 'out-of-range'}
						class:border-red-400={position.status === 'out-of-range'}
					>
						<div class="flex items-center justify-between mb-2">
							<div class="flex items-center gap-2">
								<div class="flex items-center">
									<span class="text-lg">{position.token0Logo}</span>
									<span class="text-lg -ml-1">{position.token1Logo}</span>
								</div>
								<span class="font-mono font-bold text-sm">{position.pair}</span>
							</div>
							<div class="text-right">
								<div class="text-sm font-bold font-mono">{formatPrice(position.totalValue)}</div>
								<div class="text-xs font-mono {getPnLColor(position.totalPnL)}">
									{position.totalPnL >= 0 ? '+' : ''}{formatPrice(position.totalPnL)}
								</div>
							</div>
						</div>

						<div class="mb-2 flex items-center justify-between">
							<span class="text-xs px-1.5 py-0.5 rounded font-mono {getStatusColor(position.status)}">
								{position.status === 'in-range' ? 'In Range' : 'Out of Range'}
							</span>
							<div class="text-xs font-mono text-gray-600">
								<span class="font-bold text-gray-800">{formatNumber(position.currentPrice, 4)}</span>
								<span class="text-gray-500"> ({formatNumber(position.minPrice, 4)}-{formatNumber(position.maxPrice, 4)})</span>
							</div>
						</div>

						<div class="mb-2">
							<div class="h-2 bg-gray-200 rounded-full relative" title="Price Range: {formatNumber(position.minPrice, 6)} - {formatNumber(position.maxPrice, 6)}">
								<div class="absolute top-0 left-0 h-full rounded-full"
									style="width: 100%; background-color: {position.status === 'in-range' ? '#86efac' : '#fca5a5'}">
								</div>
								<div
									class="absolute top-0 w-1 h-2 bg-white border rounded-sm transform -translate-x-0.5 shadow-sm"
									style="left: {indicator.clamped}%; border-color: {position.status === 'in-range' ? '#15803d' : '#dc2626'}; border-width: 1px;"
									title="Current Price: {formatNumber(position.currentPrice, 6)}"
								></div>
							</div>
						</div>

						<div class="flex justify-between items-center text-xs font-mono">
							<div>
								<span class="text-gray-500">Fee APY:</span>
								<span class="font-bold text-green-600">{position.feeAPY}%</span>
							</div>
							<div>
								<span class="text-gray-500">Uncollected:</span>
								<span class="font-bold">${position.uncollectedFees}</span>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<div class="w-64 border-l border-gray-200 bg-gray-50 overflow-y-auto">
			<div class="p-2">
				<div class="bg-white rounded border border-gray-200 p-2 mb-2">
					<h3 class="font-mono font-bold text-xs mb-1">💎 Portfolio Overview</h3>
					<div class="grid grid-cols-2 gap-1 text-xs font-mono">
						<div class="text-center">
							<div class="text-gray-500 text-xs">Total Value</div>
							<div class="font-bold text-xs text-gray-800">{formatPrice(poolStats.totalValueLocked)}</div>
						</div>
						<div class="text-center">
							<div class="text-gray-500 text-xs">Total P&L</div>
							<div class="font-bold text-xs" style="color: {poolStats.totalPnL >= 0 ? '#15803d' : '#dc2626'}">
								{poolStats.totalPnL >= 0 ? '+' : ''}{formatPrice(poolStats.totalPnL)}
							</div>
						</div>
						<div class="text-center">
							<div class="text-gray-500 text-xs">Active</div>
							<div class="font-bold text-xs text-gray-800">{poolStats.activePositions}/{liquidityPositions.length}</div>
						</div>
						<div class="text-center">
							<div class="text-gray-500 text-xs">Avg APY</div>
							<div class="font-bold text-xs text-gray-800">{poolStats.averageAPY.toFixed(1)}%</div>
						</div>
					</div>
				</div>

				<div class="bg-white rounded border border-gray-200 p-2 mb-2">
					<h3 class="font-mono font-bold text-xs mb-1">📊 Position Status</h3>
					<div class="space-y-1">
						{#each liquidityPositions as position}
							{@const indicator = computePriceIndicator(position)}
							<div class="space-y-0.5">
								<div class="flex items-center justify-between text-xs">
									<div class="flex items-center gap-0.5">
										<span class="text-xs">{position.token0Logo}{position.token1Logo}</span>
										<span class="font-mono font-bold text-xs">{position.pair}</span>
									</div>
									<div class="flex items-center gap-0.5">
										<span class="px-1 py-0.5 rounded font-mono text-xs"
											class:bg-green-100={position.status === 'in-range'}
											class:text-green-600={position.status === 'in-range'}
											class:bg-red-100={position.status === 'out-of-range'}
											class:text-red-600={position.status === 'out-of-range'}>
											{position.status === 'in-range' ? '✓' : '⚠️'}
										</span>
										<span class="font-bold text-xs">{formatPrice(position.totalValue)}</span>
									</div>
								</div>
								<div class="h-1.5 bg-gray-200 rounded-full relative" title="Price Range: {formatNumber(position.minPrice, 6)} - {formatNumber(position.maxPrice, 6)}">
									<div class="absolute top-0 left-0 h-full rounded-full"
										style="width: 100%; background-color: {position.status === 'in-range' ? '#86efac' : '#fca5a5'}">
									</div>
									<div
										class="absolute top-0 w-1 h-1.5 bg-white border rounded-sm transform -translate-x-0.5 shadow-sm"
										style="left: {indicator.clamped}%; border-color: {position.status === 'in-range' ? '#15803d' : '#dc2626'}; border-width: 1px;"
										title="Current Price: {formatNumber(position.currentPrice, 6)}"
									></div>
								</div>
							</div>
						{/each}
					</div>
				</div>

				<div class="bg-white rounded border border-gray-200 p-2">
					<h3 class="font-mono font-bold text-xs mb-1">⚡ Quick Actions</h3>
					<button class="w-full border border-gray-300 text-gray-700 py-1 px-2 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
						📊 View Analytics
					</button>
				</div>
			</div>
		</div>
	</div>
</div>
