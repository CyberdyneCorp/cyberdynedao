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

<!-- Own the full viewport as a fixed, opaque, self-scrolling panel. The app's
     global CSS pins `html, body { overflow: hidden }` for the terminal desktop
     and paints an animated background behind everything; a static document page
     must scroll on its own and fully cover that layer, independent of the app. -->
<div class="shell retro-scrollbar">
	<header>
		<a class="brand" href="/">CYBERDYNE<span class="cursor">_</span></a>
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
			<a href="/">Home</a><span aria-hidden="true"> · </span><a href="/privacy">Privacy Policy</a
			><span aria-hidden="true"> · </span><a href="/support">Support</a>
		</p>
	</footer>
</div>

<style>
	.shell {
		position: fixed;
		inset: 0;
		overflow-y: auto;
		overflow-x: hidden;
		display: flex;
		flex-direction: column;
		/* Faint green aurora at the top, over a near-black base — on-brand but
		   stays out of the way of long-form reading. */
		background:
			radial-gradient(130% 90% at 50% -20%, rgba(74, 222, 128, 0.08), transparent 55%),
			#080b08;
		color: #cfe8cf;
		font-family: 'JetBrains Mono', ui-monospace, 'SFMono-Regular', 'Courier New', monospace;
		line-height: 1.7;
		scroll-behavior: smooth;
	}

	header {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem 1.5rem;
		align-items: baseline;
		justify-content: space-between;
		padding: 1.1rem clamp(1rem, 5vw, 3rem);
		border-bottom: 1px solid #17331a;
		position: sticky;
		top: 0;
		z-index: 10;
		background: rgba(8, 11, 8, 0.82);
		backdrop-filter: blur(10px);
	}

	.brand {
		font-weight: 700;
		letter-spacing: 0.14em;
		color: #4ade80;
		text-decoration: none;
		font-size: 1.05rem;
		text-shadow: 0 0 18px rgba(74, 222, 128, 0.35);
	}

	.cursor {
		animation: blink 1.1s step-end infinite;
	}

	@keyframes blink {
		50% {
			opacity: 0;
		}
	}

	nav {
		display: flex;
		gap: 1.5rem;
	}

	nav a {
		color: #9fce9f;
		text-decoration: none;
		font-size: 0.9rem;
		padding-bottom: 3px;
		border-bottom: 2px solid transparent;
		transition:
			color 0.15s ease,
			border-color 0.15s ease;
	}

	nav a:hover,
	nav a[aria-current='page'] {
		color: #4ade80;
		border-bottom-color: #4ade80;
	}

	main {
		flex: 1;
		width: 100%;
		max-width: 48rem;
		margin: 0 auto;
		padding: clamp(2rem, 6vw, 4rem) clamp(1.15rem, 5vw, 3rem) 4.5rem;
	}

	footer {
		border-top: 1px solid #17331a;
		padding: 2rem clamp(1rem, 5vw, 3rem) 2.5rem;
		font-size: 0.8rem;
		color: #6f9e6f;
		text-align: center;
	}

	.foot-links {
		margin-top: 0.4rem;
	}

	footer a {
		color: #9fce9f;
		text-decoration: none;
	}

	footer a:hover {
		color: #4ade80;
		text-decoration: underline;
	}

	/* Keyboard focus is clearly visible on the dark theme. */
	.shell :global(a:focus-visible),
	.shell :global(button:focus-visible) {
		outline: 2px solid #4ade80;
		outline-offset: 3px;
		border-radius: 3px;
	}

	@media (prefers-reduced-motion: reduce) {
		.cursor {
			animation: none;
		}
		.shell {
			scroll-behavior: auto;
		}
	}

	/* ── Shared document typography for the child pages (rendered outside this
	   component's scope, hence :global). Tuned for readable long-form copy. ── */
	:global(.prose > * + *) {
		margin-top: 0.9rem;
	}

	:global(.prose h1) {
		color: #4ade80;
		font-size: clamp(1.8rem, 5vw, 2.5rem);
		letter-spacing: 0.01em;
		line-height: 1.15;
		margin: 0 0 0.35rem;
		text-shadow: 0 0 26px rgba(74, 222, 128, 0.25);
	}

	:global(.prose h2) {
		color: #86efac;
		font-size: 1.22rem;
		margin: 2.5rem 0 0.5rem;
		padding-bottom: 0.35rem;
		border-bottom: 1px solid #17331a;
		scroll-margin-top: 5rem;
	}

	:global(.prose h3) {
		color: #9fce9f;
		font-size: 1rem;
		margin: 1.6rem 0 0.4rem;
	}

	:global(.prose p),
	:global(.prose li) {
		color: #c4dfc4;
	}

	:global(.prose ul) {
		padding-left: 1.3rem;
		margin: 0.4rem 0 0.9rem;
	}

	:global(.prose li) {
		margin: 0.4rem 0;
	}

	:global(.prose li::marker) {
		color: #4ade80;
	}

	:global(.prose a) {
		color: #6ee79b;
		text-decoration: underline;
		text-underline-offset: 3px;
		text-decoration-color: rgba(110, 231, 155, 0.45);
		transition: text-decoration-color 0.15s ease;
	}

	:global(.prose a:hover) {
		text-decoration-color: #6ee79b;
	}

	:global(.prose strong) {
		color: #eafff0;
	}

	:global(.prose table) {
		width: 100%;
		border-collapse: collapse;
		margin: 1.1rem 0 1.5rem;
		font-size: 0.86rem;
		display: block;
		overflow-x: auto;
		border: 1px solid #17331a;
		border-radius: 10px;
	}

	:global(.prose th),
	:global(.prose td) {
		border-bottom: 1px solid #142a16;
		border-right: 1px solid #142a16;
		padding: 0.6rem 0.8rem;
		text-align: left;
		vertical-align: top;
	}

	:global(.prose tr:last-child td) {
		border-bottom: none;
	}

	:global(.prose th) {
		background: #0e1a0e;
		color: #86efac;
		white-space: nowrap;
		position: sticky;
		top: 0;
	}

	:global(.prose .lead) {
		font-size: 1.08rem;
		color: #b8dcb8;
		max-width: 42rem;
	}

	:global(.prose .updated) {
		display: inline-block;
		font-size: 0.75rem;
		color: #7fae7f;
		border: 1px solid #17331a;
		border-radius: 999px;
		padding: 0.15rem 0.7rem;
		margin: 0.25rem 0 0.5rem;
	}

	:global(.prose .contact-card) {
		border: 1px solid #1e3a1e;
		border-radius: 12px;
		padding: 1.15rem 1.35rem;
		background: linear-gradient(180deg, rgba(20, 42, 22, 0.55), rgba(14, 26, 14, 0.55));
		margin: 1.25rem 0 1.75rem;
	}

	:global(.prose .contact-card p) {
		margin: 0.15rem 0;
	}
</style>
