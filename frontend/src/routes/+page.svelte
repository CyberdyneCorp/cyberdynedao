<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import {
		CRTBackground,
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
		{ id: 'team', label: 'Our Team', icon: '/assets/the_team.svg' },
		{ id: 'terminal', label: 'Terminal', icon: '/assets/icon_terminal.svg' },
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
		<div class="relative">
			<button
				class="retro-start-btn font-mono font-bold text-white px-3 py-1 border-2 border-black"
				style="background: rgba(255,255,255,0.18);"
				on:click={() => (startOpen = !startOpen)}
				aria-expanded={startOpen}
			>
				<img src="/assets/icon_menu.svg" alt="" class="inline w-5 h-5 mr-2 align-middle" />
				Start {startOpen ? '▼' : '▶'}
			</button>
			{#if startOpen}
				<div class="absolute left-0 top-full mt-1 z-50">
					<StartMenu
						label="Menu"
						header="Cyberdyne"
						items={startMenuItems}
						open={startOpen}
						onItemSelect={onStartSelect}
					/>
				</div>
			{/if}
		</div>
		<div class="w-48 sm:w-32"><Web3Wallet /></div>
	</header>

	<!-- Desktop area -->
	<main class="relative flex-1 overflow-hidden" aria-label="Desktop">
		<!-- CRT background layer -->
		<div class="absolute inset-0 z-0">
			<CRTBackground color="#4338ca" showGrid showScanlines fullScreen>
				{''}
			</CRTBackground>
		</div>

		<!-- Background click handler + decorations -->
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
		>
			<div class="pointer-events-none absolute inset-0">
				<div class="ascii-logo">
					<pre class="logo-text">{CYBERDYNE_ASCII_LOGO}</pre>
				</div>
				<div class="glow-particle glow-1"></div>
				<div class="glow-particle glow-2"></div>
				<div class="glow-particle glow-3"></div>
			</div>
		</div>

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
		<div class="absolute right-4 top-4 z-10">
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

<style>
	.ascii-logo {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		pointer-events: none;
		opacity: 0.35;
	}
	.logo-text {
		color: rgba(255, 255, 255, 0.85);
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		font-size: 10px;
		line-height: 1.1;
		white-space: pre;
		margin: 0;
	}
	@media (max-width: 768px) {
		.ascii-logo { display: none; }
	}
</style>
