<script lang="ts">
	import '../app.css';
	import 'highlight.js/styles/github.css'; // light syntax-highlighting theme
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href="/assets/favicon.svg" />
	<title>CyberdyneCorp</title>
</svelte:head>

{@render children?.()}
