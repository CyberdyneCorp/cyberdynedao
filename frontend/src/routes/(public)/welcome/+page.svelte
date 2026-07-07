<script lang="ts">
	const GITHUB = 'https://github.com/CyberdyneCorp';

	// Sovereignty thesis — the three pillars every product shares.
	const pillars = [
		{
			title: 'Your data, your infra',
			body: 'Every product is self-hostable. No mandatory cloud, and no data leaving your perimeter.'
		},
		{
			title: 'Agent-first by design',
			body: 'REST and MCP at the same core — humans and AI agents are first-class clients of every service.'
		},
		{
			title: 'Regulation-ready',
			body: 'Multi-tenancy, audit logs, provenance and LGPD — over a single identity spine.'
		}
	];

	// What we can do — breadth without listing every product.
	const capabilities = [
		{
			n: '01',
			title: 'AI, agents & knowledge',
			body: 'RAG and knowledge graphs, MCP servers, and agent-native platforms on hexagonal FastAPI + Svelte.'
		},
		{
			n: '02',
			title: 'Apple & engineering software',
			body: 'Swift 6 / SwiftUI / Metal apps; precision CAD, CAE simulation, and C++20 compilers that run on the GPU.'
		},
		{
			n: '03',
			title: 'Geospatial',
			body: '3D Cesium globes, STAC catalogues, and RF-propagation planning built on live data sources.'
		},
		{
			n: '04',
			title: 'Blockchain & identity',
			body: 'Solidity, DAOs and wallet-based identity — up to launching your own EVM chain and oracle network.'
		}
	];

	// How we work — the two engagement tracks.
	const tracks = [
		{
			tag: 'Track A',
			title: 'We build it',
			body: 'We design and build your product end-to-end: AI systems, full-stack SaaS, Apple-native apps, high-performance C++. The delivery is yours.'
		},
		{
			tag: 'Track B',
			title: 'Use our products',
			body: 'License and deploy our existing suite — a corporate OS, RAG engine, geospatial platform, engineering tools — on your infra or ours.'
		}
	];

	// Engineering discipline — how the work stays auditable.
	const discipline = [
		'Spec before code (OpenSpec)',
		'Oracle-validated correctness',
		'A regression test per fix',
		'Hexagonal backends + MVVM',
		'Stable ABIs',
		'CI-gated builds'
	];

	const faqs = [
		{
			q: 'Can we self-host everything?',
			a: 'Yes. Every product runs on your own infrastructure — identity, AI, data, even your own blockchain. No vendor lock-in at any layer.'
		},
		{
			q: 'Do you build custom software, or sell products?',
			a: 'Both. Hire the studio to build end-to-end, license our ready-made suite, or start with a product and grow custom work on top of it.'
		},
		{
			q: 'How do you handle data and support?',
			a: 'We process only what a service needs and keep it inside your perimeter. See the Privacy Policy for the detail, or the Support page for help.'
		}
	];
</script>

<svelte:head>
	<title>Cyberdyne — Sovereign, agent-first software</title>
	<meta
		name="description"
		content="CyberdyneCorp builds sovereign, agent-first software with engineering discipline — full-stack from GPU kernels and compilers to native apps and multi-tenant SaaS, self-hostable and proven in the open."
	/>
</svelte:head>

<div class="landing">
	<!-- Hero -->
	<section class="hero">
		<div class="hero-copy">
			<p class="eyebrow">// SOVEREIGN · AGENT-FIRST</p>
			<h1>Sovereign,<br />agent-first software.</h1>
			<p class="lead">
				One systems architect directing a fleet of AI agents — building full-stack, from GPU
				kernels and compilers to native apps and multi-tenant SaaS. Self-hostable by default,
				audit-ready, and proven in the open.
			</p>
			<div class="cta-row">
				<a class="cta" href="/">Launch the app →</a>
				<a class="cta-ghost" href="#capabilities">What we do</a>
			</div>
		</div>

		<!-- Stylised build session (decorative) -->
		<div class="term" aria-hidden="true">
			<div class="term-bar">
				<span class="dot"></span><span class="dot"></span><span class="dot"></span>
				<span class="term-title">cyberdyne@studio</span>
			</div>
			<pre class="term-body"><span class="p">cyberdyne@studio:~$</span> spec new payments-api
