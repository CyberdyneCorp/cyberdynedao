<script lang="ts">
	import type { MarketplaceItem } from '$lib/types/components';
	import {
		createShopViewModel,
		getStatusText,
		formatMarketplacePrice as formatPrice
	} from '$lib/viewmodels/shopViewModel';

	export let onAddToCart: ((item: MarketplaceItem) => void) | undefined = undefined;

	const vm = createShopViewModel(undefined, (item) => onAddToCart?.(item));
	const { selectedCategory, selectedItem, filteredItems } = vm;
	const { items: marketplaceItems, categories, popularItems } = vm;

	function selectItem(item: MarketplaceItem) { vm.selectItem(item); }
	function addToCart(item: MarketplaceItem) { vm.addToCart(item); }

	type Pal = 'blue' | 'green' | 'purple' | 'orange' | 'red';
	const palette: Record<Pal, { accent: string; accentDark: string }> = {
		blue: { accent: '#3b82f6', accentDark: '#1d4ed8' },
		green: { accent: '#22c55e', accentDark: '#15803d' },
		purple: { accent: '#a855f7', accentDark: '#7e22ce' },
		orange: { accent: '#f97316', accentDark: '#c2410c' },
		red: { accent: '#ef4444', accentDark: '#b91c1c' }
	};
	const categoryPalette: Record<string, Pal> = {
		Services: 'blue',
		'Training Material': 'green',
		Licenses: 'purple'
	};
	const statusPalette: Record<string, Pal> = {
		available: 'green',
		beta: 'orange',
		'coming-soon': 'red'
	};
	const palStyle = (p: Pal) => `--accent: ${palette[p].accent}; --accent-dark: ${palette[p].accentDark};`;
	const catPal = (cat: string): Pal => categoryPalette[cat] ?? 'orange';
	const statusPal = (st: string): Pal => statusPalette[st] ?? 'blue';

	const ORANGE = palette.orange;
</script>

