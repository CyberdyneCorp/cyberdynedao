<script lang="ts">
	import { page } from '$app/stores';
	import { LEGAL_ENTITY, CNPJ, POLICY_LAST_UPDATED } from '$lib/constants/company';

	let { children } = $props();

	const links = [
		{ href: '/welcome', label: 'Product' },
		{ href: '/privacy', label: 'Privacy' },
		{ href: '/support', label: 'Support' }
	];

	// Highlight the active tab (works with the SvelteKit relative-paths base).
	let current = $derived($page.url.pathname.replace(/\/$/, ''));
</script>

<div class="shell">
	<header>
		<a class="brand" href="/">CYBERDYNE<span class="blink">_</span></a>
		<nav aria-label="Public pages">
			{#each links as link (link.href)}
				<a href={link.href} aria-current={current === link.href ? 'page' : undefined}>
					{link.label}
				</a>
			{/each}
		</nav>
	</header>

	<main>
		{@render children?.()}
	</main>

	<footer>
		<p>
			© {POLICY_LAST_UPDATED.slice(0, 4)}
			{LEGAL_ENTITY} · CNPJ {CNPJ}
		</p>
		<p class="foot-links">
			<a href="/">Home</a> · <a href="/privacy">Privacy Policy</a> ·
			<a href="/support">Support</a>
		</p>
	</footer>
</div>

<style>
	.shell {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
		background: #0a0e0a;
		color: #cfe8cf;
		font-family:
			'IBM Plex Mono', ui-monospace, 'SFMono-Regular', 'Courier New', monospace;
		line-height: 1.65;
	}

	header {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem 1.5rem;
		align-items: baseline;
		justify-content: space-between;
		padding: 1.25rem clamp(1rem, 5vw, 3rem);
		border-bottom: 1px solid #1e3a1e;
		position: sticky;
		top: 0;
		background: rgba(10, 14, 10, 0.92);
		backdrop-filter: blur(6px);
	}

	.brand {
		font-weight: 700;
		letter-spacing: 0.12em;
		color: #4ade80;
		text-decoration: none;
		font-size: 1.05rem;
	}

	.blink {
		animation: blink 1.1s step-end infinite;
	}

	@keyframes blink {
		50% {
			opacity: 0;
		}
	}

	nav {
		display: flex;
		gap: 1.25rem;
	}

	nav a {
		color: #9fce9f;
		text-decoration: none;
		font-size: 0.9rem;
		padding-bottom: 2px;
		border-bottom: 1px solid transparent;
	}

	nav a:hover,
	nav a[aria-current='page'] {
		color: #4ade80;
		border-bottom-color: #4ade80;
	}

	main {
		flex: 1;
		width: 100%;
		max-width: 52rem;
		margin: 0 auto;
		padding: clamp(1.75rem, 5vw, 3.5rem) clamp(1rem, 5vw, 3rem) 4rem;
	}

	footer {
		border-top: 1px solid #1e3a1e;
		padding: 1.5rem clamp(1rem, 5vw, 3rem);
		font-size: 0.8rem;
		color: #7fae7f;
		text-align: center;
	}

	.foot-links {
		margin-top: 0.35rem;
	}

	footer a {
		color: #9fce9f;
		text-decoration: none;
	}

	footer a:hover {
		color: #4ade80;
		text-decoration: underline;
	}

	@media (prefers-reduced-motion: reduce) {
		.blink {
			animation: none;
		}
	}

	/* Shared document typography for the child pages (rendered outside this
	   component's scope, hence :global). Tuned for readable long-form legal
	   and support copy. */
	:global(.prose h1) {
		color: #4ade80;
		font-size: clamp(1.6rem, 4vw, 2.2rem);
		letter-spacing: 0.02em;
		margin: 0 0 0.5rem;
	}

	:global(.prose h2) {
		color: #86efac;
		font-size: 1.2rem;
		margin: 2.25rem 0 0.75rem;
		padding-bottom: 0.3rem;
		border-bottom: 1px solid #1e3a1e;
	}

	:global(.prose h3) {
		color: #9fce9f;
		font-size: 1rem;
		margin: 1.5rem 0 0.5rem;
	}

	:global(.prose p),
	:global(.prose li) {
		color: #cfe8cf;
	}

	:global(.prose ul) {
		padding-left: 1.25rem;
		margin: 0.5rem 0 1rem;
	}

	:global(.prose li) {
		margin: 0.35rem 0;
	}

	:global(.prose a) {
		color: #4ade80;
		text-decoration: underline;
		text-underline-offset: 2px;
	}

	:global(.prose strong) {
		color: #eafff0;
	}

	:global(.prose table) {
		width: 100%;
		border-collapse: collapse;
		margin: 1rem 0 1.5rem;
		font-size: 0.88rem;
		display: block;
		overflow-x: auto;
	}

	:global(.prose th),
	:global(.prose td) {
		border: 1px solid #1e3a1e;
		padding: 0.5rem 0.7rem;
		text-align: left;
		vertical-align: top;
	}

	:global(.prose th) {
		background: #0f1a0f;
		color: #86efac;
		white-space: nowrap;
	}

	:global(.prose .lead) {
		font-size: 1.05rem;
		color: #b8dcb8;
	}

	:global(.prose .updated) {
		font-size: 0.82rem;
		color: #7fae7f;
		margin-top: 0.25rem;
	}

	:global(.prose .contact-card) {
		border: 1px solid #1e3a1e;
		border-radius: 8px;
		padding: 1rem 1.25rem;
		background: #0f1a0f;
		margin: 1rem 0 1.5rem;
	}
</style>
