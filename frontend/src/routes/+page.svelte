<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import {
		DesktopGrid,
		DesktopIcon,
		RetroWindow,
		Taskbar,
		StartMenu,
		ErrorBoundary
	} from '@cyberdynecorp/svelte-ui-core';
	import { closeWindow, bringToFront, toggleWindowSlide } from '$lib/stores/windowStore';
	import { navItems } from '$lib/constants/navigation';
	import { CYBERDYNE_ASCII_LOGO } from '$lib/constants/asciiLogo';
	import { createShellViewModel } from '$lib/viewmodels/shellViewModel';
	import ViewRouter from '$lib/components/ViewRouter.svelte';
	import Web3Wallet from '$lib/components/Web3Wallet.svelte';
	import { isMobileDevice } from '$lib/utils/mobileDetection';

	const shell = createShellViewModel();
	const { windows, cartCount, startMenuItems } = shell;

	let cartCountValue = 0;
	const unsubCart = cartCount.subscribe((v) => (cartCountValue = v));

	let isMobile = false;
	let startOpen = false;

	$: taskbarItems = $windows.map((w) => ({
		id: w.id,
		label: w.title,
		active: !w.minimized,
		icon: undefined as string | undefined
	}));

	function onStartSelect(id: string) {
		startOpen = false;
		shell.handleStartSelect(id);
	}

	function onSlideToggleKey(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			if ($windows.length > 0) toggleWindowSlide();
		}
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
		class="retro-topbar flex items-center justify-between px-6 py-3 border-b-4 border-black gap-3"
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
		<!-- Dedicated accessible slide toggle covering the empty desktop -->
		<button
			type="button"
			class="absolute inset-0 w-full h-full bg-transparent border-0 p-0 m-0 cursor-default"
			aria-label="Toggle window slide"
			on:click={shell.handleDesktopBgClick}
			on:keydown={onSlideToggleKey}
			style="z-index:1;"
		></button>

		<!-- Animated retro background (grid + glow + ASCII logo + digital rain) -->
		<div style="position:absolute; inset:0; pointer-events:none; z-index:0;">
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

		<!-- Left-side app launcher grid -->
		<div class="absolute left-4 top-4 z-10 w-[min(420px,60vw)]">
			<DesktopGrid
				columns={isMobile ? 1 : 2}
				gap={isMobile ? 10 : 16}
				align="start"
				side="left"
				ariaLabel="Applications"
			>
				{#each navItems as item}
					<DesktopIcon
						label={isMobile && item.mobileLabel ? item.mobileLabel : item.name}
						iconSrc={item.icon}
						onActivate={() => shell.openWindowByNavItem(item)}
					/>
				{/each}
			</DesktopGrid>
		</div>

		<!-- Cart icon top-right -->
		<div style="position:absolute; top:16px; right:16px; z-index:10;">
			<DesktopIcon
				label={`Your Bag${cartCountValue > 0 ? ` (${cartCountValue})` : ''}`}
				iconSrc="/assets/cart.svg"
				badge={cartCountValue > 0 ? cartCountValue : undefined}
				onActivate={() => shell.openCart()}
			/>
		</div>

		<!-- Windows: each wrapped in ErrorBoundary so a broken view can't take the shell down -->
		{#each [...$windows].sort((a, b) => a.zIndex - b.zIndex) as w (w.id)}
			{#if !w.minimized}
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
					<ErrorBoundary>
						<ViewRouter content={w.content} onAddToCart={shell.addToCart} {isMobile} />
					</ErrorBoundary>
				</RetroWindow>
			{/if}
		{/each}
	</main>

	<!-- Bottom taskbar showing open windows -->
	{#if taskbarItems.length > 0}
		<footer class="retro-bottom-taskbar border-t-2 border-black">
			<Taskbar items={taskbarItems} position="bottom" onItemClick={bringToFront} ariaLabel="Open windows" />
		</footer>
	{/if}
</div>
