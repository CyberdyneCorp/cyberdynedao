<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href="/assets/favicon.svg" />
	<title>CyberdyneCorp</title>
</svelte:head>

{@render children?.()}
