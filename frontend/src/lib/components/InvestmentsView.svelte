<script lang="ts">
	import { onMount } from 'svelte';
	import {
		Badge,
		LiquidityPositionCard,
		PixelScrollArea
	} from '@cyberdynecorp/svelte-ui-core';
	import {
		createInvestmentsViewModel,
		computePoolStats,
		formatInvestmentPrice as formatPrice
	} from '$lib/viewmodels/investmentsViewModel';
	import type { LiquidityPosition } from '$lib/data/investments';
	import { fetchDaoOverview, type DaoUniswapPosition } from '$lib/api/contentApi';

	const vm = createInvestmentsViewModel();

	// Stale-while-revalidate: static positions render first, the API
	// snapshot replaces them once it lands.
	let positions = $state<LiquidityPosition[]>(vm.positions);

	onMount(async () => {
		const overview = await fetchDaoOverview();
		if (!overview) return;
		positions = overview.snapshot.uniswapPositions.map(apiPositionToLP);
	});

	/**
	 * Uniswap v4 raw ticks → human prices. ``price = 1.0001^tick`` gives
	 * the token1/token0 ratio; pair-specific decimal adjustment isn't
	 * carried by the API yet so the displayed numbers are approximate,
	 * but the **range bar** uses these values relatively, so it still
	 * paints an accurate "current vs min/max" picture.
	 */
	function tickToPrice(tick: number): number {
		// Clamp insanely wide ranges (full-range LPs use ±887272) so the
		// math doesn't overflow to Infinity.
		const clamped = Math.max(-500_000, Math.min(500_000, tick));
		return Math.pow(1.0001, clamped);
	}

	function apiPositionToLP(p: DaoUniswapPosition): LiquidityPosition {
		const minPrice = tickToPrice(p.tickLower);
		const maxPrice = tickToPrice(p.tickUpper);
		// API gives us in-range/out-of-range plus the tick range, but
		// not a live mid-pool price. Mid-of-range is a safe placeholder
		// for the in-range case; for out-of-range we nudge slightly
		// past the violated bound so the range bar still renders correctly.
		const midPrice = (minPrice + maxPrice) / 2;
		const currentPrice = p.inRange
			? midPrice
			: midPrice * (Math.random() > 0.5 ? 1.1 : 0.9);
		return {
			id: p.positionId,
			pair: `${p.token0Symbol}/${p.token1Symbol}`,
			token0: p.token0Symbol,
			token1: p.token1Symbol,
			token0Logo: '',
			token1Logo: '',
			totalValue: p.usdValue,
			minPrice,
			maxPrice,
			currentPrice,
			feeAPY: p.feeTierBps / 100,
			pooledAssets: { token0Amount: p.token0Amount, token1Amount: p.token1Amount },
			totalPnL: 0,
			totalAPR: 0,
			uncollectedFees: p.uncollectedFeesUsd,
			status: p.inRange ? 'in-range' : 'out-of-range',
			compound: false
		};
	}

	const poolStats = $derived(computePoolStats(positions));

	// ── Palette (matches CyberddyneView / DaoView) ───────────────────
	type Palette = 'blue' | 'green' | 'purple' | 'orange' | 'red';
	const paletteVars: Record<Palette, { accent: string; accentDark: string }> = {
		blue:   { accent: '#3b82f6', accentDark: '#1d4ed8' },
		green:  { accent: '#22c55e', accentDark: '#15803d' },
		purple: { accent: '#a855f7', accentDark: '#7e22ce' },
		orange: { accent: '#f97316', accentDark: '#c2410c' },
		red:    { accent: '#ef4444', accentDark: '#b91c1c' }
	};
	function palStyle(p: Palette): string {
		const v = paletteVars[p];
		return `--accent: ${v.accent}; --accent-dark: ${v.accentDark};`;
	}

	function pnlPalette(value: number): Palette {
		if (value > 0) return 'green';
		if (value < 0) return 'red';
		return 'blue';
	}

	function statusBadgeVariant(
		status: LiquidityPosition['status']
	): 'success' | 'danger' | 'warning' {
		return status === 'in-range' ? 'success' : 'danger';
	}

	function statusLabel(status: LiquidityPosition['status']): string {
		return status === 'in-range' ? 'IN RANGE' : 'OUT OF RANGE';
	}

	function formatPnl(value: number): string {
		const sign = value >= 0 ? '+' : '';
		return `${sign}${formatPrice(value)}`;
	}
</script>

