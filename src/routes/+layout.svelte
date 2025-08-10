<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import '../app.css';
    import TopBar from '$lib/components/TopBar.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>CyberdyneCorp</title>
</svelte:head>

<TopBar />
<div class="pixel-dot w-screen h-screen bg-retro-bg pt-12">
    {@render children?.()}
    </div>
