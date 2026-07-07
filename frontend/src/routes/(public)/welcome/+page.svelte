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
	<h1>Learn, build, and own it.</h1>
	<p class="lead">
		Cyberdyne is a retro-terminal learning platform — hands-on courses, quizzes and
		learning tracks, wrapped in secure accounts, a managed wallet, and DAO membership.
	</p>

	<p class="cta-row">
		<a class="cta" href="/">Launch the app →</a>
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
	<ul>
		<li><a href="/privacy">Privacy Policy</a> — what we collect, why, and your rights.</li>
		<li><a href="/support">Support</a> — get help with your account, wallet, or purchases.</li>
	</ul>
</article>

<style>
	.cta-row {
		margin: 1.5rem 0 2.5rem;
	}

	.cta {
		display: inline-block;
		padding: 0.7rem 1.4rem;
		border: 1px solid #4ade80;
		border-radius: 8px;
		color: #4ade80;
		text-decoration: none;
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	.cta:hover {
		background: #4ade80;
		color: #0a0e0a;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
		gap: 1rem;
		margin: 1.5rem 0 2rem;
	}

	.card {
		border: 1px solid #1e3a1e;
		border-radius: 8px;
		padding: 1.1rem 1.25rem;
		background: #0f1a0f;
	}

	.card h3 {
		margin: 0 0 0.4rem;
		color: #86efac;
	}

	.card p {
		margin: 0;
		font-size: 0.92rem;
		color: #b8dcb8;
	}
</style>
