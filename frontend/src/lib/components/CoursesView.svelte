<script lang="ts">
	import { onMount } from 'svelte';
	import { PixelScrollArea, PixelButton, PixelInput, Badge } from '@cyberdynecorp/svelte-ui-core';
	import { createCoursesViewModel } from '$lib/viewmodels/coursesViewModel';
	import {
		courseCertificatePdfUrl,
		courseCodeLanguage,
		fetchMyCoursesProgress,
		type CourseLevel,
		type CourseSummary,
		type DeadlineStatus,
		type LessonType,
		type MyCourseProgress
	} from '$lib/api/coursesApi';
	import { authVM } from '$lib/auth/authViewModel.svelte';
	import { t, locale } from '$lib/i18n';
	import QuizPlayer from './QuizPlayer.svelte';
	import LessonContent from './LessonContent.svelte';

	// The view-model owns all backend orchestration (catalogue, detail,
	// progress, mark-complete, certificate) over the new /api/v1/courses
	// endpoints.
	const vm = createCoursesViewModel();
	const {
		courses,
		selected,
		progress,
		certificate,
		dashboard,
		recommendations,
		verification,
		verifying,
		loading,
		error
	} = vm;

	// Public "verify a certificate" panel.
	let verifyId = $state('');

	const authReady = $derived(authVM.isRestored && authVM.isAuthenticated);

	// Lesson id whose quiz the learner is currently taking (inline player).
	let takingQuiz = $state<string | null>(null);
	// Lesson id whose content is expanded for viewing.
	let openLesson = $state<string | null>(null);
	let meLoaded = $state(false);

	// Per-course progress for the catalogue (slug -> progress), loaded once
	// auth is ready. Powers per-card progress bars + Continue buttons.
	let progressBySlug = $state<Record<string, MyCourseProgress>>({});
	async function loadProgress(): Promise<void> {
		try {
			const rows = await fetchMyCoursesProgress();
			progressBySlug = Object.fromEntries(rows.map((r) => [r.slug, r]));
		} catch {
			/* anonymous / offline — cards just show "Start" */
		}
	}

	onMount(() => {
		void vm.loadCatalogue();
	});

	// Load the learner's dashboard + recommendations once auth is ready.
	$effect(() => {
		if (authReady && !meLoaded) {
			meLoaded = true;
			void vm.loadMe();
			void loadProgress();
		}
	});

	function openCourse(slug: string): void {
		void vm.open(slug, { withProgress: authReady });
	}

	function markComplete(lessonId: string): void {
		if (!authReady) return; // signed-in only — the button is hidden, this is defence-in-depth
		const course = $selected;
		if (course) void vm.completeLesson(course.slug, lessonId);
	}

	function onQuizDone(): void {
		const slug = $selected?.slug;
		takingQuiz = null;
		// A passed quiz auto-completes its lesson server-side; refresh.
		if (slug && authReady) void vm.refreshProgress(slug);
	}

	function lessonCompleted(lessonId: string): boolean {
		return $progress?.lessons.find((l) => l.lessonId === lessonId)?.completed ?? false;
	}

	const lessonIcon: Record<LessonType, string> = {
		text: '📄',
		code: '💻',
		quiz: '❓',
		video: '🎬',
		pdf: '📕',
		presentation: '📊'
	};

	// The first not-yet-completed lesson — highlighted as "Next up" so the
	// learner always knows where to resume.
	const nextLessonId = $derived(
		$selected?.lessons.find((l) => !lessonCompleted(l.id))?.id ?? null
	);

	// Code lessons run on the engine that matches the course (Python vs MATLAB).
	const codeLanguage = $derived(
		$selected ? courseCodeLanguage(`${$selected.slug} ${$selected.title}`) : 'matlab'
	);

	const levelVariant: Record<CourseLevel, 'success' | 'info' | 'danger'> = {
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

	// Deadline badge text is resolved in markup via `$t('deadline.<status>')`
	// (the 'none' case is never rendered).

	// ── Catalogue search + level filter (client-side over the loaded list) ──
	let search = $state('');
	type LevelFilter = 'all' | CourseLevel;
	let levelFilter = $state<LevelFilter>('all');
	// `labelKey` resolves through `$t` in markup so chips re-label on locale change.
	const levelChips: { value: LevelFilter; labelKey: string }[] = [
		{ value: 'all', labelKey: 'courses.chip.all' },
		{ value: 'Beginner', labelKey: 'courses.chip.basic' },
		{ value: 'Intermediate', labelKey: 'courses.chip.intermediate' },
		{ value: 'Advanced', labelKey: 'courses.chip.advanced' }
	];

	// Sort options.
	type SortKey = 'default' | 'title' | 'level' | 'lessons';
	let sortBy = $state<SortKey>('default');
	const sortOptions: { value: SortKey; labelKey: string }[] = [
		{ value: 'default', labelKey: 'courses.sortOpt.default' },
		{ value: 'title', labelKey: 'courses.sortOpt.title' },
		{ value: 'level', labelKey: 'courses.sortOpt.level' },
		{ value: 'lessons', labelKey: 'courses.sortOpt.lessons' }
	];
	const levelRank: Record<CourseLevel, number> = { Beginner: 0, Intermediate: 1, Advanced: 2 };

	// Topic grouping — derived from the slug (no per-course category field yet).
	let groupByTopic = $state(true);
	const topicOrder = [
		'Foundations',
		'Languages',
		'Databases',
		'DevOps',
		'Blockchain',
		'Physics',
		'Mathematics',
		'Vector Calculus',
		'Statistics',
		'Robotics',
		'Algorithms',
		'Electronic Engineering',
		'Other'
	];
	// The Tier-3 engineering curriculum: every electronics/EE family (each with
	// basics/intermediate/advanced) collapses into one browsable category.
	const electronicEngineeringSlug =
		/^(electronics|analog-ic|power-electronics|pcb|semiconductor|embedded|signals|control|dsp|rf-comms|microwave|digital-comms|digital-logic|fpga|comparch|electromagnetics|vlsi|photonics|power-systems|battery|sensors|machines)-/;
	function courseTopic(slug: string): string {
		if (/^(c|cpp|swift|go|rust|javascript|typescript)-/.test(slug)) return 'Languages';
		if (slug === 'sql-basics' || slug === 'sql-intermediate' || slug === 'mongodb' || slug === 'postgresql')
			return 'Databases';
		if (/^(docker|kubernetes|terraform|ansible)-/.test(slug)) return 'DevOps';
		if (slug.startsWith('blockchain')) return 'Blockchain';
		if (slug.startsWith('physics')) return 'Physics';
		if (slug.startsWith('vectorcalc')) return 'Vector Calculus';
		if (slug.startsWith('statinf')) return 'Statistics';
		if (slug.startsWith('robotics')) return 'Robotics';
		if (slug.startsWith('algorithms')) return 'Algorithms';
		if (slug.startsWith('math')) return 'Mathematics';
		if (electronicEngineeringSlug.test(slug)) return 'Electronic Engineering';
		if (slug === 'matlab-basics' || slug === 'python-course') return 'Foundations';
		return 'Other';
	}

	const filteredCourses = $derived.by(() => {
		const q = search.trim().toLowerCase();
		const list = $courses.filter(
			(c) =>
				(levelFilter === 'all' || c.level === levelFilter) &&
				(q === '' ||
					c.title.toLowerCase().includes(q) ||
					c.description.toLowerCase().includes(q))
		);
		const sorted = [...list];
		if (sortBy === 'title') sorted.sort((a, b) => a.title.localeCompare(b.title));
		else if (sortBy === 'level')
			sorted.sort((a, b) => levelRank[a.level] - levelRank[b.level] || a.title.localeCompare(b.title));
		else if (sortBy === 'lessons') sorted.sort((a, b) => b.lessonCount - a.lessonCount);
		return sorted;
	});

	// Group the filtered+sorted list by topic, in a stable topic order.
	const groupedCourses = $derived.by(() => {
		const groups = new Map<string, typeof filteredCourses>();
		for (const c of filteredCourses) {
			const t = courseTopic(c.slug);
			(groups.get(t) ?? groups.set(t, []).get(t)!).push(c);
		}
		return topicOrder
			.filter((t) => groups.has(t))
			.map((t) => ({ topic: t, courses: groups.get(t)! }));
	});

	// ── Category left-menu (mirrors the Blog view's CATEGORIES sidebar) ──
	// Icon + accent colour per topic so each category gets a coloured edge.
	const topicMeta: Record<string, { icon: string; accent: string; accentDark: string }> = {
		Foundations: { icon: '🎯', accent: '#22c55e', accentDark: '#15803d' },
		Languages: { icon: '💻', accent: '#3b82f6', accentDark: '#1d4ed8' },
		Databases: { icon: '🗄️', accent: '#a855f7', accentDark: '#7e22ce' },
		DevOps: { icon: '⚙️', accent: '#f97316', accentDark: '#c2410c' },
		Blockchain: { icon: '⛓️', accent: '#eab308', accentDark: '#a16207' },
		Physics: { icon: '⚛️', accent: '#06b6d4', accentDark: '#0e7490' },
		Mathematics: { icon: '➗', accent: '#ec4899', accentDark: '#be185d' },
		'Vector Calculus': { icon: '📐', accent: '#8b5cf6', accentDark: '#6d28d9' },
		Statistics: { icon: '📊', accent: '#f59e0b', accentDark: '#b45309' },
		Robotics: { icon: '🤖', accent: '#ef4444', accentDark: '#b91c1c' },
		Algorithms: { icon: '🧮', accent: '#14b8a6', accentDark: '#0f766e' },
		'Electronic Engineering': { icon: '🔌', accent: '#6366f1', accentDark: '#4338ca' },
		Other: { icon: '📦', accent: '#6b7280', accentDark: '#374151' }
	};
	const fallbackTopicMeta = { icon: '📦', accent: '#6b7280', accentDark: '#374151' };

	// Selected category in the sidebar ('all' or a topic name).
	let selectedTopic = $state<string>('all');

	// Categories with live counts over the search/level-filtered set, so the
	// numbers always match what a click reveals.
	const topicCategories = $derived.by(() => {
		const counts = new Map<string, number>();
		for (const c of filteredCourses) {
			const t = courseTopic(c.slug);
			counts.set(t, (counts.get(t) ?? 0) + 1);
		}
		const all = {
			id: 'all',
			name: 'All Courses',
			icon: '📚',
			count: filteredCourses.length,
			style: '--accent: #3b82f6; --accent-dark: #1d4ed8;'
		};
		const rest = topicOrder
			.filter((t) => (counts.get(t) ?? 0) > 0)
			.map((t) => {
				const m = topicMeta[t] ?? fallbackTopicMeta;
				return {
					id: t,
					name: t,
					icon: m.icon,
					count: counts.get(t)!,
					style: `--accent: ${m.accent}; --accent-dark: ${m.accentDark};`
				};
			});
		return [all, ...rest];
	});

	// Courses after the sidebar's category filter (on top of search/level).
	const coursesInTopic = $derived(
		selectedTopic === 'all'
			? filteredCourses
			: filteredCourses.filter((c) => courseTopic(c.slug) === selectedTopic)
	);

	// ── Lesson focus mode ──
	// Opening a lesson (or starting a quiz) collapses the rest of the list so
	// the learner focuses on that lesson's content. `takingQuiz` wins over
	// `openLesson` if both somehow set; the View/Take-quiz handlers keep them
	// mutually exclusive anyway.
	const focusedLessonId = $derived(takingQuiz ?? openLesson);
	const focusedIndex = $derived(
		$selected ? $selected.lessons.findIndex((l) => l.id === focusedLessonId) : -1
	);

	function focusLesson(lesson: { id: string; lessonType: LessonType }): void {
		if (lesson.lessonType === 'quiz') {
			openLesson = null;
			takingQuiz = lesson.id;
		} else {
			takingQuiz = null;
			openLesson = lesson.id;
		}
	}
	function exitFocus(): void {
		openLesson = null;
		takingQuiz = null;
	}

	function backToCatalogue(): void {
		vm.close();
		exitFocus();
		if (authReady) void loadProgress(); // reflect any lessons just completed
	}
</script>

<PixelScrollArea maxHeight="100%" ariaLabel="Cyberdyne Academy courses">
<div class="courses-view">
	<header class="hero">
		<span class="hero__mark" aria-hidden="true">📚</span>
		<div>
			<h1>{$t('courses.hero.title')}</h1>
			<p>{$t('courses.hero.subtitle')}</p>
		</div>
	</header>

	{#if !authReady}
		<div class="auth-banner">
			<strong>{$t('courses.guest.title')}</strong>
			<span>{$t('courses.guest.body')}</span>
		</div>
	{/if}

	{#if $error}
		<p class="banner banner--error" role="alert">{$error}</p>
	{/if}

	{#if $selected}
		{@const course = $selected}
		<!-- Course detail / player -->
		<PixelButton variant="ghost" size="sm" onclick={backToCatalogue}>{$t('courses.allCourses')}</PixelButton>

		<article class="detail">
			<div class="detail__head">
				<h2>{course.title}</h2>
				<Badge variant={levelVariant[course.level]} size="sm">{$t(`level.${course.level}`)}</Badge>
				{#if course.deadlineStatus !== 'none'}
					<Badge variant={deadlineVariant[course.deadlineStatus]} size="sm">
						{$t(`deadline.${course.deadlineStatus}`)}{#if course.daysRemaining !== null}&nbsp;({course.daysRemaining}d){/if}
					</Badge>
				{/if}
			</div>
			<p class="detail__desc">{course.description}</p>

			{#if authReady && $progress}
				<div class="progress" aria-label="course progress">
					<div class="progress__bar"><span style="width:{$progress.percent}%"></span></div>
					<span class="progress__label">
						{$t('courses.progressLabel', {
							completed: $progress.completedLessons,
							total: $progress.totalLessons,
							percent: $progress.percent
						})}
						{#if $progress.completed} · {$t('courses.complete')}{/if}
					</span>
				</div>
			{:else if !authReady}
				<p class="hint">{$t('courses.signInToTrack')}</p>
			{/if}

			{#if authReady}
				{#if $certificate}
					<div class="cert" aria-label="certificate earned">
						<span class="cert__mark">🎓</span>
						<span>{$t('courses.certEarned')}</span>
						<a
							class="cert__link"
							href={courseCertificatePdfUrl($certificate.id)}
							target="_blank"
							rel="noopener"
						>
							{$t('courses.downloadPdf')}
						</a>
					</div>
				{:else if $progress?.completed}
					<div class="cert__claim">
						<PixelButton variant="solid" size="sm" onclick={() => vm.claimCertificate(course.slug)}>
							{$t('courses.claimCert')}
						</PixelButton>
					</div>
				{/if}
			{/if}

			{#if focusedLessonId !== null}
				<div class="lessons__focusbar">
					<PixelButton variant="ghost" size="sm" onclick={exitFocus}>{$t('courses.backToLessons')}</PixelButton>
					{#if focusedIndex >= 0}
						<span class="lessons__pos">{$t('courses.lessonPosition', { index: focusedIndex + 1, total: course.lessons.length })}</span>
					{/if}
				</div>
			{/if}
			<ol class="lessons" class:lessons--focus={focusedLessonId !== null}>
				{#each course.lessons as lesson, i (lesson.id)}
					{#if focusedLessonId === null || focusedLessonId === lesson.id}
						{@const done = lessonCompleted(lesson.id)}
						{@const isNext = authReady && lesson.id === nextLessonId}
						{@const locked = !authReady && i > 0}
						{@const nextLesson = course.lessons[i + 1]}
						<li class="lesson-wrap">
							<div
								class="lesson"
								class:lesson--done={done}
								class:lesson--next={isNext}
								class:lesson--locked={locked}
							>
								<span class="lesson__num" class:lesson__num--done={done}>
									{#if done}✓{:else if locked}🔒{:else}{i + 1}{/if}
								</span>
								<span class="lesson__icon" aria-hidden="true">{lessonIcon[lesson.lessonType]}</span>
								<span class="lesson__main">
									<span class="lesson__title">{lesson.title}</span>
									<span class="lesson__meta">
										<span class="lesson__type">{$t(`lessonType.${lesson.lessonType}`)}</span>
										{#if lesson.duration}<span class="lesson__dur">· {lesson.duration}</span>{/if}
										{#if isNext}<span class="lesson__next">· {$t('courses.nextUp')}</span>{/if}
									</span>
								</span>
								<span class="lesson__actions">
									{#if locked}
										<span class="lesson__lock" title={$t('courses.signInToView')}>
											{$t('courses.signInToContinue')}
										</span>
									{:else if lesson.lessonType !== 'quiz'}
										<PixelButton
											variant="outline"
											size="sm"
											onclick={() => (openLesson === lesson.id ? exitFocus() : focusLesson(lesson))}
										>
											{openLesson === lesson.id ? $t('courses.hide') : $t('courses.view')}
										</PixelButton>
									{/if}
									{#if authReady}
										{#if lesson.lessonType === 'quiz'}
											<PixelButton
												variant="outline"
												size="sm"
												onclick={() => (takingQuiz === lesson.id ? exitFocus() : focusLesson(lesson))}
											>
												{takingQuiz === lesson.id ? $t('courses.hideQuiz') : $t('courses.takeQuiz')}
											</PixelButton>
										{/if}
										{#if done}
											<span class="lesson__done">{$t('courses.done')}</span>
										{:else if lesson.lessonType !== 'quiz'}
											<PixelButton variant="ghost" size="sm" onclick={() => markComplete(lesson.id)}>
												{$t('courses.markComplete')}
											</PixelButton>
										{/if}
									{/if}
								</span>
							</div>
							{#if openLesson === lesson.id && !locked}
								<LessonContent {lesson} language={codeLanguage} />
							{/if}
							{#if takingQuiz === lesson.id}
								<QuizPlayer lessonId={lesson.id} onDone={onQuizDone} />
							{/if}
							{#if focusedLessonId === lesson.id && authReady && nextLesson}
								<div class="lesson__nav">
									<PixelButton variant="solid" size="sm" onclick={() => focusLesson(nextLesson)}>
										{$t('courses.nextLesson', { title: nextLesson.title })}
									</PixelButton>
								</div>
							{/if}
						</li>
					{/if}
				{/each}
			</ol>
		</article>
	{:else}
		<!-- Catalogue -->
		{#if authReady && $dashboard}
			{@const d = $dashboard}
			<div class="dash" aria-label="my learning summary">
				<div class="dash__stat"><strong>{d.completedCourses}</strong> {$t('courses.dash.coursesDone')}</div>
				<div class="dash__stat"><strong>{d.inProgressCourses}</strong> {$t('courses.dash.inProgress')}</div>
				<div class="dash__stat"><strong>{d.quizzesPassed}/{d.quizzesAttempted}</strong> {$t('courses.dash.quizzesPassed')}</div>
				<div class="dash__stat"><strong>{d.certificates}</strong> {$t('courses.dash.certificates')}</div>
			</div>
		{/if}

		{#if authReady && $recommendations && $recommendations.courses.length > 0}
			<section class="recs">
				<h2>{$t('courses.recs.title')}</h2>
				<p class="recs__summary">{$recommendations.summary}</p>
				<div class="recs__row">
					{#each $recommendations.courses as rec (rec.slug)}
						<button class="rec" onclick={() => openCourse(rec.slug)}>
							<Badge variant={levelVariant[rec.level]} size="sm">{$t(`level.${rec.level}`)}</Badge>
							<span class="rec__title">{rec.title}</span>
							<span class="rec__reason">{rec.reason}</span>
						</button>
					{/each}
				</div>
			</section>
		{/if}

		{#if $loading && $courses.length === 0}
			<p class="hint">{$t('courses.loading')}</p>
		{:else if $courses.length === 0}
			<p class="hint">{$t('courses.noneYet')}</p>
		{:else}
			<div class="catalogue-layout">
			<!-- Category left menu (mirrors the Blog view's CATEGORIES sidebar) -->
			<aside class="cat-sidebar">
				<section class="cat-card">
					<h2 class="cat-card__title">{$t('courses.categories')}</h2>
					<div class="cat-list">
						{#each topicCategories as cat (cat.id)}
							<button
								type="button"
								class="cat-btn"
								class:cat-btn--active={selectedTopic === cat.id}
								style={cat.style}
								onclick={() => (selectedTopic = cat.id)}
							>
								<span class="cat-btn__icon" aria-hidden="true">{cat.icon}</span>
								<span class="cat-btn__name">{cat.id === 'all' ? $t('courses.allCoursesCat') : $t(`topic.${cat.id}`)}</span>
								<Badge variant="neutral" size="sm">{cat.count}</Badge>
							</button>
						{/each}
					</div>
				</section>
			</aside>

			<div class="catalogue-main">
			<!-- Browse toolbar: search + level filter + sort + grouping -->
			<section class="browse">
				<div class="browse__head">
					<h2>{$t('courses.browseTitle')}</h2>
					<span class="browse__count">{$t('courses.browseCount', { shown: coursesInTopic.length, total: $courses.length })}</span>
				</div>
				<div class="toolbar">
					<div class="toolbar__search">
						<span class="toolbar__icon" aria-hidden="true">🔍</span>
						<input
							class="toolbar__input"
							type="search"
							placeholder={$t('courses.searchPlaceholder')}
							bind:value={search}
							aria-label={$t('courses.searchAria')}
						/>
					</div>
					<div class="chips" role="group" aria-label={$t('courses.filterByLevel')}>
						{#each levelChips as chip}
							<button
								type="button"
								class="chip"
								class:chip--active={levelFilter === chip.value}
								onclick={() => (levelFilter = chip.value)}
							>
								{$t(chip.labelKey)}
							</button>
						{/each}
					</div>
					<div class="toolbar__opts">
						<label class="sortsel">
							<span class="sortsel__lbl">{$t('courses.sort')}</span>
							<select bind:value={sortBy} aria-label={$t('courses.sortAria')}>
								{#each sortOptions as o}<option value={o.value}>{$t(o.labelKey)}</option>{/each}
							</select>
						</label>
						{#if selectedTopic === 'all'}
							<label class="toggle">
								<input type="checkbox" bind:checked={groupByTopic} /> {$t('courses.groupByTopic')}
							</label>
						{/if}
					</div>
				</div>
			</section>

			{#snippet courseCard(course: CourseSummary)}
				{@const prog = progressBySlug[course.slug]}
				<li>
					<button
						class="card card--{course.level.toLowerCase()}"
						class:card--done={prog?.completed}
						onclick={() => openCourse(course.slug)}
					>
						<div class="card__top">
							<Badge variant={levelVariant[course.level]} size="sm">{$t(`level.${course.level}`)}</Badge>
							{#if course.mandatory}<Badge variant="neutral" size="sm">{$t('courses.required')}</Badge>{/if}
							{#if course.deadlineStatus !== 'none'}
								<Badge variant={deadlineVariant[course.deadlineStatus]} size="sm">
									{$t(`deadline.${course.deadlineStatus}`)}
								</Badge>
							{/if}
							{#if prog?.completed}<span class="card__check">{$t('courses.completed')}</span>{/if}
						</div>
						<h3>{course.title}</h3>
						<p>{course.description}</p>
						{#if prog && !prog.completed}
							<div class="cardprog" aria-label="course progress">
								<div class="cardprog__bar"><span style="width:{prog.percent}%"></span></div>
								<span class="cardprog__label">{$t('courses.cardProgress', { completed: prog.completedLessons, total: prog.totalLessons, percent: prog.percent })}</span>
							</div>
						{/if}
						<span class="card__foot">
							<span class="card__meta">{$t('courses.lessonsCount', { count: course.lessonCount })}</span>
							<span class="card__cta" class:card__cta--show={!!prog}>
								{prog?.completed ? $t('courses.cta.review') : prog ? $t('courses.cta.continue') : $t('courses.cta.start')}
							</span>
						</span>
					</button>
				</li>
			{/snippet}

			{#if coursesInTopic.length === 0}
				<p class="hint empty">
					{$t('courses.noMatch', {
						query: search,
						level: levelFilter !== 'all' ? $t('courses.noMatch.atLevel', { level: $t(`level.${levelFilter}`) }) : '',
						topic: selectedTopic !== 'all' ? $t('courses.noMatch.inTopic', { topic: $t(`topic.${selectedTopic}`) }) : ''
					})}
					<button class="link" onclick={() => { search = ''; levelFilter = 'all'; selectedTopic = 'all'; }}>{$t('courses.clearFilters')}</button>
				</p>
			{:else if selectedTopic === 'all' && groupByTopic}
				{#each groupedCourses as group (group.topic)}
					<section class="topic">
						<h3 class="topic__head">
							{$t(`topic.${group.topic}`)} <span class="topic__count">{group.courses.length}</span>
						</h3>
						<ul class="catalogue">
							{#each group.courses as course (course.id)}{@render courseCard(course)}{/each}
						</ul>
					</section>
				{/each}
			{:else}
				<ul class="catalogue">
					{#each coursesInTopic as course (course.id)}{@render courseCard(course)}{/each}
				</ul>
			{/if}
			</div>
			</div>
		{/if}

		<!-- Public certificate verification -->
		<section class="verify">
			<h2>{$t('courses.verify.title')}</h2>
			<p class="verify__hint">{$t('courses.verify.hint')}</p>
			<div class="verify__row">
				<div class="grow">
					<PixelInput placeholder={$t('courses.verify.placeholder')} bind:value={verifyId} ariaLabel={$t('courses.verify.placeholder')} />
				</div>
				<PixelButton
					variant="solid"
					size="sm"
					disabled={$verifying || !verifyId.trim()}
					onclick={() => vm.verify(verifyId.trim())}
				>
					{$verifying ? $t('courses.verify.checking') : $t('courses.verify.verify')}
				</PixelButton>
			</div>
			{#if $verification}
				{#if $verification.valid && $verification.certificate}
					<p class="verify__result">
						<Badge variant="success" size="sm">{$t('courses.verify.valid')}</Badge>
						<strong>{$verification.certificate.courseSlug}</strong>, {$t('courses.verify.issued', { date: new Date($verification.certificate.issuedAt).toLocaleDateString($locale) })}.
					</p>
				{:else}
					<p class="verify__result">
						<Badge variant="danger" size="sm">{$t('courses.verify.notValid')}</Badge>
						{$t('courses.verify.noMatch')}
					</p>
				{/if}
			{/if}
		</section>
	{/if}
</div>
</PixelScrollArea>

<style>
	.courses-view {
		padding: 1.25rem;
		color: #000000;
		font-family: system-ui, sans-serif;
	}
	.hero {
		display: flex;
		gap: 0.75rem;
		align-items: center;
		margin-bottom: 1rem;
	}
	.hero__mark {
		font-size: 2rem;
	}
	.hero h1 {
		margin: 0;
		font-size: 1.25rem;
	}
	.hero p {
		margin: 0.15rem 0 0;
		font-size: 0.85rem;
		color: #374151;
	}
	.banner--error {
		background: #fee2e2;
		color: #991b1b;
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		font-size: 0.85rem;
	}
	.auth-banner {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		background: #fef3c7;
		color: #92400e;
		padding: 0.6rem 0.85rem;
		border-radius: 6px;
		font-size: 0.85rem;
	}
	.dash {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem 1.25rem;
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 8px;
		padding: 0.6rem 0.85rem;
		margin-bottom: 0.85rem;
		font-size: 0.82rem;
		color: #374151;
	}
	.dash__stat strong {
		color: #000000;
		font-size: 1rem;
		margin-right: 0.25rem;
	}
	.recs {
		margin-bottom: 1.1rem;
	}
	.recs h2 {
		margin: 0 0 0.2rem;
		font-size: 1rem;
	}
	.recs__summary {
		margin: 0 0 0.5rem;
		font-size: 0.82rem;
		color: #374151;
	}
	.recs__row {
		display: flex;
		gap: 0.6rem;
		flex-wrap: wrap;
	}
	.rec {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		align-items: flex-start;
		text-align: left;
		background: #f3f4f6;
		border: 2px solid #000000;
		border-radius: 8px;
		padding: 0.6rem 0.7rem;
		cursor: pointer;
		color: inherit;
		min-width: 180px;
		max-width: 240px;
	}
	.rec:hover {
		border-color: #3b82f6;
	}
	.rec__title {
		font-size: 0.9rem;
		font-weight: 600;
	}
	.rec__reason {
		font-size: 0.75rem;
		color: #374151;
	}
	/* ── Browse toolbar (search + level chips) ── */
	.browse {
		margin: 0.5rem 0 0.9rem;
	}
	.browse__head {
		display: flex;
		align-items: baseline;
		gap: 0.6rem;
		margin-bottom: 0.5rem;
	}
	.browse__head h2 {
		margin: 0;
		font-size: 1.05rem;
	}
	.browse__count {
		font-size: 0.78rem;
		color: #6b7280;
	}
	.toolbar {
		display: flex;
		gap: 0.6rem;
		flex-wrap: wrap;
		align-items: center;
	}
	.toolbar__search {
		flex: 1 1 240px;
		display: flex;
		align-items: center;
		gap: 0.4rem;
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 8px;
		padding: 0.35rem 0.6rem;
	}
	.toolbar__search:focus-within {
		border-color: #3b82f6;
	}
	.toolbar__icon {
		font-size: 0.85rem;
		opacity: 0.7;
	}
	.toolbar__input {
		flex: 1;
		border: 0;
		outline: none;
		font: inherit;
		font-size: 0.9rem;
		background: transparent;
		color: #111827;
	}
	.chips {
		display: flex;
		gap: 0.35rem;
		flex-wrap: wrap;
	}
	.chip {
		font: inherit;
		font-size: 0.8rem;
		padding: 0.35rem 0.8rem;
		border: 2px solid #000000;
		border-radius: 999px;
		background: #ffffff;
		color: #374151;
		cursor: pointer;
		transition:
			background 0.12s ease,
			color 0.12s ease;
	}
	.chip:hover {
		border-color: #3b82f6;
	}
	.chip--active {
		background: #111827;
		color: #ffffff;
		border-color: #111827;
	}
	.toolbar__opts {
		display: flex;
		gap: 0.6rem;
		align-items: center;
		flex-wrap: wrap;
	}
	.sortsel {
		display: flex;
		align-items: center;
		gap: 0.35rem;
		font-size: 0.8rem;
		color: #374151;
	}
	.sortsel select {
		font: inherit;
		font-size: 0.8rem;
		padding: 0.3rem 0.5rem;
		border: 2px solid #000000;
		border-radius: 6px;
		background: #ffffff;
		cursor: pointer;
	}
	.toggle {
		display: flex;
		align-items: center;
		gap: 0.35rem;
		font-size: 0.8rem;
		color: #374151;
		cursor: pointer;
	}

	/* ── Topic sections ── */
	.topic {
		margin-top: 1.1rem;
	}
	.topic__head {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin: 0 0 0.55rem;
		font-size: 0.95rem;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: #111827;
		border-bottom: 2px solid #e5e7eb;
		padding-bottom: 0.3rem;
	}
	.topic__count {
		font-size: 0.72rem;
		font-weight: 700;
		color: #ffffff;
		background: #111827;
		border-radius: 999px;
		padding: 0.05rem 0.5rem;
	}

	.empty {
		padding: 1rem 0;
	}
	.link {
		background: none;
		border: 0;
		color: #2563eb;
		cursor: pointer;
		font: inherit;
		text-decoration: underline;
		padding: 0;
	}

	.catalogue {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
		gap: 0.9rem;
	}
	.card {
		width: 100%;
		height: 100%;
		text-align: left;
		background: #ffffff;
		border: 2px solid #000000;
		border-left-width: 6px;
		border-radius: 8px;
		padding: 0.9rem 0.95rem;
		cursor: pointer;
		color: inherit;
		display: flex;
		flex-direction: column;
		transition:
			transform 0.12s ease,
			box-shadow 0.12s ease,
			border-color 0.12s ease;
	}
	.card--beginner {
		border-left-color: #22c55e;
	}
	.card--intermediate {
		border-left-color: #3b82f6;
	}
	.card--advanced {
		border-left-color: #ef4444;
	}
	.card:hover {
		border-color: #3b82f6;
		transform: translateY(-2px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.18);
	}
	.card__top {
		display: flex;
		gap: 0.4rem;
		flex-wrap: wrap;
		margin-bottom: 0.4rem;
	}
	.card h3 {
		margin: 0 0 0.25rem;
		font-size: 1.02rem;
	}
	.card p {
		margin: 0 0 0.6rem;
		font-size: 0.82rem;
		color: #374151;
		display: -webkit-box;
		-webkit-line-clamp: 3;
		line-clamp: 3;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
	.card__foot {
		margin-top: auto;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
	}
	.card__meta {
		font-size: 0.75rem;
		color: #6b7280;
	}
	.card__cta {
		font-size: 0.78rem;
		font-weight: 700;
		color: #2563eb;
		opacity: 0;
		transition: opacity 0.12s ease;
	}
	.card:hover .card__cta,
	.card__cta--show {
		opacity: 1;
	}
	.card--done {
		border-left-color: #16a34a;
		background: #f6fef9;
	}
	.card__check {
		margin-left: auto;
		font-size: 0.7rem;
		font-weight: 700;
		color: #166534;
	}
	/* Per-card progress bar */
	.cardprog {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin: 0 0 0.55rem;
	}
	.cardprog__bar {
		flex: 1;
		height: 6px;
		background: #e5e7eb;
		border-radius: 999px;
		overflow: hidden;
	}
	.cardprog__bar span {
		display: block;
		height: 100%;
		background: #22c55e;
	}
	.cardprog__label {
		font-size: 0.68rem;
		color: #6b7280;
		white-space: nowrap;
	}
	.detail__head {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		flex-wrap: wrap;
	}
	.detail__head h2 {
		margin: 0;
		font-size: 1.15rem;
	}
	.detail__desc {
		color: #374151;
		font-size: 0.88rem;
	}
	.progress {
		margin: 0.75rem 0;
	}
	.progress__bar {
		height: 8px;
		background: #d4d4d8;
		border-radius: 999px;
		overflow: hidden;
	}
	.progress__bar span {
		display: block;
		height: 100%;
		background: #22c55e;
	}
	.progress__label {
		font-size: 0.78rem;
		color: #374151;
	}
	.cert {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		background: #dcfce7;
		color: #166534;
		border-radius: 6px;
		padding: 0.5rem 0.7rem;
		margin: 0.5rem 0;
		font-size: 0.85rem;
	}
	.cert__mark {
		font-size: 1.1rem;
	}
	.cert__link {
		margin-left: auto;
		color: #166534;
		font-weight: 600;
	}
	.cert__claim {
		margin: 0.5rem 0;
	}
	.hint {
		color: #374151;
		font-size: 0.85rem;
	}
	.lessons {
		list-style: none;
		margin: 0.75rem 0 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}
	.lesson-wrap {
		display: flex;
		flex-direction: column;
	}
	.lesson {
		display: flex;
		gap: 0.7rem;
		align-items: center;
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 6px;
		padding: 0.55rem 0.7rem;
		transition: border-color 0.12s ease;
	}
	.lesson--done {
		border-color: #bbf7d0;
		background: #f6fef9;
	}
	.lesson--next {
		border-color: #3b82f6;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
	}
	.lesson__num {
		flex: none;
		width: 26px;
		height: 26px;
		display: grid;
		place-items: center;
		border: 2px solid #000;
		border-radius: 999px;
		font-size: 0.78rem;
		font-weight: 700;
		background: #fff;
	}
	.lesson__num--done {
		background: #22c55e;
		border-color: #166534;
		color: #fff;
	}
	.lesson__icon {
		font-size: 1.05rem;
		flex: none;
	}
	.lesson__main {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 0.1rem;
		min-width: 0;
	}
	.lesson__title {
		font-size: 0.88rem;
		font-weight: 600;
	}
	.lesson__meta {
		display: flex;
		gap: 0.3rem;
		align-items: center;
		font-size: 0.7rem;
		color: #6b7280;
	}
	.lesson__type {
		text-transform: uppercase;
		letter-spacing: 0.03em;
	}
	.lesson__dur {
		color: #6b7280;
	}
	.lesson__next {
		color: #1d4ed8;
		font-weight: 700;
	}
	.lesson__actions {
		display: flex;
		gap: 0.4rem;
		align-items: center;
		flex: none;
	}
	.lesson__done {
		font-size: 0.75rem;
		font-weight: 600;
		color: #166534;
	}
	.lesson--locked {
		opacity: 0.6;
	}
	.lesson__lock {
		font-size: 0.75rem;
		font-weight: 600;
		color: #92400e;
		white-space: nowrap;
	}
	.verify {
		margin-top: 1.5rem;
		padding-top: 1rem;
		border-top: 2px solid #000000;
	}
	.verify h2 {
		margin: 0 0 0.2rem;
		font-size: 1rem;
	}
	.verify__hint {
		margin: 0 0 0.5rem;
		font-size: 0.8rem;
		color: #374151;
	}
	.verify__row {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		max-width: 520px;
	}
	.verify__row .grow {
		flex: 1;
	}
	.verify__result {
		display: flex;
		gap: 0.4rem;
		align-items: center;
		font-size: 0.82rem;
		color: #374151;
		margin: 0.6rem 0 0;
	}

	/* ── Catalogue layout: category sidebar + course list ── */
	.catalogue-layout {
		display: grid;
		grid-template-columns: minmax(210px, 270px) minmax(0, 1fr);
		gap: 1rem;
		align-items: start;
	}
	@media (max-width: 760px) {
		.catalogue-layout {
			grid-template-columns: 1fr;
		}
	}
	.catalogue-main {
		min-width: 0;
	}
	.cat-sidebar {
		position: sticky;
		top: 0;
	}
	.cat-card {
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 8px;
		padding: 0.85rem;
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}
	.cat-card__title {
		margin: 0;
		font-size: 0.8rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: #111827;
	}
	.cat-list {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}
	.cat-btn {
		position: relative;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		width: 100%;
		text-align: left;
		padding: 0.5rem 0.6rem 0.5rem 0.85rem;
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 6px;
		font: inherit;
		font-size: 0.82rem;
		font-weight: 600;
		color: #1f2937;
		cursor: pointer;
		transition:
			transform 0.1s ease,
			box-shadow 0.1s ease,
			background 0.1s ease;
	}
	.cat-btn::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 5px;
		background: var(--accent, #3b82f6);
		border-right: 2px solid #000000;
		border-radius: 4px 0 0 4px;
	}
	.cat-btn:hover {
		transform: translateY(-1px);
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.2);
	}
	.cat-btn--active {
		background: color-mix(in srgb, var(--accent, #3b82f6) 14%, #ffffff);
		color: var(--accent-dark, #1d4ed8);
		border-color: var(--accent-dark, #1d4ed8);
	}
	.cat-btn__icon {
		flex: 0 0 auto;
		font-size: 0.95rem;
		line-height: 1;
	}
	.cat-btn__name {
		flex: 1 1 auto;
		min-width: 0;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	/* ── Lesson focus mode ── */
	.lessons__focusbar {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		margin: 0.75rem 0 0;
	}
	.lessons__pos {
		font-size: 0.78rem;
		font-weight: 600;
		color: #6b7280;
	}
	.lesson__nav {
		display: flex;
		justify-content: flex-end;
		margin-top: 0.6rem;
	}
</style>
