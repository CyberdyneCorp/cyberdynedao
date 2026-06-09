<script lang="ts">
	import { onMount } from 'svelte';
	import { Badge } from '@cyberdynecorp/svelte-ui-core';
	import {
		heroTagline as staticHeroTagline,
		introLead as staticIntroLead,
		introBullets as staticIntroBullets,
		domains as staticDomains,
		beliefs as staticBeliefs,
		targetUsers as staticTargetUsers,
		tokenomicsRows as staticTokenomicsRows,
		tokenUtilityPoints as staticTokenUtilityPoints,
		exampleEconomics as staticExampleEconomics,
		roadmapPhases as staticRoadmapPhases,
		closingHeadline as staticClosingHeadline,
		closingBody as staticClosingBody,
		type Palette
	} from '$lib/data/cyberdyne';
	import { fetchCyberdynePage, type CyberdynePagePayload } from '$lib/api/contentApi';

	// Stale-while-revalidate: bundled static payload renders instantly,
	// API result replaces it once it lands. On any failure the static
	// payload stays — the user never sees an error.
	let page = $state<CyberdynePagePayload>({
		heroTagline: staticHeroTagline,
		introLead: staticIntroLead,
		introBullets: [...staticIntroBullets],
		domains: [...staticDomains],
		beliefs: [...staticBeliefs],
		targetUsers: [...staticTargetUsers],
		tokenomicsRows: [...staticTokenomicsRows],
		tokenUtilityPoints: [...staticTokenUtilityPoints],
		exampleEconomics: [...staticExampleEconomics],
		roadmapPhases: [...staticRoadmapPhases],
		closingHeadline: staticClosingHeadline,
		closingBody: staticClosingBody
	});

	onMount(async () => {
		page = await fetchCyberdynePage();
	});

	const paletteVars: Record<Palette, { accent: string; accentDark: string }> = {
		blue: { accent: '#3b82f6', accentDark: '#1d4ed8' },
		green: { accent: '#22c55e', accentDark: '#15803d' },
		purple: { accent: '#a855f7', accentDark: '#7e22ce' },
		orange: { accent: '#f97316', accentDark: '#c2410c' },
		red: { accent: '#ef4444', accentDark: '#b91c1c' }
	};

	const sectionAccents: Record<string, Palette> = {
		intro: 'blue',
		domains: 'green',
		beliefs: 'purple',
		audience: 'orange',
		tokenomics: 'orange',
		economics: 'green',
		roadmap: 'blue',
		closing: 'red'
	};

	const acc = (key: keyof typeof sectionAccents) => paletteVars[sectionAccents[key]];
	const sectionStyle = (key: keyof typeof sectionAccents) => {
		const a = acc(key);
		return `--accent: ${a.accent}; --accent-dark: ${a.accentDark};`;
	};

	const domainStatusLabel: Record<string, string> = {
		live: 'Live',
		shipping: 'Shipping',
		active: 'Active',
		planned: 'Planned'
	};
	const domainStatusVariant: Record<string, 'success' | 'info' | 'warning' | 'neutral'> = {
		live: 'success',
		shipping: 'success',
		active: 'info',
		planned: 'warning'
	};

	const phaseStatusLabel: Record<string, string> = {
		shipped: 'Shipped',
		shipping: 'Shipping',
		active: 'Active',
		planned: 'Planned'
	};
	const phaseStatusVariant: Record<string, 'success' | 'info' | 'warning' | 'neutral'> = {
		shipped: 'success',
		shipping: 'success',
		active: 'info',
		planned: 'warning'
	};
</script>

