<script lang="ts">
	import { onMount } from 'svelte';
	import { PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import {
		heroSubtitle as staticHeroSubtitle,
		serviceSections as staticServiceSections,
		workflowSteps as staticWorkflowSteps,
		whyCyberdynePoints as staticWhyPoints,
		ctaHeadline as staticCtaHeadline,
		ctaBody as staticCtaBody,
		ctaPills as staticCtaPills,
		type ServicePalette
	} from '$lib/data/services';
	import { fetchServicesPage, type ServicesPagePayload } from '$lib/api/contentApi';

	// Stale-while-revalidate. Static data renders instantly; API
	// response replaces it on success; on failure the static stays.
	let page = $state<ServicesPagePayload>({
		sections: staticServiceSections.map((s) => ({ ...s, fullWidth: s.fullWidth ?? false })),
		heroSubtitle: staticHeroSubtitle,
		workflowSteps: [...staticWorkflowSteps],
		whyPoints: [...staticWhyPoints],
		ctaHeadline: staticCtaHeadline,
		ctaBody: staticCtaBody,
		ctaPills: [...staticCtaPills]
	});

	onMount(async () => {
		page = await fetchServicesPage();
	});

	// Backwards-compat aliases for the existing template references.
	const heroSubtitle = $derived(page.heroSubtitle);
	const serviceSections = $derived(page.sections);
	const workflowSteps = $derived(page.workflowSteps);
	const whyCyberdynePoints = $derived(page.whyPoints);
	const ctaHeadline = $derived(page.ctaHeadline);
	const ctaBody = $derived(page.ctaBody);
	const ctaPills = $derived(page.ctaPills);

	const paletteVars: Record<ServicePalette, { accent: string; accentDark: string }> = {
		blue: { accent: '#3b82f6', accentDark: '#1d4ed8' },
		green: { accent: '#22c55e', accentDark: '#15803d' },
		purple: { accent: '#a855f7', accentDark: '#7e22ce' },
		orange: { accent: '#f97316', accentDark: '#c2410c' },
		red: { accent: '#ef4444', accentDark: '#b91c1c' }
	};

	const workflowPalette = paletteVars.orange;
	const whyPalette = paletteVars.purple;
</script>

<div class="services-view">
	<header class="hero">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">⚙️</span>
			<h1 class="hero__title">CYBERDYNE SERVICES</h1>
		</div>
		<p class="hero__tagline">{heroSubtitle}</p>
	</header>

	<PixelScrollArea maxHeight="100%" ariaLabel="Services">
		<div class="content">
			<!-- Services grid -->
			<div class="services-grid">
				{#each serviceSections as section}
					{@const p = paletteVars[section.palette]}
					<article
						class="service-card"
						class:service-card--full={section.fullWidth}
						style="--accent: {p.accent}; --accent-dark: {p.accentDark};"
					>
						<header class="service-card__header">
							<div class="service-card__icon" aria-hidden="true">{section.icon}</div>
							<h2 class="service-card__title">{section.title}</h2>
						</header>
						<p class="service-card__intro">{section.intro}</p>
						<ul class="service-card__bullets">
							{#each section.bullets as bullet}
								<li>
									<strong>{bullet.title}</strong>
									<span>{bullet.description}</span>
								</li>
							{/each}
						</ul>
					</article>
				{/each}
			</div>

			<!-- How we work -->
			<section
				class="work-section"
				style="--accent: {workflowPalette.accent}; --accent-dark: {workflowPalette.accentDark};"
			>
				<h2 class="work-section__title">How We Work</h2>
				<p class="work-section__lead">Six steps from idea to running software, with no theatre in between.</p>
				<ol class="workflow">
					{#each workflowSteps as step, i}
						<li class="workflow__step">
							<div class="workflow__num">{i + 1}</div>
							<div class="workflow__body">
								<div class="workflow__name">{step.title}</div>
								<div class="workflow__desc">{step.description}</div>
							</div>
						</li>
					{/each}
				</ol>
			</section>

			<!-- Why Cyberdyne -->
			<section
				class="why-section"
				style="--accent: {whyPalette.accent}; --accent-dark: {whyPalette.accentDark};"
			>
				<h2 class="why-section__title">Why Cyberdyne</h2>
				<div class="why-grid">
					{#each whyCyberdynePoints as p}
						<div class="why-card">
							<h3 class="why-card__title">{p.title}</h3>
							<p class="why-card__desc">{p.description}</p>
						</div>
					{/each}
				</div>
			</section>

			<!-- CTA -->
			<section class="cta">
				<h2 class="cta__headline">{ctaHeadline}</h2>
				<p class="cta__body">{ctaBody}</p>
				<div class="cta__pills">
					{#each ctaPills as pill}
						<span class="cta__pill">{pill}</span>
					{/each}
				</div>
			</section>
		</div>
	</PixelScrollArea>
</div>

<style>
	.services-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		display: flex;
		flex-direction: column;
	}

	/* ---------- Hero ---------- */
	.hero {
		padding: 22px 28px;
		background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
		flex: 0 0 auto;
	}
	.hero__brand {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 8px;
	}
	.hero__mark {
		font-size: 1.6rem;
	}
	.hero__title {
		font-size: 1.6rem;
		font-weight: 800;
		margin: 0;
		letter-spacing: 0.1em;
		color: #ffffff;
	}
	.hero__tagline {
		margin: 0;
		font-size: 0.9rem;
		line-height: 1.55;
		color: #e0e7ff;
		max-width: 880px;
	}

	/* ---------- Content layout ---------- */
	.content {
		padding: 24px 20px 32px;
		display: flex;
		flex-direction: column;
		gap: 22px;
		max-width: 1200px;
		margin: 0 auto;
	}

	/* ---------- Services grid ---------- */
	.services-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 18px;
	}
	@media (max-width: 720px) {
		.services-grid {
			grid-template-columns: minmax(0, 1fr);
		}
	}

	.service-card {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 18px 18px 18px 26px;
		display: flex;
		flex-direction: column;
		gap: 12px;
		transition: transform 0.15s ease, box-shadow 0.15s ease;
	}
	.service-card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.service-card:hover {
		transform: translate(-2px, -2px);
		box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.55);
	}
	.service-card--full {
		grid-column: 1 / -1;
	}

	.service-card__header {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.service-card__icon {
		flex: 0 0 auto;
		width: 40px;
		height: 40px;
		border: 2px solid #000;
		background: var(--accent);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 20px;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.4);
	}
	.service-card__title {
		flex: 1 1 auto;
		font-size: 1.125rem;
		font-weight: 700;
		color: #000;
		margin: 0;
		line-height: 1.2;
		min-width: 0;
	}

	.service-card__intro {
		font-size: 0.875rem;
		line-height: 1.55;
		color: #1f2937;
		margin: 0;
		font-weight: 500;
	}

	.service-card__bullets {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 6px;
	}
	.service-card--full .service-card__bullets {
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 6px 22px;
	}
	@media (max-width: 720px) {
		.service-card--full .service-card__bullets {
			grid-template-columns: minmax(0, 1fr);
		}
	}
	.service-card__bullets li {
		position: relative;
		padding-left: 18px;
		font-size: 0.8125rem;
		line-height: 1.5;
		color: #374151;
	}
	.service-card__bullets li::before {
		content: '▸';
		position: absolute;
		left: 0;
		top: 0;
		color: var(--accent-dark);
		font-weight: 700;
	}
	.service-card__bullets strong {
		color: #000;
		font-weight: 700;
	}

	/* ---------- How We Work ---------- */
	.work-section {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 20px 20px 20px 28px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.work-section::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.work-section__title {
		font-size: 1.125rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
		margin: 0;
	}
	.work-section__lead {
		font-size: 0.9375rem;
		color: #1f2937;
		margin: 0;
	}
	.workflow {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 12px;
	}
	@media (max-width: 900px) {
		.workflow {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
	}
	@media (max-width: 540px) {
		.workflow {
			grid-template-columns: minmax(0, 1fr);
		}
	}
	.workflow__step {
		display: flex;
		align-items: flex-start;
		gap: 12px;
		background: #f9fafb;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 12px 14px;
	}
	.workflow__num {
		flex: 0 0 auto;
		width: 28px;
		height: 28px;
		border: 2px solid #000;
		background: var(--accent);
		color: #000;
		font-weight: 800;
		font-size: 0.875rem;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.35);
	}
	.workflow__body {
		min-width: 0;
	}
	.workflow__name {
		font-size: 0.9375rem;
		font-weight: 700;
		color: #000;
		line-height: 1.2;
	}
	.workflow__desc {
		font-size: 0.8125rem;
		color: #374151;
		line-height: 1.45;
		margin-top: 2px;
	}

	/* ---------- Why Cyberdyne ---------- */
	.why-section {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 20px 20px 20px 28px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.why-section::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.why-section__title {
		font-size: 1.125rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
		margin: 0;
	}
	.why-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 14px;
	}
	@media (max-width: 720px) {
		.why-grid {
			grid-template-columns: minmax(0, 1fr);
		}
	}
	.why-card {
		background: #f9fafb;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 12px 14px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.why-card__title {
		font-size: 0.875rem;
		font-weight: 700;
		color: #000;
		margin: 0;
	}
	.why-card__desc {
		font-size: 0.8125rem;
		line-height: 1.5;
		color: #374151;
		margin: 0;
	}

	/* ---------- CTA ---------- */
	.cta {
		background: #000;
		color: #fff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 24px;
		text-align: center;
		display: flex;
		flex-direction: column;
		gap: 14px;
		position: relative;
	}
	.cta::before {
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
	.cta__headline {
		font-size: 1.25rem;
		font-weight: 700;
		margin: 0;
		color: #22c55e;
		letter-spacing: 0.04em;
	}
	.cta__body {
		font-size: 0.9375rem;
		line-height: 1.55;
		color: #e5e7eb;
		margin: 0;
		max-width: 720px;
		align-self: center;
	}
	.cta__pills {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 8px;
		margin-top: 4px;
	}
	.cta__pill {
		background: #ffffff;
		color: #000;
		border: 2px solid #22c55e;
		padding: 4px 10px;
		font-size: 0.75rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		text-transform: uppercase;
	}
</style>
