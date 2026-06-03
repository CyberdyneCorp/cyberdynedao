<script lang="ts">
	import '../app.css';
	import 'highlight.js/styles/github-dark.css'; // dark syntax-highlighting theme
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href="/assets/favicon.svg" />
	<title>CyberdyneCorp</title>
</svelte:head>

{@render children?.()}