<div class="cyberdyne-view">
	<!-- Hero -->
	<header class="hero" style="--accent: {paletteVars.blue.accent}; --accent-dark: {paletteVars.blue.accentDark};">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">🧠</span>
			<h1 class="hero__title">CYBERDYNE</h1>
		</div>
		<p class="hero__tagline">{page.heroTagline}</p>
	</header>

	<div class="content">
		<!-- Intro -->
		<section class="card" style={sectionStyle('intro')}>
			<h2 class="card__title">What is Cyberdyne?</h2>
			<p class="card__lead">{page.introLead}</p>
			<ul class="bullets">
				{#each page.introBullets as b}
					<li>{b}</li>
				{/each}
			</ul>
		</section>

		<!-- Domains -->
		<section class="card" style={sectionStyle('domains')}>
			<h2 class="card__title">The Domains</h2>
			<p class="card__lead">Four domains, a dozen projects, one open stack.</p>
			<div class="domain-grid">
				{#each page.domains as d}
					{@const p = paletteVars[d.palette]}
					<article class="domain" style="--accent: {p.accent}; --accent-dark: {p.accentDark};">
						<header class="domain__header">
							<span class="domain__icon" aria-hidden="true">{d.icon}</span>
							<h3 class="domain__name">{d.name}</h3>
							<Badge variant={domainStatusVariant[d.status]} size="sm">
								{domainStatusLabel[d.status]}
							</Badge>
						</header>
						<p class="domain__tagline">{d.tagline}</p>
						<ul class="domain__projects">
							{#each d.projects as proj}
								<li>{proj}</li>
							{/each}
						</ul>
					</article>
				{/each}
			</div>
		</section>

		<!-- Beliefs -->
		<section class="card" style={sectionStyle('beliefs')}>
			<h2 class="card__title">What We Believe</h2>
			<div class="belief-grid">
				{#each page.beliefs as b}
					<div class="belief">
						<h4 class="belief__title">{b.title}</h4>
						<p class="belief__desc">{b.description}</p>
					</div>
				{/each}
			</div>
		</section>

		<!-- Audience -->
		<section class="card" style={sectionStyle('audience')}>
			<h2 class="card__title">Who It’s For</h2>
			<ul class="audience">
				{#each page.targetUsers as u}
					<li>
						<strong>{u.name}</strong>
						<span class="audience__sep">→</span>
						<span>{u.description}</span>
					</li>
				{/each}
			</ul>
		</section>

		<!-- Tokenomics -->
		<section class="card" style={sectionStyle('tokenomics')}>
			<h2 class="card__title">Tokenomics · CBY</h2>
			<p class="card__lead">Fixed supply 25,000,000 CBY · EVM-compatible</p>
			<div class="table-wrap">
				<table class="tokenomics">
					<thead>
						<tr>
							<th>Allocation</th>
							<th>%</th>
							<th>Vesting</th>
						</tr>
					</thead>
					<tbody>
						{#each page.tokenomicsRows as row}
							<tr>
								<td>{row.allocation}</td>
								<td>{row.percentage}</td>
								<td>{row.vesting}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
			<h3 class="subsection-title">Utility</h3>
			<ul class="bullets">
				{#each page.tokenUtilityPoints as u}
					<li>{u}</li>
				{/each}
			</ul>
		</section>

		<!-- Economics -->
		<section class="card" style={sectionStyle('economics')}>
			<h2 class="card__title">Example Economics</h2>
			<p class="card__lead">A worked example at $40k treasury — the loop scales linearly.</p>
			<div class="econ-grid">
				{#each page.exampleEconomics as e}
					<div class="econ">
						<div class="econ__label">{e.label}</div>
						<div class="econ__value">{e.value}</div>
					</div>
				{/each}
			</div>
			<p class="card__footer">
				<strong>Net effect:</strong> infrastructure is free for users, the DAO grows, stakers earn real yield.
			</p>
		</section>

		<!-- Roadmap -->
		<section class="card" style={sectionStyle('roadmap')}>
			<h2 class="card__title">Roadmap</h2>
			<div class="roadmap">
				{#each page.roadmapPhases as phase}
					{@const ph = paletteVars[phase.color]}
					<div class="phase" style="--accent: {ph.accent}; --accent-dark: {ph.accentDark};">
						<header class="phase__header">
							<h3 class="phase__title">{phase.title}</h3>
							<Badge variant={phaseStatusVariant[phase.status]} size="sm">
								{phaseStatusLabel[phase.status]}
							</Badge>
						</header>
						<p class="phase__subtitle">{phase.subtitle}</p>
						<ul class="phase__items">
							{#each phase.items as item}
								<li>
									<span class="phase__icon">{item.icon}</span>
									<span>{item.text}</span>
								</li>
							{/each}
						</ul>
					</div>
				{/each}
			</div>
		</section>

		<!-- Closing -->
		<section class="closing" style={sectionStyle('closing')}>
			<h2 class="closing__headline">{page.closingHeadline}</h2>
			<p class="closing__body">{page.closingBody}</p>
		</section>
	</div>
</div>

<style>
	.cyberdyne-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		overflow-y: auto;
	}

	/* ---------- Hero ---------- */
	.hero {
		padding: 24px 28px;
		background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
	}
	.hero__brand {
		display: flex;
		align-items: center;
		gap: 14px;
		margin-bottom: 10px;
	}
	.hero__mark {
		font-size: 1.75rem;
	}
	.hero__title {
		font-size: 1.875rem;
		font-weight: 800;
		margin: 0;
		letter-spacing: 0.12em;
		color: #ffffff;
	}
	.hero__tagline {
		margin: 0;
		font-size: 0.95rem;
		line-height: 1.55;
		color: #e0e7ff;
		max-width: 820px;
	}

	/* ---------- Content layout ---------- */
	.content {
		padding: 24px 20px 28px;
		display: flex;
		flex-direction: column;
		gap: 20px;
		max-width: 1200px;
		margin: 0 auto;
	}

	/* ---------- Card primitive ---------- */
	.card {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 20px 20px 20px 28px;
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
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.card__title {
		font-size: 1.125rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
		margin: 0;
	}
	.card__lead {
		font-size: 0.9375rem;
		line-height: 1.6;
		color: #1f2937;
		margin: 0;
	}
	.card__footer {
		font-size: 0.875rem;
		color: #1f2937;
		margin: 0;
	}

	.subsection-title {
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: var(--accent-dark);
		font-weight: 700;
		margin: 6px 0 0;
	}

	/* ---------- Bullets ---------- */
	.bullets {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 6px;
	}
	.bullets li {
		position: relative;
		padding-left: 18px;
		font-size: 0.875rem;
		line-height: 1.5;
		color: #374151;
	}
	.bullets li::before {
		content: '▸';
		position: absolute;
		left: 0;
		top: 0;
		color: var(--accent-dark);
		font-weight: 700;
	}

	/* ---------- Domains grid ---------- */
	.domain-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 14px;
	}
	@media (max-width: 720px) {
		.domain-grid {
			grid-template-columns: minmax(0, 1fr);
		}
	}
	.domain {
		position: relative;
		background: #fafafa;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 14px 14px 14px 20px;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.domain::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.domain__header {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.domain__icon {
		flex: 0 0 auto;
		width: 32px;
		height: 32px;
		border: 2px solid #000;
		background: var(--accent);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 16px;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.35);
	}
	.domain__name {
		flex: 1 1 auto;
		font-size: 0.9375rem;
		font-weight: 700;
		color: #000;
		margin: 0;
		min-width: 0;
	}
	.domain__tagline {
		font-size: 0.8125rem;
		line-height: 1.5;
		color: #374151;
		margin: 0;
	}
	.domain__projects {
		list-style: none;
		margin: 4px 0 0;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}
	.domain__projects li {
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 3px 7px;
		background: var(--accent);
		color: #ffffff;
		border: 1.5px solid #000;
		letter-spacing: 0.03em;
	}

	/* ---------- Beliefs ---------- */
	.belief-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 14px;
	}
	@media (max-width: 720px) {
		.belief-grid {
			grid-template-columns: minmax(0, 1fr);
		}
	}
	.belief {
		background: #f9fafb;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 12px 14px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.belief__title {
		font-size: 0.875rem;
		font-weight: 700;
		color: #000;
		margin: 0;
	}
	.belief__desc {
		font-size: 0.8125rem;
		line-height: 1.5;
		color: #374151;
		margin: 0;
	}

	/* ---------- Audience ---------- */
	.audience {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 6px;
	}
	.audience li {
		position: relative;
		padding: 6px 10px 6px 18px;
		font-size: 0.875rem;
		color: #1f2937;
		background: #f9fafb;
		border-left: 4px solid var(--accent);
	}
	.audience__sep {
		color: var(--accent-dark);
		font-weight: 700;
		margin: 0 6px;
	}
	.audience strong {
		color: #000;
	}

	/* ---------- Tokenomics table ---------- */
	.table-wrap {
		overflow-x: auto;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
	}
	.tokenomics {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.8125rem;
	}
	.tokenomics thead th {
		background: var(--accent);
		color: #ffffff;
		text-align: left;
		padding: 8px 10px;
		border-bottom: 2px solid #000;
		font-weight: 700;
		letter-spacing: 0.04em;
	}
	.tokenomics tbody td {
		padding: 7px 10px;
		border-top: 1px solid #d4d4d8;
		color: #1f2937;
	}
	.tokenomics tbody tr:nth-child(odd) td {
		background: #fafafa;
	}

	/* ---------- Economics grid ---------- */
	.econ-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 12px;
	}
	@media (max-width: 720px) {
		.econ-grid {
			grid-template-columns: minmax(0, 1fr);
		}
	}
	.econ {
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 10px 14px;
	}
	.econ__label {
		font-size: 0.6875rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
		font-weight: 700;
		margin-bottom: 2px;
	}
	.econ__value {
		font-size: 1rem;
		font-weight: 700;
		color: #000;
	}

	/* ---------- Roadmap ---------- */
	.roadmap {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	.phase {
		position: relative;
		background: #f9fafb;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 12px 14px 12px 22px;
	}
	.phase::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.phase__header {
		display: flex;
		align-items: center;
		gap: 10px;
		margin-bottom: 2px;
		flex-wrap: wrap;
	}
	.phase__title {
		flex: 0 1 auto;
		font-size: 0.9375rem;
		font-weight: 700;
		color: var(--accent-dark);
		margin: 0;
	}
	.phase__subtitle {
		font-size: 0.75rem;
		color: #6b7280;
		font-style: italic;
		margin: 0 0 8px;
	}
	.phase__items {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 4px;
	}
	.phase__items li {
		display: grid;
		grid-template-columns: 18px 1fr;
		gap: 6px;
		font-size: 0.8125rem;
		line-height: 1.45;
		color: #1f2937;
	}
	.phase__icon {
		color: var(--accent-dark);
		font-weight: 700;
		text-align: center;
	}

	/* ---------- Closing ---------- */
	.closing {
		background: #000000;
		color: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 24px 24px;
		text-align: center;
		display: flex;
		flex-direction: column;
		gap: 10px;
		position: relative;
	}
	.closing::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(
			to right,
			#22c55e 0%,
			#22c55e 20%,
			#3b82f6 20%,
			#3b82f6 40%,
			#a855f7 40%,
			#a855f7 60%,
			#f97316 60%,
			#f97316 80%,
			#ef4444 80%,
			#ef4444 100%
		);
		border-bottom: 2px solid #000;
	}
	.closing__headline {
		font-size: 1.25rem;
		font-weight: 700;
		margin: 0;
		color: #22c55e;
		letter-spacing: 0.02em;
	}
	.closing__body {
		font-size: 0.9375rem;
		line-height: 1.55;
		color: #e5e7eb;
		margin: 0;
		max-width: 720px;
		align-self: center;
	}
</style>
