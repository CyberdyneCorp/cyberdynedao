<script lang="ts">
	import { onMount } from 'svelte';
	import {
		createDaoViewModel,
		formatCurrency,
		formatDecimals as formatNumber,
		formatDaoDate as formatDate,
		getProposalStatusColor as getStatusColor,
		getVotePercentage,
		acceptedProposalCount,
		successRate
	} from '$lib/viewmodels/daoViewModel';

	const vm = createDaoViewModel();
	const { treasuryAssets, recentProposals, dividendInfo, operationalData, totalTreasuryValue } = vm;
	const timeUntilDividend = vm.timeUntilDividend;

	onMount(() => vm.startCountdown());
	import { PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
</script>

<div class="flex flex-col h-full bg-white">
	<div class="bg-gradient-to-r from-purple-600 to-blue-600 p-3 border-b-2 border-black">
		<h1 class="text-xl font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-2xl">⚡</span>
			CYBERDYNE DAO
		</h1>
		<p class="font-mono text-xs text-black">Decentralized Autonomous Organization</p>
	</div>

	<PixelScrollArea maxHeight="100%" ariaLabel="DAO content">
	<div class="p-2 space-y-2">
		<section class="grid grid-cols-2 gap-2">
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

		<section class="bg-blue-50 rounded border border-blue-200 p-2">
			<div class="flex items-center gap-2 mb-1">
				<span class="text-lg">💰</span>
				<h2 class="text-sm font-bold font-mono text-gray-800">Next Dividend</h2>
				<span class="ml-auto text-2xl font-bold font-mono text-blue-600">{$timeUntilDividend}</span>
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

		<section class="bg-gray-800 text-white rounded border border-gray-600 p-2">
			<div class="grid grid-cols-4 gap-2 text-center text-xs font-mono">
				<div>
					<div class="font-bold text-cyan-400">{(dividendInfo.totalHolders / 1000).toFixed(1)}K</div>
					<div class="text-gray-300">Members</div>
				</div>
				<div>
					<div class="font-bold text-cyan-400">{acceptedProposalCount(recentProposals)}/5</div>
					<div class="text-gray-300">Accepted</div>
				</div>
				<div>
					<div class="font-bold text-cyan-400">${(totalTreasuryValue / dividendInfo.totalHolders).toFixed(0)}</div>
					<div class="text-gray-300">Per Member</div>
				</div>
				<div>
					<div class="font-bold text-cyan-400">{successRate(recentProposals).toFixed(0)}%</div>
					<div class="text-gray-300">Success Rate</div>
				</div>
			</div>
		</section>
	</div>
	</PixelScrollArea>
</div>
