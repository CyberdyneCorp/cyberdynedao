<script lang="ts">
	import { highlight } from '$lib/utils/highlight';

	let {
		value = $bindable(''),
		language = 'matlab',
		ariaLabel = 'Code',
		minHeight = '8rem'
	}: {
		value?: string;
		language?: string;
		ariaLabel?: string;
		minHeight?: string;
	} = $props();

	let ta = $state<HTMLTextAreaElement | null>(null);
	let pre = $state<HTMLPreElement | null>(null);

	// hljs output. Trailing newline keeps the highlight layer's height in
	// sync with the textarea when the code ends on a blank line.
	const html = $derived(highlight(value, language) + '\n');

	// Mirror the textarea's scroll onto the (non-interactive) highlight layer.
	function syncScroll(): void {
		if (ta && pre) {
			pre.scrollTop = ta.scrollTop;
			pre.scrollLeft = ta.scrollLeft;
		}
	}

	// Tab inserts two spaces instead of moving focus.
	function onKeydown(e: KeyboardEvent): void {
		if (e.key !== 'Tab' || !ta) return;
		e.preventDefault();
		const start = ta.selectionStart;
		const end = ta.selectionEnd;
		value = value.slice(0, start) + '  ' + value.slice(end);
		queueMicrotask(() => ta && (ta.selectionStart = ta.selectionEnd = start + 2));
	}
</script>

<div class="ce" style="--ce-min-h:{minHeight}">
	{#if language}<span class="ce__lang">{language}</span>{/if}
	<pre class="ce__layer hljs" aria-hidden="true" bind:this={pre}><code>{@html html}</code></pre>
	<textarea
		class="ce__input"
		bind:this={ta}
		bind:value
		onscroll={syncScroll}
		onkeydown={onKeydown}
		spellcheck="false"
		autocapitalize="off"
		autocomplete="off"
		aria-label={ariaLabel}
	></textarea>
</div>

<style>
	.ce {
		position: relative;
		border: 2px solid #000000;
		border-radius: 6px;
		overflow: hidden;
		background: #0d1117; /* matches the github-dark hljs theme surface */
	}
	.ce__lang {
		position: absolute;
		top: 0;
		right: 0;
		z-index: 2;
		font-family: ui-monospace, monospace;
		font-size: 0.6rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: #8b949e;
		background: rgba(255, 255, 255, 0.06);
		border-left: 1px solid rgba(255, 255, 255, 0.12);
		border-bottom: 1px solid rgba(255, 255, 255, 0.12);
		border-bottom-left-radius: 4px;
		padding: 0.1rem 0.4rem;
		pointer-events: none;
	}
	/* The highlight layer and the textarea must render identically so the
	   caret/text line up exactly. */
	.ce__layer,
	.ce__input {
		margin: 0;
		padding: 0.7rem;
		border: 0;
		box-sizing: border-box;
		width: 100%;
		min-height: var(--ce-min-h);
		font-family: ui-monospace, 'JetBrains Mono', monospace;
		font-size: 0.8rem;
		line-height: 1.5;
		tab-size: 2;
		white-space: pre;
		overflow: auto;
	}
	.ce__layer {
		position: absolute;
		inset: 0;
		z-index: 0;
		pointer-events: none;
		overflow: hidden;
		color: #c9d1d9; /* fallback if the hljs theme is slow to load */
		background: #0d1117;
	}
	.ce__layer code {
		font: inherit;
	}
	.ce__input {
		position: relative;
		z-index: 1;
		background: transparent;
		color: transparent;
		caret-color: #e6edf3;
		resize: vertical;
	}
	.ce__input::selection {
		background: rgba(56, 139, 253, 0.4);
	}
</style>
