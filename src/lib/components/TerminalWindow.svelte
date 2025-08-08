<script lang="ts">
	export let title: string = 'Terminal';
	export let showCart: boolean = false;
	export let cartItems: any[] = [];
	export let currentView: string = 'read';
	export let onAddToCart: ((item: any) => void) | undefined = undefined;
	export let embedded: boolean = false;

	interface NewsItem {
		title: string;
		source: string;
		author: string;
		image?: string;
	}

	const newsItems: NewsItem[] = [
		{
			title: 'Cyan Banister — From Homeless and Broke to Top Angel Investor...',
			source: '4',
			author: 'Tim Ferriss',
			image: 'https://images.unsplash.com/photo-1494790108755-2616c1f3c85d?w=150&h=150&fit=crop&crop=face'
		},
		{
			title: 'Cyan Banister, Arielle Zuckerberg Raise $181 Million to Back "Magi...',
			source: 'B',
			author: 'Lizette Chapman',
			image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'
		},
		{
			title: 'Zivity founder finally takes it all off',
			source: 'VB',
			author: 'Paul Boutin',
			image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face'
		},
		{
			title: 'JFK Files, Nvidia\'s New Chip, Taco Bell AI, Intel CEO | Wed, March 19',
			source: '📺',
			author: 'TBPN',
			image: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=150&h=150&fit=crop'
		},
		{
			title: 'LA\'s Wildfire Disaster, Zuck Flips on Free Speech, Why Trump Wants...',
			source: '📺',
			author: 'All-In Podcast',
			image: 'https://images.unsplash.com/photo-1611348586804-61bf6c080437?w=150&h=150&fit=crop'
		},
		{
			title: 'News Panel with Cyan Banister and Erik Lanigan - TWiST #225',
			source: '📺',
			author: 'This Week in Startups',
			image: 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=150&h=150&fit=crop'
		}
	];


	const shopItems = [
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

	function removeFromCart(index: number) {
		cartItems = cartItems.filter((_, i) => i !== index);
	}

	function addToCart(item: any) {
		if (onAddToCart) {
			onAddToCart(item);
		}
	}
</script>

{#if embedded}
    <div class="p-4 overflow-y-auto flex-1">
		{#if showCart}
			<div class="space-y-4">
				<h3 class="text-2xl font-bold font-mono mb-6">Your Items</h3>
				
				{#if cartItems.length === 0}
					<p class="text-gray-600 font-mono">Your cart is empty</p>
				{:else}
					{#each cartItems as item, index}
						<div class="flex items-center gap-4 p-4 border border-gray-300 rounded">
							<img src={item.image} alt={item.title} class="w-15 h-15 object-cover border border-black" />
							<div class="flex-1">
								<h4 class="font-mono font-bold">{item.title}</h4>
								<p class="font-mono text-gray-600">${item.price}</p>
							</div>
							<div class="flex items-center gap-2">
								<select class="border border-black p-1 font-mono">
									<option>1</option>
									<option>2</option>
									<option>3</option>
								</select>
								<button 
									class="bg-red-500 text-white px-2 py-1 border border-black hover:bg-red-600"
									on:click={() => removeFromCart(index)}
								>
									🗑
								</button>
							</div>
						</div>
					{/each}
					
					<div class="border-t border-gray-300 pt-4 mt-6">
						<div class="space-y-2 font-mono">
							<div class="flex justify-between">
								<span>Subtotal</span>
								<span>${cartItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}</span>
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
								<span>${cartItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}</span>
							</div>
						</div>
						<button class="w-full bg-blue-600 text-white py-3 mt-4 font-mono font-bold retro-button">
							Checkout
						</button>
					</div>
				{/if}
			</div>
{:else if currentView === 'investments'}
			<div class="grid grid-cols-2 gap-x-16 gap-y-12 p-12 justify-items-center">
				<!-- Row 1 -->
				<div class="flex flex-col items-center gap-2">
					<div class="w-20 h-24 bg-orange-200 border-2 border-black relative retro-button cursor-pointer">
						<!-- Folder icon -->
						<div class="absolute top-2 left-2 w-14 h-2 bg-white border border-black"></div>
						<div class="absolute top-4 left-2 w-12 h-12 bg-orange-300 border border-black"></div>
						<div class="absolute top-6 left-3 w-3 h-1 bg-black"></div>
						<div class="absolute top-8 left-3 w-8 h-1 bg-black"></div>
						<div class="absolute top-10 left-3 w-6 h-1 bg-black"></div>
					</div>
					<div class="px-2 py-1 bg-blue-400 border border-black text-center">
						<span class="font-mono text-xs font-bold text-white">All</span>
					</div>
				</div>

				<div class="flex flex-col items-center gap-2">
					<div class="w-20 h-24 bg-orange-400 border-2 border-black relative retro-button cursor-pointer flex items-center justify-center">
						<!-- Pixel character/angel -->
						<div class="w-12 h-16 relative">
							<!-- Head -->
							<div class="absolute top-0 left-4 w-4 h-4 bg-yellow-300 border border-black"></div>
							<!-- Wings -->
							<div class="absolute top-2 left-1 w-2 h-3 bg-white border border-black"></div>
							<div class="absolute top-2 right-1 w-2 h-3 bg-white border border-black"></div>
							<!-- Body -->
							<div class="absolute top-4 left-3 w-6 h-8 bg-blue-400 border border-black"></div>
							<!-- Arms -->
							<div class="absolute top-6 left-1 w-2 h-2 bg-yellow-200 border border-black"></div>
							<div class="absolute top-6 right-1 w-2 h-2 bg-yellow-200 border border-black"></div>
						</div>
					</div>
					<div class="px-2 py-1 bg-blue-400 border border-black text-center">
						<span class="font-mono text-xs font-bold text-white">Banister Angels</span>
					</div>
				</div>

				<!-- Row 2 -->
				<div class="flex flex-col items-center gap-2">
					<div class="w-20 h-24 bg-orange-200 border-2 border-black relative retro-button cursor-pointer">
						<!-- Folder icon -->
						<div class="absolute top-2 left-2 w-14 h-2 bg-white border border-black"></div>
						<div class="absolute top-4 left-2 w-12 h-12 bg-orange-300 border border-black"></div>
						<div class="absolute top-6 left-3 w-3 h-1 bg-black"></div>
						<div class="absolute top-8 left-3 w-8 h-1 bg-black"></div>
						<div class="absolute top-10 left-3 w-6 h-1 bg-black"></div>
					</div>
					<div class="px-2 py-1 bg-blue-400 border border-black text-center">
						<span class="font-mono text-xs font-bold text-white">Growth</span>
					</div>
				</div>

				<div class="flex flex-col items-center gap-2">
					<div class="w-20 h-24 bg-red-400 border-2 border-black relative retro-button cursor-pointer flex items-center justify-center">
						<!-- Building/chart icon -->
						<div class="w-12 h-16 relative">
							<div class="absolute bottom-0 left-1 w-2 h-4 bg-red-600"></div>
							<div class="absolute bottom-0 left-4 w-2 h-8 bg-cyan-400"></div>
							<div class="absolute bottom-0 left-7 w-2 h-6 bg-blue-600"></div>
							<div class="absolute bottom-0 right-1 w-2 h-3 bg-gray-600"></div>
						</div>
					</div>
					<div class="px-2 py-1 bg-blue-400 border border-black text-center">
						<span class="font-mono text-xs font-bold text-white">Founders Fund</span>
					</div>
				</div>

				<!-- Row 3 -->
				<div class="flex flex-col items-center gap-2">
					<div class="w-20 h-24 bg-blue-500 border-2 border-black relative retro-button cursor-pointer flex items-center justify-center">
						<!-- Eye icon -->
						<div class="w-16 h-16 bg-blue-600 border-2 border-black rounded-full flex items-center justify-center relative">
							<div class="w-8 h-8 bg-white rounded-full flex items-center justify-center">
								<div class="w-4 h-4 bg-black rounded-full"></div>
							</div>
						</div>
					</div>
					<div class="px-2 py-1 bg-blue-400 border border-black text-center">
						<span class="font-mono text-xs font-bold text-white">Long Journey</span>
					</div>
				</div>

				<div class="flex flex-col items-center gap-2">
					<div class="w-20 h-24 bg-orange-200 border-2 border-black relative retro-button cursor-pointer">
						<!-- Folder icon -->
						<div class="absolute top-2 left-2 w-14 h-2 bg-white border border-black"></div>
						<div class="absolute top-4 left-2 w-12 h-12 bg-orange-300 border border-black"></div>
						<div class="absolute top-6 left-3 w-3 h-1 bg-black"></div>
						<div class="absolute top-8 left-3 w-8 h-1 bg-black"></div>
						<div class="absolute top-10 left-3 w-6 h-1 bg-black"></div>
					</div>
					<div class="px-2 py-1 bg-blue-400 border border-black text-center">
						<span class="font-mono text-xs font-bold text-white">Exited</span>
					</div>
				</div>
			</div>
		{:else if currentView === 'shop'}
			<div class="space-y-4">
				<h3 class="text-2xl font-bold font-mono mb-6">Shop</h3>
				<div class="grid gap-4">
					{#each shopItems as item}
						<div class="flex items-center gap-4 p-4 border-2 border-black rounded retro-button">
							<img 
								src={item.image} 
								alt={item.title} 
								class="w-20 h-20 object-cover border-2 border-black rounded"
							/>
							<div class="flex-1">
								<h4 class="font-mono font-bold text-lg">{item.title}</h4>
								<p class="font-mono text-gray-600 mb-2">{item.subtitle}</p>
								<p class="font-mono font-bold text-xl">${item.price.toFixed(2)}</p>
							</div>
							<button 
								class="retro-button px-4 py-2 font-mono font-bold"
								on:click={() => addToCart(item)}
							>
								Add to Cart
							</button>
						</div>
					{/each}
				</div>
			</div>
		{:else}
			<div class="space-y-4">
				{#each newsItems as item}
					<div class="flex items-start gap-4 p-4 hover:bg-gray-50 cursor-pointer border-b border-gray-200">
						<img 
							src={item.image} 
							alt={item.title} 
							class="w-20 h-20 object-cover border-2 border-black rounded"
						/>
						<div class="flex-1">
							<h3 class="font-mono font-bold text-lg mb-2 leading-tight">
								{item.title}
							</h3>
							<div class="flex items-center gap-2 text-sm text-gray-600 font-mono">
								<span class="bg-blue-100 px-2 py-1 rounded border border-gray-300 text-blue-600 font-bold">
									{item.source}
								</span>
								<span>•</span>
								<span>{item.author}</span>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
{:else}
	<div class="retro-window flex-1 mx-4 my-4 overflow-hidden">
		<div class="bg-white p-4 h-full overflow-y-auto">
			{#if showCart}
				<div class="space-y-4">
					<h3 class="text-2xl font-bold font-mono mb-6">Your Items</h3>
					
					{#if cartItems.length === 0}
						<p class="text-gray-600 font-mono">Your cart is empty</p>
					{:else}
						{#each cartItems as item, index}
							<div class="flex items-center gap-4 p-4 border border-gray-300 rounded">
								<img src={item.image} alt={item.title} class="w-15 h-15 object-cover border border-black" />
								<div class="flex-1">
									<h4 class="font-mono font-bold">{item.title}</h4>
									<p class="font-mono text-gray-600">${item.price}</p>
								</div>
								<div class="flex items-center gap-2">
									<select class="border border-black p-1 font-mono">
										<option>1</option>
										<option>2</option>
										<option>3</option>
									</select>
									<button 
										class="bg-red-500 text-white px-2 py-1 border border-black hover:bg-red-600"
										on:click={() => removeFromCart(index)}
									>
										🗑
									</button>
								</div>
							</div>
						{/each}
						
						<div class="border-t border-gray-300 pt-4 mt-6">
							<div class="space-y-2 font-mono">
								<div class="flex justify-between">
									<span>Subtotal</span>
									<span>${cartItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}</span>
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
									<span>${cartItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}</span>
								</div>
							</div>
							<button class="w-full bg-blue-600 text-white py-3 mt-4 font-mono font-bold retro-button">
								Checkout
							</button>
						</div>
					{/if}
				</div>
			{:else if currentView === 'shop'}
				<div class="space-y-4">
					<h3 class="text-2xl font-bold font-mono mb-6">Shop</h3>
					<div class="grid gap-4">
						{#each shopItems as item}
							<div class="flex items-center gap-4 p-4 border-2 border-black rounded retro-button">
								<img 
									src={item.image} 
									alt={item.title} 
									class="w-20 h-20 object-cover border-2 border-black rounded"
								/>
								<div class="flex-1">
									<h4 class="font-mono font-bold text-lg">{item.title}</h4>
									<p class="font-mono text-gray-600 mb-2">{item.subtitle}</p>
									<p class="font-mono font-bold text-xl">${item.price.toFixed(2)}</p>
								</div>
								<button 
									class="retro-button px-4 py-2 font-mono font-bold"
									on:click={() => addToCart(item)}
								>
									Add to Cart
								</button>
							</div>
						{/each}
					</div>
				</div>
			{:else}
				<div class="space-y-4">
					{#each newsItems as item}
						<div class="flex items-start gap-4 p-4 hover:bg-gray-50 cursor-pointer border-b border-gray-200">
							<img 
								src={item.image} 
								alt={item.title} 
								class="w-20 h-20 object-cover border-2 border-black rounded"
							/>
							<div class="flex-1">
								<h3 class="font-mono font-bold text-lg mb-2 leading-tight">
									{item.title}
								</h3>
								<div class="flex items-center gap-2 text-sm text-gray-600 font-mono">
									<span class="bg-blue-100 px-2 py-1 rounded border border-gray-300 text-blue-600 font-bold">
										{item.source}
									</span>
									<span>•</span>
									<span>{item.author}</span>
								</div>
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	</div>
{/if}