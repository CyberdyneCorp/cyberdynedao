<script lang="ts">
	export let cartItems: any[] = [];

	interface CartItem {
		id: string;
		title: string;
		description?: string;
		category?: string;
		price: number;
		duration?: string;
		image: string;
		quantity?: number;
	}

	function removeFromCart(index: number) {
		cartItems = cartItems.filter((_, i) => i !== index);
	}

	function updateQuantity(index: number, quantity: number) {
		cartItems = cartItems.map((item, i) => 
			i === index ? { ...item, quantity } : item
		);
	}

	function clearCart() {
		cartItems = [];
	}

	function formatPrice(price: number) {
		return price >= 1000 ? `$${(price / 1000).toFixed(1)}k` : `$${price}`;
	}

	function getItemTotal(item: CartItem) {
		return item.price * (item.quantity || 1);
	}

	$: total = cartItems.reduce((sum, item) => sum + getItemTotal(item), 0);
	$: itemCount = cartItems.reduce((sum, item) => sum + (item.quantity || 1), 0);
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<!-- Header -->
	<div class="bg-gradient-to-r from-green-600 to-emerald-600 p-2 border-b-2 border-black">
		<h1 class="text-sm font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-lg">🛒</span>
			YOUR BAG ({itemCount})
		</h1>
		<p class="font-mono text-xs text-black">Review your items • Complete your purchase</p>
	</div>
	
	<div class="flex-1 p-2">
		{#if cartItems.length === 0}
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
			<!-- Cart Items -->
			<div class="space-y-2 mb-4">
				{#each cartItems as item, index}
					<div class="bg-gray-50 rounded border border-gray-200 p-2">
						<div class="flex items-start gap-2">
							<img 
								src={item.image} 
								alt={item.title} 
								class="w-10 h-10 object-cover rounded border border-gray-300 flex-shrink-0" 
							/>
							<div class="flex-1 min-w-0">
								<h4 class="font-mono font-bold text-xs leading-tight mb-1">{item.title}</h4>
								{#if item.category}
									<span class="text-xs px-1.5 py-0.5 bg-blue-100 text-blue-700 rounded font-mono">
										{item.category}
									</span>
								{/if}
								{#if item.duration}
									<span class="text-xs text-gray-500 font-mono ml-1">• {item.duration}</span>
								{/if}
								<div class="flex items-center justify-between mt-1">
									<span class="text-xs font-mono font-bold text-gray-800">{formatPrice(item.price)}</span>
									<div class="flex items-center gap-1">
										<select 
											class="text-xs border border-gray-300 rounded px-1 py-0.5 font-mono"
											value={item.quantity || 1}
											on:change={(e) => updateQuantity(index, parseInt(e.target.value))}
										>
											<option value="1">1</option>
											<option value="2">2</option>
											<option value="3">3</option>
											<option value="4">4</option>
											<option value="5">5</option>
										</select>
										<button 
											class="text-xs bg-red-100 text-red-700 px-1.5 py-0.5 rounded hover:bg-red-200 transition-colors"
											on:click={() => removeFromCart(index)}
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

			<!-- Summary -->
			<div class="border-t border-gray-200 pt-3">
				<div class="space-y-1 mb-3">
					<div class="flex justify-between text-xs font-mono">
						<span class="text-gray-600">Subtotal ({itemCount} items)</span>
						<span class="font-bold">{formatPrice(total)}</span>
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
						<span class="text-green-600">{formatPrice(total)}</span>
					</div>
				</div>

				<!-- Actions -->
				<div class="space-y-2">
					<button class="w-full bg-green-600 text-white py-2 px-3 rounded font-mono text-xs font-bold hover:bg-green-700 transition-colors">
						💳 Checkout Now
					</button>
					<div class="flex gap-1">
						<button class="flex-1 border border-gray-300 text-gray-700 py-1.5 px-2 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							💬 Contact Sales
						</button>
						<button 
							class="flex-1 border border-red-300 text-red-700 py-1.5 px-2 rounded font-mono text-xs hover:bg-red-50 transition-colors"
							on:click={clearCart}
						>
							🗑️ Clear All
						</button>
					</div>
				</div>

				<!-- Security Info -->
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
</div>