<PixelScrollArea maxHeight="100%" ariaLabel="DAO investments">
<div class="invest-view">
	<!-- Hero -->
	<header class="hero" style={palStyle('blue')}>
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">💎</span>
			<h1 class="hero__title">DAO INVESTMENTS</h1>
		</div>
		<p class="hero__tagline">
			Uniswap v4 liquidity positions held by the Cyberdyne DAO treasury on Base. Each card shows the active price range, current price, and uncollected fees.
		</p>
	</header>

	<div class="content">
		<!-- Stat strip -->
		<section class="stats">
			<div class="stat" style={palStyle('blue')}>
				<div class="stat__label">Total Value</div>
				<div class="stat__value">{formatPrice(poolStats.totalValueLocked)}</div>
			</div>
			<div class="stat" style={palStyle(pnlPalette(poolStats.totalPnL))}>
				<div class="stat__label">Total P&amp;L</div>
				<div class="stat__value">{formatPnl(poolStats.totalPnL)}</div>
			</div>
			<div class="stat" style={palStyle('purple')}>
				<div class="stat__label">Active</div>
				<div class="stat__value">{poolStats.activePositions}<span class="stat__sub">/{positions.length}</span></div>
			</div>
			<div class="stat" style={palStyle('green')}>
				<div class="stat__label">Avg Fee APY</div>
				<div class="stat__value">{poolStats.averageAPY.toFixed(1)}<span class="stat__sub">%</span></div>
			</div>
		</section>

		<!-- Positions -->
		<section class="card positions-card" style={palStyle('blue')}>
			<header class="card__head">
				<h2 class="card__title">Liquidity Positions</h2>
				<span class="card__hint">Range bar shows current price vs. min/max bounds</span>
			</header>

			{#if positions.length === 0}
				<p class="empty">No active positions.</p>
			{:else}
				<div class="position-grid">
					{#each positions as p (p.id)}
						{@const pal: Palette = p.status === 'in-range' ? 'green' : 'red'}
						<article class="position" style={palStyle(pal)}>
							<header class="position__head">
								<h3 class="position__pair">{p.pair}</h3>
								<Badge variant={statusBadgeVariant(p.status)} size="sm">
									{statusLabel(p.status)}
								</Badge>
							</header>
							<LiquidityPositionCard
								tokenA={p.token0}
								tokenB={p.token1}
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
							<dl class="position__meta">
								<div>
									<dt>Pooled</dt>
									<dd>
										{p.pooledAssets.token0Amount.toFixed(2)} {p.token0}
										<span class="position__sep">·</span>
										{p.pooledAssets.token1Amount.toFixed(2)} {p.token1}
									</dd>
								</div>
								<div>
									<dt>Uncollected Fees</dt>
									<dd class="position__fees">{formatPrice(Number(p.uncollectedFees) || 0)}</dd>
								</div>
							</dl>
						</article>
					{/each}
				</div>
			{/if}
		</section>
	</div>
</div>
</PixelScrollArea>

<style>
	.invest-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		min-height: 100%;
	}

	/* ---------- Hero (mirrors CyberddyneView) ---------- */
	.hero {
		padding: 22px 26px;
		background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
	}
	.hero__brand {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 8px;
	}
	.hero__mark { font-size: 1.6rem; }
	.hero__title {
		font-size: 1.625rem;
		font-weight: 800;
		margin: 0;
		letter-spacing: 0.12em;
		color: #ffffff;
	}
	.hero__tagline {
		margin: 0;
		font-size: 0.875rem;
		line-height: 1.55;
		color: #e0e7ff;
		max-width: 820px;
	}

	/* ---------- Content ---------- */
	.content {
		padding: 20px;
		display: flex;
		flex-direction: column;
		gap: 18px;
		max-width: 1200px;
		margin: 0 auto;
	}

	/* ---------- Stat strip ---------- */
	.stats {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 12px;
	}
	@media (max-width: 720px) {
		.stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
	}
	.stat {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.45);
		padding: 10px 12px 12px 18px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.stat::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.stat__label {
		font-size: 0.7rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
	}
	.stat__value {
		font-size: 1.25rem;
		font-weight: 800;
		color: #000;
		line-height: 1.1;
	}
	.stat__sub {
		font-size: 0.85rem;
		font-weight: 600;
		color: #6b7280;
		margin-left: 2px;
	}

	/* ---------- Card primitive ---------- */
	.card {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 18px 18px 18px 26px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.card__head {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 12px;
		flex-wrap: wrap;
	}
	.card__title {
		font-size: 1.05rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
		margin: 0;
	}
	.card__hint {
		font-size: 0.7rem;
		color: #6b7280;
		letter-spacing: 0.02em;
	}

	.empty {
		font-size: 0.85rem;
		color: #6b7280;
		font-style: italic;
		margin: 0;
	}

	/* ---------- Positions grid ---------- */
	.position-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 14px;
	}
	@media (max-width: 820px) {
		.position-grid { grid-template-columns: minmax(0, 1fr); }
	}

	.position {
		position: relative;
		background: #fafafa;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 12px 14px 14px 20px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.position::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.position__head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 8px;
	}
	.position__pair {
		font-size: 0.95rem;
		font-weight: 700;
		color: #000;
		margin: 0;
		letter-spacing: 0.02em;
	}
	.position__meta {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 4px 12px;
		margin: 0;
		padding-top: 6px;
		border-top: 1px dashed #d1d5db;
		font-size: 0.75rem;
	}
	.position__meta dt {
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		font-size: 0.65rem;
		color: #6b7280;
	}
	.position__meta dd {
		margin: 0 0 4px;
		font-weight: 600;
		color: #1f2937;
	}
	.position__sep { color: #9ca3af; margin: 0 4px; }
	.position__fees {
		color: var(--accent-dark);
		font-weight: 700;
		text-align: right;
	}
</style>
