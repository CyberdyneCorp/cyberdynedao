<script lang="ts">
	import { PixelButton, PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import { cart } from '$lib/viewmodels/cartViewModel';
	import { formatMarketplacePrice as formatPrice } from '$lib/viewmodels/shopViewModel';

	const items = cart.items;
	const count = cart.count;
	const total = cart.total;

	function onQuantityChange(id: string, event: Event) {
		const value = parseInt((event.currentTarget as HTMLSelectElement).value, 10);
		cart.updateQuantity(id, value);
	}
</script>

<div class="flex flex-col h-full bg-white">
	<div class="bg-gradient-to-r from-green-600 to-emerald-600 p-2 border-b-2 border-black">
		<h1 class="text-sm font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-lg">🛒</span>
			YOUR BAG ({$count})
		</h1>
		<p class="font-mono text-xs text-black">Review your items • Complete your purchase</p>
	</div>

	<PixelScrollArea maxHeight="100%" ariaLabel="Cart contents">
	<div class="p-2">
		{#if $items.length === 0}
			<div class="text-center py-8">
				<div class="text-4xl mb-3">🛒</div>
				<h3 class="font-mono font-bold text-sm text-gray-800 mb-2">Your bag is empty</h3>
				<p class="text-xs text-gray-600 font-mono mb-4">Add some items from our marketplace to get started!</p>
				<div class="space-y-2">
					<div class="bg-blue-50 rounded border border-blue-200 p-2">
						<h4 class="font-mono font-bold text-xs text-blue-800">⚙️ Services</h4>
						<p class="text-xs text-blue-600">Custom development solutions</p>
					</div>
					<div class="bg-green-50 rounded border border-green-200 p-2">
						<h4 class="font-mono font-bold text-xs text-green-800">📚 Training</h4>
						<p class="text-xs text-green-600">Learn Web3 development</p>
					</div>
					<div class="bg-purple-50 rounded border border-purple-200 p-2">
						<h4 class="font-mono font-bold text-xs text-purple-800">🔑 Licenses</h4>
						<p class="text-xs text-purple-600">Software subscriptions</p>
					</div>
				</div>
			</div>
		{:else}
			<div class="space-y-2 mb-4">
				{#each $items as item (item.id)}
					<div class="bg-gray-50 rounded border border-gray-200 p-2">
						<div class="flex items-start gap-2">
							{#if item.icon}
								<img src={item.icon} alt={item.name} class="w-10 h-10 object-cover rounded border border-gray-300 flex-shrink-0" />
							{/if}
							<div class="flex-1 min-w-0">
								<h4 class="font-mono font-bold text-xs leading-tight mb-1">{item.name}</h4>
								<div class="flex items-center justify-between mt-1">
									<span class="text-xs font-mono font-bold text-gray-800">{formatPrice(item.price)}</span>
									<div class="flex items-center gap-1">
										<select
											class="text-xs border border-gray-300 rounded px-1 py-0.5 font-mono"
											value={item.quantity || 1}
											on:change={(e) => onQuantityChange(item.id, e)}
										>
											<option value="1">1</option>
											<option value="2">2</option>
											<option value="3">3</option>
											<option value="4">4</option>
											<option value="5">5</option>
										</select>
										<button
											class="text-xs bg-red-100 text-red-700 px-1.5 py-0.5 rounded hover:bg-red-200 transition-colors"
											on:click={() => cart.removeItem(item.id)}
											title="Remove item"
										>
											🗑️
										</button>
									</div>
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>

			<div class="border-t border-gray-200 pt-3">
				<div class="space-y-1 mb-3">
					<div class="flex justify-between text-xs font-mono">
						<span class="text-gray-600">Subtotal ({$count} items)</span>
						<span class="font-bold">{formatPrice($total)}</span>
					</div>
					<div class="flex justify-between text-xs font-mono">
						<span class="text-gray-600">Processing Fee</span>
						<span class="text-green-600 font-bold">FREE</span>
					</div>
					<div class="flex justify-between text-xs font-mono">
						<span class="text-gray-600">Support</span>
						<span class="text-green-600 font-bold">Included</span>
					</div>
				</div>

				<div class="border-t border-gray-200 pt-2 mb-3">
					<div class="flex justify-between text-sm font-mono font-bold">
						<span>Total</span>
						<span class="text-green-600">{formatPrice($total)}</span>
					</div>
				</div>

				<div class="space-y-2">
					<PixelButton variant="solid" size="md" fullWidth>💳 Checkout Now</PixelButton>
					<div class="flex gap-1">
						<div class="flex-1"><PixelButton variant="outline" size="sm" fullWidth>💬 Contact Sales</PixelButton></div>
						<div class="flex-1"><PixelButton variant="outline" size="sm" fullWidth onclick={() => cart.clear()}>🗑️ Clear All</PixelButton></div>
					</div>
				</div>

				<div class="mt-3 bg-gray-50 rounded border border-gray-200 p-2">
					<div class="flex items-center gap-1 mb-1">
						<span class="text-xs">🔒</span>
						<span class="text-xs font-mono font-bold text-gray-700">Secure Checkout</span>
					</div>
					<ul class="text-xs text-gray-600 font-mono space-y-0.5">
						<li>• SSL encrypted payment</li>
						<li>• 30-day money-back guarantee</li>
						<li>• 24/7 customer support</li>
					</ul>
				</div>
			</div>
		{/if}
	</div>
	</PixelScrollArea>
</div>
