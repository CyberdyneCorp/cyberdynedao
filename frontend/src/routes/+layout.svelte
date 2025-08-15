<script lang="ts">
	import { onMount } from 'svelte';
	import { isMobileDevice } from '$lib/utils/mobileDetection';
	
	// Use favicon from static assets
	import '../app.css';
    import TopBar from '$lib/components/TopBar.svelte';

	let { children } = $props();
	let isMobile = $state(false);
	
	onMount(() => {
		isMobile = isMobileDevice();
		
		// Listen for window resize
		const handleResize = () => {
			isMobile = isMobileDevice();
		};
		
		window.addEventListener('resize', handleResize);
		
		return () => {
			window.removeEventListener('resize', handleResize);
		};
	});
</script>

<svelte:head>
	<link rel="icon" href="/assets/favicon.svg" />
	<title>CyberdyneCorp</title>
</svelte:head>

<TopBar />
<div class="pixel-dot w-screen h-screen bg-retro-bg pt-20 sm:pt-16" class:mobile={isMobile}>
    {@render children?.()}
</div>

<style>
	.mobile {
		overflow-x: hidden;
	}
	
	/* Mobile-specific layout adjustments */
	@media (max-width: 768px) {
		.mobile {
			padding-top: 16px !important;
		}
	}
	
	@media (max-width: 480px) {
		.mobile {
			padding-top: 12px !important;
		}
	}
</style>
