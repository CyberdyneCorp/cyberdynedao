<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { Badge, PixelButton, PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import { authVM } from '$lib/auth/authViewModel.svelte';
	import { createInterpreterVM } from '$lib/viewmodels/interpreterViewModel.svelte';

	const vm = createInterpreterVM();

	let textareaEl = $state<HTMLTextAreaElement | null>(null);
	let uploadInputEl = $state<HTMLInputElement | null>(null);
	let bottomSentinelEl = $state<HTMLElement | null>(null);

	const authReady = $derived(authVM.isRestored && authVM.isAuthenticated);

	onMount(() => {
		if (authReady) void vm.refreshFiles();
	});

	// Auto-scroll the cell log to the bottom as new cells land / fill in.
	const scrollSignal = $derived.by(() => {
		const last = vm.cells[vm.cells.length - 1];
		if (!last) return '';
		return `${vm.cells.length}|${last.status}|${last.stdout.length}|${last.stderr.length}`;
	});
	$effect(() => {
		void scrollSignal;
		void tick().then(() =>
			bottomSentinelEl?.scrollIntoView({ block: 'end', inline: 'nearest' })
		);
	});

	function badgeVariant(status: 'running' | 'ok' | 'error'): 'success' | 'warning' | 'danger' {
		if (status === 'ok') return 'success';
		if (status === 'running') return 'warning';
		return 'danger';
	}

	function formatElapsed(cell: { startedAt: number; finishedAt: number | null }): string {
		if (cell.finishedAt === null) return '…';
		const ms = cell.finishedAt - cell.startedAt;
		return ms < 1000 ? `${ms} ms` : `${(ms / 1000).toFixed(2)} s`;
	}

	function formatBytes(n: number): string {
		if (n < 1024) return `${n} B`;
		if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
		return `${(n / (1024 * 1024)).toFixed(1)} MB`;
	}

	function pickFile() {
		uploadInputEl?.click();
	}
	async function onUploadChange(e: Event) {
		const target = e.currentTarget as HTMLInputElement;
		const file = target.files?.[0];
		if (file) await vm.uploadWorkspaceFile(file);
		target.value = '';
	}
	function onKeydown(e: KeyboardEvent) {
		if (e.shiftKey && e.key === 'Enter') {
			e.preventDefault();
			void vm.runCode();
		}
	}
	async function onRun() {
		await vm.runCode();
		textareaEl?.focus();
	}

	const heroStyle = '--accent: #ffd43b; --accent-dark: #306998;';
</script>

<div class="py" style={heroStyle}>
	<header class="hero">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">🐍</span>
			<h1 class="hero__title">PYTHON SANDBOX</h1>
			<span class="hero__chip">session {vm.sessionId.slice(-6)}</span>
		</div>
		<p class="hero__tagline">
			Sandboxed Python on a remote engine. Upload datasets, write files, crunch numbers.
			<kbd>Shift + Enter</kbd> to run.
		</p>
	</header>

	{#if !authReady}
		<div class="auth-banner">
			<strong>Sign in required.</strong>
			<span>The Python backend uses your CyberdyneAuth session. Open the Connect menu and sign in to enable the REPL.</span>
		</div>
	{/if}

	<div class="main">
		<div class="cells">
			<PixelScrollArea maxHeight="100%" ariaLabel="Python cells">
				{#if vm.cells.length === 0}
					<div class="empty">
						<p class="empty__line"># Welcome to the Cyberdyne Python sandbox.</p>
						<p class="empty__line"># Try one of these:</p>
						<pre class="empty__code">print(sum(range(10)))
import statistics; print(statistics.mean([2, 4, 6]))</pre>
						<p class="empty__hint">Press <em>Run</em> (or Shift + Enter) to execute.</p>
					</div>
				{/if}

				{#each vm.cells as cell (cell.id)}
					<article class="cell">
						<header class="cell__head">
							<span class="cell__no">[{cell.id}]</span>
							<Badge variant={badgeVariant(cell.status)} size="sm">
								{cell.status === 'running' ? 'RUNNING' : cell.status === 'ok' ? 'OK' : 'ERROR'}
							</Badge>
							{#if cell.truncated}<Badge variant="warning" size="sm">TRUNCATED</Badge>{/if}
							<span class="cell__elapsed">{formatElapsed(cell)}</span>
						</header>
						<pre class="cell__source">{cell.source}</pre>
						{#if cell.stdout}<pre class="cell__stdout">{cell.stdout}</pre>{/if}
						{#if cell.result}<pre class="cell__result">{cell.result}</pre>{/if}
						{#if cell.stderr}<pre class="cell__stderr">{cell.stderr}</pre>{/if}
						{#if cell.error}<pre class="cell__error">{cell.error}</pre>{/if}
					</article>
				{/each}
				<div class="cells__bottom" bind:this={bottomSentinelEl} aria-hidden="true"></div>
			</PixelScrollArea>
		</div>

		<aside class="workspace" aria-label="Python workspace">
			<header class="workspace__head">
				<h2 class="workspace__title">Workspace</h2>
				<button
					type="button"
					class="workspace__refresh"
					onclick={() => vm.refreshFiles()}
					disabled={!authReady || vm.filesLoading}
					title="Refresh files"
				>
					{vm.filesLoading ? '…' : '↻'}
				</button>
			</header>

			{#if vm.error}
				<div class="workspace__error" role="status">{vm.error}</div>
			{/if}

			<div class="workspace__actions">
				<input type="file" class="workspace__file-input" bind:this={uploadInputEl} onchange={onUploadChange} />
				<PixelButton variant="outline" size="sm" onclick={pickFile} disabled={!authReady || vm.filesLoading}>
					⬆ Upload
				</PixelButton>
			</div>

			{#if vm.files.length === 0}
				<p class="workspace__empty">
					{authReady
						? 'No files yet. Upload a dataset or write one from your code (e.g. open("out.txt", "w")).'
						: 'Sign in to see workspace files.'}
				</p>
			{:else}
				<ul class="file-list">
					{#each vm.files as f (f.name)}
						<li>
							<button type="button" class="file" onclick={() => vm.downloadWorkspaceFile(f.name)} title={`Download ${f.name}`}>
								<span class="file__name">{f.name}</span>
								<span class="file__meta">{formatBytes(f.size_bytes)}</span>
							</button>
						</li>
					{/each}
				</ul>
			{/if}
		</aside>
	</div>

	<form class="prompt" onsubmit={(e) => { e.preventDefault(); void onRun(); }}>
		<div class="prompt__head">
			<span class="prompt__caret" aria-hidden="true">&gt;&gt;&gt;</span>
			<div class="prompt__buttons">
				<PixelButton variant="solid" size="sm" type="submit" disabled={!authReady || vm.running}>
					{vm.running ? 'Running…' : '▶ Run'}
				</PixelButton>
				<PixelButton variant="ghost" size="sm" onclick={() => vm.clearCells()} disabled={vm.running}>Clear</PixelButton>
				<PixelButton variant="ghost" size="sm" onclick={() => vm.resetSession()} disabled={vm.running}>Reset session</PixelButton>
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
			placeholder={authReady ? 'Python source…  (Shift + Enter to run)' : 'Sign in to enable the REPL'}
			disabled={!authReady || vm.running}
		></textarea>
	</form>
</div>

<style>
	.py {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}

	/* Hero — Python blue → gold brand */
	.hero {
		padding: 18px 22px;
		background: linear-gradient(135deg, #1e3a5f 0%, #306998 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
	}
	.hero__brand { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
	.hero__mark { font-size: 1.4rem; }
	.hero__title { font-size: 1.25rem; font-weight: 800; margin: 0; letter-spacing: 0.12em; flex: 1 1 auto; min-width: 0; }
	.hero__chip {
		font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
		background: rgba(0, 0, 0, 0.4); color: #ffe873; padding: 3px 8px; border: 1.5px solid #000;
	}
	.hero__tagline { margin: 0; font-size: 0.8125rem; line-height: 1.55; color: #dbeafe; }
	.hero kbd { background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(255, 255, 255, 0.4); padding: 1px 5px; font-size: 0.7rem; border-radius: 2px; }

	.auth-banner {
		padding: 10px 18px; background: #fef3c7; border-bottom: 2px solid #000;
		display: flex; gap: 8px; flex-wrap: wrap; font-size: 0.8125rem; color: #92400e;
	}

	.main { flex: 1 1 auto; min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(200px, 280px); }
	@media (max-width: 720px) { .main { grid-template-columns: minmax(0, 1fr); } .workspace { display: none; } }

	.cells { flex: 1 1 auto; min-height: 0; overflow-y: auto; background: #0a0f1e; }
	.empty { padding: 16px 20px; color: #94a3b8; font-size: 0.8rem; line-height: 1.6; }
	.empty__line { margin: 0; color: #94a3b8; }
	.empty__code { margin: 8px 0; padding: 12px; background: #050913; border: 2px solid #1e293b; border-left: 6px solid var(--accent); color: #fde68a; font-size: 0.8rem; white-space: pre-wrap; overflow-x: auto; }
	.empty__hint { margin: 8px 0 0; color: #64748b; font-style: italic; }

	.cell { margin: 12px 16px; background: #0f172a; border: 2px solid #1e293b; border-left: 6px solid var(--accent); display: flex; flex-direction: column; color: #e2e8f0; }
	.cell__head { display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: #1e293b; border-bottom: 1px solid #334155; font-size: 0.7rem; flex-wrap: wrap; }
	.cell__no { color: var(--accent); font-weight: 700; letter-spacing: 0.04em; }
	.cell__elapsed { color: #64748b; margin-left: auto; font-variant-numeric: tabular-nums; }
	.cell__source, .cell__stdout, .cell__stderr, .cell__error, .cell__result {
		margin: 0; padding: 8px 12px; font-size: 0.8rem; line-height: 1.55; white-space: pre-wrap; overflow-x: auto; font-family: inherit;
	}
	.cell__source { background: #050913; color: #fde68a; border-bottom: 1px dashed #1e293b; }
	.cell__stdout { color: #86efac; }
	.cell__result { color: #7dd3fc; }
	.cell__stderr { color: #fda4af; background: rgba(127, 29, 29, 0.2); }
	.cell__error { color: #fecaca; background: rgba(127, 29, 29, 0.4); border-top: 1px solid #b91c1c; }

	/* Prompt */
	.prompt { padding: 10px 14px 14px; background: #0a0f1e; border-top: 2px solid #000; display: flex; flex-direction: column; gap: 8px; }
	.prompt__head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
	.prompt__caret { color: var(--accent); font-weight: 800; font-size: 1rem; }
	.prompt__buttons { display: flex; gap: 6px; flex-wrap: wrap; margin-left: auto; }
	.prompt__input {
		width: 100%; min-height: 64px; resize: vertical; background: #050913; color: #fde68a;
		border: 2px solid var(--accent); padding: 10px 12px; font-family: inherit; font-size: 0.85rem; line-height: 1.5; outline: none;
	}
	.prompt__input:disabled { opacity: 0.5; cursor: not-allowed; }

	/* Workspace sidebar */
	.workspace { background: #1e293b; color: #e2e8f0; border-left: 2px solid #000; display: flex; flex-direction: column; gap: 12px; padding: 12px; overflow-y: auto; min-height: 0; }
	.workspace__head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
	.workspace__title { margin: 0; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent); }
	.workspace__refresh { background: transparent; border: 1px solid #334155; color: #cbd5e1; font-family: inherit; font-size: 0.9rem; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; cursor: pointer; }
	.workspace__refresh:hover:not(:disabled) { color: var(--accent); border-color: var(--accent); }
	.workspace__refresh:disabled { opacity: 0.5; cursor: not-allowed; }
	.workspace__error { background: rgba(127, 29, 29, 0.4); border: 1px solid #b91c1c; color: #fecaca; padding: 6px 8px; font-size: 0.7rem; white-space: pre-wrap; word-break: break-word; }
	.workspace__actions { display: flex; }
	.workspace__file-input { position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0; }
	.workspace__empty { margin: 0; font-size: 0.7rem; color: #64748b; font-style: italic; line-height: 1.45; }
	.file-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
	.file { display: flex; flex-direction: column; gap: 2px; background: #0f172a; border: 1px solid #334155; border-left: 4px solid var(--accent); padding: 6px 8px; font-family: inherit; color: inherit; text-align: left; cursor: pointer; }
	.file:hover { background: #1e293b; border-color: var(--accent); }
	.file__name { font-size: 0.8rem; font-weight: 700; color: #fde68a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.file__meta { font-size: 0.65rem; color: #94a3b8; font-variant-numeric: tabular-nums; }
</style>
