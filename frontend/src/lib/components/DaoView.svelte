<script lang="ts">
	import { onMount } from 'svelte';
	import { treasuryAssets, recentProposals, dividendInfo, operationalData, DAYS_UNTIL_DIVIDEND } from '$lib/constants/daoData';
	import type { TreasuryAsset, DaoProposal, DividendInfo, OperationalData } from '$lib/types/dao';

	let timeUntilDividend = '';
	let totalTreasuryValue = 0;

	// Calculate total treasury value
	$: totalTreasuryValue = treasuryAssets.reduce((sum, asset) => sum + asset.usdValue, 0);

	// Calculate countdown to next dividend
	function updateCountdown() {
		const now = new Date();
		const next = dividendInfo.nextDistribution;
		const diff = next.getTime() - now.getTime();

		if (diff > 0) {
			const days = Math.floor(diff / (1000 * 60 * 60 * 24));
			const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
			const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
			
			timeUntilDividend = `${days}d ${hours}h ${minutes}m`;
		} else {
			timeUntilDividend = 'Distribution in progress...';
		}
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 2,
			maximumFractionDigits: 2
		}).format(amount);
	}

	function formatNumber(num: number, decimals: number = 2): string {
		return new Intl.NumberFormat('en-US', {
			minimumFractionDigits: decimals,
			maximumFractionDigits: decimals
		}).format(num);
	}

	function formatDate(date: Date): string {
		return date.toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	function getStatusColor(status: string): string {
		switch (status) {
			case 'accepted': return 'text-green-600 bg-green-100';
			case 'rejected': return 'text-red-600 bg-red-100';
			case 'pending': return 'text-yellow-600 bg-yellow-100';
			default: return 'text-gray-600 bg-gray-100';
		}
	}

	function getVotePercentage(votesFor: number, totalVotes: number): number {
		return totalVotes > 0 ? (votesFor / totalVotes) * 100 : 0;
	}

	onMount(() => {
		updateCountdown();
		const interval = setInterval(updateCountdown, 60000); // Update every minute
		
		return () => clearInterval(interval);
	});
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<!-- Header -->
	<div class="bg-gradient-to-r from-purple-600 to-blue-600 p-3 border-b-2 border-black">
		<h1 class="text-xl font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-2xl">⚡</span>
			CYBERDYNE DAO
		</h1>
		<p class="font-mono text-xs text-black">Decentralized Autonomous Organization</p>
	</div>

	<div class="flex-1 p-2 space-y-2">
		<!-- Key Metrics Overview -->
		<section class="grid grid-cols-2 gap-2">
			<!-- Treasury -->
			<div class="bg-gray-50 rounded border border-gray-200 p-2">
				<div class="flex items-center gap-2 mb-1">
					<span class="text-lg">🏦</span>
					<h2 class="text-sm font-bold font-mono text-gray-800">Treasury</h2>
				</div>
				<div class="text-xl font-bold font-mono text-green-600 mb-1">
					{formatCurrency(totalTreasuryValue)}
				</div>
				<div class="grid grid-cols-3 gap-1 text-xs">
					{#each treasuryAssets as asset}
						<div class="bg-white rounded p-1 border">
							<div class="font-mono font-bold">{asset.symbol}</div>
							<div class="text-gray-600">{formatNumber(asset.balance, asset.symbol === 'USDC' ? 0 : 2)}</div>
						</div>
					{/each}
				</div>
			</div>

			<!-- Operations -->
			<div class="bg-gray-50 rounded border border-gray-200 p-2">
				<div class="flex items-center gap-2 mb-1">
					<span class="text-lg">💼</span>
					<h2 class="text-sm font-bold font-mono text-gray-800">Operations</h2>
				</div>
				<div class="space-y-1 text-xs font-mono">
					<div class="flex justify-between bg-white rounded p-1">
						<span class="text-gray-600">Income:</span>
						<span class="font-bold text-green-600">{formatCurrency(operationalData.monthlyIncome)}</span>
					</div>
					<div class="flex justify-between bg-white rounded p-1">
						<span class="text-gray-600">Costs:</span>
						<span class="font-bold text-red-600">{formatCurrency(operationalData.monthlyOperationalCosts)}</span>
					</div>
					<div class="flex justify-between bg-white rounded p-1">
						<span class="text-gray-600">Profit:</span>
						<span class="font-bold text-blue-600">{formatCurrency(operationalData.netProfit)}</span>
					</div>
					<div class="flex justify-between bg-white rounded p-1">
						<span class="text-gray-600">Margin:</span>
						<span class="font-bold">{operationalData.profitMargin}%</span>
					</div>
				</div>
			</div>
		</section>

		<!-- Dividend Timer -->
		<section class="bg-blue-50 rounded border border-blue-200 p-2">
			<div class="flex items-center gap-2 mb-1">
				<span class="text-lg">💰</span>
				<h2 class="text-sm font-bold font-mono text-gray-800">Next Dividend</h2>
				<span class="ml-auto text-2xl font-bold font-mono text-blue-600">{timeUntilDividend}</span>
			</div>
			<div class="grid grid-cols-3 gap-2 text-xs font-mono">
				<div class="bg-white rounded p-1 text-center">
					<div class="text-gray-600">Amount</div>
					<div class="font-bold">${dividendInfo.estimatedAmount}</div>
				</div>
				<div class="bg-white rounded p-1 text-center">
					<div class="text-gray-600">Holders</div>
					<div class="font-bold">{(dividendInfo.totalHolders / 1000).toFixed(1)}K</div>
				</div>
				<div class="bg-white rounded p-1 text-center">
					<div class="text-gray-600">Date</div>
					<div class="font-bold">{dividendInfo.nextDistribution.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</div>
				</div>
			</div>
		</section>

		<!-- Recent Proposals -->
		<section class="bg-gray-50 rounded border border-gray-200 p-2">
			<div class="flex items-center gap-2 mb-1">
				<span class="text-lg">📋</span>
				<h2 class="text-sm font-bold font-mono text-gray-800">Recent Proposals</h2>
			</div>
			
			<div class="space-y-2">
				{#each recentProposals as proposal}
					<div class="bg-white rounded border p-2">
						<div class="flex items-center justify-between mb-1">
							<div class="flex items-center gap-2">
								<h3 class="font-bold font-mono text-xs">#{proposal.id}: {proposal.title.slice(0, 25)}...</h3>
								<span class="px-1 py-0.5 rounded text-xs font-bold font-mono {getStatusColor(proposal.status)}">
									{proposal.status === 'accepted' ? '✓' : proposal.status === 'rejected' ? '✗' : '⏳'}
								</span>
							</div>
							<div class="text-xs text-gray-500 font-mono">
								{getVotePercentage(proposal.votesFor, proposal.totalVotes).toFixed(0)}%
							</div>
						</div>
						
						<div class="flex items-center justify-between text-xs font-mono">
							<div class="text-green-600">✓ {(proposal.votesFor / 1000).toFixed(1)}K</div>
							<div class="text-red-600">✗ {(proposal.votesAgainst / 1000).toFixed(1)}K</div>
							<div class="text-gray-500">{formatDate(proposal.endDate)}</div>
						</div>
						
						<!-- Compact Vote Progress Bar -->
						<div class="mt-1 bg-gray-200 rounded-full h-1">
							<div 
								class="{proposal.status === 'accepted' ? 'bg-green-500' : 'bg-red-500'} h-1 rounded-full transition-all duration-300" 
								style="width: {getVotePercentage(proposal.votesFor, proposal.totalVotes)}%"
							></div>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- Stats Footer -->
		<section class="bg-gray-800 text-white rounded border border-gray-600 p-2">
			<div class="grid grid-cols-4 gap-2 text-center text-xs font-mono">
				<div>
					<div class="font-bold text-cyan-400">{(dividendInfo.totalHolders / 1000).toFixed(1)}K</div>
					<div class="text-gray-300">Members</div>
				</div>
				<div>
					<div class="font-bold text-cyan-400">{recentProposals.filter(p => p.status === 'accepted').length}/5</div>
					<div class="text-gray-300">Accepted</div>
				</div>
				<div>
					<div class="font-bold text-cyan-400">${(totalTreasuryValue / dividendInfo.totalHolders).toFixed(0)}</div>
					<div class="text-gray-300">Per Member</div>
				</div>
				<div>
					<div class="font-bold text-cyan-400">{((recentProposals.filter(p => p.status === 'accepted').length / recentProposals.length) * 100).toFixed(0)}%</div>
					<div class="text-gray-300">Success Rate</div>
				</div>
			</div>
		</section>
	</div>
</div>