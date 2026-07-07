<script lang="ts">
	const features = [
		{
			title: 'Learn by doing',
			body: 'A catalogue of hands-on courses, lessons, quizzes and learning tracks — from an interactive retro-terminal desktop.'
		},
		{
			title: 'Secure by default',
			body: 'Account sign-in with multi-factor authentication, recovery codes, and audited access — your credentials are never stored in the clear.'
		},
		{
			title: 'Managed wallet',
			body: 'A built-in custodial wallet and on-chain identity, so you can take part in the DAO without wrangling keys.'
		},
		{
			title: 'Buy once, everywhere',
			body: 'Purchases and subscriptions made on the web or the App Store unlock the same entitlements across your devices.'
		}
	];
</script>

<svelte:head>
	<title>Cyberdyne — Learn, build, and own it</title>
	<meta
		name="description"
		content="Cyberdyne is a retro-terminal learning platform: hands-on courses and quizzes, secure accounts with MFA, a managed wallet, and DAO membership."
	/>
</svelte:head>

<article class="prose landing">
	<p class="eyebrow">// CYBERDYNE_OS</p>
	<h1>Learn, build, and own it.</h1>
	<p class="lead">
		Cyberdyne is a retro-terminal learning platform — hands-on courses, quizzes and
		learning tracks, wrapped in secure accounts, a managed wallet, and DAO membership.
	</p>

	<p class="cta-row">
		<a class="cta" href="/">Launch the app →</a>
		<a class="cta-ghost" href="/support">Get support</a>
	</p>

	<div class="grid">
		{#each features as f (f.title)}
			<section class="card">
				<h3>{f.title}</h3>
				<p>{f.body}</p>
			</section>
		{/each}
	</div>

	<h2>Legal &amp; help</h2>
	<div class="link-cards">
		<a class="link-card" href="/privacy">
			<span class="lc-title">Privacy Policy →</span>
			<span class="lc-sub">What we collect, why, and your rights.</span>
		</a>
		<a class="link-card" href="/support">
			<span class="lc-title">Support →</span>
			<span class="lc-sub">Help with your account, wallet, or purchases.</span>
		</a>
	</div>
</article>

<style>
	.eyebrow {
		color: #4ade80;
		font-size: 0.8rem;
		letter-spacing: 0.25em;
		opacity: 0.8;
		margin: 0 0 0.75rem;
	}

	.cta-row {
		display: flex;
		flex-wrap: wrap;
		gap: 0.85rem;
		margin: 1.75rem 0 2.75rem;
	}

	.cta,
	.cta-ghost {
		display: inline-block;
		padding: 0.7rem 1.5rem;
		border-radius: 8px;
		text-decoration: none;
		font-weight: 600;
		letter-spacing: 0.02em;
		transition:
			transform 0.15s ease,
			background 0.15s ease,
			box-shadow 0.15s ease;
	}

	.cta {
		border: 1px solid #4ade80;
		background: #4ade80;
		color: #06120a;
		box-shadow: 0 0 0 rgba(74, 222, 128, 0);
	}

	.cta:hover {
		transform: translateY(-2px);
		box-shadow: 0 8px 24px rgba(74, 222, 128, 0.25);
	}

	.cta-ghost {
		border: 1px solid #2a5230;
		color: #9fce9f;
	}

	.cta-ghost:hover {
		border-color: #4ade80;
		color: #4ade80;
		transform: translateY(-2px);
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
		gap: 1rem;
		margin: 1.75rem 0 1rem;
	}

	.card {
		border: 1px solid #1e3a1e;
		border-radius: 12px;
		padding: 1.2rem 1.35rem;
		background: linear-gradient(180deg, rgba(16, 26, 15, 0.9), rgba(10, 16, 10, 0.9));
		transition:
			transform 0.15s ease,
			border-color 0.15s ease,
			box-shadow 0.15s ease;
	}

	.card:hover {
		transform: translateY(-3px);
		border-color: #2f6b39;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
	}

	.card h3 {
		margin: 0 0 0.45rem;
		color: #86efac;
	}

	.card p {
		margin: 0;
		font-size: 0.92rem;
		color: #b8dcb8;
	}

	.link-cards {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
		gap: 1rem;
		margin-top: 0.75rem;
	}

	.link-card {
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
		padding: 1rem 1.25rem;
		border: 1px solid #1e3a1e;
		border-radius: 12px;
		text-decoration: none;
		background: rgba(14, 26, 14, 0.6);
		transition:
			transform 0.15s ease,
			border-color 0.15s ease;
	}

	.link-card:hover {
		transform: translateY(-3px);
		border-color: #4ade80;
	}

	.lc-title {
		color: #4ade80;
		font-weight: 600;
	}

	.lc-sub {
		color: #a7cba7;
		font-size: 0.88rem;
	}
</style>
