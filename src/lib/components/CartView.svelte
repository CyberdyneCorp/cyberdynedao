<script lang="ts">
	export let cartItems: any[] = [];

	function removeFromCart(index: number) {
		cartItems = cartItems.filter((_, i) => i !== index);
	}

	$: total = cartItems.reduce((sum, item) => sum + item.price, 0);
</script>

<div class="p-4 flex flex-col gap-4">
	<h3 class="text-32 font-bold font-mono mb-6">Your Items</h3>
	
	{#if cartItems.length === 0}
		<p class="text-gray-600 font-mono">Your cart is empty</p>
	{:else}
		<div class="flex flex-col gap-4">
			{#each cartItems as item, index}
				<div class="flex items-center gap-4 p-4 border border-gray-300 rounded">
					<img 
						src={item.image} 
						alt={item.title} 
						class="w-15 h-15 object-cover border border-black" 
					/>
					<div class="flex-1">
						<h4 class="font-mono font-bold mb-1">{item.title}</h4>
						<p class="font-mono text-gray-600">${item.price}</p>
					</div>
					<div class="flex items-center gap-2">
						<select class="border border-black p-1 font-mono">
							<option>1</option>
							<option>2</option>
							<option>3</option>
						</select>
						<button 
							class="bg-red-500 text-white px-2 py-1 border border-black cursor-pointer transition-colors duration-150 hover:bg-red-600"
							on:click={() => removeFromCart(index)}
						>
							🗑
						</button>
					</div>
				</div>
			{/each}
		</div>
		
		<div class="border-t border-gray-300 pt-4 mt-6 flex flex-col gap-2 font-mono">
			<div class="flex justify-between">
				<span>Subtotal</span>
				<span>${total.toFixed(2)}</span>
			</div>
			<div class="flex justify-between">
				<span>Shipping</span>
				<span>Free</span>
			</div>
			<div class="flex justify-between">
				<span>Taxes</span>
				<span class="text-gray-600">Calculated at next step</span>
			</div>
			<div class="flex justify-between font-bold text-lg border-t border-gray-300 pt-2">
				<span>Total</span>
				<span>${total.toFixed(2)}</span>
			</div>
			<button class="w-full bg-blue-600 text-white p-3 mt-4 font-mono font-bold border-2 border-black shadow-retro cursor-pointer transition-all duration-100 hover:translate-x-px hover:translate-y-px hover:shadow-retro-hover active:translate-x-0.5 active:translate-y-0.5 active:shadow-retro-pressed">
				Checkout
			</button>
		</div>
	{/if}
</div>

