<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { Badge, PixelButton, PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import { createAgentVM } from '$lib/viewmodels/agentViewModel.svelte';

	const vm = createAgentVM();

	let scrollEl = $state<HTMLElement | null>(null);
	let textareaEl = $state<HTMLTextAreaElement | null>(null);
	let expandedTools = $state<Set<string>>(new Set());

	onMount(async () => {
		await vm.bootstrap();
		await scrollToBottom();
	});

	async function scrollToBottom(): Promise<void> {
		await tick();
		if (scrollEl) scrollEl.scrollTop = scrollEl.scrollHeight;
	}

	const bubbleCount = $derived(vm.bubbles.length);
	$effect(() => {
		void bubbleCount;
		void scrollToBottom();
	});

	async function onSubmit(e: SubmitEvent): Promise<void> {
		e.preventDefault();
		await vm.send();
		textareaEl?.focus();
	}

	function onKeydown(e: KeyboardEvent): void {
		if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
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
			Replies are LLM-backed and route to real backend tools. <kbd>⌘/Ctrl + Enter</kbd> to send.
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
						<p class="bubble__content">{bubble.content}</p>
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

	.bubble__content,
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
</style>
