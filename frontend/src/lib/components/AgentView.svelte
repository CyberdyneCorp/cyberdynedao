<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { Badge, PixelButton, PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import {
		createAgentVM,
		type AgentArtifact,
		type AgentPlot
	} from '$lib/viewmodels/agentViewModel.svelte';
	import { downloadArtifact } from '$lib/api/matlabApi';
	import { downloadFile } from '$lib/api/interpreterApi';
	import { parseSegments } from '$lib/utils/chatSegments';
	import MermaidDiagram from './MermaidDiagram.svelte';

	const vm = createAgentVM();

	let scrollEl = $state<HTMLElement | null>(null);
	let bottomSentinelEl = $state<HTMLElement | null>(null);
	let textareaEl = $state<HTMLTextAreaElement | null>(null);
	let expandedTools = $state<Set<string>>(new Set());
	let expandedPlots = $state<Set<string>>(new Set());

	function togglePlot(key: string): void {
		const next = new Set(expandedPlots);
		if (next.has(key)) next.delete(key);
		else next.add(key);
		expandedPlots = next;
	}

	// Assistant text is split into prose / fenced code / Mermaid segments by
	// the shared `parseSegments` util (unit-tested). Mermaid renders as a
	// diagram; everything else stays XSS-safe Svelte markup (no {@html}).

	// Download each figure once (→ blob URL) and memoize the promise so
	// re-renders don't re-fetch. The proxy depends on the figure's source:
	// matlab_* figures live in the MATLAB workspace (/api/matlab); python_exec
	// figures live in the interpreter workspace (/api/interpreter).
	const plotUrlCache = new Map<string, Promise<string>>();
	function plotUrl(p: AgentPlot): Promise<string> {
		const key = `${p.source}:${p.sessionId}/${p.artifactPath}`;
		let pending = plotUrlCache.get(key);
		if (!pending) {
			pending =
				p.source === 'interpreter'
					? downloadFile(p.sessionId, p.artifactPath).then((r) => r.url)
					: downloadArtifact(p.artifactPath, p.sessionId).then((r) => r.url);
			plotUrlCache.set(key, pending);
		}
		return pending;
	}

	function fileIcon(name: string): string {
		const ext = name.split('.').pop()?.toLowerCase() ?? '';
		if (ext === 'pdf') return '📕';
		if (ext === 'md' || ext === 'markdown') return '📝';
		if (ext === 'mmd' || ext === 'mermaid') return '🧜';
		if (ext === 'csv' || ext === 'json' || ext === 'txt') return '📄';
		return '📎';
	}

	function formatBytes(n: number): string {
		if (n <= 0) return '';
		if (n < 1024) return `${n} B`;
		if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
		return `${(n / (1024 * 1024)).toFixed(1)} MB`;
	}

	// Stream the agent-generated file through the authed /api/interpreter
	// proxy and save it. Per-artifact in-flight guard so a double-click
	// doesn't double-download.
	let downloading = $state<Set<string>>(new Set());
	async function downloadAgentFile(a: AgentArtifact): Promise<void> {
		const key = `${a.sessionId}/${a.name}`;
		if (downloading.has(key)) return;
		downloading = new Set(downloading).add(key);
		try {
			const { url } = await downloadFile(a.sessionId, a.name);
			const anchor = document.createElement('a');
			anchor.href = url;
			anchor.download = a.name.split('/').pop() ?? a.name;
			document.body.appendChild(anchor);
			anchor.click();
			document.body.removeChild(anchor);
			setTimeout(() => URL.revokeObjectURL(url), 30_000);
		} finally {
			const next = new Set(downloading);
			next.delete(key);
			downloading = next;
		}
	}

	onMount(async () => {
		await vm.bootstrap();
		await scrollToBottom();
	});

	async function scrollToBottom(): Promise<void> {
		await tick();
		// Outer ``.log`` div isn't the actual overflow element —
		// PixelScrollArea wraps the scrollable container inside. Using
		// scrollIntoView on a sentinel walks ancestors and pulls the
		// real one down regardless.
		bottomSentinelEl?.scrollIntoView({ block: 'end', inline: 'nearest' });
	}

	// Re-scroll on every populate — not just on bubble-count change.
	// The assistant bubble is appended *pending* first; ``content`` /
	// ``pending`` flip when the reply lands. Watching just ``length``
	// missed that second update and the user had to scroll manually.
	const scrollSignal = $derived.by(() => {
		const last = vm.bubbles[vm.bubbles.length - 1];
		if (!last) return '';
		return `${vm.bubbles.length}|${last.pending}|${last.content.length}|${last.error ?? ''}`;
	});
	$effect(() => {
		void scrollSignal;
		void scrollToBottom();
	});

	async function onSubmit(e: SubmitEvent): Promise<void> {
		e.preventDefault();
		await vm.send();
		textareaEl?.focus();
	}

	function onKeydown(e: KeyboardEvent): void {
		// ChatGPT-style: Enter sends, Shift+Enter inserts a newline.
		// The matlab REPL uses Shift+Enter for the inverse reason —
		// multi-line scripts there default to "just type", here single
		// turns are the norm.
		if (e.key === 'Enter' && !e.shiftKey && !e.metaKey && !e.ctrlKey && !e.altKey) {
			e.preventDefault();
			void vm.send();
		}
	}

	function toggleTools(id: string): void {
		const next = new Set(expandedTools);
		if (next.has(id)) next.delete(id);
		else next.add(id);
		expandedTools = next;
	}

	function prettyJson(s: string): string {
		try {
			return JSON.stringify(JSON.parse(s), null, 2);
		} catch {
			return s;
		}
	}
</script>

<div class="agent">
	<!-- Hero -->
	<header class="hero">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">🤖</span>
			<h1 class="hero__title">CYBERDYNE AGENT</h1>
			<span class="hero__chip">
				{vm.sessionId ? `session ${vm.sessionId.slice(-6)}` : 'no session'}
			</span>
		</div>
		<p class="hero__tagline">
			Ask about Cyberdyne — projects, training, DAO, marketplace — or pitch a project idea.
			Replies are LLM-backed and route to real backend tools. <kbd>Enter</kbd> to send, <kbd>Shift + Enter</kbd> for a new line.
		</p>
	</header>

	{#if vm.error}
		<div class="banner banner--error" role="alert">
			<span>{vm.error}</span>
			<button type="button" onclick={() => vm.clearError()}>×</button>
		</div>
	{/if}

	<!-- Conversation -->
	<div class="log" bind:this={scrollEl}>
		<PixelScrollArea maxHeight="100%" ariaLabel="Agent conversation">
			{#if vm.bubbles.length === 0}
				<div class="empty">
					<p class="empty__title">Hi — I'm the Cyberdyne agent.</p>
					<p class="empty__body">Try one of these to get started:</p>
					<ul class="empty__list">
						<li>What does Cyberdyne actually do?</li>
						<li>What training paths do you offer for DeFi?</li>
						<li>How does the DAO model work?</li>
						<li>I want to build a geospatial dashboard — can we talk?</li>
					</ul>
				</div>
			{/if}

			{#each vm.bubbles as bubble (bubble.id)}
				<article class="bubble bubble--{bubble.role}" class:bubble--pending={bubble.pending} class:bubble--error={bubble.error}>
					<header class="bubble__head">
						<span class="bubble__role">{bubble.role === 'user' ? 'YOU' : 'AGENT'}</span>
						{#if bubble.model}
							<Badge variant="neutral" size="sm">{bubble.model}</Badge>
						{/if}
						{#if bubble.pending}
							<Badge variant="warning" size="sm">THINKING…</Badge>
						{:else if bubble.error}
							<Badge variant="danger" size="sm">ERROR</Badge>
						{/if}
					</header>

					{#if bubble.pending && !bubble.content}
						<p class="bubble__placeholder">
							<span class="dot"></span><span class="dot"></span><span class="dot"></span>
						</p>
					{:else if bubble.error}
						<p class="bubble__error">{bubble.error}</p>
					{:else}
						<div class="bubble__content">
							{#each parseSegments(bubble.content) as seg}
								{#if seg.kind === 'code'}
									<div class="code">
										{#if seg.lang}<span class="code__lang">{seg.lang}</span>{/if}
										<pre>{seg.code}</pre>
									</div>
								{:else if seg.kind === 'mermaid'}
									<MermaidDiagram code={seg.code} />
								{:else}
									<p class="bubble__text">{seg.text}</p>
								{/if}
							{/each}
						</div>
					{/if}

					{#if bubble.plots.length > 0}
						<div class="plots">
							{#each bubble.plots as plot, i (bubble.id + '-' + i)}
								{@const key = bubble.id + '-' + i}
								{@const expanded = expandedPlots.has(key)}
								<figure class="plot" class:plot--expanded={expanded}>
									{#await plotUrl(plot)}
										<div class="plot__loading">rendering figure…</div>
									{:then url}
										<button
											type="button"
											class="plot__zoom"
											aria-label={expanded ? 'Collapse figure' : 'Expand figure'}
											onclick={() => togglePlot(key)}
										>
											<img src={url} alt={plot.caption} loading="lazy" />
										</button>
										<figcaption>{plot.caption} · click to {expanded ? 'collapse' : 'expand'}</figcaption>
									{:catch}
										<div class="plot__loading">Figure unavailable.</div>
									{/await}
								</figure>
							{/each}
						</div>
					{/if}

					{#if bubble.artifacts.length > 0}
						<div class="files">
							{#each bubble.artifacts as file (file.sessionId + '/' + file.name)}
								{@const key = file.sessionId + '/' + file.name}
								<button
									type="button"
									class="file"
									onclick={() => downloadAgentFile(file)}
									disabled={downloading.has(key)}
									title={`Download ${file.name}`}
								>
									<span class="file__icon" aria-hidden="true">{fileIcon(file.name)}</span>
									<span class="file__name">{file.name}</span>
									<span class="file__meta">
										{downloading.has(key) ? 'downloading…' : `⬇ ${formatBytes(file.sizeBytes)}`}
									</span>
								</button>
							{/each}
						</div>
					{/if}

					{#if bubble.toolCalls.length > 0}
						<div class="tools">
							<button
								type="button"
								class="tools__toggle"
								onclick={() => toggleTools(bubble.id)}
								aria-expanded={expandedTools.has(bubble.id)}
							>
								{expandedTools.has(bubble.id) ? '▼' : '▶'} {bubble.toolCalls.length} tool call{bubble.toolCalls.length === 1 ? '' : 's'}
							</button>
							{#if expandedTools.has(bubble.id)}
								<div class="tools__list">
									{#each bubble.toolCalls as tc (tc.id)}
										<div class="tool">
											<div class="tool__name">{tc.name}</div>
											<pre class="tool__args">{prettyJson(tc.argumentsJson)}</pre>
										</div>
									{/each}
								</div>
							{/if}
						</div>
					{/if}
				</article>
			{/each}
			<!-- Auto-scroll anchor. scrollIntoView walks ancestors to
			     whichever element is actually overflowing inside
			     PixelScrollArea. -->
			<div class="log__bottom" bind:this={bottomSentinelEl} aria-hidden="true"></div>
		</PixelScrollArea>
	</div>

	<!-- Input -->
	<form class="prompt" onsubmit={onSubmit}>
		<textarea
			bind:this={textareaEl}
			class="prompt__input"
			value={vm.input}
			oninput={(e) => vm.setInput((e.currentTarget as HTMLTextAreaElement).value)}
			onkeydown={onKeydown}
			rows="2"
			spellcheck="true"
			placeholder={vm.running ? 'Agent is thinking…' : 'Ask the Cyberdyne agent…'}
			disabled={vm.running}
		></textarea>
		<div class="prompt__row">
			<PixelButton variant="ghost" size="sm" onclick={() => vm.resetSession()} disabled={vm.running}>
				New conversation
			</PixelButton>
			<PixelButton type="submit" variant="solid" size="md" disabled={vm.running || !vm.input.trim()}>
				{vm.running ? 'Sending…' : '→ Send'}
			</PixelButton>
		</div>
	</form>
</div>

<style>
	.agent {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		display: flex;
		flex-direction: column;
		min-height: 0;
		--accent: #a855f7;
		--accent-dark: #7e22ce;
	}

	/* ---------- Hero ---------- */
	.hero {
		padding: 18px 22px;
		background: linear-gradient(135deg, #4c1d95 0%, #a855f7 100%);
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
		flex: 1 1 auto;
	}
	.hero__chip {
		font-size: 0.65rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		background: rgba(0, 0, 0, 0.4);
		color: #e9d5ff;
		padding: 3px 8px;
		border: 1.5px solid #000;
	}
	.hero__tagline {
		margin: 0;
		font-size: 0.8125rem;
		line-height: 1.55;
		color: #f3e8ff;
	}
	.hero kbd {
		background: rgba(0, 0, 0, 0.4);
		border: 1px solid rgba(255, 255, 255, 0.4);
		padding: 1px 5px;
		font-size: 0.7rem;
	}

	/* ---------- Banner ---------- */
	.banner {
		padding: 8px 16px;
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.8125rem;
		border-bottom: 2px solid #000;
	}
	.banner--error { background: #fef2f2; color: #b91c1c; }
	.banner button {
		background: none;
		border: 1px solid currentColor;
		color: inherit;
		cursor: pointer;
		padding: 2px 8px;
		font-family: inherit;
	}

	/* ---------- Log ---------- */
	.log {
		flex: 1 1 auto;
		min-height: 0;
		overflow-y: auto;
		background: #f9fafb;
	}
	.empty {
		padding: 24px 22px;
		color: #4b5563;
	}
	.empty__title { font-weight: 700; color: #111827; margin: 0 0 6px; font-size: 0.95rem; }
	.empty__body { margin: 0 0 6px; font-size: 0.8rem; }
	.empty__list {
		margin: 0;
		padding-left: 18px;
		font-size: 0.8125rem;
		line-height: 1.6;
		color: #4338ca;
	}

	/* ---------- Bubble (relies on .agent's --accent vars) ---------- */
	.bubble {
		position: relative;
		margin: 10px 14px;
		padding: 10px 12px 10px 18px;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.bubble::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0;
		bottom: 0;
		width: 6px;
		border-right: 2px solid #000;
	}
	.bubble--user::before { background: #3b82f6; }
	.bubble--assistant::before { background: var(--accent); }
	.bubble--error::before { background: #ef4444; }
	.bubble--pending { opacity: 0.85; }

	.bubble__head {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.7rem;
	}
	.bubble__role {
		font-weight: 800;
		letter-spacing: 0.1em;
		color: var(--accent-dark);
	}
	.bubble--user .bubble__role { color: #1d4ed8; }

	.bubble__content {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.bubble__text,
	.bubble__error,
	.bubble__placeholder {
		margin: 0;
		font-size: 0.875rem;
		line-height: 1.55;
		white-space: pre-wrap;
		word-break: break-word;
		color: #1f2937;
	}
	.bubble__error { color: #b91c1c; }

	/* Fenced code blocks (e.g. the MATLAB the agent wrote). */
	.code {
		position: relative;
		background: #0b1120;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
	}
	.code__lang {
		display: block;
		font-size: 0.625rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #9fb4ff;
		background: #1a2440;
		padding: 2px 8px;
		border-bottom: 1px solid #2a3a66;
	}
	.code pre {
		margin: 0;
		padding: 10px 12px;
		overflow-x: auto;
		font-family: 'Courier New', ui-monospace, monospace;
		font-size: 0.8125rem;
		line-height: 1.5;
		color: #c9ffd9;
		white-space: pre;
		tab-size: 2;
	}

	.bubble__placeholder {
		display: inline-flex;
		gap: 4px;
		padding: 4px 0;
	}
	.dot {
		display: inline-block;
		width: 6px;
		height: 6px;
		background: var(--accent);
		border: 1.5px solid #000;
		animation: blink 1.2s infinite;
	}
	.dot:nth-child(2) { animation-delay: 0.2s; }
	.dot:nth-child(3) { animation-delay: 0.4s; }
	@keyframes blink {
		0%, 60%, 100% { opacity: 0.3; }
		30% { opacity: 1; }
	}

	/* ---------- Tool calls (collapsed by default) ---------- */
	.tools { display: flex; flex-direction: column; gap: 6px; }
	.tools__toggle {
		align-self: flex-start;
		background: none;
		border: 1px dashed #6b7280;
		padding: 3px 8px;
		font-size: 0.7rem;
		font-family: inherit;
		color: #6b7280;
		cursor: pointer;
	}
	.tools__toggle:hover { color: #1f2937; border-color: #1f2937; }
	.tools__list { display: grid; gap: 6px; }
	.tool {
		background: #1e293b;
		color: #e2e8f0;
		border: 1px solid #334155;
		padding: 6px 10px;
		font-size: 0.7rem;
	}
	.tool__name {
		color: var(--accent);
		font-weight: 700;
		letter-spacing: 0.04em;
		margin-bottom: 4px;
	}
	.tool__args {
		margin: 0;
		font-size: 0.65rem;
		white-space: pre-wrap;
		overflow-x: auto;
		color: #cbd5e1;
	}

	/* ---------- Prompt ---------- */
	.prompt {
		padding: 10px 14px 14px;
		background: #ffffff;
		border-top: 2px solid #000;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.prompt__input {
		width: 100%;
		min-height: 56px;
		resize: vertical;
		background: #fafafa;
		color: #111827;
		border: 2px solid var(--accent);
		padding: 8px 10px;
		font-family: inherit;
		font-size: 0.85rem;
		line-height: 1.5;
		outline: none;
	}
	.prompt__input:focus { border-color: var(--accent-dark); }
	.prompt__input:disabled { opacity: 0.6; cursor: not-allowed; }
	.prompt__row {
		display: flex;
		justify-content: space-between;
		gap: 8px;
		flex-wrap: wrap;
	}

	/* ---------- Inline MATLAB figures ---------- */
	.plots {
		display: flex;
		flex-direction: column;
		gap: 8px;
		margin-top: 8px;
	}

	/* Downloadable files produced by python_exec / create_document. */
	.files {
		display: flex;
		flex-direction: column;
		gap: 6px;
		margin-top: 8px;
	}
	.file {
		display: flex;
		align-items: center;
		gap: 8px;
		width: 100%;
		text-align: left;
		background: #0f172a;
		border: 2px solid #334155;
		border-left: 6px solid #7dd3fc;
		padding: 8px 10px;
		font-family: inherit;
		color: #e2e8f0;
		cursor: pointer;
	}
	.file:hover:not(:disabled) {
		border-color: #7dd3fc;
	}
	.file:disabled {
		opacity: 0.6;
		cursor: progress;
	}
	.file__icon {
		font-size: 1rem;
	}
	.file__name {
		flex: 1 1 auto;
		font-size: 0.82rem;
		font-weight: 700;
		color: #7dd3fc;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.file__meta {
		font-size: 0.7rem;
		color: #94a3b8;
		flex-shrink: 0;
	}
	.plot {
		margin: 0;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 8px;
	}
	.plot__zoom {
		all: unset;
		display: block;
		width: 100%;
		cursor: zoom-in;
	}
	.plot--expanded .plot__zoom {
		cursor: zoom-out;
	}
	.plot__zoom:focus-visible {
		outline: 2px solid #7e22ce;
		outline-offset: 2px;
	}
	.plot img {
		display: block;
		width: 100%;
		height: auto;
		max-height: 240px;
		object-fit: contain;
	}
	.plot--expanded img {
		max-height: 70vh;
	}
	.plot figcaption {
		font-size: 0.7rem;
		color: #6b7280;
		margin-top: 4px;
	}
	.plot__loading {
		font-size: 0.8125rem;
		color: #6b7280;
		font-style: italic;
		padding: 12px;
	}
</style>
