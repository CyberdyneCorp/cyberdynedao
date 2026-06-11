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
	import { CYBERFLIES_MCP_URL, type MeetingPlatform } from '$lib/api/cyberfliesApi';

	type Tab = 'meetings' | 'chat' | 'channels' | 'bot' | 'agent' | 'apikeys';
	let tab = $state<Tab>('meetings');

	const meetings = createCyberfliesVM();

	let audioInputEl = $state<HTMLInputElement | null>(null);
	let chatInput = $state<string>('');
	let chatScrollBottom = $state<HTMLElement | null>(null);
	// Bot tab: send-to-meeting form.
	let botPlatform = $state<MeetingPlatform>('google_meet');
	let botUrl = $state<string>('');
	let botName = $state<string>('');
	let botConsent = $state<string>('');
	let botCaptureVideo = $state<boolean>(false);

	// Inline media playback for the selected recording (presigned URL on demand).
	let mediaSrc = $state<string | null>(null);
	let mediaKind = $state<string>('audio');
	let mediaLoading = $state<boolean>(false);
	// Reset the player whenever the selected recording changes.
	$effect(() => {
		meetings.selectedId;
		mediaSrc = null;
	});
	async function onPlayMedia(id: string, kind: string) {
		mediaLoading = true;
		const url = await meetings.mediaUrl(id);
		mediaLoading = false;
		if (url) {
			mediaKind = kind;
			mediaSrc = url;
		}
	}
	function clockFromSeconds(s: number): string {
		const m = Math.floor(s / 60);
		const sec = Math.floor(s % 60);
		return `${m}:${sec.toString().padStart(2, '0')}`;
	}

	// Inline channel rename.
	let renamingId = $state<string | null>(null);
	let renameValue = $state<string>('');
	function startRename(id: string, name: string) {
		renamingId = id;
		renameValue = name;
	}
	async function saveRename(id: string) {
		await meetings.renameChannel(id, renameValue);
		if (!meetings.error) renamingId = null;
	}

	// Agent-tools tab: MCP server registration form.
	let mcpName = $state<string>('');
	let mcpUrl = $state<string>('');
	let mcpToken = $state<string>('');
	async function onAddMcp(e: SubmitEvent) {
		e.preventDefault();
		await meetings.addMcpServer(mcpName, mcpUrl, mcpToken);
		if (!meetings.mcpError) {
			mcpName = '';
			mcpUrl = '';
			mcpToken = '';
		}
	}
	// API-keys tab: create-key form + copy feedback.
	let apiKeyName = $state<string>('');
	// The one-time-secret modal mirrors the VM's `newApiKeyToken`. Opening is
	// driven by the VM; closing (X / backdrop / Done) clears the secret so it
	// can't be reopened.
	let tokenModalOpen = $state<boolean>(false);
	$effect(() => {
		if (meetings.newApiKeyToken !== null) tokenModalOpen = true;
	});
	$effect(() => {
		if (!tokenModalOpen && meetings.newApiKeyToken !== null) meetings.clearNewApiKeyToken();
	});
	async function onCreateApiKey(e: SubmitEvent) {
		e.preventDefault();
		const token = await meetings.createApiKey(apiKeyName);
		if (token) apiKeyName = '';
	}
	function onRevokeApiKey(id: string, name: string) {
		askConfirm({
			title: 'Revoke API key',
			message: `Revoke "${name}"? Any Claude/ChatGPT connection using it stops working immediately. This can't be undone.`,
			label: 'Revoke',
			action: () => meetings.revokeApiKey(id)
		});
	}

	// Generic "copy to clipboard" with transient per-key feedback.
	let copiedKey = $state<string | null>(null);
	let copyTimer: ReturnType<typeof setTimeout> | null = null;
	async function copyToClipboard(text: string, marker: string) {
		try {
			await navigator.clipboard.writeText(text);
			copiedKey = marker;
			if (copyTimer) clearTimeout(copyTimer);
			copyTimer = setTimeout(() => (copiedKey = null), 2000);
		} catch {
			/* clipboard blocked (insecure context / permissions) — no-op */
		}
	}

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
			void meetings.refreshMeetingSessions();
		}
	});

	onDestroy(() => {
		if (copyTimer) clearTimeout(copyTimer);
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

	async function onSendBot(e: SubmitEvent) {
		e.preventDefault();
		await meetings.joinMeeting({
			platform: botPlatform,
			meeting_url: botUrl,
			bot_display_name: botName,
			consent_message: botConsent,
			capture_video: botCaptureVideo
		});
		if (!meetings.botError) botUrl = '';
	}

	async function onViewRecording(recordingId: string) {
		await meetings.refreshRecordings();
		meetings.selectRecording(recordingId);
		tab = 'meetings';
	}

	function platformLabel(p: string): string {
		if (p === 'google_meet') return 'Google Meet';
		if (p === 'microsoft_teams') return 'Microsoft Teams';
		return p;
	}

	function botStatusVariant(status: string): 'success' | 'warning' | 'danger' {
		const s = status.toLowerCase();
		if (s === 'completed') return 'success';
		if (s === 'failed') return 'danger';
		return 'warning';
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
			<button type="button" class="tab" class:tab--active={tab === 'bot'} onclick={() => (tab = 'bot')}>
				🤖 Bot
			</button>
			<button type="button" class="tab" class:tab--active={tab === 'agent'} onclick={() => { tab = 'agent'; void meetings.refreshMcpServers(); }}>
				🔌 Agent tools
			</button>
			<button type="button" class="tab" class:tab--active={tab === 'apikeys'} onclick={() => { tab = 'apikeys'; void meetings.refreshApiKeys(); }}>
				🔑 API keys
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
						{#if rec.media?.available}
							<PixelButton
								variant="outline"
								size="sm"
								disabled={mediaLoading}
								onclick={() => onPlayMedia(rec.id, rec.media?.kind ?? 'audio')}
							>
								{mediaLoading ? 'Loading…' : mediaSrc ? '↻ Reload' : '▶ Play'}
							</PixelButton>
						{/if}
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

					{#if mediaSrc}
						<div class="player">
							{#if mediaKind === 'video'}
								<!-- svelte-ignore a11y_media_has_caption -->
								<video class="player__el" src={mediaSrc} controls></video>
							{:else}
								<audio class="player__el" src={mediaSrc} controls></audio>
							{/if}
						</div>
					{/if}

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
							{#if rec.summary.action_items && rec.summary.action_items.length > 0}
								<h4 class="block__subtitle">✅ Action items</h4>
								<ul class="actions">
									{#each rec.summary.action_items as item}
										<li>
											<span class="actions__text">{item.text}</span>
											{#if item.assignee}<span class="actions__who">{item.assignee}</span>{/if}
										</li>
									{/each}
								</ul>
							{/if}
						</section>
					{/if}

					{#if rec.transcription}
						<section class="block">
							<h3 class="block__title">Transcript <span class="block__count">{rec.transcription.word_count} words</span></h3>
							<PixelScrollArea maxHeight="320px" ariaLabel="Transcript">
								{#if rec.transcription.segments && rec.transcription.segments.length > 0}
									<ol class="segments">
										{#each rec.transcription.segments as seg}
											<li class="segment">
												<span class="segment__t">{clockFromSeconds(seg.start)}</span>
												<span class="segment__text">{seg.text}</span>
											</li>
										{/each}
									</ol>
								{:else}
									<pre class="transcript">{rec.transcription.text}</pre>
								{/if}
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
									{#if renamingId === ch.id}
										<input
											class="ch-input ch-rename"
											value={renameValue}
											oninput={(e) => (renameValue = (e.currentTarget as HTMLInputElement).value)}
											onkeydown={(e) => { if (e.key === 'Enter') void saveRename(ch.id); if (e.key === 'Escape') renamingId = null; }}
											aria-label="New channel name"
										/>
										<div class="ch-item__actions">
											<PixelButton variant="solid" size="sm" onclick={() => saveRename(ch.id)} disabled={meetings.busy || renameValue.trim() === ''}>Save</PixelButton>
											<PixelButton variant="ghost" size="sm" onclick={() => (renamingId = null)}>Cancel</PixelButton>
										</div>
									{:else}
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
											<PixelButton variant="ghost" size="sm" onclick={() => startRename(ch.id, ch.name)} disabled={meetings.busy}>
												✏️ Rename
											</PixelButton>
											<PixelButton variant="outline" size="sm" onclick={() => meetings.recapChannel(ch.id)} disabled={meetings.recapLoading}>
												✨ Recap
											</PixelButton>
											<PixelButton variant="ghost" size="sm" onclick={() => onDeleteChannel(ch.id, ch.name)} disabled={meetings.busy}>
												🗑 Delete
											</PixelButton>
										</div>
									{/if}
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

	<!-- ── Bot (meeting capture) ────────────────────────────────── -->
	{#if tab === 'bot'}
		<div class="bot-view">
			<form class="bot-form" onsubmit={onSendBot}>
				<h2 class="bot-form__title">Send the bot to a meeting</h2>
				<p class="bot-form__hint">
					A capture bot joins your Google Meet / Microsoft Teams call, records it, and the
					recording lands in your Meetings list — transcribed and summarized like an upload.
				</p>
				<div class="bot-form__row">
					<select
						class="ch-input"
						value={botPlatform}
						onchange={(e) => (botPlatform = (e.currentTarget as HTMLSelectElement).value as MeetingPlatform)}
						disabled={!authReady || meetings.sendingBot}
					>
						<option value="google_meet">Google Meet</option>
						<option value="microsoft_teams">Microsoft Teams</option>
					</select>
					<input
						class="ch-input ch-input--desc"
						type="url"
						placeholder="Meeting URL (https://meet.google.com/… or Teams link)"
						value={botUrl}
						oninput={(e) => (botUrl = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.sendingBot}
					/>
				</div>
				<div class="bot-form__row">
					<input
						class="ch-input"
						type="text"
						placeholder="Bot display name (optional)"
						value={botName}
						oninput={(e) => (botName = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.sendingBot}
					/>
					<input
						class="ch-input ch-input--desc"
						type="text"
						placeholder="Consent message posted in chat (optional)"
						value={botConsent}
						oninput={(e) => (botConsent = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.sendingBot}
					/>
					<PixelButton
						variant="solid"
						size="sm"
						type="submit"
						disabled={!authReady || meetings.sendingBot || botUrl.trim() === ''}
					>
						{meetings.sendingBot ? 'Sending…' : '🤖 Send bot'}
					</PixelButton>
				</div>
				<label class="bot-form__video">
					<input
						type="checkbox"
						checked={botCaptureVideo}
						onchange={(e) => (botCaptureVideo = (e.currentTarget as HTMLInputElement).checked)}
						disabled={!authReady || meetings.sendingBot}
					/>
					🎥 Capture video (record the screen, not just audio)
				</label>
			</form>

			{#if meetings.botError}
				<div class="banner banner--err">{meetings.botError}</div>
			{/if}

			<div class="ch-list-head">
				<h2 class="ch-list-title">
					Bot sessions <span class="ch-count">{meetings.meetingSessions.length}</span>
				</h2>
				<button type="button" class="icon-btn" onclick={() => meetings.refreshMeetingSessions()} disabled={!authReady || meetings.sessionsLoading}>
					{meetings.sessionsLoading ? '…' : '↻'}
				</button>
			</div>

			{#if meetings.meetingSessions.length === 0}
				<p class="empty">{authReady ? 'No bot sessions yet. Paste a meeting link above and send the bot.' : 'Sign in to dispatch the capture bot.'}</p>
			{:else}
				<PixelScrollArea maxHeight="100%" ariaLabel="Bot sessions">
					<ul class="sess-list">
						{#each meetings.meetingSessions as s (s.id)}
							<li class="sess">
								<div class="sess__top">
									<span class="sess__platform">{platformLabel(s.platform)}</span>
									<Badge variant={botStatusVariant(s.status)} size="sm">{s.status}</Badge>
								</div>
								<a class="sess__url" href={s.meeting_url} target="_blank" rel="noopener">{s.meeting_url}</a>
								<div class="sess__meta">
									{formatDate(s.started_at ?? s.created_at)}
									{#if s.bot_display_name} · as “{s.bot_display_name}”{/if}
								</div>
								{#if s.error}
									<div class="banner banner--err">{s.error}</div>
								{/if}
								<div class="sess__actions">
									{#if s.status.toLowerCase() === 'completed' && s.recording_id}
										<PixelButton variant="outline" size="sm" onclick={() => onViewRecording(s.recording_id!)}>
											🎧 View recording
										</PixelButton>
									{/if}
									<PixelButton
										variant="ghost"
										size="sm"
										onclick={() => meetings.removeMeetingSession(s.id)}
										disabled={!authReady}
									>
										🗑 Remove
									</PixelButton>
								</div>
							</li>
						{/each}
					</ul>
				</PixelScrollArea>
			{/if}
		</div>
	{/if}

	<!-- ── Agent tools (MCP servers) ────────────────────────────── -->
	{#if tab === 'agent'}
		<div class="bot">
			<header class="bot__intro">
				<h2 class="bot__title">🔌 Agent tools (MCP servers)</h2>
				<p class="bot__lead">
					Connect MCP servers so the meeting agent can call extra tools when you chat with your
					meetings. Disabled servers stay registered but aren't used.
				</p>
			</header>

			<form class="bot-form" onsubmit={onAddMcp}>
				<div class="bot-form__row">
					<input
						class="ch-input"
						type="text"
						placeholder="Name (e.g. Jira)"
						value={mcpName}
						oninput={(e) => (mcpName = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.mcpLoading}
					/>
					<input
						class="ch-input ch-input--desc"
						type="url"
						placeholder="Server URL (https://…/mcp)"
						value={mcpUrl}
						oninput={(e) => (mcpUrl = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.mcpLoading}
					/>
				</div>
				<div class="bot-form__row">
					<input
						class="ch-input ch-input--desc"
						type="password"
						placeholder="Auth token (optional)"
						value={mcpToken}
						oninput={(e) => (mcpToken = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.mcpLoading}
					/>
					<PixelButton
						variant="solid"
						size="sm"
						type="submit"
						disabled={!authReady || meetings.mcpLoading || mcpName.trim() === '' || mcpUrl.trim() === ''}
					>
						{meetings.mcpLoading ? 'Saving…' : '+ Add server'}
					</PixelButton>
				</div>
			</form>

			{#if meetings.mcpError}
				<div class="banner banner--err">{meetings.mcpError}</div>
			{/if}

			{#if meetings.mcpServers.length === 0}
				<p class="empty">No MCP servers yet. Add one above to extend the meeting agent.</p>
			{:else}
				<ul class="mcp-list">
					{#each meetings.mcpServers as srv (srv.id)}
						<li class="mcp" class:mcp--off={!srv.enabled}>
							<div class="mcp__main">
								<span class="mcp__name">{srv.name}</span>
								<span class="mcp__url">{srv.url}</span>
								{#if srv.has_auth_token}<span class="mcp__auth">🔑 auth</span>{/if}
							</div>
							<div class="mcp__actions">
								<label class="toggle">
									<input
										type="checkbox"
										checked={srv.enabled}
										onchange={(e) => meetings.toggleMcpServer(srv.id, (e.currentTarget as HTMLInputElement).checked)}
									/>
									{srv.enabled ? 'Enabled' : 'Disabled'}
								</label>
								<PixelButton variant="ghost" size="sm" onclick={() => meetings.removeMcpServer(srv.id)}>
									Delete
								</PixelButton>
							</div>
						</li>
					{/each}
				</ul>
			{/if}
		</div>
	{/if}

	<!-- ── API keys (connect Claude / ChatGPT via MCP) ──────────────── -->
	{#if tab === 'apikeys'}
		<div class="keys-view">
			<header class="bot__intro">
				<h2 class="bot__title">🔑 API keys</h2>
				<p class="bot__lead">
					Create a personal API key to connect <strong>Cyberflies as an MCP server</strong> inside
					Claude or ChatGPT — then ask them to search, list and read your meeting transcripts. The
					same key also works for the mobile app and scripts. Keys are read-only and scoped to you.
				</p>
			</header>

			<form class="bot-form" onsubmit={onCreateApiKey}>
				<div class="bot-form__row">
					<input
						class="ch-input ch-input--desc"
						type="text"
						maxlength="128"
						placeholder="Key name (e.g. Claude Desktop)"
						value={apiKeyName}
						oninput={(e) => (apiKeyName = (e.currentTarget as HTMLInputElement).value)}
						disabled={!authReady || meetings.apiKeysLoading}
					/>
					<PixelButton
						variant="solid"
						size="sm"
						type="submit"
						disabled={!authReady || meetings.apiKeysLoading || apiKeyName.trim() === ''}
					>
						{meetings.apiKeysLoading ? 'Creating…' : '+ Create key'}
					</PixelButton>
				</div>
			</form>

			{#if meetings.apiKeyError}
				<div class="banner banner--err">{meetings.apiKeyError}</div>
			{/if}

			{#if meetings.apiKeys.length === 0}
				<p class="empty">{authReady ? 'No API keys yet. Create one above to connect Claude or ChatGPT.' : 'Sign in to manage API keys.'}</p>
			{:else}
				<ul class="key-list">
					{#each meetings.apiKeys as k (k.id)}
						<li class="key" class:key--revoked={k.revoked}>
							<div class="key__main">
								<span class="key__name">{k.name}</span>
								<code class="key__prefix">{k.prefix}…</code>
								{#if k.revoked}<span class="key__badge">revoked</span>{/if}
							</div>
							<div class="key__meta">
								Created {formatDate(k.created_at)}
								· {k.last_used_at ? `last used ${formatDate(k.last_used_at)}` : 'never used'}
							</div>
							{#if !k.revoked}
								<div class="key__actions">
									<PixelButton variant="ghost" size="sm" onclick={() => onRevokeApiKey(k.id, k.name)} disabled={meetings.apiKeysLoading}>
										🗑 Revoke
									</PixelButton>
								</div>
							{/if}
						</li>
					{/each}
				</ul>
			{/if}

			<!-- How to connect -->
			<section class="howto">
				<h3 class="howto__title">Connect to Claude or ChatGPT</h3>
				<div class="howto__url">
					<span class="howto__url-label">MCP server URL</span>
					<div class="howto__url-row">
						<code class="howto__code">{CYBERFLIES_MCP_URL}</code>
						<button type="button" class="copy-btn" onclick={() => copyToClipboard(CYBERFLIES_MCP_URL, 'mcp-url')}>
							{copiedKey === 'mcp-url' ? '✓ Copied' : '⧉ Copy'}
						</button>
					</div>
				</div>

				<div class="howto__cols">
					<div class="howto__card">
						<h4>Claude (Desktop / Code)</h4>
						<ol>
							<li>Create an API key above and copy the secret.</li>
							<li>Open <strong>Settings → Connectors</strong> (or add a custom MCP server).</li>
							<li>Add a remote server with the URL above.</li>
							<li>For auth, choose <strong>Bearer token</strong> and paste your API key.</li>
							<li>Ask Claude: <em>“Search my Cyberflies meetings for …”</em></li>
						</ol>
						<p class="howto__hint">
							Claude Code CLI:
							<code>claude mcp add --transport http cyberflies {CYBERFLIES_MCP_URL} --header "Authorization: Bearer YOUR_KEY"</code>
						</p>
					</div>
					<div class="howto__card">
						<h4>ChatGPT</h4>
						<ol>
							<li>Create an API key above and copy the secret.</li>
							<li>Open <strong>Settings → Connectors → Add</strong> (custom MCP / developer mode).</li>
							<li>Paste the MCP server URL above.</li>
							<li>Set authentication to <strong>Bearer</strong> and paste your API key.</li>
							<li>Enable the connector in a chat, then ask about your meetings.</li>
						</ol>
						<p class="howto__hint">
							Available tools: <code>list_recordings</code>, <code>search_recordings</code>,
							<code>get_recording</code> (read-only).
						</p>
					</div>
				</div>
			</section>
		</div>
	{/if}
</div>

<!-- One-time secret: shown ONCE right after a key is created. -->
<Modal bind:open={tokenModalOpen} title="Copy your API key now" size="md">
	<p class="confirm__msg">
		This is the only time the full key is shown. Copy it and store it somewhere safe —
		you can't see it again. If you lose it, revoke it and create a new one.
	</p>
	{#if meetings.newApiKeyToken}
		<div class="howto__url-row token-row">
			<code class="howto__code token-code">{meetings.newApiKeyToken}</code>
			<button type="button" class="copy-btn" onclick={() => copyToClipboard(meetings.newApiKeyToken!, 'new-token')}>
				{copiedKey === 'new-token' ? '✓ Copied' : '⧉ Copy'}
			</button>
		</div>
	{/if}
	{#snippet footer()}
		<div class="confirm__actions">
			<PixelButton variant="solid" size="sm" onclick={() => (tokenModalOpen = false)}>Done</PixelButton>
		</div>
	{/snippet}
</Modal>

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
	.hero__brand { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
	.hero__mark { font-size: 1.4rem; }
	.hero__title { font-size: 1.25rem; font-weight: 800; margin: 0; letter-spacing: 0.12em; }
	.hero__chip {
		font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
		background: rgba(0, 0, 0, 0.4); color: #ccfbf1; padding: 3px 8px; border: 1.5px solid #000;
	}
	.hero__tagline { margin: 6px 0 12px; font-size: 0.8125rem; line-height: 1.55; color: #d1faf4; }
	/* Scroll the tab row horizontally within its own width on narrow windows
	   (phones/iPads) instead of letting 6 tabs push the window body wider than
	   the viewport. On desktop all tabs fit, so no scrollbar appears. */
	.tabs {
		display: flex;
		gap: 4px;
		max-width: 100%;
		overflow-x: auto;
		-webkit-overflow-scrolling: touch;
		scrollbar-width: none;
	}
	.tabs::-webkit-scrollbar { display: none; }
	.tab {
		flex: 0 0 auto;
		white-space: nowrap;
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

	/* Bot subview */
	.bot-view { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; gap: 10px; padding: 14px 16px; overflow-y: auto; }
	.bot-form { display: flex; flex-direction: column; gap: 8px; }
	.bot-form__title { margin: 0; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0f766e; }
	.bot-form__hint { margin: 0; font-size: 0.72rem; color: #64748b; line-height: 1.5; }
	.bot-form__row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
	.sess-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px; }
	.sess { display: flex; flex-direction: column; gap: 4px; background: #f1f5f9; border: 2px solid #e2e8f0; border-left: 6px solid var(--accent); padding: 8px 12px; }
	.sess__top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
	.sess__platform { font-size: 0.82rem; font-weight: 700; }
	.sess__url { font-size: 0.72rem; color: #0f766e; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.sess__meta { font-size: 0.68rem; color: #64748b; }
	.sess__actions { display: flex; gap: 6px; margin-top: 2px; }

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
	.block__subtitle { margin: 12px 0 6px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: #0f766e; }
	.actions { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
	.actions li { display: flex; align-items: baseline; gap: 8px; font-size: 0.82rem; line-height: 1.5; }
	.actions li::before { content: '☐'; color: #0f766e; }
	.actions__text { flex: 1; }
	.actions__who { font-size: 0.72rem; font-weight: 700; color: #0f766e; background: #ccfbf1; border-radius: 999px; padding: 1px 8px; white-space: nowrap; }
	.bot-form__video { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #374151; margin-top: 8px; cursor: pointer; }
	.toggle { display: inline-flex; align-items: center; gap: 6px; font-size: 0.78rem; color: #374151; cursor: pointer; }
	.mcp-list { list-style: none; margin: 12px 0 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
	.mcp { display: flex; align-items: center; justify-content: space-between; gap: 12px; background: #ffffff; border: 2px solid #000; border-radius: 8px; padding: 10px 12px; }
	.mcp--off { opacity: 0.6; }
	.mcp__main { display: flex; align-items: baseline; gap: 8px; min-width: 0; flex-wrap: wrap; }
	.mcp__name { font-weight: 700; font-size: 0.9rem; }
	.mcp__url { font-size: 0.75rem; color: #6b7280; overflow: hidden; text-overflow: ellipsis; }
	.mcp__auth { font-size: 0.7rem; color: #0f766e; }
	.mcp__actions { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
	.player { margin: 10px 0; }
	.player__el { width: 100%; border-radius: 8px; background: #000; }
	.segments { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
	.segment { display: flex; gap: 10px; font-size: 0.82rem; line-height: 1.5; }
	.segment__t { flex-shrink: 0; font-variant-numeric: tabular-nums; color: #0f766e; font-weight: 700; min-width: 42px; }
	.segment__text { flex: 1; }
	.ch-rename { flex: 1; }
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

	/* API keys subview */
	.keys-view { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; gap: 12px; padding: 14px 16px; overflow-y: auto; }
	.key-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
	.key { display: flex; flex-direction: column; gap: 4px; background: #ffffff; border: 2px solid #000; border-radius: 8px; padding: 10px 12px; }
	.key--revoked { opacity: 0.55; }
	.key__main { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
	.key__name { font-weight: 700; font-size: 0.9rem; }
	.key__prefix { font-size: 0.75rem; color: #6b7280; background: #f1f5f9; padding: 1px 6px; border-radius: 4px; }
	.key__badge { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; color: #991b1b; background: #fee2e2; border: 1px solid #b91c1c; padding: 1px 6px; }
	.key__meta { font-size: 0.68rem; color: #64748b; }
	.key__actions { display: flex; gap: 6px; margin-top: 2px; }

	/* How-to (connect to Claude / ChatGPT) */
	.howto { border-top: 2px solid #000; padding-top: 12px; display: flex; flex-direction: column; gap: 12px; }
	.howto__title { margin: 0; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: #0f766e; }
	.howto__url { display: flex; flex-direction: column; gap: 4px; }
	.howto__url-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #0f766e; }
	.howto__url-row { display: flex; gap: 8px; align-items: stretch; flex-wrap: wrap; }
	.howto__code { flex: 1 1 280px; min-width: 0; font-size: 0.78rem; background: #0f172a; color: #5eead4; padding: 8px 10px; border-radius: 6px; word-break: break-all; }
	.copy-btn { font-family: inherit; font-size: 0.72rem; font-weight: 700; background: var(--accent); color: #fff; border: 2px solid #000; padding: 6px 12px; cursor: pointer; white-space: nowrap; }
	.copy-btn:hover { background: var(--accent-dark); }
	.howto__cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }
	.howto__card { background: #f1f5f9; border: 2px solid #e2e8f0; border-left: 6px solid var(--accent); padding: 10px 12px; }
	.howto__card h4 { margin: 0 0 8px; font-size: 0.82rem; font-weight: 800; color: #0f766e; }
	.howto__card ol { margin: 0; padding-left: 18px; font-size: 0.8rem; line-height: 1.6; }
	.howto__card li { margin: 2px 0; }
	.howto__card em { color: #0f766e; font-style: italic; }
	.howto__hint { margin: 8px 0 0; font-size: 0.72rem; color: #64748b; line-height: 1.5; }
	.howto__hint code { font-size: 0.7rem; background: #e2e8f0; padding: 1px 4px; border-radius: 3px; word-break: break-all; }
	.token-row { margin-top: 10px; }
	.token-code { color: #fde68a; }
</style>