<div class="shop-view">
	<header class="hero" style="--accent: {ORANGE.accent}; --accent-dark: {ORANGE.accentDark};">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">🛍️</span>
			<h1 class="hero__title">CYBERDYNE MARKETPLACE</h1>
		</div>
		<p class="hero__tagline">Services · Training · Licenses — everything we ship, available to commission or buy.</p>
	</header>

	<div class="body">
		<aside class="sidebar">
			<div class="sidebar-section">
				<h3 class="sidebar-label">Categories</h3>
				<div class="category-list">
					{#each categories as category}
						<button
							type="button"
							class="category"
							class:category--active={$selectedCategory === category.id}
							on:click={() => vm.selectCategory(category.id)}
						>
							<span class="category__icon" aria-hidden="true">{category.icon}</span>
							<span class="category__name">{category.name}</span>
							<span class="category__count">{category.count}</span>
						</button>
					{/each}
				</div>
			</div>

			{#if $selectedCategory === 'all'}
				<div class="sidebar-section">
					<h3 class="sidebar-label">⭐ Popular</h3>
					<div class="item-list">
						{#each popularItems.slice(0, 4) as item}
							{@const pal = catPal(item.category)}
							<button
								type="button"
								class="item-card"
								class:item-card--active={$selectedItem?.id === item.id}
								style={palStyle(pal)}
								on:click={() => selectItem(item)}
							>
								<div class="item-card__title">{item.title}</div>
								<div class="item-card__meta">
									<span class="chip" style={palStyle(pal)}>{item.category}</span>
									<span class="item-card__price">{formatPrice(item.price)}</span>
								</div>
							</button>
						{/each}
					</div>
				</div>
			{/if}

			<div class="sidebar-section">
				<h3 class="sidebar-label">
					{$selectedCategory === 'all' ? 'All Products' : categories.find(c => c.id === $selectedCategory)?.name}
				</h3>
				<div class="item-list">
					{#each $filteredItems.slice(0, 12) as item}
						{@const pal = catPal(item.category)}
						{@const sPal = statusPal(item.status)}
						<button
							type="button"
							class="item-card"
							class:item-card--active={$selectedItem?.id === item.id}
							style={palStyle(pal)}
							on:click={() => selectItem(item)}
						>
							<div class="item-card__head">
								<span class="item-card__title">{item.title}</span>
								{#if item.popular}<span class="item-card__star" aria-label="Popular">⭐</span>{/if}
							</div>
							<div class="item-card__meta">
								<span class="chip" style={palStyle(pal)}>{item.subcategory || item.category}</span>
								<span class="chip chip--sm" style={palStyle(sPal)}>{getStatusText(item.status)}</span>
							</div>
							<div class="item-card__foot">
								<span class="item-card__duration">{item.duration || 'Custom'}</span>
								<span class="item-card__price">{formatPrice(item.price)}</span>
							</div>
						</button>
					{/each}
				</div>
			</div>
		</aside>

		<section class="main">
			{#if $selectedItem}
				{@const pal = catPal($selectedItem.category)}
				{@const sPal = statusPal($selectedItem.status)}
				<article class="detail" style={palStyle(pal)}>
					<header class="detail__head">
						<img src={$selectedItem.image} alt={$selectedItem.title} class="detail__img" />
						<div class="detail__head-text">
							<div class="detail__title-row">
								<h2 class="detail__title">{$selectedItem.title}</h2>
								{#if $selectedItem.popular}<span class="detail__star" aria-label="Popular">⭐</span>{/if}
							</div>
							<div class="detail__meta">
								<span class="chip" style={palStyle(pal)}>{$selectedItem.subcategory || $selectedItem.category}</span>
								<span class="chip" style={palStyle(sPal)}>{getStatusText($selectedItem.status)}</span>
								{#if $selectedItem.duration}
									<span class="detail__duration">⏱ {$selectedItem.duration}</span>
								{/if}
							</div>
							<p class="detail__desc">{$selectedItem.description}</p>
						</div>
					</header>

					<div class="detail__section" style={palStyle(pal)}>
						<h3 class="detail__section-title">Features Included</h3>
						<ul class="features">
							{#each $selectedItem.features as feature}
								<li>{feature}</li>
							{/each}
						</ul>
					</div>

					<div class="pricing" style={palStyle(pal)}>
						<div class="pricing__price-block">
							<div class="pricing__price">${$selectedItem.price.toLocaleString()}</div>
							{#if $selectedItem.duration}<div class="pricing__per">per {$selectedItem.duration}</div>{/if}
						</div>
						<ul class="pricing__terms">
							{#if $selectedItem.category === 'Services'}
								<li>Custom quote based on requirements</li>
								<li>50% upfront, 50% on completion</li>
								<li>Full source + handover</li>
							{:else if $selectedItem.category === 'Licenses'}
								<li>Annual subscription</li>
								<li>Full access and updates included</li>
								<li>Priority support</li>
							{:else}
								<li>Lifetime access</li>
								<li>All future updates included</li>
								<li>Source materials & exercises</li>
							{/if}
						</ul>
					</div>

					<div class="actions">
						<button
							type="button"
							class="btn btn--primary"
							style={palStyle(pal)}
							disabled={$selectedItem.status === 'coming-soon'}
							on:click={() => $selectedItem && addToCart($selectedItem)}
						>
							{$selectedItem.status === 'coming-soon' ? 'Coming Soon' : 'Add to Cart'}
						</button>
						<button type="button" class="btn btn--ghost">💬 Contact Sales</button>
						<button type="button" class="btn btn--ghost">❤️ Wishlist</button>
					</div>
				</article>
			{:else}
				<div class="welcome">
					<div class="welcome__mark" aria-hidden="true">🛍️</div>
					<h2 class="welcome__title">Cyberdyne Marketplace</h2>
					<p class="welcome__body">
						Three ways to work with us — commission a build, learn the stack, or license the software we ship.
					</p>
					<div class="welcome-grid">
						<div class="stat" style={palStyle('blue')}>
							<div class="stat__icon" aria-hidden="true">⚙️</div>
							<div class="stat__label">Services</div>
							<div class="stat__sub">Custom builds, end-to-end</div>
							<div class="stat__count">{marketplaceItems.filter(i => i.category === 'Services').length} listings</div>
						</div>
						<div class="stat" style={palStyle('green')}>
							<div class="stat__icon" aria-hidden="true">📚</div>
							<div class="stat__label">Training</div>
							<div class="stat__sub">Workshops & courseware</div>
							<div class="stat__count">{marketplaceItems.filter(i => i.category === 'Training Material').length} listings</div>
						</div>
						<div class="stat" style={palStyle('purple')}>
							<div class="stat__icon" aria-hidden="true">🔑</div>
							<div class="stat__label">Licenses</div>
							<div class="stat__sub">Direct software access</div>
							<div class="stat__count">{marketplaceItems.filter(i => i.category === 'Licenses').length} listings</div>
						</div>
					</div>
					<p class="welcome__hint">Pick a category on the left, or open any item to see scope, pricing, and terms.</p>
				</div>
			{/if}
		</section>
	</div>
</div>

<style>
	.shop-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		display: flex;
		flex-direction: column;
	}

	.hero {
		padding: 18px 24px;
		background: linear-gradient(135deg, #9a3412 0%, #f97316 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
		flex: 0 0 auto;
	}
	.hero__brand { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
	.hero__mark { font-size: 1.5rem; }
	.hero__title { font-size: 1.5rem; font-weight: 800; letter-spacing: 0.08em; margin: 0; color: #fff; }
	.hero__tagline { margin: 0; font-size: 0.875rem; line-height: 1.5; color: #fed7aa; max-width: 880px; }

	.body { flex: 1 1 auto; display: flex; min-height: 0; }
	.sidebar {
		width: 36%;
		max-width: 380px;
		min-width: 260px;
		border-right: 2px solid #000;
		background: #f9fafb;
		overflow-y: auto;
	}
	.main { flex: 1 1 auto; overflow-y: auto; padding: 18px 20px; }
	@media (max-width: 720px) {
		.body { flex-direction: column; }
		.sidebar { width: 100%; max-width: none; max-height: 40vh; border-right: 0; border-bottom: 2px solid #000; }
	}

	.sidebar-section { padding: 14px 12px; border-bottom: 1px dashed #d1d5db; }
	.sidebar-section:last-child { border-bottom: 0; }
	.sidebar-label {
		font-size: 0.6875rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: #1f2937;
		margin: 0 0 10px;
	}

	.category-list { display: flex; flex-direction: column; gap: 6px; }
	.category {
		all: unset;
		display: grid;
		grid-template-columns: 22px 1fr auto;
		gap: 8px;
		align-items: center;
		padding: 7px 10px;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.3);
		cursor: pointer;
		font-size: 0.8125rem;
		font-weight: 600;
		color: #1f2937;
		transition: transform 0.1s ease, background 0.1s ease;
	}
	.category:hover { background: #fef3c7; transform: translate(-1px, -1px); box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4); }
	.category--active { background: #f97316; color: #000; box-shadow: 3px 3px 0 #c2410c; }
	.category__count {
		font-size: 0.6875rem;
		font-weight: 700;
		background: #000;
		color: #fff;
		padding: 1px 6px;
		border-radius: 0;
	}

	.item-list { display: flex; flex-direction: column; gap: 8px; }

	.item-card {
		all: unset;
		position: relative;
		display: flex;
		flex-direction: column;
		gap: 4px;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 8px 10px 8px 16px;
		cursor: pointer;
		transition: transform 0.12s ease, box-shadow 0.12s ease;
	}
	.item-card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.item-card:hover {
		transform: translate(-1px, -1px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
	}
	.item-card--active {
		box-shadow: 4px 4px 0 var(--accent-dark);
		background: #fff7ed;
	}
	.item-card__head { display: flex; align-items: center; gap: 6px; }
	.item-card__title {
		font-size: 0.8125rem;
		font-weight: 700;
		color: #000;
		flex: 1 1 auto;
		line-height: 1.2;
		word-break: break-word;
	}
	.item-card__star { font-size: 0.75rem; }
	.item-card__meta { display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }
	.item-card__foot { display: flex; justify-content: space-between; align-items: center; margin-top: 2px; }
	.item-card__duration { font-size: 0.6875rem; color: #6b7280; }
	.item-card__price { font-size: 0.8125rem; font-weight: 800; color: var(--accent-dark); }

	.chip {
		display: inline-flex;
		align-items: center;
		padding: 1px 6px;
		font-size: 0.625rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		background: var(--accent);
		color: #ffffff;
		border: 1.5px solid #000;
	}
	.chip--sm { font-size: 0.5625rem; }

	/* ---------- Detail ---------- */
	.detail {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 18px 18px 18px 26px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.detail::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.detail__head { display: flex; gap: 14px; align-items: flex-start; }
	.detail__img {
		width: 80px;
		height: 80px;
		object-fit: cover;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		flex: 0 0 auto;
	}
	.detail__head-text { flex: 1 1 auto; min-width: 0; }
	.detail__title-row { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
	.detail__title { font-size: 1.25rem; font-weight: 800; color: #000; margin: 0; line-height: 1.2; }
	.detail__star { font-size: 1.125rem; }
	.detail__meta { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 8px; }
	.detail__duration { font-size: 0.75rem; color: #6b7280; }
	.detail__desc { font-size: 0.9375rem; line-height: 1.55; color: #1f2937; margin: 0; }

	.detail__section {
		position: relative;
		background: #f9fafb;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.35);
		padding: 12px 14px;
	}
	.detail__section-title {
		font-size: 0.75rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
		margin: 0 0 8px;
	}
	.features {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 4px 14px;
	}
	@media (max-width: 540px) {
		.features { grid-template-columns: minmax(0, 1fr); }
	}
	.features li {
		position: relative;
		padding-left: 18px;
		font-size: 0.8125rem;
		color: #1f2937;
		line-height: 1.4;
	}
	.features li::before {
		content: '▸';
		position: absolute;
		left: 0;
		top: 0;
		color: var(--accent-dark);
		font-weight: 700;
	}

	/* Pricing */
	.pricing {
		position: relative;
		background: #fffbeb;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 14px 16px;
		display: flex;
		flex-wrap: wrap;
		gap: 18px;
		align-items: center;
	}
	.pricing__price-block { display: flex; flex-direction: column; }
	.pricing__price {
		font-size: 1.875rem;
		font-weight: 800;
		color: var(--accent-dark);
		line-height: 1;
	}
	.pricing__per {
		font-size: 0.6875rem;
		color: #6b7280;
		margin-top: 4px;
		text-transform: uppercase;
		letter-spacing: 0.06em;
	}
	.pricing__terms {
		list-style: none;
		margin: 0;
		padding: 0;
		flex: 1 1 240px;
		min-width: 200px;
	}
	.pricing__terms li {
		position: relative;
		padding-left: 16px;
		font-size: 0.75rem;
		color: #1f2937;
		line-height: 1.45;
	}
	.pricing__terms li::before {
		content: '▸';
		position: absolute;
		left: 0;
		color: var(--accent-dark);
	}

	.actions { display: flex; gap: 10px; flex-wrap: wrap; }
	.btn {
		font-family: inherit;
		font-size: 0.8125rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		padding: 8px 14px;
		border: 2px solid #000;
		cursor: pointer;
		transition: transform 0.1s ease, box-shadow 0.1s ease;
	}
	.btn--primary {
		background: var(--accent);
		color: #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
	}
	.btn--primary:not(:disabled):hover {
		transform: translate(-1px, -1px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.55);
	}
	.btn--primary:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
	.btn--ghost {
		background: #ffffff;
		color: #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.3);
	}
	.btn--ghost:hover { background: #f3f4f6; transform: translate(-1px, -1px); box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.4); }

	/* Welcome */
	.welcome {
		text-align: center;
		max-width: 760px;
		margin: 16px auto;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 12px;
	}
	.welcome__mark { font-size: 2.25rem; }
	.welcome__title { font-size: 1.5rem; font-weight: 800; color: #000; margin: 0; }
	.welcome__body { font-size: 0.9375rem; line-height: 1.55; color: #374151; margin: 0; max-width: 620px; }
	.welcome__hint { font-size: 0.75rem; color: #6b7280; margin: 6px 0 0; font-style: italic; }

	.welcome-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 12px;
		width: 100%;
		margin-top: 12px;
	}
	@media (max-width: 720px) {
		.welcome-grid { grid-template-columns: minmax(0, 1fr); }
	}
	.stat {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 14px 14px 16px 22px;
		display: flex;
		flex-direction: column;
		gap: 4px;
		align-items: flex-start;
		text-align: left;
	}
	.stat::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.stat__icon { font-size: 1.5rem; }
	.stat__label {
		font-size: 0.875rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--accent-dark);
	}
	.stat__sub { font-size: 0.75rem; color: #374151; }
	.stat__count {
		font-size: 0.6875rem;
		color: #6b7280;
		margin-top: 4px;
		font-weight: 700;
	}
</style>
