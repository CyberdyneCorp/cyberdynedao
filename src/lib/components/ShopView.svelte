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

<div class="p-4">
	<h3 class="text-32 font-bold font-mono mb-6">Shop</h3>
	<div class="flex flex-col gap-4">
		{#each shopItems as item}
			<div class="flex items-center gap-4 p-4 border-2 border-black rounded bg-retro-gradient shadow-retro transition-all duration-100 hover:translate-x-px hover:translate-y-px hover:shadow-retro-hover">
				<img 
					src={item.image} 
					alt={item.title} 
					class="w-20 h-20 object-cover border-2 border-black rounded"
				/>
				<div class="flex-1">
					<h4 class="font-mono font-bold text-lg mb-2">{item.title}</h4>
					<p class="font-mono text-gray-600 mb-2">{item.subtitle}</p>
					<p class="font-mono font-bold text-xl">${item.price.toFixed(2)}</p>
				</div>
				<button 
					class="retro-button px-4 py-2 font-mono font-bold cursor-pointer"
					on:click={() => addToCart(item)}
				>
					Add to Cart
				</button>
			</div>
		{/each}
	</div>
</div>

