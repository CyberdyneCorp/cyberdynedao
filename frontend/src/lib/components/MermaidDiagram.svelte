<script lang="ts">
	// Renders a Mermaid diagram from its source. mermaid is a heavy dep, so
	// it's dynamically imported on first render (keeps it out of the main
	// bundle). On a parse/render error we fall back to the raw definition so
	// the user still sees something useful. A "download .mmd" button exports
	// the source for import elsewhere.

	let { code }: { code: string } = $props();

	let host = $state<HTMLDivElement | null>(null);
	let errored = $state<boolean>(false);

	// Stable-ish unique id per instance for mermaid.render.
	const renderId = `mmd-${Math.random().toString(36).slice(2, 10)}`;

	$effect(() => {
		const source = code;
		const el = host;
		if (!el) return;
		let cancelled = false;
		errored = false;
		(async () => {
			try {
				const mermaid = (await import('mermaid')).default;
				mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'dark' });
				const { svg } = await mermaid.render(renderId, source);
				if (!cancelled && host) host.innerHTML = svg;
			} catch {
				if (!cancelled) {
					errored = true;
					if (host) host.innerHTML = '';
				}
			}
		})();
		return () => {
			cancelled = true;
		};
	});

	function downloadMmd() {
		const blob = new Blob([code], { type: 'text/vnd.mermaid' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = 'diagram.mmd';
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		setTimeout(() => URL.revokeObjectURL(url), 30_000);
	}
</script>

<figure class="mermaid-fig">
	<div class="mermaid-fig__canvas" bind:this={host} aria-label="Mermaid diagram"></div>
	{#if errored}
		<pre class="mermaid-fig__raw">{code}</pre>
	{/if}
	<figcaption class="mermaid-fig__bar">
		<span>{errored ? '⚠ Could not render — showing source' : '🧜 Mermaid diagram'}</span>
		<button type="button" class="mermaid-fig__dl" onclick={downloadMmd}>⬇ .mmd</button>
	</figcaption>
</figure>

<style>
	.mermaid-fig {
		margin: 8px 0 0;
		background: #0f172a;
		border: 2px solid #334155;
		border-left: 6px solid #a78bfa;
		padding: 10px;
	}
	.mermaid-fig__canvas {
		display: flex;
		justify-content: center;
		overflow-x: auto;
	}
	.mermaid-fig__canvas :global(svg) {
		max-width: 100%;
		height: auto;
	}
	.mermaid-fig__raw {
		margin: 0;
		padding: 8px;
		background: #050913;
		color: #c4b5fd;
		font-size: 0.78rem;
		white-space: pre-wrap;
		overflow-x: auto;
	}
	.mermaid-fig__bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 8px;
		font-size: 0.7rem;
		color: #94a3b8;
	}
	.mermaid-fig__dl {
		background: transparent;
		border: 1px solid #a78bfa;
		color: #c4b5fd;
		font-family: inherit;
		font-size: 0.7rem;
		padding: 2px 8px;
		cursor: pointer;
	}
	.mermaid-fig__dl:hover {
		background: rgba(167, 139, 250, 0.15);
	}
</style>
