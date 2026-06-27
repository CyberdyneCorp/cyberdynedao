<script lang="ts">
	import { onMount } from 'svelte';
	import { PixelButton, Badge } from '@cyberdynecorp/svelte-ui-core';
	import { createLearningTracksViewModel } from '$lib/viewmodels/learningTracksViewModel';
	import type {
		DeadlineStatus,
		Enrollment,
		LearningModule,
		LearningPath,
		ModuleGate,
		ModuleProgress
	} from '$lib/api/learningApi';
	import { authVM } from '$lib/auth/authViewModel.svelte';
	import { t } from '$lib/i18n';

	const vm = createLearningTracksViewModel();
	const { paths, modules, myState, deadlines, selected, gating, eligibility, loading, enrolling, error } =
		vm;

	const authReady = $derived(authVM.isRestored && authVM.isAuthenticated);

	let loaded = $state(false);
	onMount(() => void vm.load({ authed: authReady }));
	// Re-load "me" data once auth restores after the first (anonymous) load.
	$effect(() => {
		if (authReady && !loaded) {
			loaded = true;
			void vm.load({ authed: true });
		}
	});

	const levelVariant: Record<string, 'success' | 'info' | 'danger'> = {
		Beginner: 'success',
		Intermediate: 'info',
		Advanced: 'danger'
	};
	const deadlineVariant: Record<DeadlineStatus, 'neutral' | 'info' | 'warning' | 'danger'> = {
		none: 'neutral',
		upcoming: 'info',
		urgent: 'warning',
		overdue: 'danger'
	};

	// ── Derived lookups (join catalogue + my state by slug) ──────────────
	const moduleBySlug = $derived(
		new Map<string, LearningModule>($modules.map((m) => [m.slug, m]))
	);
	const enrollmentByPath = $derived(
		new Map<string, Enrollment>($myState.enrollments.map((e) => [e.pathSlug, e]))
	);
	const progressByModule = $derived(
		new Map<string, ModuleProgress>($myState.progress.map((p) => [p.moduleSlug, p]))
	);
	const gateByModule = $derived(new Map<string, ModuleGate>($gating.map((g) => [g.moduleSlug, g])));
	const deadlineByPath = $derived(
		new Map($deadlines.map((d) => [d.pathSlug, d]))
	);

	// Ordered, resolved modules for the open path (skips slugs the catalogue
	// no longer resolves, e.g. an unpublished module).
	const selectedModules = $derived(
		$selected
			? $selected.moduleSlugs
					.map((slug) => moduleBySlug.get(slug))
					.filter((m): m is LearningModule => m !== undefined)
			: []
	);

	function pathProgressPercent(path: LearningPath): number {
		if (path.moduleSlugs.length === 0) return 0;
		const done = path.moduleSlugs.filter(
			(s) => (progressByModule.get(s)?.percent ?? 0) >= 100
		).length;
		return Math.round((done / path.moduleSlugs.length) * 100);
	}

	function openPath(slug: string): void {
		void vm.openPath(slug, { authed: authReady });
	}
</script>

