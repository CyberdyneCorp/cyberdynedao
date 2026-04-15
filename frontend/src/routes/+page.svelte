<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import {
		DesktopGrid,
		DesktopIcon,
		RetroWindow,
		Taskbar,
		StartMenu
	} from '@cyberdynecorp/svelte-ui-core';
	import {
		windows,
		createWindow,
		closeWindow,
		bringToFront,
		closeAllWindows,
		toggleWindowSlide
	} from '$lib/stores/windowStore';
	import { navItems, viewMap } from '$lib/constants/navigation';
	import { CYBERDYNE_ASCII_LOGO } from '$lib/constants/asciiLogo';
	import type { MarketplaceItem } from '$lib/types/components';
	import { cart, marketplaceItemToCartItem } from '$lib/viewmodels/cartViewModel';
	import ViewRouter from '$lib/components/ViewRouter.svelte';
	import Web3Wallet from '$lib/components/Web3Wallet.svelte';
	import { isMobileDevice } from '$lib/utils/mobileDetection';

	let cartCount = 0;
	const unsubCart = cart.count.subscribe((v) => (cartCount = v));

	let isMobile = false;
	let startOpen = false;

	function addToCart(item: MarketplaceItem) {
		cart.addItem(marketplaceItemToCartItem(item));
	}

	function openWindowFor(name: string) {
		const view = viewMap[name] || name.toLowerCase();
		createWindow(view as any, name);
	}

	function handleDesktopBgClick(e: MouseEvent) {
		const target = e.target as HTMLElement;
		if (target.closest('[data-retro-window]') || target.closest('button')) return;
		if ($windows.length > 0) toggleWindowSlide();
	}

	const startMenuItems = [
		{ id: 'team', label: 'Our Team', icon: '👥' },
		{ id: 'terminal', label: 'Terminal', icon: '💻' },
		{ id: 'close-all', label: 'Close All Windows', icon: '❌' }
	];

	function onStartSelect(id: string) {
		startOpen = false;
		if (id === 'terminal') createWindow('terminal', 'Terminal');
		else if (id === 'team') openWindowFor('Team');
		else if (id === 'close-all') closeAllWindows();
	}

	$: taskbarItems = $windows.map((w) => ({
		id: w.id,
		label: w.title,
		active: !w.minimized,
		icon: undefined as string | undefined
	}));

	function onTaskbarItemClick(id: string) {
		bringToFront(id);
	}

	onMount(() => {
		isMobile = isMobileDevice();
		const onResize = () => (isMobile = isMobileDevice());
		window.addEventListener('resize', onResize);
		return () => window.removeEventListener('resize', onResize);
	});

	onDestroy(() => unsubCart?.());
</script>

<svelte:head>
	<title>CyberdyneCorp</title>
	<link rel="icon" href="/assets/favicon.svg" />
</svelte:head>

<div class="cyberdyne-retro-shell flex flex-col h-screen w-screen overflow-hidden">
	<!-- Top taskbar: Start button + wallet -->
	<header
		class="retro-topbar flex items-center justify-between px-3 py-2 border-b-4 border-black"
		style="background: var(--retro-taskbar-gradient, linear-gradient(to right,#1e3a8a,#3b82f6));"
	>
		<StartMenu
			label="Start"
			header="Cyberdyne"
			items={startMenuItems}
			bind:open={startOpen}
			onItemSelect={onStartSelect}
		/>
		<div class="w-48 sm:w-32"><Web3Wallet /></div>
	</header>

	<!-- Desktop area -->
	<main class="relative flex-1 overflow-hidden" aria-label="Desktop" style="background:#4338ca;">
		<!-- Animated retro background (grid + glow + ASCII logo + digital rain) -->
		<div class="pointer-events-none absolute inset-0 z-0">
			<div class="cyber-grid"></div>
			<div class="glow-particle glow-1"></div>
			<div class="glow-particle glow-2"></div>
			<div class="glow-particle glow-3"></div>
			<div class="digital-rain rain-1"></div>
			<div class="digital-rain rain-2"></div>
			<div class="ascii-logo">
				<pre class="logo-text">{CYBERDYNE_ASCII_LOGO}</pre>
			</div>
		</div>

		<!-- Background click handler (transparent, covers desktop) -->
		<div
			class="absolute inset-0 z-[1]"
			on:click={handleDesktopBgClick}
			on:keydown={(e) => {
				if (e.key === 'Enter' || e.key === ' ') {
					e.preventDefault();
					if ($windows.length > 0) toggleWindowSlide();
				}
			}}
			role="button"
			tabindex="0"
			aria-label="Desktop background"
		></div>

		<!-- Left-side app launcher grid -->
		<div class="absolute left-4 top-4 z-10 w-[min(420px,50vw)]">
			<DesktopGrid columns={2} gap={16} align="start" side="left" ariaLabel="Applications">
				{#each navItems as item}
					<DesktopIcon
						label={isMobile && item.mobileLabel ? item.mobileLabel : item.name}
						iconSrc={item.icon}
						onActivate={() => openWindowFor(item.name)}
					/>
				{/each}
			</DesktopGrid>
		</div>

		<!-- Cart icon top-right -->
		<div style="position:absolute; top:16px; right:16px; z-index:10;">
			<DesktopIcon
				label={`Your Bag${cartCount > 0 ? ` (${cartCount})` : ''}`}
				iconSrc="/assets/cart.svg"
				badge={cartCount > 0 ? cartCount : undefined}
				onActivate={() => createWindow('cart', `Your Bag (${cartCount})`)}
			/>
		</div>

		<!-- Windows: RetroWindow self-positions via fixed + x/y; DOM order = stacking -->
		{#each [...$windows].sort((a, b) => a.zIndex - b.zIndex) as w (w.id)}
			{#if !w.isSlideHidden && !w.minimized}
				<RetroWindow
					title={w.title}
					open
					x={w.x}
					y={w.y}
					width={w.width}
					height={w.height}
					draggable
					resizable
					onClose={() => closeWindow(w.id)}
					onFocus={() => bringToFront(w.id)}
				>
					<ViewRouter content={w.content} onAddToCart={addToCart} {isMobile} />
				</RetroWindow>
			{/if}
		{/each}
	</main>

	<!-- Bottom taskbar showing open windows -->
	{#if taskbarItems.length > 0}
		<footer class="retro-bottom-taskbar border-t-2 border-black">
			<Taskbar items={taskbarItems} position="bottom" onItemClick={onTaskbarItemClick} ariaLabel="Open windows" />
		</footer>
	{/if}
</div>

