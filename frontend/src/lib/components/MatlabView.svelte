<script lang="ts">
	import { onDestroy, tick } from 'svelte';
	import { Badge, PixelButton, PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import { createMatlabTerminalVM, type MatlabCell } from '$lib/viewmodels/matlabTerminalViewModel.svelte';
	import { authVM } from '$lib/auth/authViewModel.svelte';

	const vm = createMatlabTerminalVM();

	let scrollEl = $state<HTMLElement | null>(null);
	let textareaEl = $state<HTMLTextAreaElement | null>(null);

	// Auto-scroll the cell log to the bottom whenever a new cell lands
	// or finishes streaming.
	const cellCount = $derived(vm.cells.length);
	$effect(() => {
		void cellCount;
		void tick().then(() => {
			if (scrollEl) scrollEl.scrollTop = scrollEl.scrollHeight;
		});
	});

	onDestroy(() => {
		vm.clearCells();
	});

	async function onSubmit(e: SubmitEvent) {
		e.preventDefault();
		await vm.submitRepl();
		textareaEl?.focus();
	}

	async function onPlot() {
		await vm.submitPlot();
		textareaEl?.focus();
	}

	function onKeydown(e: KeyboardEvent) {
		// Cmd/Ctrl+Enter → Run (matches notebook conventions). Plain
		// Enter inserts a newline so multi-line snippets stay readable.
		if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
			e.preventDefault();
			void vm.submitRepl();
		}
	}

	function badgeVariant(status: MatlabCell['status']): 'success' | 'warning' | 'danger' {
		if (status === 'ok') return 'success';
		if (status === 'running') return 'warning';
		return 'danger';
	}

	function formatElapsed(cell: MatlabCell): string {
		if (cell.finishedAt === null) return '…';
		const ms = cell.finishedAt - cell.startedAt;
		if (ms < 1000) return `${ms} ms`;
		return `${(ms / 1000).toFixed(2)} s`;
	}

	const heroStyle = '--accent: #f97316; --accent-dark: #c2410c;';
	const authReady = $derived(authVM.isRestored && authVM.isAuthenticated);
</script>

