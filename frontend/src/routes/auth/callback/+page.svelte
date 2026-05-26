<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authVM } from '$lib/auth/authViewModel.svelte';

	let status = $state<'working' | 'error'>('working');
	let detail = $state<string>('Completing sign-in…');

	function parseFragment(): { access?: string; refresh?: string; error?: string } {
		if (typeof window === 'undefined') return {};
		// Hash arrives as `#access_token=…&refresh_token=…&token_type=bearer`
		const raw = window.location.hash.replace(/^#/, '');
		if (!raw) return {};
		const params = new URLSearchParams(raw);
		return {
			access: params.get('access_token') ?? undefined,
			refresh: params.get('refresh_token') ?? undefined,
			error: params.get('error') ?? undefined
		};
	}

	onMount(async () => {
		const { access, refresh, error } = parseFragment();
		if (error) {
			status = 'error';
			detail = `Sign-in cancelled: ${error}`;
			return;
		}
		if (!access || !refresh) {
			status = 'error';
			detail = 'No tokens in callback URL. Try signing in again.';
			return;
		}
		try {
			await authVM.installSession(access, refresh);
			// Strip the fragment from the URL bar before redirecting so
			// the tokens never linger in the browser's history.
			history.replaceState(null, '', '/');
			await goto('/', { replaceState: true });
		} catch (e) {
			status = 'error';
			detail = e instanceof Error ? e.message : 'Could not install session.';
		}
	});
</script>

<svelte:head>
	<title>Signing in — Cyberdyne</title>
</svelte:head>

<main class="callback">
	<div class="card" class:card--error={status === 'error'}>
		<h1 class="card__title">
			{status === 'working' ? '⏳ SIGNING IN' : '⚠ SIGN-IN FAILED'}
		</h1>
		<p class="card__detail">{detail}</p>
		{#if status === 'error'}
			<a class="card__link" href="/">← Back to Cyberdyne</a>
		{/if}
	</div>
</main>

<style>
	.callback {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #0a0f1e;
		color: #e0e7ff;
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		padding: 24px;
	}
	.card {
		position: relative;
		max-width: 480px;
		width: 100%;
		background: #ffffff;
		color: #111827;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 22px 22px 22px 30px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: #3b82f6;
		border-right: 2px solid #000;
	}
	.card--error::before { background: #ef4444; }
	.card__title {
		font-size: 1.1rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		margin: 0;
		color: #1d4ed8;
	}
	.card--error .card__title { color: #b91c1c; }
	.card__detail { margin: 0; font-size: 0.9rem; line-height: 1.55; }
	.card__link {
		align-self: flex-start;
		font-size: 0.8125rem;
		color: #1d4ed8;
		text-decoration: underline;
	}
</style>
