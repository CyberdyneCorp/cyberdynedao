<script lang="ts">
	import { PixelButton, PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import {
		teamMembers,
		teamHeroTitle,
		teamHeroBody,
		teamCtaHeadline,
		teamCtaBody,
		teamCtaButton,
		type TeamPalette
	} from '$lib/data/team';

	const paletteVars: Record<TeamPalette, { accent: string; accentDark: string }> = {
		blue: { accent: '#3b82f6', accentDark: '#1d4ed8' },
		green: { accent: '#22c55e', accentDark: '#15803d' },
		purple: { accent: '#a855f7', accentDark: '#7e22ce' },
		orange: { accent: '#f97316', accentDark: '#c2410c' }
	};
	const cardStyle = (p: TeamPalette) => {
		const v = paletteVars[p];
		return `--accent: ${v.accent}; --accent-dark: ${v.accentDark};`;
	};
</script>

<div class="team-view">
	<PixelScrollArea maxHeight="100%" ariaLabel="Team">
		<div class="content">
			<!-- About Us -->
			<section class="about">
				<h1 class="about__title">{teamHeroTitle}</h1>
				<p class="about__body">{teamHeroBody}</p>
				<div class="about__divider" aria-hidden="true"></div>
				<div class="about__stats">
					<div class="about__stat"><strong>{teamMembers.length}</strong> Builders</div>
					<div class="about__stat"><strong>18</strong> Projects</div>
					<div class="about__stat"><strong>5</strong> Domains</div>
				</div>
			</section>

			<!-- Team grid -->
			<section class="team-section">
				<header class="team-section__header">
					<h2 class="team-section__title">Meet the Team</h2>
					<div class="team-section__rule" aria-hidden="true"></div>
				</header>

				<div class="team-grid">
					{#each teamMembers as member}
						<article class="member" style={cardStyle(member.palette)}>
							<div class="member__avatar-wrap">
								<img src={member.image} alt={member.name} class="member__avatar" />
							</div>
							<div class="member__body">
								<h3 class="member__name">{member.name}</h3>
								<div class="member__role">{member.title}</div>
								<p class="member__bio">{member.bio}</p>
								<ul class="member__tags" aria-label="Skills">
									{#each member.tags as tag}
										<li class="member__tag">{tag}</li>
									{/each}
								</ul>
							</div>
						</article>
					{/each}
				</div>
			</section>

			<!-- CTA -->
			<section class="cta">
				<h2 class="cta__headline">{teamCtaHeadline}</h2>
				<p class="cta__body">{teamCtaBody}</p>
				<div class="cta__action">
					<PixelButton variant="solid" size="lg">{teamCtaButton}</PixelButton>
				</div>
			</section>
		</div>
	</PixelScrollArea>
</div>

<style>
	.team-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
	}

	.content {
		max-width: 1100px;
		margin: 0 auto;
		padding: 24px 20px 32px;
		display: flex;
		flex-direction: column;
		gap: 24px;
	}

	/* ---------- About ---------- */
	.about {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 26px 26px 22px 34px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.about::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: #3b82f6;
		border-right: 2px solid #000;
	}
	.about__title {
		font-size: 1.625rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #1d4ed8;
		margin: 0;
		text-align: center;
	}
	.about__body {
		font-size: 1rem;
		line-height: 1.6;
		color: #1f2937;
		margin: 0;
		text-align: center;
		max-width: 760px;
		align-self: center;
	}
	.about__divider {
		height: 2px;
		background: linear-gradient(
			to right,
			#22c55e 0%,
			#22c55e 25%,
			#3b82f6 25%,
			#3b82f6 50%,
			#a855f7 50%,
			#a855f7 75%,
			#f97316 75%,
			#f97316 100%
		);
		width: 100%;
		max-width: 320px;
		align-self: center;
	}
	.about__stats {
		display: flex;
		justify-content: center;
		gap: 22px;
		flex-wrap: wrap;
		font-size: 0.8125rem;
		color: #374151;
	}
	.about__stat strong {
		display: block;
		font-size: 1.25rem;
		color: #000;
		font-weight: 800;
		text-align: center;
	}

	/* ---------- Team section header ---------- */
	.team-section__header {
		display: flex;
		align-items: center;
		gap: 14px;
		margin-bottom: 4px;
	}
	.team-section__title {
		font-size: 1rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: #000;
		margin: 0;
	}
	.team-section__rule {
		flex: 1 1 auto;
		height: 2px;
		background: #000;
	}

	/* ---------- Team grid ---------- */
	.team-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 16px;
	}
	@media (max-width: 720px) {
		.team-grid { grid-template-columns: minmax(0, 1fr); }
	}

	.member {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 16px 18px 16px 26px;
		display: grid;
		grid-template-columns: 96px 1fr;
		gap: 16px;
		transition: transform 0.15s ease, box-shadow 0.15s ease;
	}
	.member::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.member:hover {
		transform: translate(-2px, -2px);
		box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.55);
	}

	.member__avatar-wrap {
		width: 96px;
		height: 96px;
		border: 2px solid #000;
		background: var(--accent);
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}
	.member__avatar {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.member__body {
		min-width: 0;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.member__name {
		font-size: 1.125rem;
		font-weight: 700;
		color: #000;
		margin: 0;
		line-height: 1.2;
		word-break: break-word;
	}
	.member__role {
		font-size: 0.6875rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: var(--accent-dark);
	}
	.member__bio {
		font-size: 0.8125rem;
		line-height: 1.55;
		color: #374151;
		margin: 0;
	}
	.member__tags {
		list-style: none;
		margin: 4px 0 0;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: 5px;
	}
	.member__tag {
		font-size: 0.6875rem;
		font-weight: 700;
		padding: 2px 7px;
		background: var(--accent);
		color: #ffffff;
		border: 1.5px solid #000;
		letter-spacing: 0.02em;
		white-space: nowrap;
	}

	/* ---------- CTA ---------- */
	.cta {
		background: #000;
		color: #fff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 26px 24px 24px;
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
			#22c55e 25%,
			#3b82f6 25%,
			#3b82f6 50%,
			#a855f7 50%,
			#a855f7 75%,
			#f97316 75%,
			#f97316 100%
		);
		border-bottom: 2px solid #000;
	}
	.cta__headline {
		font-size: 1.25rem;
		font-weight: 800;
		color: #22c55e;
		margin: 0;
		letter-spacing: 0.04em;
	}
	.cta__body {
		font-size: 0.9375rem;
		line-height: 1.55;
		color: #e5e7eb;
		margin: 0;
		max-width: 640px;
		align-self: center;
	}
	.cta__action {
		display: flex;
		justify-content: center;
		margin-top: 4px;
	}
</style>
