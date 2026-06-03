<script lang="ts">
	import { onDestroy, onMount, tick } from 'svelte';
	import { Badge, PixelButton, PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import { authVM } from '$lib/auth/authViewModel.svelte';
	import { createCyberfliesVM } from '$lib/viewmodels/cyberfliesViewModel.svelte';
	import { createInterpreterVM } from '$lib/viewmodels/interpreterViewModel.svelte';

	type Tab = 'meetings' | 'chat' | 'code';
	let tab = $state<Tab>('meetings');

	const meetings = createCyberfliesVM();
	const code = createInterpreterVM();

	let audioInputEl = $state<HTMLInputElement | null>(null);
	let codeUploadEl = $state<HTMLInputElement | null>(null);
	let codeTextareaEl = $state<HTMLTextAreaElement | null>(null);
	let chatInput = $state<string>('');
	let chatScrollBottom = $state<HTMLElement | null>(null);
	let codeScrollBottom = $state<HTMLElement | null>(null);

	const authReady = $derived(authVM.isRestored && authVM.isAuthenticated);

	onMount(() => {
		if (authReady) {
			void meetings.refreshRecordings();
			void meetings.refreshChannels();
		}
	});

	onDestroy(() => {
		meetings.destroy();
	});

	// Auto-scroll chat + code logs as new turns/cells land.
	$effect(() => {
		void meetings.chatTurns.length;
		void meetings.chatSending;
		void tick().then(() =>
			chatScrollBottom?.scrollIntoView({ block: 'end', inline: 'nearest' })
		);
	});
	$effect(() => {
		const last = code.cells[code.cells.length - 1];
		void `${code.cells.length}|${last?.status}|${last?.stdout.length}`;
		void tick().then(() =>
			codeScrollBottom?.scrollIntoView({ block: 'end', inline: 'nearest' })
		);
	});

	function statusVariant(status: string): 'success' | 'warning' | 'danger' {
		const s = status.toLowerCase();
		if (s === 'completed') return 'success';
		if (s === 'failed' || s === 'error') return 'danger';
		return 'warning';
	}

	function formatBytes(n: number): string {
		if (n < 1024) return `${n} B`;
		if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
		return `${(n / (1024 * 1024)).toFixed(1)} MB`;
	}

	function formatDate(iso: string | null | undefined): string {
		if (!iso) return '—';
		const d = new Date(iso);
		return Number.isNaN(d.getTime()) ? iso : d.toLocaleString();
	}

	function formatDuration(seconds: number | null | undefined): string {
		if (seconds == null) return '';
		const m = Math.floor(seconds / 60);
		const s = Math.round(seconds % 60);
		return m > 0 ? `${m}m ${s}s` : `${s}s`;
	}

	function pickAudio() {
		audioInputEl?.click();
	}
	async function onAudioChange(e: Event) {
		const target = e.currentTarget as HTMLInputElement;
		const file = target.files?.[0];
		if (file) await meetings.uploadAudio(file);
		target.value = '';
	}

	async function onDownloadAudio(id: string) {
		try {
			const url = await meetings.audioUrlFor(id);
			window.open(url, '_blank', 'noopener');
		} catch {
			/* surfaced via the meetings error banner on next action */
		}
	}

	async function onSendChat(e: SubmitEvent) {
		e.preventDefault();
		const text = chatInput;
		chatInput = '';
		await meetings.sendChat(text);
	}

	function pickCodeFile() {
		codeUploadEl?.click();
	}
	async function onCodeFileChange(e: Event) {
		const target = e.currentTarget as HTMLInputElement;
		const file = target.files?.[0];
		if (file) await code.uploadWorkspaceFile(file);
		target.value = '';
	}
	function onCodeKeydown(e: KeyboardEvent) {
		if (e.shiftKey && e.key === 'Enter') {
			e.preventDefault();
			void code.runCode();
		}
	}
	async function onRunCode() {
		await code.runCode();
		codeTextareaEl?.focus();
	}

	const heroStyle = '--accent: #14b8a6; --accent-dark: #0f766e;';
</script>

<div class="cf" style={heroStyle}>
	<header class="hero">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">🎙️</span>
			<h1 class="hero__title">CYBERFLIES</h1>
			<span class="hero__chip">Meetings</span>
		</div>
		<p class="hero__tagline">
			Upload audio, get transcripts + summaries, ask questions across your meetings, and crunch
			the data in a Python sandbox.
		</p>
		<nav class="tabs" aria-label="Cyberflies sections">
			<button type="button" class="tab" class:tab--active={tab === 'meetings'} onclick={() => (tab = 'meetings')}>
				🎧 Meetings
			</button>
			<button type="button" class="tab" class:tab--active={tab === 'chat'} onclick={() => (tab = 'chat')}>
				💬 Chat
			</button>
			<button type="button" class="tab" class:tab--active={tab === 'code'} onclick={() => (tab = 'code')}>
				🐍 Code
			</button>
		</nav>
	</header>

	{#if !authReady}
		<div class="auth-banner">
			<strong>Sign in required.</strong>
			<span>Cyberflies uses your CyberdyneAuth session. Open the Connect menu and sign in to load your meetings.</span>
		</div>
	{/if}

	<!-- ── Meetings ─────────────────────────────────────────────── -->
	{#if tab === 'meetings'}
		<div class="meetings">
			<aside class="list">
				<div class="list__head">
					<h2 class="list__title">Past meetings</h2>
					<button
						type="button"
						class="icon-btn"
						onclick={() => meetings.refreshRecordings()}
						disabled={!authReady || meetings.loading}
						title="Refresh"
					>
						{meetings.loading ? '…' : '↻'}
					</button>
				</div>
				<div class="list__actions">
					<input
						type="file"
						accept="audio/*"
						class="hidden-input"
						bind:this={audioInputEl}
						onchange={onAudioChange}
					/>
					<PixelButton variant="solid" size="sm" onclick={pickAudio} disabled={!authReady || meetings.uploading}>
						{meetings.uploading ? 'Uploading…' : '⬆ Upload audio'}
					</PixelButton>
				</div>

				{#if meetings.error}
					<div class="banner banner--err">{meetings.error}</div>
				{/if}

				{#if meetings.recordings.length === 0}
					<p class="empty">
						{authReady ? 'No meetings yet. Upload an audio file to get started.' : 'Sign in to see your meetings.'}
					</p>
				{:else}
					<PixelScrollArea maxHeight="100%" ariaLabel="Recordings">
						<ul class="rec-list">
							{#each meetings.recordings as rec (rec.id)}
								<li>
									<button
										type="button"
										class="rec"
										class:rec--active={rec.id === meetings.selectedId}
										onclick={() => meetings.selectRecording(rec.id)}
									>
										<span class="rec__top">
											<span class="rec__title">
												{rec.summary?.headline ?? `Recording ${rec.id.slice(0, 8)}`}
											</span>
											<Badge variant={statusVariant(rec.status)} size="sm">{rec.status}</Badge>
										</span>
										<span class="rec__meta">
											{formatDate(rec.captured_at ?? rec.created_at)} · {formatBytes(rec.size_bytes)}
										</span>
									</button>
								</li>
							{/each}
						</ul>
					</PixelScrollArea>
				{/if}
			</aside>

			<section class="detail">
				{#if !meetings.selectedRecording}
					<p class="empty empty--detail">Select a meeting to see its transcript and summary.</p>
				{:else}
					{@const rec = meetings.selectedRecording}
					<div class="detail__head">
						<h2 class="detail__title">{rec.summary?.headline ?? `Recording ${rec.id.slice(0, 8)}`}</h2>
						<Badge variant={statusVariant(rec.status)} size="sm">{rec.status}</Badge>
					</div>
					<p class="detail__sub">
						{formatDate(rec.captured_at ?? rec.created_at)}
						{#if rec.transcription?.duration_seconds} · {formatDuration(rec.transcription.duration_seconds)}{/if}
						{#if rec.transcription?.language} · {rec.transcription.language}{/if}
						· {rec.audio_format} · {formatBytes(rec.size_bytes)}
					</p>
					<div class="detail__actions">
						<PixelButton variant="outline" size="sm" onclick={() => onDownloadAudio(rec.id)}>
							⬇ Download audio
						</PixelButton>
						<PixelButton
							variant="ghost"
							size="sm"
							onclick={() => {
								meetings.setChatScope('all');
								chatInput = `Summarize the meeting "${rec.summary?.headline ?? rec.id}".`;
								tab = 'chat';
							}}
						>
							💬 Ask about this
						</PixelButton>
					</div>

					{#if rec.error}
						<div class="banner banner--err">Processing failed: {rec.error}</div>
					{/if}

					{#if !rec.summary && !rec.transcription && !rec.error}
						<div class="banner banner--info">Transcribing… this panel updates automatically when it's ready.</div>
					{/if}

					{#if rec.summary}
						<section class="block">
							<h3 class="block__title">Summary</h3>
							<p class="block__abstract">{rec.summary.abstract}</p>
							{#if rec.summary.bullets.length > 0}
								<ul class="bullets">
									{#each rec.summary.bullets as b}
										<li>{b}</li>
									{/each}
								</ul>
							{/if}
						</section>
					{/if}

					{#if rec.transcription}
						<section class="block">
							<h3 class="block__title">Transcript <span class="block__count">{rec.transcription.word_count} words</span></h3>
							<PixelScrollArea maxHeight="320px" ariaLabel="Transcript">
								<pre class="transcript">{rec.transcription.text}</pre>
							</PixelScrollArea>
						</section>
					{/if}
				{/if}
			</section>
		</div>
	{/if}

	<!-- ── Chat ─────────────────────────────────────────────────── -->
	{#if tab === 'chat'}
		<div class="chat">
			<div class="chat__scope">
				<label for="cf-scope">Scope</label>
				<select
					id="cf-scope"
					value={meetings.chatScope}
					onchange={(e) => meetings.setChatScope((e.currentTarget as HTMLSelectElement).value)}
				>
					<option value="all">All meetings</option>
					{#each meetings.channels as ch (ch.id)}
						<option value={ch.id}>{ch.name}</option>
					{/each}
				</select>
			</div>

			<div class="chat__log">
				<PixelScrollArea maxHeight="100%" ariaLabel="Chat messages">
					{#if meetings.chatTurns.length === 0}
						<p class="empty">Ask anything about your meetings — “What did we decide last week?”, “Summarize my standups.”</p>
					{/if}
					{#each meetings.chatTurns as turn, i (i)}
						<div class="msg" class:msg--user={turn.role === 'user'}>
							<span class="msg__role">{turn.role === 'user' ? 'You' : 'Cyberflies'}</span>
							<p class="msg__content">{turn.content}</p>
							{#if turn.usedTools && turn.usedTools.length > 0}
								<span class="msg__tools">tools: {turn.usedTools.join(', ')}</span>
							{/if}
						</div>
					{/each}
					{#if meetings.chatSending}
						<div class="msg"><span class="msg__role">Cyberflies</span><p class="msg__content">…</p></div>
					{/if}
					<div bind:this={chatScrollBottom} aria-hidden="true"></div>
				</PixelScrollArea>
			</div>

			{#if meetings.chatError}
				<div class="banner banner--err">{meetings.chatError}</div>
			{/if}

			<form class="chat__form" onsubmit={onSendChat}>
				<input
					class="chat__input"
					type="text"
					placeholder={authReady ? 'Ask about your meetings…' : 'Sign in to chat'}
					value={chatInput}
					oninput={(e) => (chatInput = (e.currentTarget as HTMLInputElement).value)}
					disabled={!authReady || meetings.chatSending}
				/>
				<PixelButton variant="solid" size="sm" type="submit" disabled={!authReady || meetings.chatSending}>
					{meetings.chatSending ? '…' : 'Send'}
				</PixelButton>
			</form>
		</div>
	{/if}

	<!-- ── Code (Python interpreter) ───────────────────────────── -->
	{#if tab === 'code'}
		<div class="code">
			<div class="code__main">
				<div class="cells">
					<PixelScrollArea maxHeight="100%" ariaLabel="Python cells">
						{#if code.cells.length === 0}
							<div class="empty empty--code">
								<p># Python sandbox. Shift + Enter to run.</p>
								<pre class="empty__code">import statistics
print(statistics.mean([1, 2, 3, 4]))</pre>
							</div>
						{/if}
						{#each code.cells as cell (cell.id)}
							<article class="cell">
								<header class="cell__head">
									<span class="cell__no">[{cell.id}]</span>
									<Badge variant={cell.status === 'ok' ? 'success' : cell.status === 'running' ? 'warning' : 'danger'} size="sm">
										{cell.status === 'running' ? 'RUNNING' : cell.status === 'ok' ? 'OK' : 'ERROR'}
									</Badge>
									{#if cell.truncated}<Badge variant="warning" size="sm">TRUNCATED</Badge>{/if}
								</header>
								<pre class="cell__source">{cell.source}</pre>
								{#if cell.stdout}<pre class="cell__stdout">{cell.stdout}</pre>{/if}
								{#if cell.result}<pre class="cell__result">{cell.result}</pre>{/if}
								{#if cell.stderr}<pre class="cell__stderr">{cell.stderr}</pre>{/if}
								{#if cell.error}<pre class="cell__error">{cell.error}</pre>{/if}
							</article>
						{/each}
						<div bind:this={codeScrollBottom} aria-hidden="true"></div>
					</PixelScrollArea>
				</div>

				<aside class="files">
					<div class="files__head">
						<h3 class="files__title">Workspace <span class="files__count">{code.files.length}</span></h3>
						<button type="button" class="icon-btn" onclick={() => code.refreshFiles()} disabled={!authReady || code.filesLoading} title="Refresh files">
							{code.filesLoading ? '…' : '↻'}
						</button>
					</div>
					<input type="file" class="hidden-input" bind:this={codeUploadEl} onchange={onCodeFileChange} />
					<PixelButton variant="outline" size="sm" onclick={pickCodeFile} disabled={!authReady || code.filesLoading}>⬆ Upload</PixelButton>
					{#if code.error}<div class="banner banner--err">{code.error}</div>{/if}
					{#if code.files.length === 0}
						<p class="empty">No files. Run code that writes a file, or upload a dataset.</p>
					{:else}
						<ul class="file-list">
							{#each code.files as f (f.name)}
								<li>
									<button type="button" class="file" onclick={() => code.downloadWorkspaceFile(f.name)} title={`Download ${f.name}`}>
										<span class="file__name">{f.name}</span>
										<span class="file__meta">{formatBytes(f.size_bytes)}</span>
									</button>
								</li>
							{/each}
						</ul>
					{/if}
				</aside>
			</div>

			<form class="prompt" onsubmit={(e) => { e.preventDefault(); void onRunCode(); }}>
				<div class="prompt__head">
					<span class="prompt__caret" aria-hidden="true">&gt;&gt;&gt;</span>
					<div class="prompt__buttons">
						<PixelButton variant="solid" size="sm" type="submit" disabled={!authReady || code.running}>
							{code.running ? 'Running…' : '▶ Run'}
						</PixelButton>
						<PixelButton variant="ghost" size="sm" onclick={() => code.clearCells()} disabled={code.running}>Clear</PixelButton>
						<PixelButton variant="ghost" size="sm" onclick={() => code.resetSession()} disabled={code.running}>Reset session</PixelButton>
					</div>
				</div>
				<textarea
					bind:this={codeTextareaEl}
					class="prompt__input"
					value={code.input}
					oninput={(e) => code.setInput((e.currentTarget as HTMLTextAreaElement).value)}
					onkeydown={onCodeKeydown}
					rows="3"
					spellcheck="false"
					placeholder={authReady ? 'Python source…  (Shift + Enter to run)' : 'Sign in to run code'}
					disabled={!authReady || code.running}
				></textarea>
			</form>
		</div>
	{/if}
</div>

<style>
	.cf {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}

	/* Hero */
	.hero {
		padding: 16px 22px 0;
		background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
	}
	.hero__brand { display: flex; align-items: center; gap: 12px; }
	.hero__mark { font-size: 1.4rem; }
	.hero__title { font-size: 1.25rem; font-weight: 800; margin: 0; letter-spacing: 0.12em; }
	.hero__chip {
		font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
		background: rgba(0, 0, 0, 0.4); color: #ccfbf1; padding: 3px 8px; border: 1.5px solid #000;
	}
	.hero__tagline { margin: 6px 0 12px; font-size: 0.8125rem; line-height: 1.55; color: #d1faf4; }
	.tabs { display: flex; gap: 4px; }
	.tab {
		font-family: inherit; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.04em;
		background: rgba(0, 0, 0, 0.25); color: #ccfbf1; padding: 8px 14px;
		border: 2px solid #000; border-bottom: none; cursor: pointer;
	}
	.tab--active { background: #ffffff; color: #0f766e; }
	.tab:hover:not(.tab--active) { background: rgba(255, 255, 255, 0.2); }

	.auth-banner {
		padding: 10px 18px; background: #fef3c7; border-bottom: 2px solid #000;
		display: flex; gap: 8px; flex-wrap: wrap; font-size: 0.8125rem; color: #92400e;
	}

	.banner { padding: 8px 12px; font-size: 0.75rem; white-space: pre-wrap; word-break: break-word; }
	.banner--err { background: #fee2e2; border: 1px solid #b91c1c; color: #991b1b; }
	.banner--info { background: #cffafe; border: 1px solid #0e7490; color: #155e63; }

	.empty { padding: 16px; color: #6b7280; font-size: 0.8rem; line-height: 1.6; font-style: italic; }
	.empty--detail { text-align: center; margin-top: 40px; }

	/* Meetings layout */
	.meetings { flex: 1 1 auto; min-height: 0; display: grid; grid-template-columns: minmax(240px, 320px) minmax(0, 1fr); }
	@media (max-width: 720px) { .meetings { grid-template-columns: minmax(0, 1fr); } .detail { display: none; } }

	.list { border-right: 2px solid #000; display: flex; flex-direction: column; min-height: 0; background: #f1f5f9; }
	.list__head { display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; border-bottom: 1px solid #cbd5e1; }
	.list__title { margin: 0; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: #0f766e; }
	.list__actions { padding: 10px 12px; border-bottom: 1px solid #cbd5e1; }

	.rec-list { list-style: none; margin: 0; padding: 6px; display: flex; flex-direction: column; gap: 4px; }
	.rec {
		display: flex; flex-direction: column; gap: 4px; width: 100%; text-align: left;
		background: #ffffff; border: 1px solid #cbd5e1; border-left: 4px solid var(--accent);
		padding: 8px 10px; cursor: pointer; font-family: inherit; color: inherit;
	}
	.rec:hover { border-color: var(--accent); }
	.rec--active { background: #ccfbf1; border-color: var(--accent-dark); }
	.rec__top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
	.rec__title { font-size: 0.8rem; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.rec__meta { font-size: 0.65rem; color: #64748b; }

	.detail { padding: 16px 20px; overflow-y: auto; min-height: 0; display: flex; flex-direction: column; gap: 10px; }
	.detail__head { display: flex; align-items: center; gap: 10px; }
	.detail__title { margin: 0; font-size: 1.05rem; font-weight: 800; }
	.detail__sub { margin: 0; font-size: 0.72rem; color: #64748b; }
	.detail__actions { display: flex; gap: 6px; flex-wrap: wrap; }
	.block { border: 2px solid #e2e8f0; border-left: 6px solid var(--accent); padding: 10px 12px; }
	.block__title { margin: 0 0 6px; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0f766e; display: flex; justify-content: space-between; }
	.block__count { font-size: 0.65rem; color: #94a3b8; font-weight: 600; }
	.block__abstract { margin: 0 0 8px; font-size: 0.85rem; line-height: 1.55; }
	.bullets { margin: 0; padding-left: 18px; font-size: 0.82rem; line-height: 1.6; }
	.transcript { margin: 0; font-size: 0.8rem; line-height: 1.6; white-space: pre-wrap; font-family: inherit; color: #1f2937; }

	/* Chat layout */
	.chat { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }
	.chat__scope { display: flex; align-items: center; gap: 8px; padding: 10px 16px; border-bottom: 1px solid #cbd5e1; font-size: 0.75rem; }
	.chat__scope label { font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #0f766e; }
	.chat__scope select { font-family: inherit; font-size: 0.78rem; padding: 4px 8px; border: 2px solid #000; background: #fff; }
	.chat__log { flex: 1 1 auto; min-height: 0; overflow-y: auto; background: #f8fafc; }
	.msg { margin: 10px 16px; border: 2px solid #e2e8f0; border-left: 6px solid #94a3b8; padding: 8px 12px; }
	.msg--user { border-left-color: var(--accent); background: #ecfeff; }
	.msg__role { font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0f766e; }
	.msg__content { margin: 4px 0 0; font-size: 0.85rem; line-height: 1.55; white-space: pre-wrap; }
	.msg__tools { display: block; margin-top: 6px; font-size: 0.65rem; color: #94a3b8; }
	.chat__form { display: flex; gap: 8px; padding: 10px 16px; border-top: 2px solid #000; background: #fff; }
	.chat__input { flex: 1 1 auto; font-family: inherit; font-size: 0.85rem; padding: 8px 12px; border: 2px solid var(--accent); outline: none; }
	.chat__input:disabled { opacity: 0.5; }

	/* Code layout (dark, mirrors the MATLAB REPL) */
	.code { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }
	.code__main { flex: 1 1 auto; min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(200px, 260px); }
	@media (max-width: 720px) { .code__main { grid-template-columns: minmax(0, 1fr); } .files { display: none; } }
	.cells { flex: 1 1 auto; min-height: 0; overflow-y: auto; background: #0a0f1e; }
	.empty--code { color: #94a3b8; }
	.empty__code { margin: 8px 16px; padding: 12px; background: #050913; border: 2px solid #1e293b; border-left: 6px solid var(--accent); color: #99f6e4; font-size: 0.8rem; white-space: pre-wrap; }
	.cell { margin: 12px 16px; background: #0f172a; border: 2px solid #1e293b; border-left: 6px solid var(--accent); color: #e2e8f0; }
	.cell__head { display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: #1e293b; border-bottom: 1px solid #334155; font-size: 0.7rem; }
	.cell__no { color: var(--accent); font-weight: 700; }
	.cell__source, .cell__stdout, .cell__stderr, .cell__error, .cell__result { margin: 0; padding: 8px 12px; font-size: 0.8rem; line-height: 1.55; white-space: pre-wrap; overflow-x: auto; font-family: inherit; }
	.cell__source { background: #050913; color: #99f6e4; border-bottom: 1px dashed #1e293b; }
	.cell__stdout { color: #86efac; }
	.cell__result { color: #5eead4; }
	.cell__stderr { color: #fda4af; background: rgba(127, 29, 29, 0.2); }
	.cell__error { color: #fecaca; background: rgba(127, 29, 29, 0.4); border-top: 1px solid #b91c1c; }

	.files { background: #1e293b; color: #e2e8f0; border-left: 2px solid #000; display: flex; flex-direction: column; gap: 10px; padding: 12px; overflow-y: auto; min-height: 0; }
	.files__head { display: flex; align-items: center; justify-content: space-between; }
	.files__title { margin: 0; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent); }
	.files__count { font-size: 0.65rem; color: #64748b; }
	.file-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
	.file { display: flex; flex-direction: column; gap: 2px; width: 100%; text-align: left; background: #0f172a; border: 1px solid #334155; border-left: 4px solid var(--accent); padding: 6px 8px; cursor: pointer; font-family: inherit; color: inherit; }
	.file:hover { border-color: var(--accent); }
	.file__name { font-size: 0.78rem; font-weight: 700; color: #99f6e4; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.file__meta { font-size: 0.62rem; color: #94a3b8; }

	.prompt { padding: 10px 14px 14px; background: #0a0f1e; border-top: 2px solid #000; display: flex; flex-direction: column; gap: 8px; }
	.prompt__head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
	.prompt__caret { color: var(--accent); font-weight: 800; }
	.prompt__buttons { display: flex; gap: 6px; flex-wrap: wrap; margin-left: auto; }
	.prompt__input { width: 100%; min-height: 64px; resize: vertical; background: #050913; color: #99f6e4; border: 2px solid var(--accent); padding: 10px 12px; font-family: inherit; font-size: 0.85rem; line-height: 1.5; outline: none; }
	.prompt__input:disabled { opacity: 0.5; }

	.icon-btn { background: transparent; border: 1px solid #94a3b8; color: #475569; font-family: inherit; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; cursor: pointer; }
	.icon-btn:hover:not(:disabled) { color: var(--accent-dark); border-color: var(--accent); }
	.icon-btn:disabled { opacity: 0.5; cursor: not-allowed; }
	.files .icon-btn { color: #cbd5e1; border-color: #334155; }

	.hidden-input { position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0; }
</style>
