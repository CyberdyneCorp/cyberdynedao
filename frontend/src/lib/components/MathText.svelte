<script lang="ts">
	// Renders a prose run with inline `\( … \)` math typeset via KaTeX and the
	// rest left as plain (XSS-safe) text. Kept on one logical line in the
	// markup so no stray whitespace text nodes break up the prose.
	import { parseInlineMath } from '$lib/utils/mathText';
	import KatexMath from './KatexMath.svelte';

	let { text }: { text: string } = $props();
</script>
{#each parseInlineMath(text) as run}{#if run.kind === 'math'}<KatexMath code={run.code} />{:else}{run.text}{/if}{/each}
