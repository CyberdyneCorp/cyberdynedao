<script lang="ts">
	import { onMount } from 'svelte';
	import { PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import {
		createDaoViewModel,
		formatCurrency,
		formatDecimals as formatNumber,
		formatDaoDate as formatDate,
		getVotePercentage,
		acceptedProposalCount,
		successRate,
		sumTreasury
	} from '$lib/viewmodels/daoViewModel';
	import type { TreasuryAsset } from '$lib/types/dao';
	import { fetchDaoOverview } from '$lib/api/contentApi';

	const vm = createDaoViewModel();
	const { recentProposals, dividendInfo, operationalData } = vm;
	const timeUntilDividend = vm.timeUntilDividend;

	// Stale-while-revalidate the treasury slice. Proposals + dividend
	// stay static until the governance subgraph ships in Phase 6.
	let treasuryAssets = $state<TreasuryAsset[]>(vm.treasuryAssets);
	let totalTreasuryValue = $state<number>(vm.totalTreasuryValue);

	onMount(() => {
		const stop = vm.startCountdown();
		void (async () => {
			const overview = await fetchDaoOverview();
			if (overview) {
				treasuryAssets = overview.snapshot.tokenBalances.map((b) => ({
					symbol: b.symbol,
					name: b.name,
					balance: b.balance,
					usdValue: b.usdValue,
					change24h: b.change24hPct,
					icon: b.icon
				}));
				totalTreasuryValue = sumTreasury(treasuryAssets);
			}
		})();
		return stop;
	});

	function statusGlyph(status: string): string {
		if (status === 'accepted') return '✓';
		if (status === 'rejected') return '✗';
		return '⏳';
	}
	function statusPalette(status: string): { accent: string; accentDark: string } {
		if (status === 'accepted') return { accent: '#22c55e', accentDark: '#15803d' };
		if (status === 'rejected') return { accent: '#ef4444', accentDark: '#b91c1c' };
		return { accent: '#f97316', accentDark: '#c2410c' };
	}
	function assetAccent(symbol: string): string {
		switch (symbol) {
			case 'ETH': return '#3b82f6';
			case 'USDC': return '#22c55e';
			case 'BTC': return '#f97316';
			default: return '#a855f7';
		}
	}

	const PURPLE = '#a855f7';
	const PURPLE_DK = '#7e22ce';
	const BLUE_DK = '#1d4ed8';
</script>

<div class="dao-view">
	<header class="hero">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">⚡</span>
			<h1 class="hero__title">CYBERDYNE DAO</h1>
		</div>
		<p class="hero__tagline">Decentralized treasury, on-chain governance, builder dividends.</p>
	</header>

	<PixelScrollArea maxHeight="100%" ariaLabel="DAO content">
		<div class="content">
			<!-- Top row: Treasury + Operations -->
			<div class="top-row">
				<!-- Treasury card -->
				<section class="card card--green">
					<header class="card__head">
						<div class="card__icon" aria-hidden="true">🏦</div>
						<h2 class="card__title">Treasury</h2>
					</header>
					<div class="treasury__total">
						<div class="treasury__total-label">Total Value</div>
						<div class="treasury__total-value">{formatCurrency(totalTreasuryValue)}</div>
					</div>
					<div class="treasury__assets">
						{#each treasuryAssets as asset}
							<div class="asset" style="--accent: {assetAccent(asset.symbol)};">
								<div class="asset__sym">{asset.symbol}</div>
								<div class="asset__bal">{formatNumber(asset.balance, asset.symbol === 'USDC' ? 0 : 2)}</div>
							</div>
						{/each}
					</div>
				</section>

				<!-- Operations card -->
				<section class="card card--blue">
					<header class="card__head">
						<div class="card__icon" aria-hidden="true">💼</div>
						<h2 class="card__title">Operations</h2>
					</header>
					<div class="ops-list">
						<div class="ops-row">
							<span class="ops-row__label">Income</span>
							<span class="ops-row__value ops-row__value--pos">{formatCurrency(operationalData.monthlyIncome)}</span>
						</div>
						<div class="ops-row">
							<span class="ops-row__label">Costs</span>
							<span class="ops-row__value ops-row__value--neg">{formatCurrency(operationalData.monthlyOperationalCosts)}</span>
						</div>
						<div class="ops-row ops-row--accent">
							<span class="ops-row__label">Profit</span>
							<span class="ops-row__value">{formatCurrency(operationalData.netProfit)}</span>
						</div>
						<div class="ops-row">
							<span class="ops-row__label">Margin</span>
							<span class="ops-row__value">{operationalData.profitMargin}%</span>
						</div>
					</div>
				</section>
			</div>

			<!-- Next Dividend -->
			<section class="card card--purple dividend">
				<header class="dividend__head">
					<div class="dividend__icon" aria-hidden="true">💰</div>
					<h2 class="card__title">Next Dividend</h2>
					<div class="dividend__countdown">{$timeUntilDividend}</div>
				</header>
				<div class="dividend__stats">
					<div class="div-stat">
						<div class="div-stat__label">Amount per holder</div>
						<div class="div-stat__value">${dividendInfo.estimatedAmount}</div>
					</div>
					<div class="div-stat">
						<div class="div-stat__label">Holders</div>
						<div class="div-stat__value">{(dividendInfo.totalHolders / 1000).toFixed(1)}K</div>
					</div>
					<div class="div-stat">
						<div class="div-stat__label">Distribution date</div>
						<div class="div-stat__value">
							{dividendInfo.nextDistribution.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
						</div>
					</div>
				</div>
			</section>

			<!-- Recent Proposals -->
			<section class="card card--blue">
				<header class="card__head">
					<div class="card__icon" aria-hidden="true">📋</div>
					<h2 class="card__title">Recent Proposals</h2>
				</header>

				<div class="proposals">
					{#each recentProposals as proposal}
						{@const pct = getVotePercentage(proposal.votesFor, proposal.totalVotes)}
						{@const sp = statusPalette(proposal.status)}
						<article class="proposal" style="--accent: {sp.accent}; --accent-dark: {sp.accentDark};">
							<div class="proposal__head">
								<div class="proposal__title-row">
									<span class="proposal__id">#{proposal.id}</span>
									<h3 class="proposal__title">{proposal.title}</h3>
									<span class="proposal__status" style="--accent: {sp.accent};">
										{statusGlyph(proposal.status)}
									</span>
								</div>
								<div class="proposal__pct">{pct.toFixed(0)}%</div>
							</div>

							<div class="proposal__bar" aria-hidden="true">
								<div class="proposal__bar-fill" style="width: {pct}%; background: {sp.accent};"></div>
							</div>

							<div class="proposal__foot">
								<span class="vote vote--for">
									<span class="vote__icon">✓</span>
									<span>{(proposal.votesFor / 1000).toFixed(1)}K for</span>
								</span>
								<span class="vote vote--against">
									<span class="vote__icon">✗</span>
									<span>{(proposal.votesAgainst / 1000).toFixed(1)}K against</span>
								</span>
								<span class="proposal__date">{formatDate(proposal.endDate)}</span>
							</div>
						</article>
					{/each}
				</div>
			</section>

			<!-- Stats footer -->
			<section class="stats">
				<div class="stats__pixel-stripe" aria-hidden="true"></div>
				<div class="stats__grid">
					<div class="stat">
						<div class="stat__value">{(dividendInfo.totalHolders / 1000).toFixed(1)}K</div>
						<div class="stat__label">Members</div>
					</div>
					<div class="stat">
						<div class="stat__value">{acceptedProposalCount(recentProposals)} / {recentProposals.length}</div>
						<div class="stat__label">Accepted</div>
					</div>
					<div class="stat">
						<div class="stat__value">${(totalTreasuryValue / dividendInfo.totalHolders).toFixed(0)}</div>
						<div class="stat__label">Per Member</div>
					</div>
					<div class="stat">
						<div class="stat__value">{successRate(recentProposals).toFixed(0)}%</div>
						<div class="stat__label">Success Rate</div>
					</div>
				</div>
			</section>
		</div>
	</PixelScrollArea>
</div>

<style>
	.dao-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		display: flex;
		flex-direction: column;
	}

	.hero {
		padding: 18px 24px;
		background: linear-gradient(135deg, #4c1d95 0%, #3b82f6 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
		flex: 0 0 auto;
	}
	.hero__brand { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
	.hero__mark { font-size: 1.5rem; }
	.hero__title { font-size: 1.5rem; font-weight: 800; letter-spacing: 0.08em; margin: 0; color: #fff; }
	.hero__tagline { margin: 0; font-size: 0.875rem; line-height: 1.5; color: #ddd6fe; }

	.content {
		max-width: 1100px;
		margin: 0 auto;
		padding: 18px 16px 22px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}

	/* ---------- Card primitive ---------- */
	.card {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 16px 16px 16px 24px;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	.card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		border-right: 2px solid #000;
	}
	.card--green::before { background: #22c55e; }
	.card--blue::before  { background: #3b82f6; }
	.card--purple::before { background: #a855f7; }
	.card__head { display: flex; align-items: center; gap: 10px; }
	.card__icon {
		width: 32px;
		height: 32px;
		border: 2px solid #000;
		background: #f3f4f6;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1rem;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.35);
	}
	.card--green .card__icon { background: #22c55e; }
	.card--blue .card__icon  { background: #3b82f6; }
	.card__title {
		font-size: 0.9375rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #000;
		margin: 0;
	}

	.top-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 14px;
	}
	@media (max-width: 720px) {
		.top-row { grid-template-columns: 1fr; }
	}

	/* ---------- Treasury ---------- */
	.treasury__total { display: flex; flex-direction: column; gap: 2px; }
	.treasury__total-label {
		font-size: 0.6875rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #6b7280;
		font-weight: 700;
	}
	.treasury__total-value {
		font-size: 1.625rem;
		font-weight: 800;
		color: #15803d;
		line-height: 1.1;
	}
	.treasury__assets {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 8px;
	}
	.asset {
		position: relative;
		background: #f9fafb;
		border: 2px solid #000;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.3);
		padding: 8px 10px 8px 14px;
	}
	.asset::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 4px;
		background: var(--accent);
		border-right: 1.5px solid #000;
	}
	.asset__sym { font-size: 0.75rem; font-weight: 800; color: #000; }
	.asset__bal { font-size: 0.8125rem; color: #1f2937; margin-top: 2px; }

	/* ---------- Operations ---------- */
	.ops-list { display: flex; flex-direction: column; gap: 6px; }
	.ops-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 7px 10px 7px 14px;
		background: #f9fafb;
		border: 2px solid #000;
		font-size: 0.8125rem;
		position: relative;
	}
	.ops-row::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 4px;
		background: #9ca3af;
		border-right: 1.5px solid #000;
	}
	.ops-row__label { color: #4b5563; font-weight: 600; }
	.ops-row__value { font-weight: 800; color: #000; }
	.ops-row__value--pos { color: #15803d; }
	.ops-row__value--neg { color: #b91c1c; }
	.ops-row--accent::before { background: #3b82f6; }
	.ops-row--accent .ops-row__value { color: #1d4ed8; }

	/* ---------- Dividend ---------- */
	.dividend__head {
		display: flex;
		align-items: center;
		gap: 10px;
		flex-wrap: wrap;
	}
	.dividend__icon {
		width: 36px;
		height: 36px;
		border: 2px solid #000;
		background: #a855f7;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.125rem;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.35);
	}
	.dividend__countdown {
		margin-left: auto;
		font-size: 1.625rem;
		font-weight: 800;
		color: #7e22ce;
		font-variant-numeric: tabular-nums;
		letter-spacing: 0.02em;
	}
	.dividend__stats {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 10px;
	}
	@media (max-width: 540px) {
		.dividend__stats { grid-template-columns: minmax(0, 1fr); }
	}
	.div-stat {
		background: #faf5ff;
		border: 2px solid #000;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.3);
		padding: 10px 12px;
		text-align: center;
	}
	.div-stat__label {
		font-size: 0.6875rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: #6b7280;
	}
	.div-stat__value {
		font-size: 1.125rem;
		font-weight: 800;
		color: #000;
		margin-top: 2px;
	}

	/* ---------- Proposals ---------- */
	.proposals { display: flex; flex-direction: column; gap: 8px; }
	.proposal {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 10px 12px 10px 18px;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.proposal::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.proposal__head { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
	.proposal__title-row {
		display: flex;
		align-items: center;
		gap: 8px;
		min-width: 0;
		flex: 1 1 auto;
	}
	.proposal__id {
		font-size: 0.6875rem;
		font-weight: 800;
		color: var(--accent-dark);
		background: #f3f4f6;
		padding: 2px 6px;
		border: 1.5px solid #000;
		flex: 0 0 auto;
	}
	.proposal__title {
		font-size: 0.875rem;
		font-weight: 700;
		color: #000;
		margin: 0;
		flex: 1 1 auto;
		min-width: 0;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.proposal__status {
		flex: 0 0 auto;
		width: 22px;
		height: 22px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--accent);
		color: #000;
		border: 1.5px solid #000;
		font-weight: 800;
		font-size: 0.875rem;
	}
	.proposal__pct {
		font-size: 0.8125rem;
		font-weight: 800;
		color: var(--accent-dark);
		flex: 0 0 auto;
	}
	.proposal__bar {
		height: 8px;
		background: #f3f4f6;
		border: 1.5px solid #000;
		overflow: hidden;
	}
	.proposal__bar-fill { height: 100%; transition: width 0.3s ease; }
	.proposal__foot {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.75rem;
		flex-wrap: wrap;
		gap: 6px;
	}
	.vote {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		font-weight: 700;
	}
	.vote--for { color: #15803d; }
	.vote--against { color: #b91c1c; }
	.vote__icon { font-weight: 800; }
	.proposal__date { color: #6b7280; font-size: 0.6875rem; }

	/* ---------- Stats footer ---------- */
	.stats {
		position: relative;
		background: #0f172a;
		color: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 18px 16px 16px;
	}
	.stats__pixel-stripe {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(
			to right,
			#22c55e 0%, #22c55e 25%,
			#3b82f6 25%, #3b82f6 50%,
			#a855f7 50%, #a855f7 75%,
			#f97316 75%, #f97316 100%
		);
		border-bottom: 2px solid #000;
	}
	.stats__grid {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 12px;
		text-align: center;
	}
	@media (max-width: 540px) {
		.stats__grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
	}
	.stat__value {
		font-size: 1.375rem;
		font-weight: 800;
		color: #67e8f9;
		line-height: 1;
	}
	.stat__label {
		font-size: 0.6875rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #94a3b8;
		margin-top: 4px;
	}
</style>
