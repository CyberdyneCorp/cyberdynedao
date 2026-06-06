<script lang="ts">
	// Renders the agent's prose as Markdown — headings, lists, bold/italic,
	// inline code, links, and inline math — using a tiny dependency-free
	// parser. All text is rendered as escaped Svelte content (no {@html});
	// links are restricted to http(s)/mailto by the parser.
	import { parseBlocks, parseInline } from '$lib/utils/markdown';
	import KatexMath from './KatexMath.svelte';

	let { source }: { source: string } = $props();
</script>

{#snippet inline(text: string)}
	{#each parseInline(text) as run}{#if run.kind === 'bold'}<strong>{run.text}</strong
			>{:else if run.kind === 'italic'}<em>{run.text}</em
			>{:else if run.kind === 'code'}<code class="md-code">{run.text}</code
			>{:else if run.kind === 'link'}<a href={run.href} target="_blank" rel="noopener noreferrer"
				>{run.text}</a
			>{:else if run.kind === 'math'}<KatexMath code={run.code} />{:else}{run.text}{/if}{/each}
{/snippet}

<div class="md">
	{#each parseBlocks(source) as block}
		{#if block.kind === 'heading'}
			{#if block.level <= 2}
				<p class="md-h md-h--lg">{@render inline(block.text)}</p>
			{:else}
				<p class="md-h">{@render inline(block.text)}</p>
			{/if}
		{:else if block.kind === 'list'}
			{#if block.ordered}
				<ol class="md-list">
					{#each block.items as item}<li>{@render inline(item)}</li>{/each}
				</ol>
			{:else}
				<ul class="md-list">
					{#each block.items as item}<li>{@render inline(item)}</li>{/each}
				</ul>
			{/if}
		{:else}
			<p class="md-p">{@render inline(block.text)}</p>
		{/if}
	{/each}
</div>

<style>
	.md {
		display: flex;
		flex-direction: column;
		gap: 6px;
		font-size: 0.875rem;
		line-height: 1.55;
		color: #1f2937;
		word-break: break-word;
	}
	.md-p,
	.md-h {
		margin: 0;
	}
	.md-h {
		font-weight: 700;
		color: #111827;
	}
	.md-h--lg {
		font-size: 1.02rem;
	}
	.md-list {
		margin: 2px 0;
		padding-left: 22px;
		display: flex;
		flex-direction: column;
		gap: 3px;
	}
	.md-list li {
		padding-left: 2px;
	}
	.md-code {
		background: #ede9fe;
		color: #5b21b6;
		padding: 1px 5px;
		border-radius: 3px;
		font-family: var(--font-mono, monospace);
		font-size: 0.82em;
	}
	.md a {
		color: #6d28d9;
		text-decoration: underline;
	}
	.md a:hover {
		color: #4c1d95;
	}
</style>
