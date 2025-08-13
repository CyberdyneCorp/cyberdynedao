<script lang="ts">
	interface LiquidityPosition {
		id: string;
		pair: string;
		token0: string;
		token1: string;
		token0Logo: string;
		token1Logo: string;
		totalValue: number;
		minPrice: number;
		maxPrice: number;
		currentPrice: number;
		feeAPY: number;
		pooledAssets: {
			token0Amount: number;
			token1Amount: number;
		};
		totalPnL: number;
		totalAPR: number;
		uncollectedFees: number;
		status: 'in-range' | 'out-of-range';
		compound: boolean;
	}

	interface PoolStats {
		totalValueLocked: number;
		totalPnL: number;
		averageAPY: number;
		activePositions: number;
	}

	const liquidityPositions: LiquidityPosition[] = [
		{
			id: 'pos-1',
			pair: 'WETH/USDC',
			token0: 'WETH',
			token1: 'USDC',
			token0Logo: '🔷',
			token1Logo: '💵',
			totalValue: 12607.79,
			minPrice: 3099.514,
			maxPrice: 4101.002,
			currentPrice: 4601.119,
			feeAPY: 68.43,
			pooledAssets: {
				token0Amount: 3.2,
				token1Amount: 316.96
			},
			totalPnL: -316.96,
			totalAPR: -46.59,
			uncollectedFees: 7.91,
			status: 'out-of-range',
			compound: true
		},
		{
			id: 'pos-2',
			pair: 'UNI/WETH',
			token0: 'UNI',
			token1: 'WETH',
			token0Logo: '🦄',
			token1Logo: '🔷',
			totalValue: 8450.32,
			minPrice: 0.0032,
			maxPrice: 0.0045,
			currentPrice: 0.0039,
			feeAPY: 24.8,
			pooledAssets: {
				token0Amount: 1250.5,
				token1Amount: 1.85
			},
			totalPnL: 125.43,
			totalAPR: 12.4,
			uncollectedFees: 15.23,
			status: 'in-range',
			compound: false
		},
		{
			id: 'pos-3',
			pair: 'USDC/USDT',
			token0: 'USDC',
			token1: 'USDT',
			token0Logo: '💵',
			token1Logo: '💚',
			totalValue: 15000.00,
			minPrice: 0.998,
			maxPrice: 1.002,
			currentPrice: 0.9995,
			feeAPY: 8.2,
			pooledAssets: {
				token0Amount: 7500.25,
				token1Amount: 7499.75
			},
			totalPnL: 45.80,
			totalAPR: 8.2,
			uncollectedFees: 12.34,
			status: 'in-range',
			compound: true
		},
		{
			id: 'pos-4',
			pair: 'ARB/WETH',
			token0: 'ARB',
			token1: 'WETH',
			token0Logo: '🔵',
			token1Logo: '🔷',
			totalValue: 5234.67,
			minPrice: 0.00045,
			maxPrice: 0.00065,
			currentPrice: 0.00052,
			feeAPY: 45.6,
			pooledAssets: {
				token0Amount: 5000.0,
				token1Amount: 1.15
			},
			totalPnL: -89.23,
			totalAPR: -8.5,
			uncollectedFees: 28.45,
			status: 'in-range',
			compound: true
		}
	];

	let selectedPosition: LiquidityPosition | null = null;
	let activeTab: 'positions' | 'analytics' = 'positions';

	$: poolStats = {
		totalValueLocked: liquidityPositions.reduce((sum, pos) => sum + pos.totalValue, 0),
		totalPnL: liquidityPositions.reduce((sum, pos) => sum + pos.totalPnL, 0),
		averageAPY: liquidityPositions.reduce((sum, pos) => sum + pos.feeAPY, 0) / liquidityPositions.length,
		activePositions: liquidityPositions.filter(pos => pos.status === 'in-range').length
	};

	function formatPrice(price: number, decimals: number = 2): string {
		if (price >= 1000) {
			return `$${(price / 1000).toFixed(1)}k`;
		}
		return `$${price.toFixed(decimals)}`;
	}

	function formatNumber(num: number, decimals: number = 2): string {
		if (num >= 1000) {
			return `${(num / 1000).toFixed(1)}k`;
		}
		return num.toFixed(decimals);
	}

	function getPnLColor(value: number): string {
		return value >= 0 ? 'text-green-500' : 'text-red-500';
	}

	function getStatusColor(status: string): string {
		return status === 'in-range' ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100';
	}
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<!-- Header -->
	<div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-2 border-b-2 border-black">
		<h1 class="text-lg font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-xl">💎</span>
			CYBERDYNE DAO INVESTMENTS
		</h1>
		<p class="font-mono text-xs text-black">Uniswap V3 Liquidity Positions • Active Portfolio Management</p>
	</div>

	<!-- Summary Stats -->
	<div class="bg-gray-900 text-white p-2 border-b border-gray-600">
		<div class="grid grid-cols-4 gap-4 text-center">
			<div>
				<div class="text-xs font-mono text-gray-400">Total Value</div>
				<div class="text-sm font-bold font-mono">{formatPrice(poolStats.totalValueLocked)}</div>
			</div>
			<div>
				<div class="text-xs font-mono text-gray-400">Total PnL</div>
				<div class="text-sm font-bold font-mono" style="color: {poolStats.totalPnL >= 0 ? '#86efac' : '#fca5a5'}">
					{poolStats.totalPnL >= 0 ? '+' : ''}{formatPrice(poolStats.totalPnL)}
				</div>
			</div>
			<div>
				<div class="text-xs font-mono text-gray-400">Avg APY</div>
				<div class="text-sm font-bold font-mono text-yellow-400">{poolStats.averageAPY.toFixed(1)}%</div>
			</div>
			<div>
				<div class="text-xs font-mono text-gray-400">Active</div>
				<div class="text-sm font-bold font-mono" style="color: {poolStats.activePositions > 0 ? '#86efac' : '#fca5a5'}">{poolStats.activePositions}/{liquidityPositions.length}</div>
			</div>
		</div>
	</div>

	<div class="flex-1 flex">
		<!-- Positions List -->
		<div class="flex-1 overflow-y-auto">
			<div class="p-2 space-y-1">
				{#each liquidityPositions as position}
					<div 
						class="border-2 rounded p-2 cursor-pointer transition-all hover:shadow-md"
						class:bg-green-50={position.status === 'in-range'}
						class:border-green-400={position.status === 'in-range'}
						class:bg-red-50={position.status === 'out-of-range'}
						class:border-red-400={position.status === 'out-of-range'}
						class:ring-2={selectedPosition?.id === position.id}
						class:ring-blue-500={selectedPosition?.id === position.id}
						on:click={() => selectedPosition = position}
						role="button"
						tabindex="0"
					>
						<!-- Position Header -->
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

						<!-- Status Badge -->
						<div class="mb-2">
							<span class="text-xs px-1.5 py-0.5 rounded font-mono {getStatusColor(position.status)}">
								{position.status === 'in-range' ? 'In Range' : 'Out of Range'}
							</span>
						</div>

						<!-- Price Range Indicator -->
						<div class="mb-2">
							{#each [position] as pos}
								{@const currentPos = ((pos.currentPrice - pos.minPrice) / (pos.maxPrice - pos.minPrice)) * 100}
								{@const isInRange = pos.currentPrice >= pos.minPrice && pos.currentPrice <= pos.maxPrice}
								{@const clampedPos = Math.min(Math.max(currentPos, 0), 100)}
								
								<div class="h-2 bg-gray-200 rounded-full relative" title="Price Range: {formatNumber(pos.minPrice, 6)} - {formatNumber(pos.maxPrice, 6)}">
									<!-- Range background (represents the entire range) -->
									<div class="absolute top-0 left-0 h-full rounded-full" 
										style="width: 100%; background-color: {pos.status === 'in-range' ? '#86efac' : '#fca5a5'}">
									</div>
									<!-- Current price indicator (small vertical line) -->
									<div 
										class="absolute top-0 w-0.5 h-2 rounded-sm transform -translate-x-0.5"
										style="left: {clampedPos}%; background-color: {pos.status === 'in-range' ? '#15803d' : '#dc2626'}"
										title="Current Price: {formatNumber(pos.currentPrice, 6)}"
									></div>
								</div>
							{/each}
						</div>

						<!-- APY and Fees -->
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

		<!-- Position Details Panel -->
		{#if selectedPosition}
			<div class="w-80 border-l border-gray-200 bg-gray-50 overflow-y-auto">
				<div class="p-3">
					<!-- Position Title -->
					<div class="flex items-center gap-2 mb-3">
						<div class="flex items-center">
							<span class="text-2xl">{selectedPosition.token0Logo}</span>
							<span class="text-2xl -ml-1">{selectedPosition.token1Logo}</span>
						</div>
						<div>
							<h3 class="font-mono font-bold text-lg">{selectedPosition.pair}</h3>
							<div class="flex items-center gap-1">
								<span class="text-xs px-1.5 py-0.5 rounded font-mono {getStatusColor(selectedPosition.status)}">
									{selectedPosition.status === 'in-range' ? 'In Range' : 'Out of Range'}
								</span>
							</div>
						</div>
					</div>

					<!-- Summary Stats -->
					<div class="bg-white rounded border border-gray-200 p-2 mb-3">
						<div class="grid grid-cols-2 gap-2 text-xs font-mono">
							<div class="text-center">
								<div class="text-gray-500">Value</div>
								<div class="font-bold">{formatPrice(selectedPosition.totalValue)}</div>
							</div>
							<div class="text-center">
								<div class="text-gray-500">P&L</div>
								<div class="font-bold {getPnLColor(selectedPosition.totalPnL)}">
									{selectedPosition.totalPnL >= 0 ? '+' : ''}{formatPrice(selectedPosition.totalPnL)}
								</div>
							</div>
							<div class="text-center">
								<div class="text-gray-500">Fee APY</div>
								<div class="font-bold text-green-600">{selectedPosition.feeAPY}%</div>
							</div>
							<div class="text-center">
								<div class="text-gray-500">Uncollected</div>
								<div class="font-bold">${selectedPosition.uncollectedFees}</div>
							</div>
						</div>
					</div>

					<!-- Price Range Visualization -->
					<div class="bg-white rounded border border-gray-200 p-2 mb-3">
						<h4 class="font-mono font-bold text-sm mb-2">📊 Price Range</h4>
						<div class="space-y-2">
							<!-- Price labels -->
							<div class="flex justify-between text-xs font-mono text-gray-600">
								<span>{formatNumber(selectedPosition.minPrice, 4)}</span>
								<span class="font-bold text-gray-800">{formatNumber(selectedPosition.currentPrice, 4)}</span>
								<span>{formatNumber(selectedPosition.maxPrice, 4)}</span>
							</div>
							<!-- Visual range bar -->
							{#each [selectedPosition] as pos}
								{@const currentPos = Math.min(Math.max(
									((pos.currentPrice - pos.minPrice) / (pos.maxPrice - pos.minPrice)) * 100, 0
								), 100)}
								<div class="h-3 bg-gray-200 rounded-full relative">
									<!-- Range background -->
									<div class="absolute top-0 left-0 h-full rounded-full" 
										style="width: 100%; background-color: {pos.status === 'in-range' ? '#86efac' : '#fca5a5'}">
									</div>
									<!-- Current price indicator -->
									<div 
										class="absolute top-0 w-1 h-3 bg-white border-2 rounded-sm transform -translate-x-0.5"
										style="left: {currentPos}%; border-color: {pos.status === 'in-range' ? '#15803d' : '#dc2626'}"
										title="Current: {formatNumber(pos.currentPrice, 6)}"
									></div>
								</div>
							{/each}
						</div>
					</div>

				</div>
			</div>
		{:else}
			<div class="w-80 border-l border-gray-200 bg-gray-50 overflow-y-auto">
				<div class="p-3">
					<!-- Portfolio Overview -->
					<div class="bg-white rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">💎 Portfolio Overview</h3>
						<div class="grid grid-cols-2 gap-2 text-xs font-mono">
							<div class="text-center">
								<div class="text-gray-500">Total Value</div>
								<div class="font-bold">{formatPrice(poolStats.totalValueLocked)}</div>
							</div>
							<div class="text-center">
								<div class="text-gray-500">Total P&L</div>
								<div class="font-bold {getPnLColor(poolStats.totalPnL)}">
									{poolStats.totalPnL >= 0 ? '+' : ''}{formatPrice(poolStats.totalPnL)}
								</div>
							</div>
							<div class="text-center">
								<div class="text-gray-500">Active Positions</div>
								<div class="font-bold text-green-600">{poolStats.activePositions}/{liquidityPositions.length}</div>
							</div>
							<div class="text-center">
								<div class="text-gray-500">Avg APY</div>
								<div class="font-bold text-yellow-600">{poolStats.averageAPY.toFixed(1)}%</div>
							</div>
						</div>
					</div>

					<!-- Position Status Summary -->
					<div class="bg-white rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">📊 Position Status</h3>
						<div class="space-y-2">
							{#each liquidityPositions as position}
								{@const currentPos = ((position.currentPrice - position.minPrice) / (position.maxPrice - position.minPrice)) * 100}
								{@const clampedPos = Math.min(Math.max(currentPos, 0), 100)}
								<div class="space-y-1">
									<div class="flex items-center justify-between text-xs">
										<div class="flex items-center gap-1">
											<span>{position.token0Logo}{position.token1Logo}</span>
											<span class="font-mono font-bold">{position.pair}</span>
										</div>
										<div class="flex items-center gap-1">
											<span class="px-1 py-0.5 rounded font-mono text-xs" 
												class:bg-green-100={position.status === 'in-range'}
												class:text-green-600={position.status === 'in-range'}
												class:bg-red-100={position.status === 'out-of-range'}
												class:text-red-600={position.status === 'out-of-range'}>
												{position.status === 'in-range' ? '✓' : '⚠️'}
											</span>
											<span class="font-bold">{formatPrice(position.totalValue)}</span>
										</div>
									</div>
									<!-- Mini price range bar -->
									<div class="h-1.5 bg-gray-200 rounded-full relative" title="Price Range: {formatNumber(position.minPrice, 6)} - {formatNumber(position.maxPrice, 6)}">
										<!-- Range background -->
										<div class="absolute top-0 left-0 h-full rounded-full" 
											style="width: 100%; background-color: {position.status === 'in-range' ? '#86efac' : '#fca5a5'}">
										</div>
										<!-- Current price indicator -->
										<div 
											class="absolute top-0 w-0.5 h-1.5 rounded-sm transform -translate-x-0.5"
											style="left: {clampedPos}%; background-color: {position.status === 'in-range' ? '#15803d' : '#dc2626'}"
											title="Current Price: {formatNumber(position.currentPrice, 6)}"
										></div>
									</div>
								</div>
							{/each}
						</div>
					</div>

					<!-- Quick Actions -->
					<div class="bg-white rounded border border-gray-200 p-2">
						<h3 class="font-mono font-bold text-sm mb-2">⚡ Quick Actions</h3>
						<div class="space-y-1">
							<button class="w-full border border-gray-300 text-gray-700 py-1.5 px-2 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
								📊 View Analytics
							</button>
						</div>
						<p class="text-xs text-gray-600 font-mono mt-2">
							Click on a position for detailed management options.
						</p>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>