<script lang="ts">
	export let onAddToCart: ((item: any) => void) | undefined = undefined;

	interface ShopItem {
		id: number;
		title: string;
		subtitle: string;
		price: number;
		image: string;
	}

	const shopItems: ShopItem[] = [
		{
			id: 1,
			title: 'The Sacred Order',
			subtitle: 'Sterling Silver Dice Cage',
			price: 475.00,
			image: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=150&h=150&fit=crop'
		},
		{
			id: 2,
			title: 'Retro Terminal Poster',
			subtitle: 'Vintage Computer Art',
			price: 25.00,
			image: 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=150&h=150&fit=crop'
		},
		{
			id: 3,
			title: 'Pixel Art Book',
			subtitle: 'Digital Nostalgia Collection',
			price: 45.00,
			image: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=150&h=150&fit=crop'
		}
	];

	function addToCart(item: ShopItem) {
		if (onAddToCart) {
			onAddToCart(item);
		}
	}
</script>

<div class="shop-container">
	<h3 class="shop-title">Shop</h3>
	<div class="shop-grid">
		{#each shopItems as item}
			<div class="shop-item">
				<img 
					src={item.image} 
					alt={item.title} 
					class="shop-image"
				/>
				<div class="shop-content">
					<h4 class="shop-item-title">{item.title}</h4>
					<p class="shop-subtitle">{item.subtitle}</p>
					<p class="shop-price">${item.price.toFixed(2)}</p>
				</div>
				<button 
					class="shop-button"
					on:click={() => addToCart(item)}
				>
					Add to Cart
				</button>
			</div>
		{/each}
	</div>
</div>

<style>
	.shop-container {
		padding: 16px;
	}
	
	.shop-title {
		font-size: 32px;
		font-weight: 700;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		margin-bottom: 24px;
	}
	
	.shop-grid {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	
	.shop-item {
		display: flex;
		align-items: center;
		gap: 16px;
		padding: 16px;
		border: 2px solid #000;
		border-radius: 4px;
		background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
		box-shadow: 2px 2px 0px #000, 4px 4px 0px rgba(0,0,0,0.3);
		transition: all 0.1s ease;
	}
	
	.shop-item:hover {
		transform: translate(1px, 1px);
		box-shadow: 1px 1px 0px #000, 2px 2px 0px rgba(0,0,0,0.3);
	}
	
	.shop-image {
		width: 80px;
		height: 80px;
		object-fit: cover;
		border: 2px solid #000;
		border-radius: 4px;
	}
	
	.shop-content {
		flex: 1;
	}
	
	.shop-item-title {
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		font-weight: 700;
		font-size: 18px;
		margin-bottom: 8px;
	}
	
	.shop-subtitle {
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		color: #6b7280;
		margin-bottom: 8px;
	}
	
	.shop-price {
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		font-weight: 700;
		font-size: 20px;
	}
	
	.shop-button {
		background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
		border: 2px solid #000;
		box-shadow: 2px 2px 0px #000, 4px 4px 0px rgba(0,0,0,0.3);
		padding: 8px 16px;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		font-weight: 700;
		cursor: pointer;
		transition: all 0.1s ease;
	}
	
	.shop-button:hover {
		transform: translate(1px, 1px);
		box-shadow: 1px 1px 0px #000, 2px 2px 0px rgba(0,0,0,0.3);
	}
	
	.shop-button:active {
		transform: translate(2px, 2px);
		box-shadow: none;
	}
</style>