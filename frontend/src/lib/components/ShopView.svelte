<script lang="ts">
	import type { MarketplaceItem } from '$lib/types/components';
	import {
		createShopViewModel,
		getCategoryColor,
		getStatusColor,
		getStatusText,
		formatMarketplacePrice as formatPrice
	} from '$lib/viewmodels/shopViewModel';

	export let onAddToCart: ((item: MarketplaceItem) => void) | undefined = undefined;

	const vm = createShopViewModel(undefined, (item) => onAddToCart?.(item));
	const { selectedCategory, selectedItem, filteredItems } = vm;
	const { items: marketplaceItems, categories, popularItems } = vm;

	function selectItem(item: MarketplaceItem) {
		vm.selectItem(item);
	}

	function addToCart(item: MarketplaceItem) {
		vm.addToCart(item);
	}
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<!-- Header -->
	<div class="bg-gradient-to-r from-orange-600 to-red-600 p-2 border-b-2 border-black">
		<h1 class="text-lg font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-xl">🛍️</span>
			CYBERDYNE MARKETPLACE
		</h1>
		<p class="font-mono text-xs text-black">Professional services • Training materials • Software licenses</p>
	</div>

	<div class="flex-1 flex">
		<!-- Sidebar -->
		<div class="w-1/3 border-r border-gray-200 bg-gray-50 overflow-y-auto">
			<!-- Categories -->
			<div class="p-2">
				<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">Categories</h3>
				<div class="space-y-1">
					{#each categories as category}
						<button
							class="w-full text-left px-2 py-1 text-xs font-mono rounded transition-colors flex items-center gap-1.5"
							class:bg-orange-100={$selectedCategory === category.id}
							class:text-orange-700={$selectedCategory === category.id}
							class:font-bold={$selectedCategory === category.id}
							on:click={() => vm.selectCategory(category.id)}
						>
							<span>{category.icon}</span>
							<span class="flex-1">{category.name}</span>
							<span class="text-gray-500">({category.count})</span>
						</button>
					{/each}
				</div>
			</div>

			<!-- Popular Items -->
			{#if $selectedCategory === 'all'}
				<div class="p-2 border-t border-gray-200">
					<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">⭐ Popular</h3>
					<div class="space-y-1.5">
						{#each popularItems.slice(0, 4) as item}
							<div
								class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
								class:ring-2={$selectedItem?.id === item.id}
								class:ring-orange-400={$selectedItem?.id === item.id}
								on:click={() => selectItem(item)}
								on:keydown={(e) => e.key === 'Enter' && selectItem(item)}
								role="button"
								tabindex="0"
							>
								<h4 class="font-mono font-bold text-xs leading-tight mb-1">{item.title}</h4>
								<div class="flex items-center justify-between text-xs">
									<span class="px-1.5 py-0.5 rounded font-mono {getCategoryColor(item.category)}">
										{item.category}
									</span>
									<span class="text-gray-600 font-mono font-bold">{formatPrice(item.price)}</span>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Items List -->
			<div class="p-2 border-t border-gray-200">
				<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">
					{$selectedCategory === 'all' ? 'All Products' : categories.find(c => c.id === $selectedCategory)?.name}
				</h3>
				<div class="space-y-1.5">
					{#each $filteredItems.slice(0, 8) as item}
						<div
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={$selectedItem?.id === item.id}
							class:ring-orange-400={$selectedItem?.id === item.id}
							on:click={() => selectItem(item)}
							on:keydown={(e) => e.key === 'Enter' && selectItem(item)}
							role="button"
							tabindex="0"
						>
							<div class="flex items-center gap-1 mb-1">
								<h4 class="font-mono font-bold text-xs leading-tight flex-1">{item.title}</h4>
								{#if item.popular}
									<span class="text-xs">⭐</span>
								{/if}
							</div>
							<div class="flex items-center justify-between text-xs mb-0.5">
								<span class="px-1.5 py-0.5 rounded font-mono {getCategoryColor(item.category)}">
									{item.subcategory || item.category}
								</span>
								<span class="px-1.5 py-0.5 rounded font-mono {getStatusColor(item.status)}">
									{getStatusText(item.status)}
								</span>
							</div>
							<div class="flex items-center justify-between text-xs">
								<span class="text-gray-600 font-mono">{item.duration || 'Custom'}</span>
								<span class="text-gray-800 font-mono font-bold">{formatPrice(item.price)}</span>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<!-- Main Content -->
		<div class="flex-1 overflow-y-auto">
			{#if $selectedItem}
				<div class="p-3">
					<div class="flex items-start gap-2 mb-3">
						<img
							src={$selectedItem.image}
							alt={$selectedItem.title}
							class="w-16 h-16 object-cover rounded border border-gray-200"
						/>
						<div class="flex-1">
							<div class="flex items-center gap-2 mb-1">
								<h2 class="text-lg font-bold font-mono text-gray-800">{$selectedItem.title}</h2>
								{#if $selectedItem.popular}
									<span class="text-lg">⭐</span>
								{/if}
							</div>
							<div class="flex items-center gap-2 mb-2">
								<span class="text-xs px-2 py-0.5 rounded font-mono {getCategoryColor($selectedItem.category)}">
									{$selectedItem.subcategory || $selectedItem.category}
								</span>
								<span class="text-xs px-2 py-0.5 rounded font-mono {getStatusColor($selectedItem.status)}">
									{getStatusText($selectedItem.status)}
								</span>
								{#if $selectedItem.duration}
									<span class="text-xs text-gray-600 font-mono">⏱️ {$selectedItem.duration}</span>
								{/if}
							</div>
							<p class="text-sm text-gray-700 leading-relaxed">{$selectedItem.description}</p>
						</div>
					</div>

					<div class="bg-gray-50 rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">✨ Features Included</h3>
						<div class="grid grid-cols-2 gap-1">
							{#each $selectedItem.features as feature}
								<div class="flex items-center gap-1 text-xs">
									<span class="text-green-500">✓</span>
									<span class="font-mono">{feature}</span>
								</div>
							{/each}
						</div>
					</div>

					<div class="bg-orange-50 rounded border border-orange-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">💰 Pricing</h3>
						<div class="flex items-center gap-4">
							<div>
								<span class="text-2xl font-bold font-mono text-orange-600">${$selectedItem.price.toLocaleString()}</span>
								{#if $selectedItem.duration}
									<span class="text-xs text-gray-600 font-mono">/ {$selectedItem.duration}</span>
								{/if}
							</div>
							{#if $selectedItem.category === 'Services'}
								<div class="text-xs text-gray-600 font-mono">
									<p>• Custom quote based on requirements</p>
									<p>• 50% upfront, 50% on completion</p>
								</div>
							{:else if $selectedItem.category === 'Licenses'}
								<div class="text-xs text-gray-600 font-mono">
									<p>• Annual subscription</p>
									<p>• Full access and updates included</p>
								</div>
							{:else}
								<div class="text-xs text-gray-600 font-mono">
									<p>• Lifetime access</p>
									<p>• All future updates included</p>
								</div>
							{/if}
						</div>
					</div>

					<div class="flex gap-2">
						<button
							class="bg-orange-600 text-white px-4 py-1.5 rounded font-mono text-xs font-bold hover:bg-orange-700 transition-colors"
							class:opacity-50={$selectedItem.status === 'coming-soon'}
							class:cursor-not-allowed={$selectedItem.status === 'coming-soon'}
							disabled={$selectedItem.status === 'coming-soon'}
							on:click={() => $selectedItem && addToCart($selectedItem)}
						>
							{$selectedItem.status === 'coming-soon' ? 'Coming Soon' : 'Add to Cart'}
						</button>
						<button class="border border-gray-300 text-gray-700 px-4 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							💬 Contact Sales
						</button>
						<button class="border border-gray-300 text-gray-700 px-4 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							❤️ Wishlist
						</button>
					</div>
				</div>
			{:else}
				<div class="p-3 text-center">
					<div class="text-3xl mb-2">🛍️</div>
					<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">Cyberdyne Marketplace</h2>
					<p class="text-sm text-gray-600 font-mono mb-4">Discover professional services, training materials, and software licenses for Web3 development.</p>

					<div class="grid grid-cols-3 gap-2">
						<div class="bg-blue-50 rounded border border-blue-200 p-2">
							<div class="text-lg mb-1">⚙️</div>
							<h3 class="font-mono font-bold text-xs">Services</h3>
							<p class="text-xs text-gray-600">Custom development</p>
						</div>
						<div class="bg-green-50 rounded border border-green-200 p-2">
							<div class="text-lg mb-1">📚</div>
							<h3 class="font-mono font-bold text-xs">Training</h3>
							<p class="text-xs text-gray-600">Learn & grow</p>
						</div>
						<div class="bg-purple-50 rounded border border-purple-200 p-2">
							<div class="text-lg mb-1">🔑</div>
							<h3 class="font-mono font-bold text-xs">Licenses</h3>
							<p class="text-xs text-gray-600">Software access</p>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>
