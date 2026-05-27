<script lang="ts">
	import {
		PixelButton,
		PixelScrollArea,
		EmptyState,
		Card,
		Badge
	} from '@cyberdynecorp/svelte-ui-core';
	import { cart } from '$lib/viewmodels/cartViewModel';
	import { formatMarketplacePrice as formatPrice } from '$lib/viewmodels/shopViewModel';

	const items = cart.items;
	const count = cart.count;
	const total = cart.total;

	const QTY_MAX = 99;

	function setQty(id: string, qty: number) {
		cart.updateQuantity(id, Math.max(0, Math.min(QTY_MAX, qty)));
	}

	// Marketplace entry points shown on the empty bag — each is a hint
	// at what lives in the shop, not a real link target yet.
	const categories = [
		{ icon: '⚙️', label: 'Services', blurb: 'Custom development solutions', tone: 'info' as const },
		{ icon: '📚', label: 'Training', blurb: 'Learn Web3 development', tone: 'success' as const },
		{ icon: '🔑', label: 'Licenses', blurb: 'Software subscriptions', tone: 'neutral' as const }
	];
</script>

<div class="bag">
	<header class="bag__head">
		<div class="bag__title">
			<span class="bag__icon" aria-hidden="true">🛍️</span>
			<h1>YOUR BAG</h1>
			<Badge variant={$count ? 'info' : 'neutral'} size="sm">{$count}</Badge>
		</div>
		<p class="bag__sub">Review your items · Complete your purchase</p>
	</header>

	<PixelScrollArea maxHeight="100%" ariaLabel="Cart contents">
		<div class="bag__body">
			{#if $items.length === 0}
				<EmptyState
					icon="🛒"
					title="Your bag is empty"
					description="Add something from the marketplace to get started."
				/>
				<div class="cats">
					{#each categories as c (c.label)}
						<Card variant="outlined" padding="sm">
							<div class="cat">
								<span class="cat__icon" aria-hidden="true">{c.icon}</span>
								<div class="cat__text">
									<div class="cat__row">
										<span class="cat__label">{c.label}</span>
										<Badge variant={c.tone} size="sm">shop</Badge>
									</div>
									<span class="cat__blurb">{c.blurb}</span>
								</div>
							</div>
						</Card>
					{/each}
				</div>
			{:else}
				<div class="lines">
					{#each $items as item (item.id)}
						<Card variant="outlined" padding="sm">
							<div class="line">
								{#if item.icon}
									<img class="line__icon" src={item.icon} alt={item.name} />
								{:else}
									<div class="line__icon line__icon--ph" aria-hidden="true">📦</div>
								{/if}
								<div class="line__main">
									<h4 class="line__name">{item.name}</h4>
									<div class="line__row">
										<span class="line__price">{formatPrice(item.price)}</span>
										<div class="qty" role="group" aria-label="Quantity for {item.name}">
											<PixelButton
												variant="outline"
												size="sm"
												ariaLabel="Decrease quantity"
												onclick={() => setQty(item.id, (item.quantity || 1) - 1)}
											>
												−
											</PixelButton>
											<span class="qty__val" aria-live="polite">{item.quantity || 1}</span>
											<PixelButton
												variant="outline"
												size="sm"
												ariaLabel="Increase quantity"
												onclick={() => setQty(item.id, (item.quantity || 1) + 1)}
											>
												+
											</PixelButton>
											<PixelButton
												variant="ghost"
												size="sm"
												ariaLabel="Remove {item.name}"
												onclick={() => cart.removeItem(item.id)}
											>
												🗑
											</PixelButton>
										</div>
									</div>
									<div class="line__subtotal">
										{item.quantity || 1} × {formatPrice(item.price)} =
										<strong>{formatPrice(item.price * (item.quantity || 1))}</strong>
									</div>
								</div>
							</div>
						</Card>
					{/each}
				</div>

				<Card variant="elevated" padding="md">
					<div class="totals">
						<div class="totals__row">
							<span>Subtotal ({$count} {$count === 1 ? 'item' : 'items'})</span>
							<span class="totals__num">{formatPrice($total)}</span>
						</div>
						<div class="totals__row">
							<span>Processing fee</span>
							<Badge variant="success" size="sm">FREE</Badge>
						</div>
						<div class="totals__row">
							<span>Support</span>
							<Badge variant="success" size="sm">Included</Badge>
						</div>
						<div class="totals__row totals__row--grand">
							<span>Total</span>
							<span class="totals__grand">{formatPrice($total)}</span>
						</div>
					</div>
				</Card>

				<div class="actions">
					<PixelButton variant="solid" size="md" fullWidth>💳 Checkout</PixelButton>
					<div class="actions__split">
						<PixelButton variant="outline" size="sm" fullWidth>💬 Contact sales</PixelButton>
						<PixelButton variant="ghost" size="sm" fullWidth onclick={() => cart.clear()}>
							Clear all
						</PixelButton>
					</div>
				</div>

				<div class="trust">
					<span class="trust__head">🔒 Secure checkout</span>
					<ul>
						<li>SSL-encrypted payment</li>
						<li>30-day money-back guarantee</li>
						<li>24/7 support</li>
					</ul>
				</div>
			{/if}
		</div>
	</PixelScrollArea>
</div>

<style>
	.bag {
		display: flex;
		flex-direction: column;
		height: 100%;
		background: #fff;
		font-family: 'Courier New', ui-monospace, monospace;
	}

	.bag__head {
		padding: 10px 12px;
		border-bottom: 2px solid #000;
		background: #f5f5fb;
		flex-shrink: 0;
	}
	.bag__title {
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.bag__icon {
		font-size: 18px;
	}
	.bag__title h1 {
		font-size: 14px;
		font-weight: 700;
		letter-spacing: 0.04em;
		margin: 0;
	}
	.bag__sub {
		margin: 4px 0 0;
		font-size: 11px;
		color: #555;
	}

	.bag__body {
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	/* Empty state category tiles */
	.cats {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.cat {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.cat__icon {
		font-size: 20px;
	}
	.cat__text {
		flex: 1;
		min-width: 0;
	}
	.cat__row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 8px;
	}
	.cat__label {
		font-weight: 700;
		font-size: 12px;
	}
	.cat__blurb {
		font-size: 11px;
		color: #666;
	}

	/* Filled state line items */
	.lines {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.line {
		display: flex;
		gap: 10px;
		align-items: flex-start;
	}
	.line__icon {
		width: 44px;
		height: 44px;
		object-fit: cover;
		border: 2px solid #000;
		border-radius: 4px;
		flex-shrink: 0;
	}
	.line__icon--ph {
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 22px;
		background: #f0f0f5;
	}
	.line__main {
		flex: 1;
		min-width: 0;
	}
	.line__name {
		margin: 0 0 4px;
		font-size: 12px;
		font-weight: 700;
		line-height: 1.25;
	}
	.line__row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 8px;
		flex-wrap: wrap;
	}
	.line__price {
		font-size: 12px;
		font-weight: 700;
	}
	.qty {
		display: flex;
		align-items: center;
		gap: 4px;
	}
	.qty__val {
		min-width: 1.6em;
		text-align: center;
		font-size: 12px;
		font-weight: 700;
	}
	.line__subtotal {
		margin-top: 4px;
		font-size: 11px;
		color: #666;
	}

	/* Totals */
	.totals {
		display: flex;
		flex-direction: column;
		gap: 6px;
		font-size: 12px;
	}
	.totals__row {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.totals__num {
		font-weight: 700;
	}
	.totals__row--grand {
		border-top: 2px solid #000;
		padding-top: 6px;
		margin-top: 2px;
		font-size: 14px;
		font-weight: 700;
	}
	.totals__grand {
		color: #1f9d55;
	}

	.actions {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.actions__split {
		display: flex;
		gap: 6px;
	}

	.trust {
		border: 2px solid #000;
		border-radius: 4px;
		background: #f5f5fb;
		padding: 8px 10px;
	}
	.trust__head {
		font-size: 11px;
		font-weight: 700;
	}
	.trust ul {
		margin: 4px 0 0;
		padding-left: 16px;
		font-size: 11px;
		color: #555;
	}
	.trust li {
		list-style: square;
	}
</style>
