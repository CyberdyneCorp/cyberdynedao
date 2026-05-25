<script lang="ts">
	import type { LearningModule, LearningPath } from '$lib/types/components';
	import {
		createLearnViewModel,
		getLevelPalette,
		getCategoryPalette,
		type LearnPalette
	} from '$lib/viewmodels/learnViewModel';
	import {
		learnHeroSubtitle,
		learnWelcomeHeadline,
		learnWelcomeBody,
		resourceGroups
	} from '$lib/data/learn';

	const vm = createLearnViewModel();
	const { selectedModule, selectedPath, activeTab } = vm;
	const { modules: learningModules, paths: learningPaths } = vm;

	function selectModule(module: LearningModule) { vm.selectModule(module); }
	function selectPath(path: LearningPath) { vm.selectPath(path); }

	const palette: Record<LearnPalette, { accent: string; accentDark: string }> = {
		blue: { accent: '#3b82f6', accentDark: '#1d4ed8' },
		green: { accent: '#22c55e', accentDark: '#15803d' },
		purple: { accent: '#a855f7', accentDark: '#7e22ce' },
		orange: { accent: '#f97316', accentDark: '#c2410c' },
		red: { accent: '#ef4444', accentDark: '#b91c1c' }
	};

	const cardStyle = (paletteKey: LearnPalette) => {
		const p = palette[paletteKey];
		return `--accent: ${p.accent}; --accent-dark: ${p.accentDark};`;
	};
</script>

