<script lang="ts">
	const features = [
		{
			n: '01',
			title: 'Learn by doing',
			body: 'Hands-on courses, lessons, quizzes and learning tracks — inside an interactive retro-terminal desktop, not a video wall.'
		},
		{
			n: '02',
			title: 'Secure by default',
			body: 'Sign-in with multi-factor auth and recovery codes. Passwords are hashed with Argon2id; secrets are encrypted at rest and access is audited.'
		},
		{
			n: '03',
			title: 'Managed wallet',
			body: 'A built-in custodial wallet and on-chain identity, so you can join the DAO and own your progress without wrangling private keys.'
		},
		{
			n: '04',
			title: 'Buy once, everywhere',
			body: 'Purchases and subscriptions made on the web or the App Store unlock the same entitlements across every device you sign in on.'
		}
	];

	const steps = [
		{ title: 'Create your account', body: 'Sign up and turn on MFA. A managed wallet is provisioned for you automatically.' },
		{ title: 'Pick a track', body: 'Browse the catalogue, start a course, and progress through lessons and quizzes at your pace.' },
		{ title: 'Own what you earn', body: 'Your progress and on-chain identity are yours — carry them into the DAO and across devices.' }
	];

	const trust = [
		'Multi-factor auth',
		'Argon2id passwords',
		'Encrypted at rest',
		'Custodial wallet',
		'On-chain identity',
		'Stripe & App Store billing'
	];

	const faqs = [
		{
			q: 'What is Cyberdyne?',
			a: 'A retro-terminal learning platform — hands-on courses, quizzes and learning tracks, wrapped in secure accounts, a managed wallet, and DAO membership.'
		},
		{
			q: 'Do I need a crypto wallet to start?',
			a: 'No. A custodial wallet is created and secured for you when you sign up — you can use everything without ever touching a private key.'
		},
		{
			q: 'How do purchases work across web and the App Store?',
			a: 'Buy on the web or through the Apple App Store; either way the same entitlements unlock on every device where you sign in.'
		},
		{
			q: 'How is my personal data handled?',
			a: 'We process only what the service needs, encrypt secrets at rest, and never sell your data. See the Privacy Policy for the full detail and your rights.'
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

<div class="landing">
	<!-- Hero -->
	<section class="hero">
		<div class="hero-copy">
			<p class="eyebrow">// CYBERDYNE_OS</p>
			<h1>Learn, build,<br />and own it.</h1>
			<p class="lead">
				A retro-terminal learning platform — hands-on courses, quizzes and learning tracks,
				wrapped in secure accounts, a managed wallet, and DAO membership.
			</p>
			<div class="cta-row">
				<a class="cta" href="/">Launch the app →</a>
				<a class="cta-ghost" href="#features">See what's inside</a>
			</div>
		</div>

		<!-- Stylised terminal session (decorative) -->
		<div class="term" aria-hidden="true">
			<div class="term-bar">
				<span class="dot"></span><span class="dot"></span><span class="dot"></span>
				<span class="term-title">cyberdyne@os</span>
			</div>
			<pre class="term-body"><span class="p">cyberdyne@os:~$</span> open academy
<span class="c">▸</span> loading catalogue… courses · tracks · quizzes
<span class="c">▸</span> resume <span class="s">"Deep Learning × Biology"</span>  <span class="bar">▓▓▓▓▓░░░</span> 63%
<span class="p">cyberdyne@os:~$</span> wallet status
<span class="c">▸</span> 0xA1b2…9F42 · on-chain identity <span class="ok">verified ✓</span>
<span class="p">cyberdyne@os:~$</span> <span class="cursor">█</span></pre>
		</div>
	</section>

	<!-- Features -->
	<section id="features" class="block">
		<h2 class="section-title">Everything in one place</h2>
		<div class="grid">
			{#each features as f (f.n)}
				<article class="card">
					<span class="card-n">{f.n}</span>
					<h3>{f.title}</h3>
					<p>{f.body}</p>
				</article>
			{/each}
		</div>
	</section>

	<!-- How it works -->
	<section class="block">
		<h2 class="section-title">How it works</h2>
		<ol class="steps">
			{#each steps as step, i (step.title)}
				<li class="step">
					<span class="step-n">{i + 1}</span>
					<div>
						<h3>{step.title}</h3>
						<p>{step.body}</p>
					</div>
				</li>
			{/each}
		</ol>
	</section>

	<!-- Trust band -->
	<section class="block">
		<h2 class="section-title">Built to be trusted</h2>
		<ul class="chips">
			{#each trust as item (item)}
				<li class="chip">{item}</li>
			{/each}
		</ul>
	</section>

	<!-- FAQ -->
	<section class="block">
		<h2 class="section-title">Questions</h2>
		<div class="faq">
			{#each faqs as item (item.q)}
				<details>
					<summary>{item.q}</summary>
					<p>{item.a}</p>
				</details>
			{/each}
		</div>
		<p class="faq-foot">
			More help on the <a href="/support">Support</a> page, or read the full
			<a href="/privacy">Privacy Policy</a>.
		</p>
	</section>

	<!-- Closing CTA -->
	<section class="cta-band">
		<h2>Ready to start?</h2>
		<p>Create an account and open the terminal — your first track is a click away.</p>
		<div class="cta-row">
			<a class="cta" href="/">Launch the app →</a>
			<a class="cta-ghost" href="/support">Get support</a>
		</div>
	</section>
</div>

<style>
	.landing {
		display: flex;
		flex-direction: column;
		gap: clamp(3rem, 8vw, 5.5rem);
	}

	/* Keep anchored sections clear of the sticky header when jumped to. */
	.landing section {
		scroll-margin-top: 5rem;
	}

	/* ── Hero ───────────────────────────────────────────── */
	.hero {
		display: grid;
		grid-template-columns: 1fr;
		gap: 2.5rem;
		align-items: center;
		padding-top: clamp(1rem, 4vw, 2.5rem);
	}

	@media (min-width: 60rem) {
		.hero {
			grid-template-columns: 1.05fr 0.95fr;
			gap: 3rem;
		}
	}

	.eyebrow {
		color: #4ade80;
		font-size: 0.8rem;
		letter-spacing: 0.28em;
		opacity: 0.85;
		margin: 0 0 1rem;
	}

	h1 {
		color: #4ade80;
		font-size: clamp(2.4rem, 7vw, 3.9rem);
		line-height: 1.05;
		letter-spacing: 0.01em;
		margin: 0 0 1.1rem;
		text-shadow: 0 0 34px rgba(74, 222, 128, 0.28);
	}

	.lead {
		color: #b8dcb8;
		font-size: 1.1rem;
		max-width: 34rem;
		margin: 0 0 1.9rem;
	}

	.cta-row {
		display: flex;
		flex-wrap: wrap;
		gap: 0.85rem;
	}

	.cta,
	.cta-ghost {
		display: inline-block;
		padding: 0.72rem 1.5rem;
		border-radius: 8px;
		text-decoration: none;
		font-weight: 600;
		letter-spacing: 0.02em;
		transition:
			transform 0.15s ease,
			background 0.15s ease,
			box-shadow 0.15s ease,
			border-color 0.15s ease,
			color 0.15s ease;
	}

	.cta {
		border: 1px solid #4ade80;
		background: #4ade80;
		color: #06120a;
	}

	.cta:hover {
		transform: translateY(-2px);
		box-shadow: 0 10px 28px rgba(74, 222, 128, 0.28);
	}

	.cta-ghost {
		border: 1px solid #2a5230;
		color: #9fce9f;
	}

	.cta-ghost:hover {
		transform: translateY(-2px);
		border-color: #4ade80;
		color: #4ade80;
	}

	/* ── Terminal mock ──────────────────────────────────── */
	.term {
		border: 1px solid #1e3a1e;
		border-radius: 12px;
		background: #060a06;
		box-shadow:
			0 20px 60px rgba(0, 0, 0, 0.5),
			0 0 0 1px rgba(74, 222, 128, 0.04);
		overflow: hidden;
	}

	.term-bar {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		padding: 0.6rem 0.85rem;
		background: #0d150d;
		border-bottom: 1px solid #17331a;
	}

	.dot {
		width: 11px;
		height: 11px;
		border-radius: 50%;
		background: #234425;
	}

	.dot:nth-child(1) {
		background: #3a6b3f;
	}

	.term-title {
		margin-left: 0.5rem;
		font-size: 0.75rem;
		color: #6f9e6f;
		letter-spacing: 0.08em;
	}

	.term-body {
		margin: 0;
		padding: 1.1rem 1.25rem 1.35rem;
		font-family: inherit;
		font-size: 0.83rem;
		line-height: 1.85;
		color: #a7cba7;
		white-space: pre-wrap;
		word-break: break-word;
	}

	.term-body .p {
		color: #4ade80;
	}
	.term-body .c {
		color: #6ee79b;
	}
	.term-body .s {
		color: #eafff0;
	}
	.term-body .ok {
		color: #4ade80;
	}
	.term-body .bar {
		color: #2f6b39;
		letter-spacing: 1px;
	}

	.cursor {
		color: #4ade80;
		animation: blink 1.1s step-end infinite;
	}

	@keyframes blink {
		50% {
			opacity: 0;
		}
	}

	/* ── Sections ───────────────────────────────────────── */
	.section-title {
		color: #86efac;
		font-size: 1.35rem;
		margin: 0 0 1.4rem;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid #17331a;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
		gap: 1rem;
	}

	.card {
		position: relative;
		border: 1px solid #1e3a1e;
		border-radius: 12px;
		padding: 1.3rem 1.4rem;
		background: linear-gradient(180deg, rgba(16, 26, 15, 0.9), rgba(10, 16, 10, 0.9));
		transition:
			transform 0.15s ease,
			border-color 0.15s ease,
			box-shadow 0.15s ease;
	}

	.card:hover {
		transform: translateY(-3px);
		border-color: #2f6b39;
		box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
	}

	.card-n {
		font-size: 0.78rem;
		color: #3f8f4f;
		letter-spacing: 0.1em;
	}

	.card h3 {
		margin: 0.35rem 0 0.5rem;
		color: #86efac;
		font-size: 1.05rem;
	}

	.card p {
		margin: 0;
		font-size: 0.92rem;
		color: #b8dcb8;
		line-height: 1.6;
	}

	/* ── Steps ──────────────────────────────────────────── */
	.steps {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
		counter-reset: step;
	}

	.step {
		display: flex;
		gap: 1rem;
		align-items: flex-start;
		border: 1px solid #17331a;
		border-radius: 12px;
		padding: 1.2rem 1.3rem;
		background: rgba(12, 20, 12, 0.5);
	}

	.step-n {
		flex: none;
		display: grid;
		place-items: center;
		width: 2rem;
		height: 2rem;
		border-radius: 50%;
		border: 1px solid #2f6b39;
		color: #4ade80;
		font-weight: 700;
		font-size: 0.9rem;
	}

	.step h3 {
		margin: 0 0 0.35rem;
		color: #cfe8cf;
		font-size: 1rem;
	}

	.step p {
		margin: 0;
		font-size: 0.9rem;
		color: #a7cba7;
		line-height: 1.6;
	}

	/* ── Trust chips ────────────────────────────────────── */
	.chips {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: 0.6rem;
	}

	.chip {
		border: 1px solid #1e3a1e;
		border-radius: 999px;
		padding: 0.45rem 1rem;
		font-size: 0.85rem;
		color: #a7cba7;
		background: rgba(14, 26, 14, 0.55);
	}

	.chip::before {
		content: '✓ ';
		color: #4ade80;
	}

	/* ── FAQ ────────────────────────────────────────────── */
	.faq {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}

	.faq details {
		border: 1px solid #17331a;
		border-radius: 10px;
		background: rgba(12, 20, 12, 0.5);
		overflow: hidden;
	}

	.faq summary {
		cursor: pointer;
		padding: 0.9rem 1.15rem;
		color: #cfe8cf;
		font-weight: 600;
		font-size: 0.95rem;
		list-style: none;
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		align-items: center;
	}

	.faq summary::-webkit-details-marker {
		display: none;
	}

	.faq summary::after {
		content: '+';
		color: #4ade80;
		font-weight: 700;
		transition: transform 0.15s ease;
	}

	.faq details[open] summary::after {
		content: '−';
	}

	.faq details[open] summary {
		border-bottom: 1px solid #17331a;
	}

	.faq p {
		margin: 0;
		padding: 0.9rem 1.15rem 1.1rem;
		color: #a7cba7;
		font-size: 0.92rem;
		line-height: 1.65;
	}

	.faq-foot {
		margin: 1.1rem 0 0;
		font-size: 0.9rem;
		color: #9fce9f;
	}

	.faq-foot a {
		color: #6ee79b;
	}

	/* ── Closing CTA ────────────────────────────────────── */
	.cta-band {
		text-align: center;
		border: 1px solid #1e3a1e;
		border-radius: 16px;
		padding: clamp(2rem, 6vw, 3.25rem) 1.5rem;
		background:
			radial-gradient(120% 130% at 50% 0%, rgba(74, 222, 128, 0.1), transparent 60%),
			rgba(10, 16, 10, 0.7);
	}

	.cta-band h2 {
		color: #4ade80;
		font-size: clamp(1.6rem, 5vw, 2.2rem);
		margin: 0 0 0.6rem;
		text-shadow: 0 0 28px rgba(74, 222, 128, 0.25);
	}

	.cta-band p {
		color: #b8dcb8;
		margin: 0 auto 1.6rem;
		max-width: 32rem;
	}

	.cta-band .cta-row {
		justify-content: center;
	}

	@media (prefers-reduced-motion: reduce) {
		.cursor {
			animation: none;
		}
		.cta:hover,
		.cta-ghost:hover,
		.card:hover {
			transform: none;
		}
	}
</style>