<div class="tracks">
	{#if $selected}
		{@const path = $selected}
		{@const enrollment = enrollmentByPath.get(path.slug)}
		{@const deadline = deadlineByPath.get(path.slug)}
		<button class="link back" onclick={() => vm.close()}>{$t('tracks.backToTracks')}</button>

		<header class="detail__head">
			<span class="detail__icon" aria-hidden="true">{path.icon || '🧭'}</span>
			<div>
				<h2>{path.title}</h2>
				<p class="detail__desc">{path.description}</p>
				<p class="detail__meta">
					<span>{$t('tracks.estimatedTime', { time: path.estimatedTime })}</span>
					<span>·</span>
					<span>{$t('tracks.moduleCount', { count: String(path.moduleSlugs.length) })}</span>
				</p>
			</div>
		</header>

		{#if authReady}
			<div class="detail__status">
				{#if enrollment}
					<Badge variant={enrollment.status === 'completed' ? 'success' : 'info'} size="sm">
						{$t(`tracks.status.${enrollment.status}`)}
					</Badge>
					<div class="bar" title={`${pathProgressPercent(path)}%`}>
						<div class="bar__fill" style={`width:${pathProgressPercent(path)}%`}></div>
					</div>
					<span class="bar__label">{pathProgressPercent(path)}%</span>
				{:else}
					<PixelButton
						variant="solid"
						size="sm"
						disabled={$enrolling}
						onclick={() => vm.enrollInPath(path.slug)}
					>
						{$enrolling ? $t('tracks.enrolling') : $t('tracks.enroll')}
					</PixelButton>
				{/if}
				{#if deadline && deadline.status !== 'none'}
					<Badge variant={deadlineVariant[deadline.status]} size="sm">
						{$t(`tracks.deadline.${deadline.status}`, {
							days: String(Math.abs(deadline.daysRemaining ?? 0))
						})}
					</Badge>
				{/if}
			</div>
		{:else}
			<p class="hint">{$t('tracks.signInToEnroll')}</p>
		{/if}

		{#if $error}<p class="err">{$error}</p>{/if}

		<ol class="modules">
			{#each selectedModules as module, i (module.slug)}
				{@const gate = gateByModule.get(module.slug)}
				{@const prog = progressByModule.get(module.slug)}
				{@const done = (prog?.percent ?? 0) >= 100}
				{@const locked = authReady && gate ? !gate.unlocked : false}
				<li class="module" class:module--locked={locked} class:module--done={done}>
					<div class="module__index" aria-hidden="true">
						{#if done}✓{:else if locked}🔒{:else}{i + 1}{/if}
					</div>
					<div class="module__body">
						<div class="module__top">
							<span class="module__icon" aria-hidden="true">{module.icon || '📦'}</span>
							<h3>{module.title}</h3>
							<Badge variant={levelVariant[module.level] ?? 'info'} size="sm">
								{$t(`level.${module.level}`)}
							</Badge>
							{#if module.duration}<span class="module__dur">{module.duration}</span>{/if}
						</div>
						<p class="module__desc">{module.description}</p>
						{#if module.courses.length > 0}
							<ul class="courses">
								{#each module.courses as c (c.slug)}
									<li class="course-pill">{c.title}</li>
								{/each}
							</ul>
						{/if}
						{#if locked && gate?.blockedBy}
							<p class="module__lock">
								{$t(`tracks.lock.${gate.reason ?? 'sequential'}`, {
									blocker: moduleBySlug.get(gate.blockedBy)?.title ?? gate.blockedBy
								})}
							</p>
						{:else if authReady && enrollment && !done && !locked}
							<PixelButton
								variant="outline"
								size="sm"
								onclick={() => vm.markModuleComplete(module.slug, path.slug)}
							>
								{$t('tracks.markComplete')}
							</PixelButton>
						{/if}
					</div>
				</li>
			{/each}
		</ol>
	{:else}
		<header class="hero">
			<h1>{$t('tracks.hero.title')}</h1>
			<p>{$t('tracks.hero.subtitle')}</p>
		</header>

		{#if $loading}
			<p class="hint">{$t('tracks.loading')}</p>
		{:else if $error}
			<p class="err">{$error}</p>
		{:else if $paths.length === 0}
			<p class="hint empty">{$t('tracks.empty')}</p>
		{:else}
			<ul class="catalogue">
				{#each $paths as path (path.slug)}
					{@const enrollment = enrollmentByPath.get(path.slug)}
					<li>
						<button class="card" onclick={() => openPath(path.slug)}>
							<div class="card__top">
								<span class="card__icon" aria-hidden="true">{path.icon || '🧭'}</span>
								{#if authReady && enrollment}
									<Badge variant={enrollment.status === 'completed' ? 'success' : 'info'} size="sm">
										{$t(`tracks.status.${enrollment.status}`)}
									</Badge>
								{/if}
							</div>
							<h3 class="card__title">{path.title}</h3>
							<p class="card__desc">{path.description}</p>
							<p class="card__meta">
								<span>{$t('tracks.estimatedTime', { time: path.estimatedTime })}</span>
								<span>·</span>
								<span>{$t('tracks.moduleCount', { count: String(path.moduleSlugs.length) })}</span>
							</p>
							{#if authReady && enrollment}
								<div class="bar">
									<div class="bar__fill" style={`width:${pathProgressPercent(path)}%`}></div>
								</div>
							{/if}
						</button>
					</li>
				{/each}
			</ul>
		{/if}
	{/if}
</div>

<style>
	.tracks {
		padding: 1rem 1.25rem 2rem;
		max-width: 980px;
		margin: 0 auto;
	}
	.hero h1 {
		margin: 0 0 0.25rem;
		font-size: 1.4rem;
	}
	.hero p {
		margin: 0 0 1.25rem;
		opacity: 0.8;
	}
	.catalogue {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 1rem;
	}
	.card {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		width: 100%;
		height: 100%;
		text-align: left;
		padding: 0.9rem;
		border: 2px solid var(--pixel-border, #2b2b3a);
		background: var(--pixel-surface, #15151f);
		color: inherit;
		cursor: pointer;
	}
	.card:hover {
		border-color: var(--pixel-accent, #6cf);
	}
	.card__top {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.card__icon,
	.detail__icon {
		font-size: 1.6rem;
	}
	.card__title {
		margin: 0;
		font-size: 1.05rem;
	}
	.card__desc {
		margin: 0;
		font-size: 0.85rem;
		opacity: 0.8;
		display: -webkit-box;
		-webkit-line-clamp: 3;
		line-clamp: 3;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
	.card__meta,
	.detail__meta {
		display: flex;
		gap: 0.4rem;
		font-size: 0.78rem;
		opacity: 0.7;
		margin: 0.15rem 0 0;
	}
	.bar {
		height: 6px;
		background: var(--pixel-border, #2b2b3a);
		overflow: hidden;
		margin-top: 0.35rem;
	}
	.bar__fill {
		height: 100%;
		background: var(--pixel-accent, #6cf);
	}
	.bar__label {
		font-size: 0.78rem;
		opacity: 0.8;
	}
	.back,
	.link {
		background: none;
		border: none;
		color: var(--pixel-accent, #6cf);
		cursor: pointer;
		padding: 0;
		font: inherit;
	}
	.back {
		margin-bottom: 0.75rem;
	}
	.detail__head {
		display: flex;
		gap: 0.8rem;
		align-items: flex-start;
	}
	.detail__head h2 {
		margin: 0;
	}
	.detail__desc {
		margin: 0.25rem 0;
		opacity: 0.85;
	}
	.detail__status {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		margin: 0.75rem 0;
		flex-wrap: wrap;
	}
	.detail__status .bar {
		flex: 1;
		min-width: 120px;
		max-width: 280px;
	}
	.modules {
		list-style: none;
		margin: 1rem 0 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}
	.module {
		display: flex;
		gap: 0.75rem;
		padding: 0.8rem;
		border: 2px solid var(--pixel-border, #2b2b3a);
		background: var(--pixel-surface, #15151f);
	}
	.module--locked {
		opacity: 0.6;
	}
	.module--done {
		border-color: var(--pixel-success, #4caf50);
	}
	.module__index {
		flex: 0 0 1.8rem;
		height: 1.8rem;
		display: grid;
		place-items: center;
		border: 2px solid var(--pixel-border, #2b2b3a);
		font-weight: bold;
	}
	.module__body {
		flex: 1;
		min-width: 0;
	}
	.module__top {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		flex-wrap: wrap;
	}
	.module__top h3 {
		margin: 0;
		font-size: 1rem;
	}
	.module__dur {
		font-size: 0.78rem;
		opacity: 0.7;
	}
	.module__desc {
		margin: 0.3rem 0;
		font-size: 0.85rem;
		opacity: 0.8;
	}
	.module__lock {
		margin: 0.3rem 0 0;
		font-size: 0.8rem;
		color: var(--pixel-warning, #e6b800);
	}
	.courses {
		list-style: none;
		margin: 0.3rem 0;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem;
	}
	.course-pill {
		font-size: 0.75rem;
		padding: 0.1rem 0.45rem;
		border: 1px solid var(--pixel-border, #2b2b3a);
		opacity: 0.85;
	}
	.hint {
		opacity: 0.75;
	}
	.empty {
		padding: 2rem 0;
		text-align: center;
	}
	.err {
		color: var(--pixel-danger, #ff5c5c);
	}
</style>
