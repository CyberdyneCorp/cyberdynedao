<script lang="ts">
	// Typesets a LaTeX formula with KaTeX. katex is a heavy dep, so it's
	// dynamically imported on first render (kept out of the main bundle, like
	// MermaidDiagram). KaTeX output is trusted markup it generates itself from
	// the formula — `trust:false` (default) + `throwOnError:false` keep it
	// XSS-safe and render parse errors inline rather than throwing. On import
	// failure we fall back to the raw `\( … \)` / `\[ … \]` source.
	import 'katex/dist/katex.min.css';

	let { code, display = false }: { code: string; display?: boolean } = $props();

	let host = $state<HTMLElement | null>(null);

	$effect(() => {
		const source = code;
		const el = host;
		if (!el) return;
		let cancelled = false;
		(async () => {
			try {
				const katex = (await import('katex')).default;
				const html = katex.renderToString(source, {
					displayMode: display,
					throwOnError: false,
					output: 'html'
				});
				if (!cancelled && host) host.innerHTML = html;
			} catch {
				if (!cancelled && host) {
					host.textContent = display ? `\\[${source}\\]` : `\\(${source}\\)`;
				}
			}
		})();
		return () => {
			cancelled = true;
		};
	});
</script>

{#if display}
	<div class="katex-block" bind:this={host} aria-label="math formula"></div>
{:else}
	<span class="katex-inline" bind:this={host} aria-label="math formula"></span>
{/if}

<style>
	.katex-block {
		margin: 4px 0;
		overflow-x: auto;
		overflow-y: hidden;
		text-align: center;
	}
	.katex-inline {
		white-space: normal;
	}
</style>