<div class="matlab" style={heroStyle}>
	<!-- Hero -->
	<header class="hero">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">📐</span>
			<h1 class="hero__title">MATLAB LLVM REPL</h1>
			<span class="hero__chip">session {vm.sessionId.slice(-6)}</span>
		</div>
		<p class="hero__tagline">
			Stateful MATLAB on a remote LLVM engine. Plots render inline. <kbd>⌘/Ctrl + Enter</kbd> to run.
		</p>
	</header>

	{#if !authReady}
		<div class="auth-banner">
			<strong>Sign in required.</strong>
			<span>The MATLAB backend uses your CyberdyneAuth session. Open the Connect menu and sign in to enable the REPL.</span>
		</div>
	{/if}

	<!-- Cell log -->
	<div class="cells" bind:this={scrollEl}>
		<PixelScrollArea maxHeight="100%" ariaLabel="MATLAB cells">
			{#if vm.cells.length === 0}
				<div class="empty">
					<p class="empty__line">% Welcome to the Cyberdyne MATLAB REPL.</p>
					<p class="empty__line">% Try one of these:</p>
					<pre class="empty__code">disp('hello, world')
A = magic(5); disp(A)
x = linspace(0, 2*pi, 200); plot(x, sin(x).*cos(2*x))</pre>
					<p class="empty__hint">Click <em>Run</em> for stdout; click <em>Plot</em> when you expect a figure.</p>
				</div>
			{/if}

			{#each vm.cells as cell (cell.id)}
				<article class="cell">
					<header class="cell__head">
						<span class="cell__no">[{cell.id}]</span>
						<span class="cell__mode">
							{cell.mode === 'plot' ? 'PLOT' : 'REPL'}{#if cell.plotFallback}<span
									class="cell__fallback"
									title="Source looked like a plot call so we transparently called /v1/plot to capture the figure"
									> → PLOT</span
								>{/if}
						</span>
						<Badge variant={badgeVariant(cell.status)} size="sm">
							{cell.status === 'running'
								? 'RUNNING'
								: cell.status === 'ok'
									? 'OK'
									: 'ERROR'}
						</Badge>
						{#if cell.timedOut}
							<Badge variant="danger" size="sm">TIMED OUT</Badge>
						{/if}
						{#if cell.truncated}
							<Badge variant="warning" size="sm">TRUNCATED</Badge>
						{/if}
						<span class="cell__elapsed">{formatElapsed(cell)}</span>
					</header>

					<pre class="cell__source">{cell.source}</pre>

					{#if cell.stdout}
						<pre class="cell__stdout">{cell.stdout}</pre>
					{/if}
					{#if cell.stderr}
						<pre class="cell__stderr">{cell.stderr}</pre>
					{/if}
					{#if cell.error}
						<pre class="cell__error">{cell.error}</pre>
					{/if}

					{#if cell.plots.length > 0}
						<div class="cell__plots">
							{#each cell.plots as plotItem, i (plotItem.url)}
								{#if plotItem.contentType.startsWith('image/')}
									<figure class="plot">
										<img src={plotItem.url} alt={`Figure ${i + 1} from cell ${cell.id}`} loading="lazy" />
										<figcaption>
											Figure {i + 1} · {(plotItem.bytes / 1024).toFixed(1)} KB · {plotItem.contentType}
										</figcaption>
									</figure>
								{:else}
									<a class="plot__download" href={plotItem.url} download>
										⬇ Artifact {i + 1} ({plotItem.contentType}, {(plotItem.bytes / 1024).toFixed(1)} KB)
									</a>
								{/if}
							{/each}
						</div>
					{/if}

					{#if cell.artifactErrors.length > 0}
						<pre class="cell__artifact-err">⚠ Some artifacts could not be downloaded:
{cell.artifactErrors.join('\n')}</pre>
					{/if}
				</article>
			{/each}
		</PixelScrollArea>
	</div>

	<!-- Input -->
	<form class="prompt" onsubmit={onSubmit}>
		<div class="prompt__head">
			<span class="prompt__caret" aria-hidden="true">&gt;&gt;</span>
			<div class="prompt__buttons">
				<PixelButton variant="solid" size="sm" type="submit" disabled={!authReady || vm.running}>
					{vm.running ? 'Running…' : '▶ Run'}
				</PixelButton>
				<PixelButton variant="outline" size="sm" onclick={onPlot} disabled={!authReady || vm.running}>
					📈 Plot
				</PixelButton>
				<PixelButton variant="ghost" size="sm" onclick={() => vm.clearCells()} disabled={vm.running}>
					Clear
				</PixelButton>
				<PixelButton variant="ghost" size="sm" onclick={() => vm.resetSession()} disabled={vm.running}>
					Reset session
				</PixelButton>
			</div>
		</div>
		<textarea
			bind:this={textareaEl}
			class="prompt__input"
			value={vm.input}
			oninput={(e) => vm.setInput((e.currentTarget as HTMLTextAreaElement).value)}
			onkeydown={onKeydown}
			rows="3"
			spellcheck="false"
			autocomplete="off"
			autocapitalize="off"
			placeholder={authReady ? 'MATLAB source…  (⌘/Ctrl + Enter to run)' : 'Sign in to enable the REPL'}
			disabled={!authReady || vm.running}
		></textarea>
	</form>
</div>

<style>
	.matlab {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}

	/* ---------- Hero (orange, matches MATLAB brand) ---------- */
	.hero {
		padding: 18px 22px;
		background: linear-gradient(135deg, #7c2d12 0%, #f97316 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
	}
	.hero__brand {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 6px;
	}
	.hero__mark { font-size: 1.4rem; }
	.hero__title {
		font-size: 1.25rem;
		font-weight: 800;
		margin: 0;
		letter-spacing: 0.12em;
		color: #ffffff;
		flex: 1 1 auto;
		min-width: 0;
	}
	.hero__chip {
		font-size: 0.65rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		background: rgba(0, 0, 0, 0.4);
		color: #fed7aa;
		padding: 3px 8px;
		border: 1.5px solid #000;
	}
	.hero__tagline {
		margin: 0;
		font-size: 0.8125rem;
		line-height: 1.55;
		color: #ffedd5;
	}
	.hero kbd {
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.4);
		padding: 1px 5px;
		font-size: 0.7rem;
		border-radius: 2px;
	}

	/* ---------- Auth banner ---------- */
	.auth-banner {
		padding: 10px 18px;
		background: #fef3c7;
		border-bottom: 2px solid #000;
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
		font-size: 0.8125rem;
		color: #92400e;
	}

	/* ---------- Cells (dark terminal aesthetic) ---------- */
	.cells {
		flex: 1 1 auto;
		min-height: 0;
		overflow-y: auto;
		background: #0a0f1e;
	}
	.empty {
		padding: 16px 20px;
		color: #6b7280;
		font-size: 0.8rem;
		line-height: 1.6;
	}
	.empty__line { margin: 0; color: #94a3b8; }
	.empty__code {
		margin: 8px 0;
		padding: 12px;
		background: #050913;
		border: 2px solid #1e293b;
		border-left: 6px solid #f97316;
		color: #fed7aa;
		font-size: 0.8rem;
		white-space: pre-wrap;
		overflow-x: auto;
	}
	.empty__hint { margin: 8px 0 0; color: #64748b; font-style: italic; }

	.cell {
		margin: 12px 16px;
		background: #0f172a;
		border: 2px solid #1e293b;
		border-left: 6px solid var(--accent);
		display: flex;
		flex-direction: column;
		gap: 6px;
		color: #e2e8f0;
	}
	.cell__head {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 12px;
		background: #1e293b;
		border-bottom: 1px solid #334155;
		font-size: 0.7rem;
		flex-wrap: wrap;
	}
	.cell__no {
		color: var(--accent);
		font-weight: 700;
		letter-spacing: 0.04em;
	}
	.cell__mode {
		color: #94a3b8;
		font-weight: 700;
		letter-spacing: 0.08em;
	}
	.cell__fallback {
		color: #fbbf24;
		font-weight: 700;
		letter-spacing: 0.04em;
	}
	.cell__elapsed {
		color: #64748b;
		margin-left: auto;
		font-variant-numeric: tabular-nums;
	}

	.cell__source,
	.cell__stdout,
	.cell__stderr,
	.cell__error {
		margin: 0;
		padding: 8px 12px;
		font-size: 0.8rem;
		line-height: 1.55;
		white-space: pre-wrap;
		overflow-x: auto;
		font-family: inherit;
	}
	.cell__source {
		background: #050913;
		color: #fed7aa;
		border-bottom: 1px dashed #1e293b;
	}
	.cell__stdout { color: #86efac; }
	.cell__stderr { color: #fda4af; background: rgba(127, 29, 29, 0.2); }
	.cell__error {
		color: #fecaca;
		background: rgba(127, 29, 29, 0.4);
		border-top: 1px solid #b91c1c;
	}
	.cell__artifact-err {
		margin: 0;
		padding: 8px 12px;
		font-size: 0.75rem;
		color: #fde68a;
		background: rgba(146, 64, 14, 0.4);
		border-top: 1px dashed #f59e0b;
		white-space: pre-wrap;
	}

	.cell__plots {
		display: grid;
		gap: 10px;
		padding: 8px 12px 12px;
	}
	.plot {
		margin: 0;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
		padding: 8px;
	}
	.plot img {
		display: block;
		width: 100%;
		height: auto;
		max-height: 480px;
		object-fit: contain;
	}
	.plot figcaption {
		font-size: 0.7rem;
		color: #6b7280;
		margin-top: 4px;
		font-family: inherit;
	}
	.plot__download {
		display: inline-block;
		padding: 6px 10px;
		background: var(--accent);
		color: #000;
		border: 2px solid #000;
		font-size: 0.75rem;
		font-weight: 700;
		text-decoration: none;
	}

	/* ---------- Prompt ---------- */
	.prompt {
		padding: 10px 14px 14px;
		background: #0a0f1e;
		border-top: 2px solid #000;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.prompt__head {
		display: flex;
		align-items: center;
		gap: 10px;
		flex-wrap: wrap;
	}
	.prompt__caret {
		color: var(--accent);
		font-weight: 800;
		font-size: 1rem;
	}
	.prompt__buttons {
		display: flex;
		gap: 6px;
		flex-wrap: wrap;
		margin-left: auto;
	}
	.prompt__input {
		width: 100%;
		min-height: 64px;
		resize: vertical;
		background: #050913;
		color: #fed7aa;
		border: 2px solid var(--accent);
		padding: 10px 12px;
		font-family: inherit;
		font-size: 0.85rem;
		line-height: 1.5;
		outline: none;
	}
	.prompt__input:focus { border-color: #fb923c; }
	.prompt__input:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