<span class="c">▸</span> OpenSpec capability drafted · 12 scenarios
<span class="p">cyberdyne@studio:~$</span> build --agents
<span class="c">▸</span> fleet: 6 agents · architect-reviewed
<span class="p">cyberdyne@studio:~$</span> validate --oracle numpy,scipy
<span class="c">▸</span> 10,110 checks · <span class="ok">0 divergences ✓</span>
<span class="p">cyberdyne@studio:~$</span> deploy --self-host
<span class="c">▸</span> identity · MCP · isolated exec · <span class="ok">LGPD ✓</span>
<span class="p">cyberdyne@studio:~$</span> <span class="cursor">█</span></pre>
		</div>
	</section>

	<!-- Sovereignty pillars -->
	<section class="block">
		<h2 class="section-title">Sovereignty by default</h2>
		<div class="grid grid-3">
			{#each pillars as p (p.title)}
				<article class="card">
					<h3>{p.title}</h3>
					<p>{p.body}</p>
				</article>
			{/each}
		</div>
	</section>

	<!-- Capabilities -->
	<section id="capabilities" class="block">
		<h2 class="section-title">What we can do</h2>
		<div class="grid">
			{#each capabilities as f (f.n)}
				<article class="card">
					<span class="card-n">{f.n}</span>
					<h3>{f.title}</h3>
					<p>{f.body}</p>
				</article>
			{/each}
		</div>
	</section>

	<!-- How we work -->
	<section class="block">
		<h2 class="section-title">Two ways to work with us</h2>
		<div class="grid grid-2">
			{#each tracks as t (t.tag)}
				<article class="card track">
					<span class="track-tag">{t.tag}</span>
					<h3>{t.title}</h3>
					<p>{t.body}</p>
				</article>
			{/each}
		</div>
		<p class="note">
			Both run on one platform underneath: identity, ingestion, isolated execution, and MCP tools.
		</p>
		<ul class="chips">
			{#each discipline as item (item)}
				<li class="chip">{item}</li>
			{/each}
		</ul>
	</section>

	<!-- Proven in the open -->
	<section class="proven">
		<div>
			<h2>Proven in the open</h2>
			<p>
				18+ open-source repositories — a C++20 port of NumPy and SciPy, a MATLAB compiler, a CAE
				suite, an RF ray tracer. Over <strong>10,000 oracle checks</strong> against NumPy and SciPy,
				with zero divergences. Audit exactly how we build before we build anything for you.
			</p>
		</div>
		<a class="cta-ghost" href={GITHUB} target="_blank" rel="noopener noreferrer">
			Audit us on GitHub →
		</a>
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
			More on the <a href="/support">Support</a> page, or read the full
			<a href="/privacy">Privacy Policy</a>.
		</p>
	</section>

	<!-- Closing CTA -->
	<section class="cta-band">
		<h2>Audit the code. Then let's build.</h2>
		<p>Everything we ship is proven in the open. Open the app, explore the repos, or reach out about your project.</p>
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
		font-size: clamp(2.3rem, 6.4vw, 3.7rem);
		line-height: 1.06;
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
		font-size: 0.82rem;
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
	.term-body .ok {
		color: #4ade80;
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

	@media (min-width: 52rem) {
		.grid-3 {
			grid-template-columns: repeat(3, 1fr);
		}
		.grid-2 {
			grid-template-columns: repeat(2, 1fr);
		}
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

	/* ── Tracks ─────────────────────────────────────────── */
	.track {
		padding: 1.5rem 1.6rem;
	}

	.track-tag {
		display: inline-block;
		font-size: 0.72rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: #4ade80;
		border: 1px solid #2a5230;
		border-radius: 999px;
		padding: 0.15rem 0.7rem;
		margin-bottom: 0.7rem;
	}

	.note {
		margin: 1.1rem 0 1.25rem;
		color: #9fce9f;
		font-size: 0.92rem;
	}

	/* ── Discipline chips ───────────────────────────────── */
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

	/* ── Proven band ────────────────────────────────────── */
	.proven {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 1.5rem;
		border: 1px solid #1e3a1e;
		border-radius: 16px;
		padding: clamp(1.75rem, 5vw, 2.5rem);
		background:
			radial-gradient(120% 130% at 100% 0%, rgba(74, 222, 128, 0.08), transparent 55%),
			rgba(10, 16, 10, 0.7);
	}

	.proven h2 {
		color: #86efac;
		font-size: 1.35rem;
		margin: 0 0 0.6rem;
	}

	.proven p {
		color: #b8dcb8;
		margin: 0;
		max-width: 42rem;
		line-height: 1.6;
	}

	.proven strong {
		color: #eafff0;
	}

	.proven .cta-ghost {
		flex: none;
		white-space: nowrap;
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
		max-width: 34rem;
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
