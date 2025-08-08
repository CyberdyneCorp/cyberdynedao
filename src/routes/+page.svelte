<script lang="ts">
	import Window from '$lib/components/Window.svelte';
	import { windows, createWindow } from '$lib/stores/windowStore';
	
	import { navItems, viewMap, type NavItem } from '$lib/constants/navigation';

	let cartItems: any[] = [];
	
	function addToCart(item: any) {
		cartItems = [...cartItems, item];
	}
	
	function handleItemClick(item: NavItem) {
		const view = viewMap[item.name] || item.name.toLowerCase();
		createWindow(view, item.name);
	}
	
	$: cartCount = cartItems.length;
</script>

<div class="flex flex-col h-screen">
    <div class="flex-1 relative bg-retro-bg">
		<!-- Desktop Icons positioned on main area -->
		<div class="absolute left-8 top-1/15 z-10">
			<div class="grid grid-cols-2" style="gap: 50px 70px;">
				{#each navItems as item}
					<div class="flex flex-col items-center">
						<button
							class="sidebar-icon flex items-center justify-center cursor-pointer"
							on:click={() => handleItemClick(item)}
							title={item.name}
						>
							<img src={item.icon} alt={item.name} class="w-8 h-8" />
						</button>
						<span class="nav-label text-white text-xs font-mono text-center px-2 py-0.5 rounded mt-4">
							{item.name}
						</span>
					</div>
				{/each}
			</div>
		</div>
		
		<!-- Cart icon in right corner at same height as other icons -->
		<div class="absolute right-1/10 top-1/15 z-20">
			<div class="flex flex-col items-center">
				<button
					class="sidebar-icon flex items-center justify-center cursor-pointer relative"
					on:click={() => createWindow('cart', `Your Bag (${cartCount})`)}
					title="Your Bag"
				>
					<img src="/assets/cart.svg" alt="Cart" class="w-8 h-8" />
					{#if cartCount > 0}
						<div class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
							{cartCount}
						</div>
					{/if}
				</button>
				<span class="nav-label text-white text-xs font-mono text-center px-2 py-0.5 rounded mt-4">
					Your Bag {cartCount > 0 ? `(${cartCount})` : ''}
				</span>
			</div>
		</div>
		
		<!-- Windows -->
		{#each $windows as window (window.id)}
			<Window 
				{window}
				bind:cartItems
				onAddToCart={addToCart}
			/>
		{/each}
	</div>
</div>
