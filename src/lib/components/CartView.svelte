<script lang="ts">
	export let cartItems: any[] = [];

	function removeFromCart(index: number) {
		cartItems = cartItems.filter((_, i) => i !== index);
	}

	$: total = cartItems.reduce((sum, item) => sum + item.price, 0);
</script>

<div class="cart-container">
	<h3 class="cart-title">Your Items</h3>
	
	{#if cartItems.length === 0}
		<p class="cart-empty">Your cart is empty</p>
	{:else}
		<div class="cart-items">
			{#each cartItems as item, index}
				<div class="cart-item">
					<img 
						src={item.image} 
						alt={item.title} 
						class="cart-image" 
					/>
					<div class="cart-content">
						<h4 class="cart-item-title">{item.title}</h4>
						<p class="cart-item-price">${item.price}</p>
					</div>
					<div class="cart-controls">
						<select class="cart-quantity">
							<option>1</option>
							<option>2</option>
							<option>3</option>
						</select>
						<button 
							class="cart-remove"
							on:click={() => removeFromCart(index)}
						>
							🗑
						</button>
					</div>
				</div>
			{/each}
		</div>
		
		<div class="cart-summary">
			<div class="cart-summary-row">
				<span>Subtotal</span>
				<span>${total.toFixed(2)}</span>
			</div>
			<div class="cart-summary-row">
				<span>Shipping</span>
				<span>Free</span>
			</div>
			<div class="cart-summary-row">
				<span>Taxes</span>
				<span class="cart-taxes">Calculated at next step</span>
			</div>
			<div class="cart-total">
				<span>Total</span>
				<span>${total.toFixed(2)}</span>
			</div>
			<button class="cart-checkout">
				Checkout
			</button>
		</div>
	{/if}
</div>

<style>
	.cart-container {
		padding: 16px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	
	.cart-title {
		font-size: 32px;
		font-weight: 700;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		margin-bottom: 24px;
	}
	
	.cart-empty {
		color: #6b7280;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
	}
	
	.cart-items {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	
	.cart-item {
		display: flex;
		align-items: center;
		gap: 16px;
		padding: 16px;
		border: 1px solid #d1d5db;
		border-radius: 4px;
	}
	
	.cart-image {
		width: 60px;
		height: 60px;
		object-fit: cover;
		border: 1px solid #000;
	}
	
	.cart-content {
		flex: 1;
	}
	
	.cart-item-title {
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		font-weight: 700;
		margin-bottom: 4px;
	}
	
	.cart-item-price {
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		color: #6b7280;
	}
	
	.cart-controls {
		display: flex;
		align-items: center;
		gap: 8px;
	}
	
	.cart-quantity {
		border: 1px solid #000;
		padding: 4px;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
	}
	
	.cart-remove {
		background: #ef4444;
		color: white;
		padding: 4px 8px;
		border: 1px solid #000;
		cursor: pointer;
		transition: background-color 0.15s ease;
	}
	
	.cart-remove:hover {
		background: #dc2626;
	}
	
	.cart-summary {
		border-top: 1px solid #d1d5db;
		padding-top: 16px;
		margin-top: 24px;
		display: flex;
		flex-direction: column;
		gap: 8px;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
	}
	
	.cart-summary-row {
		display: flex;
		justify-content: space-between;
	}
	
	.cart-taxes {
		color: #6b7280;
	}
	
	.cart-total {
		display: flex;
		justify-content: space-between;
		font-weight: 700;
		font-size: 18px;
		border-top: 1px solid #d1d5db;
		padding-top: 8px;
	}
	
	.cart-checkout {
		width: 100%;
		background: #2563eb;
		color: white;
		padding: 12px;
		margin-top: 16px;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		font-weight: 700;
		border: 2px solid #000;
		box-shadow: 2px 2px 0px #000, 4px 4px 0px rgba(0,0,0,0.3);
		cursor: pointer;
		transition: all 0.1s ease;
	}
	
	.cart-checkout:hover {
		transform: translate(1px, 1px);
		box-shadow: 1px 1px 0px #000, 2px 2px 0px rgba(0,0,0,0.3);
	}
	
	.cart-checkout:active {
		transform: translate(2px, 2px);
		box-shadow: none;
	}
</style>