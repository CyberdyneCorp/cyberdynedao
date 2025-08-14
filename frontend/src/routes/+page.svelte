<script lang="ts">
	import Window from '$lib/components/Window.svelte';
	import { windows, createWindow, toggleWindowSlide } from '$lib/stores/windowStore';
	import { navItems } from '$lib/constants/navigation';
	import { handleItemClick } from '$lib/utils/navigationHelpers';
	import { CYBERDYNE_ASCII_LOGO } from '$lib/constants/asciiLogo';
	import type { CartItem } from '$lib/types/cart';

	let cartItems: CartItem[] = [];
	
	function addToCart(item: CartItem) {
		cartItems = [...cartItems, item];
	}

	function handleBackgroundClick(e: MouseEvent) {
		// Only trigger if clicking on the background, not on windows or icons
		const target = e.target as HTMLElement;
		if (target.closest('.retro-window') || target.closest('.sidebar-icon') || target.closest('button')) {
			return;
		}
		
		// Only toggle if there are windows open
		if ($windows.length > 0) {
			toggleWindowSlide();
		}
	}

	function handleBackgroundKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			if ($windows.length > 0) {
				toggleWindowSlide();
			}
		}
	}
	
	$: cartCount = cartItems.length;
</script>

<div class="flex flex-col h-screen">
    <div 
		class="flex-1 relative bg-retro-bg overflow-hidden" 
		on:click={handleBackgroundClick}
		on:keydown={handleBackgroundKeyDown}
		role="button"
		tabindex="0"
		aria-label="Desktop background - click to toggle window slide"
	>
		<!-- Enhanced Futuristic Background Animation -->
		<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; opacity: 1.2;">
			
			<!-- Grid Pattern -->
			<div class="cyber-grid" style="z-index: 1;"></div>
			
			<!-- Floating Particles -->
			<div class="glow-particle glow-1" style="z-index: 2;"></div>
			<div class="glow-particle glow-2" style="z-index: 2;"></div>
			<div class="glow-particle glow-3" style="z-index: 2;"></div>
			
			<!-- Digital Rain -->
			<div class="digital-rain rain-1" style="z-index: 2;"></div>
			<div class="digital-rain rain-2" style="z-index: 2;"></div>
			
			<!-- ASCII Cyberdyne Logo with Wavy Glow -->
			<div class="ascii-logo" style="z-index: 2;">
				<pre class="logo-text">{CYBERDYNE_ASCII_LOGO}</pre>
			</div>
		</div>
		<!-- Desktop Icons positioned on main area -->
		<div class="absolute left-8 z-10 sm:left-4 main-icons">
			<div class="icon-grid grid grid-cols-2 sm:grid-cols-3">
				{#each navItems as item}
					<div class="flex flex-col items-center">
						<button
							class="sidebar-icon flex items-center justify-center cursor-pointer"
							on:click={() => handleItemClick(item)}
							title={item.name}
						>
							<img src={item.icon} alt={item.name} class="w-24 h-24 md:w-24 md:h-24 sm:w-20 sm:h-20" />
						</button>
						<span class="nav-label text-white text-base md:text-base sm:text-xs font-mono text-center px-2 py-0.5 sm:px-1 sm:py-0 rounded mt-4 sm:mt-1 break-words max-w-20 sm:max-w-16">
							<span class="sm:hidden">{item.name}</span>
							<span class="hidden sm:inline">{item.mobileLabel || item.name}</span>
						</span>
					</div>
				{/each}
			</div>
		</div>
		
		<!-- Cart icon in right corner at same height as other icons -->
		<div class="absolute right-1/10 z-20 sm:right-4 cart-icon">
			<div class="flex flex-col items-center">
				<button
					class="sidebar-icon flex items-center justify-center cursor-pointer relative"
					on:click={() => createWindow('cart', `Your Bag (${cartCount})`)}
					title="Your Bag"
				>
					<img src="/assets/cart.svg" alt="Cart" class="w-24 h-24 md:w-24 md:h-24 sm:w-20 sm:h-20" />
					{#if cartCount > 0}
						<div class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
							{cartCount}
						</div>
					{/if}
				</button>
				<span class="nav-label text-white text-base md:text-base sm:text-xs font-mono text-center px-2 py-0.5 sm:px-1 sm:py-0 rounded mt-4 sm:mt-1 break-words max-w-20 sm:max-w-16">
					<span class="sm:hidden">Your Bag {cartCount > 0 ? `(${cartCount})` : ''}</span>
					<span class="hidden sm:inline">Bag {cartCount > 0 ? `(${cartCount})` : ''}</span>
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

<!-- Background animations CSS moved to /lib/styles/backgroundAnimations.css -->

<style>
	/* Desktop positioning adjustments */
	.main-icons {
		top: 120px;
	}
	
	.cart-icon {
		top: 120px;
	}
	
	/* Mobile responsive styles for main page */
	@media (max-width: 768px) {
		.main-icons {
			position: absolute !important;
			left: 16px !important;
			right: auto !important;
			top: 120px !important;
			display: flex !important;
			justify-content: flex-start !important;
			align-items: flex-start !important;
			flex-direction: column !important;
			gap: 16px !important;
		}
		
		.cart-icon {
			position: absolute !important;
			right: 16px !important;
			left: auto !important;
			top: 120px !important;
			display: flex !important;
			justify-content: flex-end !important;
			align-items: flex-start !important;
			flex-direction: column !important;
		}
		
		.icon-grid {
			grid-template-columns: repeat(2, 1fr) !important;
			gap: 24px 20px !important;
			width: auto !important;
			max-width: 320px !important;
			justify-items: flex-start !important;
			align-items: start !important;
		}
		
		.icon-grid > div {
			display: flex !important;
			flex-direction: column !important;
			align-items: center !important;
			justify-content: flex-start !important;
			width: 100% !important;
		}
		
		.sidebar-icon {
			width: 60px !important;
			height: 60px !important;
		}
		
		.sidebar-icon img {
			width: 44px !important;
			height: 44px !important;
		}
		
		.nav-label {
			font-size: 10px !important;
			margin-top: 4px !important;
			max-width: 60px !important;
			display: block !important;
			opacity: 1 !important;
			visibility: visible !important;
		}
		
		.ascii-logo {
			display: none !important;
		}
		
		.cyber-grid {
			opacity: 0.3 !important;
		}
		
		.glow-particle {
			display: none !important;
		}
		
		.digital-rain {
			display: none !important;
		}
	}
	
	@media (max-width: 480px) {
		.main-icons {
			left: 12px !important;
			top: 100px !important;
		}
		
		.cart-icon {
			right: 12px !important;
			top: 100px !important;
		}
		
		.icon-grid {
			grid-template-columns: repeat(2, 1fr) !important;
			gap: 20px 16px !important;
			max-width: 280px !important;
		}
		
		.sidebar-icon {
			width: 52px !important;
			height: 52px !important;
		}
		
		.sidebar-icon img {
			width: 36px !important;
			height: 36px !important;
		}
		
		.nav-label {
			font-size: 9px !important;
			max-width: 50px !important;
			display: block !important;
			opacity: 1 !important;
			visibility: visible !important;
		}
	}
	
	/* Touch device optimizations */
	@media (hover: none) and (pointer: coarse) {
		.sidebar-icon {
			min-width: 44px !important;
			min-height: 44px !important;
		}
		
		.sidebar-icon:hover {
			transform: none !important;
		}
	}
	
	/* Ensure nav-label is always visible */
	.nav-label {
		display: block !important;
		visibility: visible !important;
		opacity: 1 !important;
	}
	
	/* Mobile-specific nav-label overrides */
	@media (max-width: 768px) {
		.nav-label {
			display: block !important;
			visibility: visible !important;
			opacity: 1 !important;
			background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
			border: 1px solid #000 !important;
			box-shadow: 1px 1px 0px rgba(0,0,0,0.3) !important;
			color: white !important;
			font-weight: bold !important;
		}
		
		/* Override any conflicting styles */
		.desktop-icons .nav-label {
			display: block !important;
			visibility: visible !important;
			opacity: 1 !important;
		}
		
		.icon-grid .nav-label {
			display: block !important;
			visibility: visible !important;
			opacity: 1 !important;
		}
	}
	
	@media (max-width: 480px) {
		.nav-label {
			font-size: 9px !important;
			max-width: 50px !important;
			padding: 1px 3px !important;
		}
		
		/* Override any conflicting styles */
		.desktop-icons .nav-label {
			display: block !important;
			visibility: visible !important;
			opacity: 1 !important;
		}
		
		.icon-grid .nav-label {
			display: block !important;
			visibility: visible !important;
			opacity: 1 !important;
		}
	}
</style>