<div class="learn-view">
	<!-- Hero -->
	<header class="hero">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">🎓</span>
			<h1 class="hero__title">CYBERDYNE ACADEMY</h1>
		</div>
		<p class="hero__tagline">{learnHeroSubtitle}</p>
	</header>

	<!-- Tabs -->
	<div class="tabs" role="tablist">
		<button
			class="tab"
			class:tab--active={$activeTab === 'modules'}
			role="tab"
			aria-selected={$activeTab === 'modules'}
			on:click={() => vm.setTab('modules')}
		>
			<span class="tab__icon" aria-hidden="true">📚</span>
			Modules
			<span class="tab__count">{learningModules.length}</span>
		</button>
		<button
			class="tab"
			class:tab--active={$activeTab === 'paths'}
			role="tab"
			aria-selected={$activeTab === 'paths'}
			on:click={() => vm.setTab('paths')}
		>
			<span class="tab__icon" aria-hidden="true">🗺️</span>
			Paths
			<span class="tab__count">{learningPaths.length}</span>
		</button>
		<button
			class="tab"
			class:tab--active={$activeTab === 'resources'}
			role="tab"
			aria-selected={$activeTab === 'resources'}
			on:click={() => vm.setTab('resources')}
		>
			<span class="tab__icon" aria-hidden="true">📖</span>
			Resources
		</button>
	</div>

	<!-- Body: sidebar + main -->
	<div class="body">
		<aside class="sidebar">
			{#if $activeTab === 'modules'}
				<div class="list">
					{#each learningModules as module}
						{@const catPal = getCategoryPalette(module.category)}
						{@const lvlPal = getLevelPalette(module.level)}
						<button
							type="button"
							class="module-card"
							class:module-card--active={$selectedModule?.id === module.id}
							style={cardStyle(catPal)}
							on:click={() => selectModule(module)}
						>
							<div class="module-card__head">
								<span class="module-card__icon" aria-hidden="true">{module.icon}</span>
								<h3 class="module-card__title">{module.title}</h3>
							</div>
							<div class="module-card__meta">
								<span class="chip chip--cat" style={cardStyle(catPal)}>{module.category}</span>
								<span class="chip chip--lvl" style={cardStyle(lvlPal)}>{module.level}</span>
							</div>
							<div class="module-card__time">⏱ {module.duration}</div>
						</button>
					{/each}
				</div>
			{:else if $activeTab === 'paths'}
				<div class="list">
					{#each learningPaths as path, i}
						{@const pal: LearnPalette = (['blue','green','purple','orange','red'] as LearnPalette[])[i % 5]}
						<button
							type="button"
							class="path-card"
							class:path-card--active={$selectedPath?.id === path.id}
							style={cardStyle(pal)}
							on:click={() => selectPath(path)}
						>
							<div class="path-card__head">
								<span class="path-card__icon" aria-hidden="true">{path.icon}</span>
								<h3 class="path-card__title">{path.title}</h3>
							</div>
							<p class="path-card__desc">{path.description}</p>
							<div class="path-card__time">📅 {path.estimatedTime}</div>
						</button>
					{/each}
				</div>
			{:else}
				<div class="list">
					{#each resourceGroups as group, i}
						{@const pal: LearnPalette = (['blue','purple','orange','green'] as LearnPalette[])[i % 4]}
						<div class="resource-card" style={cardStyle(pal)}>
							<h3 class="resource-card__title">
								<span aria-hidden="true">{group.icon}</span>
								{group.title}
							</h3>
							<ul class="resource-card__links">
								{#each group.links as link}
									<li>
										{#if link.disabled}
											<span class="resource-link resource-link--disabled">{link.label}</span>
										{:else}
											<a class="resource-link" href={link.href} target="_blank" rel="noopener noreferrer">
												{link.label}
											</a>
										{/if}
									</li>
								{/each}
							</ul>
						</div>
					{/each}
				</div>
			{/if}
		</aside>

		<section class="main">
			{#if $selectedModule}
				{@const catPal = getCategoryPalette($selectedModule.category)}
				{@const lvlPal = getLevelPalette($selectedModule.level)}
				<article class="detail" style={cardStyle(catPal)}>
					<header class="detail__head">
						<div class="detail__icon" aria-hidden="true">{$selectedModule.icon}</div>
						<div class="detail__head-text">
							<h2 class="detail__title">{$selectedModule.title}</h2>
							<div class="detail__meta">
								<span class="chip chip--cat" style={cardStyle(catPal)}>{$selectedModule.category}</span>
								<span class="chip chip--lvl" style={cardStyle(lvlPal)}>{$selectedModule.level}</span>
								<span class="detail__time">⏱ {$selectedModule.duration}</span>
							</div>
						</div>
					</header>
					<p class="detail__desc">{$selectedModule.description}</p>

					<div class="detail__section" style={cardStyle(catPal)}>
						<h3 class="detail__section-title">Learning Topics</h3>
						<ul class="topics">
							{#each $selectedModule.topics as topic}
								<li>{topic}</li>
							{/each}
						</ul>
					</div>

					<div class="actions">
						<button type="button" class="btn btn--primary" style={cardStyle(catPal)}>Start Learning</button>
						<button type="button" class="btn btn--ghost">Add to Favorites</button>
					</div>
				</article>
			{:else if $selectedPath}
				{@const pal: LearnPalette = 'purple'}
				<article class="detail" style={cardStyle(pal)}>
					<header class="detail__head">
						<div class="detail__icon" aria-hidden="true">{$selectedPath.icon}</div>
						<div class="detail__head-text">
							<h2 class="detail__title">{$selectedPath.title}</h2>
							<p class="detail__desc">{$selectedPath.description}</p>
							<div class="detail__time-row">📅 Estimated completion: {$selectedPath.estimatedTime}</div>
						</div>
					</header>

					<div class="detail__section" style={cardStyle(pal)}>
						<h3 class="detail__section-title">Modules in this Path</h3>
						<ol class="path-modules">
							{#each $selectedPath.modules as moduleId, index}
								{@const module = learningModules.find(m => m.id === moduleId)}
								{#if module}
									{@const mPal = getCategoryPalette(module.category)}
									{@const lvlPal = getLevelPalette(module.level)}
									<li class="path-module" style={cardStyle(mPal)}>
										<div class="path-module__num">{index + 1}</div>
										<div class="path-module__icon" aria-hidden="true">{module.icon}</div>
										<div class="path-module__body">
											<div class="path-module__title">{module.title}</div>
											<div class="path-module__time">⏱ {module.duration}</div>
										</div>
										<span class="chip chip--lvl" style={cardStyle(lvlPal)}>{module.level}</span>
									</li>
								{/if}
							{/each}
						</ol>
					</div>

					<div class="actions">
						<button type="button" class="btn btn--primary" style={cardStyle(pal)}>Start Learning Path</button>
						<button type="button" class="btn btn--ghost">Save for Later</button>
					</div>
				</article>
			{:else}
				<div class="welcome">
					<div class="welcome__mark" aria-hidden="true">🎓</div>
					<h2 class="welcome__title">{learnWelcomeHeadline}</h2>
					<p class="welcome__body">{learnWelcomeBody}</p>

					<div class="stat-grid">
						<div class="stat" style={cardStyle('blue')}>
							<div class="stat__icon" aria-hidden="true">📚</div>
							<div class="stat__num">{learningModules.length}</div>
							<div class="stat__label">Modules</div>
							<div class="stat__sub">From fundamentals to mainnet</div>
						</div>
						<div class="stat" style={cardStyle('purple')}>
							<div class="stat__icon" aria-hidden="true">🗺️</div>
							<div class="stat__num">{learningPaths.length}</div>
							<div class="stat__label">Paths</div>
							<div class="stat__sub">Curated end-to-end tracks</div>
						</div>
						<div class="stat" style={cardStyle('green')}>
							<div class="stat__icon" aria-hidden="true">🏆</div>
							<div class="stat__num">∞</div>
							<div class="stat__label">Open Source</div>
							<div class="stat__sub">Every reference is public</div>
						</div>
					</div>
				</div>
			{/if}
		</section>
	</div>
</div>

<style>
	.learn-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		height: 100%;
		display: flex;
		flex-direction: column;
	}

	/* ---------- Hero ---------- */
	.hero {
		padding: 18px 24px;
		background: linear-gradient(135deg, #4c1d95 0%, #7e22ce 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
		flex: 0 0 auto;
	}
	.hero__brand {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 6px;
	}
	.hero__mark { font-size: 1.5rem; }
	.hero__title {
		font-size: 1.5rem;
		font-weight: 800;
		letter-spacing: 0.1em;
		margin: 0;
		color: #ffffff;
	}
	.hero__tagline {
		margin: 0;
		font-size: 0.875rem;
		line-height: 1.5;
		color: #e9d5ff;
		max-width: 860px;
	}

	/* ---------- Tabs ---------- */
	.tabs {
		display: flex;
		gap: 0;
		background: #f3f4f6;
		border-bottom: 2px solid #000;
		flex: 0 0 auto;
		padding: 0 12px;
	}
	.tab {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		padding: 10px 16px;
		font-family: inherit;
		font-size: 0.8125rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: #4b5563;
		background: transparent;
		border: none;
		border-right: 2px solid #000;
		cursor: pointer;
		transition: background 0.12s;
	}
	.tab:first-child { border-left: 2px solid #000; }
	.tab:hover { background: #e5e7eb; }
	.tab--active {
		background: #ffffff;
		color: #000;
		box-shadow: inset 0 -3px 0 #22c55e;
	}
	.tab__icon { font-size: 1rem; }
	.tab__count {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: 22px;
		height: 18px;
		padding: 0 5px;
		font-size: 0.6875rem;
		font-weight: 700;
		background: #000;
		color: #fff;
		border-radius: 2px;
	}

	/* ---------- Body layout ---------- */
	.body {
		flex: 1 1 auto;
		display: flex;
		min-height: 0;
	}
	.sidebar {
		width: 36%;
		max-width: 380px;
		min-width: 260px;
		border-right: 2px solid #000;
		background: #f9fafb;
		overflow-y: auto;
	}
	.main {
		flex: 1 1 auto;
		overflow-y: auto;
		padding: 18px 20px;
	}
	@media (max-width: 720px) {
		.body { flex-direction: column; }
		.sidebar { width: 100%; max-width: none; max-height: 40vh; border-right: 0; border-bottom: 2px solid #000; }
	}

	.list {
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	/* ---------- Module card (sidebar) ---------- */
	.module-card,
	.path-card {
		all: unset;
		display: flex;
		flex-direction: column;
		gap: 6px;
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 10px 12px 10px 16px;
		cursor: pointer;
		transition: transform 0.12s ease, box-shadow 0.12s ease;
	}
	.module-card::before,
	.path-card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.module-card:hover,
	.path-card:hover {
		transform: translate(-1px, -1px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
	}
	.module-card:focus-visible,
	.path-card:focus-visible {
		outline: 2px solid var(--accent-dark);
		outline-offset: 2px;
	}
	.module-card--active,
	.path-card--active {
		background: #f0fdf4;
		box-shadow: 4px 4px 0 var(--accent-dark);
	}
	.module-card__head,
	.path-card__head {
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.module-card__icon,
	.path-card__icon {
		font-size: 1.1rem;
		flex: 0 0 auto;
		width: 26px;
		height: 26px;
		border: 1.5px solid #000;
		background: var(--accent);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 14px;
	}
	.module-card__title,
	.path-card__title {
		font-size: 0.8125rem;
		font-weight: 700;
		color: #000;
		margin: 0;
		line-height: 1.25;
		min-width: 0;
		flex: 1 1 auto;
		word-break: break-word;
	}
	.module-card__meta {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		margin-left: 34px;
	}
	.module-card__time,
	.path-card__time {
		font-size: 0.6875rem;
		color: #6b7280;
		margin-left: 34px;
	}
	.path-card__desc {
		font-size: 0.75rem;
		line-height: 1.4;
		color: #374151;
		margin: 4px 0 0 34px;
	}

	/* ---------- Chips ---------- */
	.chip {
		display: inline-flex;
		align-items: center;
		padding: 1px 6px;
		font-size: 0.625rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		border: 1.5px solid #000;
		background: var(--accent);
		color: #ffffff;
		white-space: nowrap;
	}
	.chip--lvl { background: var(--accent); }

	/* ---------- Resource card ---------- */
	.resource-card {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 12px 14px 12px 18px;
	}
	.resource-card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.resource-card__title {
		font-size: 0.8125rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--accent-dark);
		margin: 0 0 8px;
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.resource-card__links {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.resource-link {
		display: inline-flex;
		font-size: 0.75rem;
		color: var(--accent-dark);
		text-decoration: none;
		font-weight: 600;
	}
	.resource-link:hover { text-decoration: underline; }
	.resource-link--disabled {
		color: #9ca3af;
		font-style: italic;
		cursor: not-allowed;
	}

	/* ---------- Detail (main) ---------- */
	.detail {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 18px 18px 18px 26px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.detail::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.detail__head {
		display: flex;
		gap: 14px;
		align-items: flex-start;
	}
	.detail__icon {
		flex: 0 0 auto;
		width: 44px;
		height: 44px;
		border: 2px solid #000;
		background: var(--accent);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 22px;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.4);
	}
	.detail__head-text { min-width: 0; flex: 1 1 auto; }
	.detail__title {
		font-size: 1.25rem;
		font-weight: 800;
		color: #000;
		margin: 0 0 6px;
		line-height: 1.2;
	}
	.detail__meta {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		align-items: center;
		margin-bottom: 4px;
	}
	.detail__time {
		font-size: 0.75rem;
		color: #6b7280;
	}
	.detail__time-row {
		font-size: 0.75rem;
		color: var(--accent-dark);
		margin-top: 4px;
		font-weight: 600;
	}
	.detail__desc {
		font-size: 0.9375rem;
		line-height: 1.55;
		color: #1f2937;
		margin: 0;
	}

	.detail__section {
		position: relative;
		background: #f9fafb;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.35);
		padding: 12px 14px;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.detail__section-title {
		font-size: 0.75rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
		margin: 0;
	}

	/* ---------- Topic checklist ---------- */
	.topics {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 6px 14px;
	}
	@media (max-width: 540px) {
		.topics { grid-template-columns: minmax(0, 1fr); }
	}
	.topics li {
		position: relative;
		padding-left: 22px;
		font-size: 0.8125rem;
		color: #1f2937;
		line-height: 1.4;
	}
	.topics li::before {
		content: '▸';
		position: absolute;
		left: 0;
		top: 0;
		color: var(--accent-dark);
		font-weight: 700;
	}

	/* ---------- Path modules ---------- */
	.path-modules {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.path-module {
		position: relative;
		display: grid;
		grid-template-columns: 28px 28px 1fr auto;
		gap: 10px;
		align-items: center;
		background: #ffffff;
		border: 1.5px solid #000;
		padding: 8px 10px 8px 14px;
	}
	.path-module::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 5px;
		background: var(--accent);
		border-right: 1.5px solid #000;
	}
	.path-module__num {
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.75rem;
		font-weight: 800;
		background: var(--accent);
		border: 1.5px solid #000;
		color: #000;
	}
	.path-module__icon {
		font-size: 16px;
		text-align: center;
	}
	.path-module__body { min-width: 0; }
	.path-module__title {
		font-size: 0.8125rem;
		font-weight: 700;
		color: #000;
		line-height: 1.2;
	}
	.path-module__time {
		font-size: 0.6875rem;
		color: #6b7280;
		margin-top: 1px;
	}

	/* ---------- Buttons ---------- */
	.actions {
		display: flex;
		gap: 10px;
		flex-wrap: wrap;
	}
	.btn {
		font-family: inherit;
		font-size: 0.8125rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		padding: 8px 14px;
		border: 2px solid #000;
		cursor: pointer;
		transition: transform 0.1s ease, box-shadow 0.1s ease;
	}
	.btn--primary {
		background: var(--accent);
		color: #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
	}
	.btn--primary:hover {
		transform: translate(-1px, -1px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.55);
	}
	.btn--ghost {
		background: #ffffff;
		color: #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.3);
	}
	.btn--ghost:hover {
		background: #f3f4f6;
		transform: translate(-1px, -1px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.4);
	}

	/* ---------- Welcome ---------- */
	.welcome {
		text-align: center;
		max-width: 720px;
		margin: 24px auto;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 12px;
	}
	.welcome__mark {
		font-size: 2.25rem;
	}
	.welcome__title {
		font-size: 1.5rem;
		font-weight: 800;
		color: #000;
		margin: 0;
		letter-spacing: 0.02em;
	}
	.welcome__body {
		font-size: 0.9375rem;
		line-height: 1.6;
		color: #374151;
		margin: 0;
		max-width: 600px;
	}

	.stat-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 12px;
		margin-top: 12px;
		width: 100%;
	}
	@media (max-width: 720px) {
		.stat-grid { grid-template-columns: minmax(0, 1fr); }
	}
	.stat {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 16px 14px 18px 22px;
		display: flex;
		flex-direction: column;
		gap: 4px;
		align-items: flex-start;
		text-align: left;
	}
	.stat::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.stat__icon { font-size: 1.5rem; }
	.stat__num {
		font-size: 1.75rem;
		font-weight: 800;
		color: #000;
		line-height: 1;
	}
	.stat__label {
		font-size: 0.875rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--accent-dark);
	}
	.stat__sub {
		font-size: 0.75rem;
		color: #374151;
	}
</style>
