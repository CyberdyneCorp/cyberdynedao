<script lang="ts">
	import { PixelButton, PixelScrollArea, Badge } from '@cyberdynecorp/svelte-ui-core';
	import { productSuite, type ProductStatus } from '$lib/data/products';

	const paletteVars = {
		blue: { accent: '#3b82f6', accentDark: '#1d4ed8' },
		green: { accent: '#22c55e', accentDark: '#15803d' },
		purple: { accent: '#a855f7', accentDark: '#7e22ce' },
		orange: { accent: '#f97316', accentDark: '#c2410c' },
		red: { accent: '#ef4444', accentDark: '#b91c1c' }
	} as const;

	const statusLabel: Record<ProductStatus, string> = {
		live: 'Live',
		active: 'Active',
		development: 'Dev',
		planning: 'Planning',
		design: 'Design'
	};

	const statusVariant: Record<ProductStatus, 'success' | 'info' | 'warning' | 'neutral'> = {
		live: 'success',
		active: 'success',
		development: 'info',
		planning: 'warning',
		design: 'warning'
	};
</script>

<PixelScrollArea maxHeight="100%" ariaLabel="Product suite">
<div class="products-container">
	<div class="header-section">
		<h1 class="products-title">CyberdyneCorp Product Suite</h1>
		<p class="products-subtitle">
			Explore the projects shaping the Cyberdyne ecosystem — geospatial intelligence, AI knowledge systems, DeFi, developer tooling, and more.
		</p>
	</div>

	<div class="products-grid">
		{#each productSuite as product}
			{@const p = paletteVars[product.palette]}
			<article
				class="product-card"
				class:product-card--full={product.fullWidth}
				style="--accent: {p.accent}; --accent-dark: {p.accentDark};"
			>
				<header class="product-card__header">
					<div class="product-card__icon" aria-hidden="true">
						<span>{product.icon}</span>
					</div>
					<h2 class="product-card__name">{product.name}</h2>
					<div class="product-card__status">
						<Badge variant={statusVariant[product.status]} size="sm">
							{statusLabel[product.status]}
						</Badge>
					</div>
				</header>

				<p class="product-card__desc">{product.description}</p>

				<h3 class="product-card__features-title">Key Features</h3>
				<ul class="product-card__features">
					{#each product.features as f}
						<li>{f}</li>
					{/each}
					{#if product.extraFeatures}
						{#each product.extraFeatures as f}
							<li>{f}</li>
						{/each}
					{/if}
				</ul>
			</article>
		{/each}
	</div>

	<div class="cta-section">
		<p class="cta-text">
			Curious about what we're building? Reach out and let's talk.
		</p>
		<PixelButton variant="solid" size="lg">Get in Touch</PixelButton>
	</div>
</div>
</PixelScrollArea>

<style>
	.products-container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 24px 20px 32px;
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
	}

	.header-section {
		margin-bottom: 28px;
		text-align: center;
	}
	.products-title {
		font-size: 1.875rem;
		font-weight: 700;
		color: #000;
		margin: 0 0 12px;
		letter-spacing: 0.5px;
	}
	.products-subtitle {
		font-size: 1rem;
		color: #374151;
		max-width: 760px;
		margin: 0 auto;
		line-height: 1.6;
	}

	.products-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 20px;
	}

	@media (max-width: 720px) {
		.products-grid {
			grid-template-columns: minmax(0, 1fr);
		}
	}

	.product-card {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 18px 18px 18px 26px;
		display: flex;
		flex-direction: column;
		gap: 12px;
		transition: transform 0.15s ease, box-shadow 0.15s ease;
	}
	.product-card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.product-card:hover {
		transform: translate(-2px, -2px);
		box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.55);
	}
	.product-card--full {
		grid-column: 1 / -1;
	}

	.product-card__header {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.product-card__icon {
		flex: 0 0 auto;
		width: 40px;
		height: 40px;
		border: 2px solid #000;
		background: var(--accent);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 22px;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.4);
	}
	.product-card__name {
		flex: 1 1 auto;
		font-size: 1.25rem;
		font-weight: 700;
		color: #000;
		margin: 0;
		line-height: 1.2;
		min-width: 0;
		word-break: break-word;
	}
	.product-card__status {
		flex: 0 0 auto;
	}

	.product-card__desc {
		font-size: 0.875rem;
		line-height: 1.55;
		color: #1f2937;
		margin: 0;
	}

	.product-card__features-title {
		font-size: 0.75rem;
		font-weight: 700;
		color: var(--accent-dark);
		margin: 4px 0 0;
		text-transform: uppercase;
		letter-spacing: 0.08em;
	}
	.product-card__features {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 4px;
	}
	.product-card--full .product-card__features {
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 4px 18px;
	}
	@media (max-width: 720px) {
		.product-card--full .product-card__features {
			grid-template-columns: minmax(0, 1fr);
		}
	}
	.product-card__features li {
		position: relative;
		padding-left: 16px;
		font-size: 0.8125rem;
		line-height: 1.45;
		color: #374151;
	}
	.product-card__features li::before {
		content: '▸';
		position: absolute;
		left: 0;
		top: 0;
		color: var(--accent-dark);
		font-weight: 700;
	}

	.cta-section {
		margin-top: 32px;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 14px;
	}
	.cta-text {
		font-size: 1rem;
		color: #374151;
		margin: 0;
	}
</style>
