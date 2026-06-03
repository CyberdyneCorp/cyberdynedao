<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { authVM } from '$lib/auth/authViewModel.svelte';
	import { createWindow } from '$lib/stores/windowStore';

	// Gate: only CyberdyneAuth admins (or editor-scoped users) reach the
	// control panel. The menu entry is already hidden for everyone else,
	// but we re-check here so a direct window open can't bypass it.
	const canAccess = $derived(
		authVM.isRestored && authVM.isAuthenticated && (authVM.isAdmin || authVM.isEditor)
	);

	const identity = $derived(authVM.user?.email || authVM.user?.wallet_address || 'Unknown');
	const scopes = $derived(
		Array.isArray(authVM.user?.scopes) && authVM.user.scopes.length
			? authVM.user.scopes.join(' ')
			: '—'
	);

	// Live "expires in" readout — ticks once a minute so it stays honest
	// without a tight render loop.
	let now = $state(Date.now());
	let ticker: ReturnType<typeof setInterval> | null = null;
	onMount(() => {
		ticker = setInterval(() => (now = Date.now()), 60_000);
	});
	onDestroy(() => {
		if (ticker !== null) clearInterval(ticker);
	});

	const expiresLabel = $derived.by(() => {
		const exp = authVM.expiresAt;
		if (!exp) return 'unknown';
		const remainingMin = Math.round((exp - now) / 60_000);
		if (remainingMin <= 0) return 'expired';
		const when = new Date(exp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
		return `${remainingMin} min (at ${when})`;
	});

	interface AdminTool {
		id: string;
		title: string;
		desc: string;
		icon: string;
		content: 'admin';
	}

	// Admin surfaces reachable from the hub. Add new admin tools here as
	// they land — each opens in its own window.
	const tools: AdminTool[] = [
		{
			id: 'academy',
			title: 'Academy Admin',
			desc: 'Author, publish, and manage courses, lessons, and quizzes.',
			icon: '🎓',
			content: 'admin'
		}
	];

	function launch(tool: AdminTool): void {
		createWindow(tool.content, tool.title);
	}
</script>

<div class="sysadmin-view">
	<header class="hero">
		<span aria-hidden="true">🛡️</span>
		<div>
			<h1>System Admin</h1>
			<p>Control panel for CyberdyneAuth administrators.</p>
		</div>
	</header>

	{#if !authVM.isRestored}
		<p class="hint">Checking your session…</p>
	{:else if !canAccess}
		<p class="banner banner--warn" role="alert">
			This panel is restricted to <strong>admin</strong> accounts.
			{#if !authVM.isAuthenticated}Sign in with an admin account to continue.{/if}
		</p>
	{:else}
		<section class="card">
			<h2>Session</h2>
			<dl class="kv">
				<dt>Signed in as</dt>
				<dd>{identity}</dd>
				<dt>Access</dt>
				<dd>
					{#if authVM.isAdmin}<span class="badge badge--admin">ADMIN</span>{/if}
					{#if authVM.isEditor}<span class="badge badge--editor">EDITOR</span>{/if}
				</dd>
				<dt>Scopes</dt>
				<dd><code>{scopes}</code></dd>
				<dt>Session expires</dt>
				<dd>{expiresLabel}</dd>
			</dl>
		</section>

		<section class="card">
			<h2>Admin tools</h2>
			<ul class="tools">
				{#each tools as tool (tool.id)}
					<li>
						<button class="tool" type="button" onclick={() => launch(tool)}>
							<span class="tool__icon" aria-hidden="true">{tool.icon}</span>
							<span class="tool__text">
								<span class="tool__title">{tool.title}</span>
								<span class="tool__desc">{tool.desc}</span>
							</span>
							<span class="tool__arrow" aria-hidden="true">→</span>
						</button>
					</li>
				{/each}
			</ul>
		</section>
	{/if}
</div>

<style>
	.sysadmin-view {
		padding: 1.25rem;
		color: #e5e7eb;
		font-family: system-ui, sans-serif;
		overflow-y: auto;
		height: 100%;
	}
	.hero {
		display: flex;
		gap: 0.75rem;
		align-items: center;
		margin-bottom: 1rem;
	}
	.hero h1 {
		margin: 0;
		font-size: 1.2rem;
	}
	.hero p {
		margin: 0.15rem 0 0;
		font-size: 0.82rem;
		color: #9ca3af;
	}
	.banner {
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		font-size: 0.85rem;
		margin-bottom: 0.75rem;
	}
	.banner--warn {
		background: #78350f;
		color: #fcd34d;
	}
	.hint {
		font-size: 0.85rem;
		color: #9ca3af;
	}
	.card {
		background: #111827;
		border: 1px solid #1f2937;
		border-radius: 8px;
		padding: 0.85rem 1rem;
		margin-bottom: 1rem;
	}
	.card h2 {
		margin: 0 0 0.6rem;
		font-size: 1rem;
	}
	.kv {
		display: grid;
		grid-template-columns: max-content 1fr;
		gap: 0.4rem 1rem;
		margin: 0;
		font-size: 0.85rem;
	}
	.kv dt {
		color: #9ca3af;
	}
	.kv dd {
		margin: 0;
		word-break: break-word;
	}
	.kv code {
		background: #0b1220;
		border: 1px solid #1f2937;
		border-radius: 4px;
		padding: 0.05rem 0.35rem;
		font-size: 0.8rem;
	}
	.badge {
		display: inline-block;
		font-size: 0.68rem;
		font-weight: 700;
		letter-spacing: 0.05em;
		padding: 0.1rem 0.4rem;
		border-radius: 4px;
		margin-right: 0.35rem;
	}
	.badge--admin {
		background: #1d4ed8;
		color: #fff;
	}
	.badge--editor {
		background: #065f46;
		color: #d1fae5;
	}
	.tools {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.tool {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		width: 100%;
		text-align: left;
		background: #0b1220;
		border: 1px solid #1f2937;
		border-radius: 6px;
		padding: 0.6rem 0.75rem;
		color: #e5e7eb;
		font: inherit;
		cursor: pointer;
	}
	.tool:hover {
		border-color: #2563eb;
		background: #0e1729;
	}
	.tool__icon {
		font-size: 1.3rem;
	}
	.tool__text {
		display: flex;
		flex-direction: column;
		flex: 1;
	}
	.tool__title {
		font-weight: 600;
	}
	.tool__desc {
		font-size: 0.78rem;
		color: #9ca3af;
	}
	.tool__arrow {
		color: #6b7280;
	}
</style>
