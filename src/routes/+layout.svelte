<script lang="ts">
	// Load polyfills first before any other imports
	import '$lib/polyfills';
	
	// Use favicon from static assets
	import '../app.css';
    import TopBar from '$lib/components/TopBar.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href="/assets/favicon.svg" />
	<title>CyberdyneCorp</title>
</svelte:head>

<TopBar />
<div class="pixel-dot w-screen h-screen bg-retro-bg pt-12">
    {@render children?.()}
    </div>
