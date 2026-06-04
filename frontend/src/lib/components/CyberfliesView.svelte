<script lang="ts">
	import { onDestroy, onMount, tick } from 'svelte';
	import {
		Badge,
		MarkdownPreview,
		Modal,
		PixelButton,
		PixelScrollArea
	} from '@cyberdynecorp/svelte-ui-core';
	import { authVM } from '$lib/auth/authViewModel.svelte';
	import { createCyberfliesVM, type ChatScope } from '$lib/viewmodels/cyberfliesViewModel.svelte';

	type Tab = 'meetings' | 'chat' | 'channels';
	let tab = $state<Tab>('meetings');

	const meetings = createCyberfliesVM();

	let audioInputEl = $state<HTMLInputElement | null>(null);
	let chatInput = $state<string>('');
	let chatScrollBottom = $state<HTMLElement | null>(null);
	// Organize-into-channel controls (per detail panel).
	let organizeChannelId = $state<string>('');
	let newChannelName = $state<string>('');
	let creatingChannel = $state<boolean>(false);
	// Channels subview create-form.
	let channelName = $state<string>('');
	let channelDesc = $state<string>('');

	// Reusable confirmation modal (replaces the native confirm() dialog).
	let confirmOpen = $state<boolean>(false);
	let confirmTitle = $state<string>('');
	let confirmMessage = $state<string>('');
	let confirmLabel = $state<string>('Delete');
	let confirmAction = $state<(() => void | Promise<void>) | null>(null);

	function askConfirm(opts: {
		title: string;
		message: string;
		label?: string;
		action: () => void | Promise<void>;
	}) {
		confirmTitle = opts.title;
		confirmMessage = opts.message;
		confirmLabel = opts.label ?? 'Delete';
		confirmAction = opts.action;
		confirmOpen = true;
	}
	function closeConfirm() {
		confirmOpen = false;
		confirmAction = null;
	}
	async function runConfirm() {
		const action = confirmAction;
		confirmOpen = false;
		confirmAction = null;
		if (action) await action();
	}

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

	// Auto-scroll the chat log as new turns land.
	$effect(() => {
		void meetings.chatTurns.length;
		void meetings.chatSending;
		void tick().then(() =>
			chatScrollBottom?.scrollIntoView({ block: 'end', inline: 'nearest' })
		);
	});

	// Reset the organize controls + transient notice when the selected
	// meeting changes, so a stale "Added to X" doesn't carry over.
	$effect(() => {
		void meetings.selectedId;
		organizeChannelId = '';
		newChannelName = '';
		creatingChannel = false;
		meetings.clearNotice();
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

	function onDeleteRecording(id: string, title: string) {
		askConfirm({
			title: 'Delete recording',
			message: `Delete "${title}"? This removes the audio, transcript and channel membership.`,
			action: () => meetings.deleteRecording(id)
		});
	}

	async function onCreateChannel(e: SubmitEvent) {
		e.preventDefault();
		const created = await meetings.createChannel(channelName, channelDesc);
		if (created) {
			channelName = '';
			channelDesc = '';
		}
	}

	function onDeleteChannel(id: string, name: string) {
		askConfirm({
			title: 'Delete channel',
			message: `Delete the channel "${name}"? Meetings stay, but their membership in this channel is removed.`,
			action: () => meetings.deleteChannel(id)
		});
	}

	function onRemoveFromChannel(channelId: string, recordingId: string, title: string) {
		askConfirm({
			title: 'Remove from channel',
			message: `Remove "${title}" from this channel? The meeting itself is kept.`,
			label: 'Remove',
			action: () => meetings.removeFromChannel(channelId, recordingId)
		});
	}

	async function onAddToChannel(recordingId: string) {
		if (!organizeChannelId) return;
		await meetings.addToChannel(recordingId, organizeChannelId);
	}

	async function onCreateChannelAndAdd(recordingId: string) {
		const channel = await meetings.createChannel(newChannelName);
		if (!channel) return;
		newChannelName = '';
		creatingChannel = false;
		organizeChannelId = channel.id;
		await meetings.addToChannel(recordingId, channel.id);
	}

	async function onSendChat(e: SubmitEvent) {
		e.preventDefault();
		const text = chatInput;
		chatInput = '';
		await meetings.sendChat(text);
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
			Upload audio or video, get transcripts + summaries, ask questions across your meetings, and crunch
			the data in a Python sandbox.
		</p>
		<nav class="tabs" aria-label="Cyberflies sections">
			<button type="button" class="tab" class:tab--active={tab === 'meetings'} onclick={() => (tab = 'meetings')}>
				🎧 Meetings
			</button>
			<button type="button" class="tab" class:tab--active={tab === 'chat'} onclick={() => (tab = 'chat')}>
				💬 Chat
			</button>
			<button type="button" class="tab" class:tab--active={tab === 'channels'} onclick={() => (tab = 'channels')}>
				🗂 Channels
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
						accept="audio/*,video/*"
						class="hidden-input"
						bind:this={audioInputEl}
						onchange={onAudioChange}
					/>
					<PixelButton variant="solid" size="sm" onclick={pickAudio} disabled={!authReady || meetings.uploading}>
						{meetings.uploading ? 'Uploading…' : '⬆ Upload media'}
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
						<PixelButton variant="outline" size="sm" onclick={() => meetings.downloadAudio(rec.id)}>
							⬇ Download
						</PixelButton>
						<PixelButton
							variant="ghost"
							size="sm"
							onclick={() => {
								// Scope the chat to THIS meeting (POST /recordings/{id}/chat).
								meetings.setChatScope(`recording:${rec.id}`);
								chatInput = '';
								tab = 'chat';
							}}
						>
							💬 Ask about this
						</PixelButton>
						<PixelButton
							variant="ghost"
							size="sm"
							onclick={() => onDeleteRecording(rec.id, rec.summary?.headline ?? `Recording ${rec.id.slice(0, 8)}`)}
							disabled={meetings.busy}
						>
							🗑 Delete
						</PixelButton>
					</div>

					<!-- Organize into a channel -->
					<div class="organize">
						<label class="organize__label" for="cf-organize">Organize</label>
						{#if creatingChannel}
							<input
								class="organize__input"
								type="text"
								placeholder="New channel name"
								value={newChannelName}
								oninput={(e) => (newChannelName = (e.currentTarget as HTMLInputElement).value)}
							/>
							<PixelButton
								variant="solid"
								size="sm"
								onclick={() => onCreateChannelAndAdd(rec.id)}
								disabled={meetings.busy || newChannelName.trim() === ''}
							>
								Create & add
							</PixelButton>
							<PixelButton variant="ghost" size="sm" onclick={() => (creatingChannel = false)}>
								Cancel
							</PixelButton>
						{:else}
							<select
								id="cf-organize"
								class="organize__select"
								value={organizeChannelId}
								onchange={(e) => (organizeChannelId = (e.currentTarget as HTMLSelectElement).value)}
							>
								<option value="">Choose a channel…</option>
								{#each meetings.channels as ch (ch.id)}
									<option value={ch.id}>{ch.name}</option>
								{/each}
							</select>
							<PixelButton
								variant="solid"
								size="sm"
								onclick={() => onAddToChannel(rec.id)}
								disabled={meetings.busy || !organizeChannelId}
							>
								Add
							</PixelButton>
							<PixelButton variant="ghost" size="sm" onclick={() => (creatingChannel = true)}>
								＋ New channel
							</PixelButton>
						{/if}
					</div>

					{#if meetings.notice}
						<div class="banner banner--ok" role="status">{meetings.notice}</div>
					{/if}
					{#if meetings.error}
						<div class="banner banner--err">{meetings.error}</div>
					{/if}

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
					onchange={(e) =>
						meetings.setChatScope((e.currentTarget as HTMLSelectElement).value as ChatScope)}
				>
					<option value="all">All meetings</option>
					{#if meetings.selectedRecording}
						{@const sr = meetings.selectedRecording}
						<option value={`recording:${sr.id}`}>
							📄 {sr.summary?.headline ?? `Recording ${sr.id.slice(0, 8)}`}
						</option>
					{/if}
					{#each meetings.channels as ch (ch.id)}
						<option value={`channel:${ch.id}`}>🗂 {ch.name}</option>
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
							{#if turn.role === 'assistant'}
								<!-- Replies are markdown (bold, bullets, headings) — render them. -->
								<div class="msg__md"><MarkdownPreview content={turn.content} /></div>
							{:else}
								<p class="msg__content">{turn.content}</p>
							{/if}
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

	<!-- ── Channels ─────────────────────────────────────────────── -->
	{#if tab === 'channels'}
		<div class="channels-view">
			<form class="ch-create" onsubmit={onCreateChannel}>
				<h2 class="ch-create__title">Create a channel</h2>
				<div class="ch-create__row">
					<input
						class="ch-input"
						type="text"
						placeholder="Channel name"
						value={channelName}
						oninput={(e) => (channelName = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.busy}
					/>
					<input
						class="ch-input ch-input--desc"
						type="text"
						placeholder="Description (optional)"
						value={channelDesc}
						oninput={(e) => (channelDesc = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.busy}
					/>
					<PixelButton
						variant="solid"
						size="sm"
						type="submit"
						disabled={!authReady || meetings.busy || channelName.trim() === ''}
					>
						＋ Create
					</PixelButton>
				</div>
			</form>

			{#if meetings.notice}
				<div class="banner banner--ok" role="status">{meetings.notice}</div>
			{/if}
			{#if meetings.error}
				<div class="banner banner--err">{meetings.error}</div>
			{/if}

			<div class="ch-list-head">
				<h2 class="ch-list-title">Your channels <span class="ch-count">{meetings.channels.length}</span></h2>
				<button type="button" class="icon-btn" onclick={() => meetings.refreshChannels()} disabled={!authReady}>↻</button>
			</div>

			{#if meetings.channels.length === 0}
				<p class="empty">{authReady ? 'No channels yet. Create one above, then organize meetings into it from the Meetings tab.' : 'Sign in to manage channels.'}</p>
			{:else}
				<PixelScrollArea maxHeight="100%" ariaLabel="Channels">
					<ul class="ch-list">
						{#each meetings.channels as ch (ch.id)}
							{@const open = meetings.expandedChannelId === ch.id}
							<li class="ch-item">
								<div class="ch-item__head">
									<button
										type="button"
										class="ch-item__main"
										onclick={() => meetings.toggleChannel(ch.id)}
										aria-expanded={open}
									>
										<span class="ch-item__caret">{open ? '▾' : '▸'}</span>
										<span class="ch-item__name">{ch.name}</span>
										{#if ch.description}<span class="ch-item__desc">{ch.description}</span>{/if}
									</button>
									<div class="ch-item__actions">
										<PixelButton variant="outline" size="sm" onclick={() => meetings.recapChannel(ch.id)} disabled={meetings.recapLoading}>
											✨ Recap
										</PixelButton>
										<PixelButton variant="ghost" size="sm" onclick={() => onDeleteChannel(ch.id, ch.name)} disabled={meetings.busy}>
											🗑 Delete
										</PixelButton>
									</div>
								</div>

								{#if open}
									<div class="ch-body">
										{#if meetings.recapLoading}
											<p class="ch-muted">Generating recap…</p>
										{:else if meetings.channelRecap}
											<div class="ch-recap">
												<h4 class="ch-recap__headline">{meetings.channelRecap.headline}</h4>
												<div class="msg__md"><MarkdownPreview content={meetings.channelRecap.abstract} /></div>
												{#if meetings.channelRecap.bullets.length > 0}
													<ul class="bullets">
														{#each meetings.channelRecap.bullets as b}<li>{b}</li>{/each}
													</ul>
												{/if}
											</div>
										{/if}

										{#if meetings.channelContentsLoading}
											<p class="ch-muted">Loading meetings…</p>
										{:else if meetings.channelRecordings.length === 0}
											<p class="ch-muted">No meetings in this channel yet. Add some from the Meetings tab.</p>
										{:else}
											<ul class="ch-rec-list">
												{#each meetings.channelRecordings as r (r.id)}
													<li class="ch-rec">
														<span class="ch-rec__title">{r.summary?.headline ?? `Recording ${r.id.slice(0, 8)}`}</span>
														<button
															type="button"
															class="ch-rec__remove"
															onclick={() => onRemoveFromChannel(ch.id, r.id, r.summary?.headline ?? r.id)}
															disabled={meetings.busy}
															title="Remove from channel"
														>
															✕
														</button>
													</li>
												{/each}
											</ul>
										{/if}
									</div>
								{/if}
							</li>
						{/each}
					</ul>
				</PixelScrollArea>
			{/if}
		</div>
	{/if}
</div>

<!-- Styled confirmation dialog (replaces the native browser confirm()) -->
<Modal bind:open={confirmOpen} title={confirmTitle} size="sm">
	<p class="confirm__msg">{confirmMessage}</p>
	{#snippet footer()}
		<div class="confirm__actions">
			<PixelButton variant="ghost" size="sm" onclick={closeConfirm}>Cancel</PixelButton>
			<PixelButton variant="solid" size="sm" onclick={runConfirm}>{confirmLabel}</PixelButton>
		</div>
	{/snippet}
</Modal>

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
	.banner--ok { background: #d1fae5; border: 1px solid #0f766e; color: #065f46; }

	/* Channels subview */
	.channels-view { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; gap: 10px; padding: 14px 16px; overflow-y: auto; }
	.ch-create { display: flex; flex-direction: column; gap: 8px; }
	.ch-create__title { margin: 0; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0f766e; }
	.ch-create__row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
	.ch-input { font-family: inherit; font-size: 0.82rem; padding: 7px 10px; border: 2px solid #000; background: #fff; }
	.ch-input--desc { flex: 1 1 220px; min-width: 160px; }
	.ch-list-head { display: flex; align-items: center; justify-content: space-between; border-top: 1px dashed #cbd5e1; padding-top: 10px; }
	.ch-list-title { margin: 0; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0f766e; }
	.ch-count { font-size: 0.65rem; color: #94a3b8; font-weight: 600; }
	.ch-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px; }
	.ch-item { display: flex; flex-direction: column; background: #f1f5f9; border: 2px solid #e2e8f0; border-left: 6px solid var(--accent); padding: 8px 12px; }
	.ch-item__head { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
	.ch-item__main { display: flex; align-items: baseline; gap: 6px; min-width: 0; flex: 1 1 auto; background: none; border: none; padding: 0; font-family: inherit; text-align: left; cursor: pointer; color: inherit; }
	.ch-item__caret { color: var(--accent-dark); font-size: 0.7rem; }
	.ch-item__name { font-size: 0.85rem; font-weight: 700; }
	.ch-item__desc { font-size: 0.7rem; color: #64748b; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.ch-item__actions { display: flex; gap: 6px; flex-shrink: 0; }
	.ch-body { margin-top: 8px; padding-top: 8px; border-top: 1px dashed #cbd5e1; display: flex; flex-direction: column; gap: 8px; }
	.ch-muted { margin: 0; font-size: 0.75rem; color: #64748b; font-style: italic; }
	.ch-recap { background: #ecfeff; border: 1px solid #99f6e4; padding: 8px 10px; }
	.ch-recap__headline { margin: 0 0 4px; font-size: 0.82rem; font-weight: 800; color: #0f766e; }
	.ch-rec-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
	.ch-rec { display: flex; align-items: center; justify-content: space-between; gap: 8px; background: #fff; border: 1px solid #e2e8f0; padding: 5px 8px; font-size: 0.78rem; }
	.ch-rec__title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.ch-rec__remove { background: transparent; border: 1px solid #cbd5e1; color: #991b1b; width: 22px; height: 22px; cursor: pointer; flex-shrink: 0; }
	.ch-rec__remove:hover:not(:disabled) { border-color: #b91c1c; background: #fee2e2; }
	.ch-rec__remove:disabled { opacity: 0.5; cursor: not-allowed; }

	/* Confirm dialog */
	.confirm__msg { margin: 0; font-size: 0.85rem; line-height: 1.55; color: #111827; }
	.confirm__actions { display: flex; gap: 8px; justify-content: flex-end; }

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
	.organize { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; padding: 8px 0; border-top: 1px dashed #cbd5e1; border-bottom: 1px dashed #cbd5e1; }
	.organize__label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #0f766e; }
	.organize__select, .organize__input { font-family: inherit; font-size: 0.78rem; padding: 5px 8px; border: 2px solid #000; background: #fff; }
	.organize__input { min-width: 160px; }
	.block { border: 2px solid #e2e8f0; border-left: 6px solid var(--accent); padding: 10px 12px; }
	.block__title { margin: 0 0 6px; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0f766e; display: flex; justify-content: space-between; }
	.block__count { font-size: 0.65rem; color: #94a3b8; font-weight: 600; }
	.block__abstract { margin: 0 0 8px; font-size: 0.85rem; line-height: 1.55; }
	.bullets { margin: 0; padding-left: 18px; font-size: 0.82rem; line-height: 1.6; }
	/* The Foundation base.css styles every <pre> with a dark surface, so
	   set explicit light text + a defined dark panel here — otherwise the
	   transcript renders dark-on-dark and is unreadable. */
	.transcript {
		margin: 0;
		padding: 12px 14px;
		font-size: 0.82rem;
		line-height: 1.65;
		white-space: pre-wrap;
		word-break: break-word;
		font-family: inherit;
		background: #0f172a;
		color: #e2e8f0;
		border-left: 4px solid var(--accent);
	}

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
	/* Rendered-markdown assistant replies: tighten the library defaults so
	   they sit naturally in the chat bubble. */
	.msg__md { margin-top: 4px; font-size: 0.85rem; line-height: 1.55; }
	.msg__md :global(p) { margin: 0 0 8px; }
	.msg__md :global(p:last-child) { margin-bottom: 0; }
	.msg__md :global(ul),
	.msg__md :global(ol) { margin: 4px 0 8px; padding-left: 20px; }
	.msg__md :global(li) { margin: 2px 0; }
	.msg__md :global(h1),
	.msg__md :global(h2),
	.msg__md :global(h3) { font-size: 0.95rem; margin: 8px 0 4px; }
	.msg__md :global(code) { font-size: 0.8rem; }
	.msg__tools { display: block; margin-top: 6px; font-size: 0.65rem; color: #94a3b8; }
	.chat__form { display: flex; gap: 8px; padding: 10px 16px; border-top: 2px solid #000; background: #fff; }
	.chat__input { flex: 1 1 auto; font-family: inherit; font-size: 0.85rem; padding: 8px 12px; border: 2px solid var(--accent); outline: none; }
	.chat__input:disabled { opacity: 0.5; }

	.icon-btn { background: transparent; border: 1px solid #94a3b8; color: #475569; font-family: inherit; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; cursor: pointer; }
	.icon-btn:hover:not(:disabled) { color: var(--accent-dark); border-color: var(--accent); }
	.icon-btn:disabled { opacity: 0.5; cursor: not-allowed; }

	.hidden-input { position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0; }
</style>
