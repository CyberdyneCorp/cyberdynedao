<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>Retro Terminal</title>
</svelte:head>

<div class="pixel-dot w-screen h-screen bg-retro-bg">
	{@render children?.()}
</div>
