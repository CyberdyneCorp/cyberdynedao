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

	const deadlineLabel: Record<DeadlineStatus, string> = {
		none: '',
		upcoming: 'Due soon',
		urgent: 'Due urgently',
		overdue: 'Overdue'
	};

	// ── Catalogue search + level filter (client-side over the loaded list) ──
	let search = $state('');
	type LevelFilter = 'all' | CourseLevel;
	let levelFilter = $state<LevelFilter>('all');
	const levelChips: { value: LevelFilter; label: string }[] = [
		{ value: 'all', label: 'All' },
		{ value: 'Beginner', label: 'Basic' },
		{ value: 'Intermediate', label: 'Intermediate' },
		{ value: 'Advanced', label: 'Advanced' }
	];

	// Sort options.
	type SortKey = 'default' | 'title' | 'level' | 'lessons';
	let sortBy = $state<SortKey>('default');
	const sortOptions: { value: SortKey; label: string }[] = [
		{ value: 'default', label: 'Recommended order' },
		{ value: 'title', label: 'Title (A–Z)' },
		{ value: 'level', label: 'Level (Basic → Advanced)' },
		{ value: 'lessons', label: 'Most lessons' }
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
		'Other'
	];
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

	function backToCatalogue(): void {
		vm.close();
		if (authReady) void loadProgress(); // reflect any lessons just completed
	}
</script>

<PixelScrollArea maxHeight="100%" ariaLabel="Cyberdyne Academy courses">
<div class="courses-view">
	<header class="hero">
		<span class="hero__mark" aria-hidden="true">📚</span>
		<div>
			<h1>Cyberdyne Academy — Courses</h1>
			<p>Structured courses with lessons, quizzes, and completion certificates.</p>
		</div>
	</header>

	{#if $error}
		<p class="banner banner--error" role="alert">{$error}</p>
	{/if}

	{#if $selected}
		{@const course = $selected}
		<!-- Course detail / player -->
		<PixelButton variant="ghost" size="sm" onclick={backToCatalogue}>← All courses</PixelButton>

		<article class="detail">
			<div class="detail__head">
				<h2>{course.title}</h2>
				<Badge variant={levelVariant[course.level]} size="sm">{course.level}</Badge>
				{#if course.deadlineStatus !== 'none'}
					<Badge variant={deadlineVariant[course.deadlineStatus]} size="sm">
						{deadlineLabel[course.deadlineStatus]}{#if course.daysRemaining !== null}&nbsp;({course.daysRemaining}d){/if}
					</Badge>
				{/if}
			</div>
			<p class="detail__desc">{course.description}</p>

			{#if authReady && $progress}
				<div class="progress" aria-label="course progress">
					<div class="progress__bar"><span style="width:{$progress.percent}%"></span></div>
					<span class="progress__label">
						{$progress.completedLessons}/{$progress.totalLessons} lessons · {$progress.percent}%
						{#if $progress.completed} · ✓ complete{/if}
					</span>
				</div>
			{:else if !authReady}
				<p class="hint">Sign in to track your progress and earn a certificate.</p>
			{/if}

			{#if authReady}
				{#if $certificate}
					<div class="cert" aria-label="certificate earned">
						<span class="cert__mark">🎓</span>
						<span>Certificate earned</span>
						<a
							class="cert__link"
							href={courseCertificatePdfUrl($certificate.id)}
							target="_blank"
							rel="noopener"
						>
							Download PDF
						</a>
					</div>
				{:else if $progress?.completed}
					<div class="cert__claim">
						<PixelButton variant="solid" size="sm" onclick={() => vm.claimCertificate(course.slug)}>
							🎓 Claim your certificate
						</PixelButton>
					</div>
				{/if}
			{/if}

			<ol class="lessons">
				{#each course.lessons as lesson, i (lesson.id)}
					{@const done = lessonCompleted(lesson.id)}
					{@const isNext = authReady && lesson.id === nextLessonId}
					<li class="lesson-wrap">
						<div class="lesson" class:lesson--done={done} class:lesson--next={isNext}>
							<span class="lesson__num" class:lesson__num--done={done}>
								{#if done}✓{:else}{i + 1}{/if}
							</span>
							<span class="lesson__icon" aria-hidden="true">{lessonIcon[lesson.lessonType]}</span>
							<span class="lesson__main">
								<span class="lesson__title">{lesson.title}</span>
								<span class="lesson__meta">
									<span class="lesson__type">{lesson.lessonType}</span>
									{#if lesson.duration}<span class="lesson__dur">· {lesson.duration}</span>{/if}
									{#if isNext}<span class="lesson__next">· Next up</span>{/if}
								</span>
							</span>
							<span class="lesson__actions">
								{#if lesson.lessonType !== 'quiz'}
									<PixelButton
										variant="outline"
										size="sm"
										onclick={() => (openLesson = openLesson === lesson.id ? null : lesson.id)}
									>
										{openLesson === lesson.id ? 'Hide' : 'View'}
									</PixelButton>
								{/if}
								{#if authReady}
									{#if lesson.lessonType === 'quiz'}
										<PixelButton
											variant="outline"
											size="sm"
											onclick={() => (takingQuiz = takingQuiz === lesson.id ? null : lesson.id)}
										>
											{takingQuiz === lesson.id ? 'Hide quiz' : 'Take quiz'}
										</PixelButton>
									{/if}
									{#if done}
										<span class="lesson__done">✓ done</span>
									{:else if lesson.lessonType !== 'quiz'}
										<PixelButton variant="ghost" size="sm" onclick={() => markComplete(lesson.id)}>
											Mark complete
										</PixelButton>
									{/if}
								{/if}
							</span>
						</div>
						{#if openLesson === lesson.id}
							<LessonContent {lesson} language={codeLanguage} />
						{/if}
						{#if takingQuiz === lesson.id}
							<QuizPlayer lessonId={lesson.id} onDone={onQuizDone} />
						{/if}
					</li>
				{/each}
			</ol>
		</article>
	{:else}
		<!-- Catalogue -->
		{#if authReady && $dashboard}
			{@const d = $dashboard}
			<div class="dash" aria-label="my learning summary">
				<div class="dash__stat"><strong>{d.completedCourses}</strong> courses done</div>
				<div class="dash__stat"><strong>{d.inProgressCourses}</strong> in progress</div>
				<div class="dash__stat"><strong>{d.quizzesPassed}/{d.quizzesAttempted}</strong> quizzes passed</div>
				<div class="dash__stat"><strong>{d.certificates}</strong> certificates</div>
			</div>
		{/if}

		{#if authReady && $recommendations && $recommendations.courses.length > 0}
			<section class="recs">
				<h2>Recommended for you</h2>
				<p class="recs__summary">{$recommendations.summary}</p>
				<div class="recs__row">
					{#each $recommendations.courses as rec (rec.slug)}
						<button class="rec" onclick={() => openCourse(rec.slug)}>
							<Badge variant={levelVariant[rec.level]} size="sm">{rec.level}</Badge>
							<span class="rec__title">{rec.title}</span>
							<span class="rec__reason">{rec.reason}</span>
						</button>
					{/each}
				</div>
			</section>
		{/if}

		{#if $loading && $courses.length === 0}
			<p class="hint">Loading courses…</p>
		{:else if $courses.length === 0}
			<p class="hint">No published courses yet — check back soon.</p>
		{:else}
			<!-- Browse toolbar: search + level filter + sort + grouping -->
			<section class="browse">
				<div class="browse__head">
					<h2>Browse all courses</h2>
					<span class="browse__count">{filteredCourses.length} of {$courses.length}</span>
				</div>
				<div class="toolbar">
					<div class="toolbar__search">
						<span class="toolbar__icon" aria-hidden="true">🔍</span>
						<input
							class="toolbar__input"
							type="search"
							placeholder="Search courses…"
							bind:value={search}
							aria-label="Search courses"
						/>
					</div>
					<div class="chips" role="group" aria-label="Filter by level">
						{#each levelChips as chip}
							<button
								type="button"
								class="chip"
								class:chip--active={levelFilter === chip.value}
								onclick={() => (levelFilter = chip.value)}
							>
								{chip.label}
							</button>
						{/each}
					</div>
					<div class="toolbar__opts">
						<label class="sortsel">
							<span class="sortsel__lbl">Sort</span>
							<select bind:value={sortBy} aria-label="Sort courses">
								{#each sortOptions as o}<option value={o.value}>{o.label}</option>{/each}
							</select>
						</label>
						<label class="toggle">
							<input type="checkbox" bind:checked={groupByTopic} /> Group by topic
						</label>
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
							<Badge variant={levelVariant[course.level]} size="sm">{course.level}</Badge>
							{#if course.mandatory}<Badge variant="neutral" size="sm">Required</Badge>{/if}
							{#if course.deadlineStatus !== 'none'}
								<Badge variant={deadlineVariant[course.deadlineStatus]} size="sm">
									{deadlineLabel[course.deadlineStatus]}
								</Badge>
							{/if}
							{#if prog?.completed}<span class="card__check">✓ Completed</span>{/if}
						</div>
						<h3>{course.title}</h3>
						<p>{course.description}</p>
						{#if prog && !prog.completed}
							<div class="cardprog" aria-label="course progress">
								<div class="cardprog__bar"><span style="width:{prog.percent}%"></span></div>
								<span class="cardprog__label">{prog.completedLessons}/{prog.totalLessons} · {prog.percent}%</span>
							</div>
						{/if}
						<span class="card__foot">
							<span class="card__meta">📘 {course.lessonCount} lessons</span>
							<span class="card__cta" class:card__cta--show={!!prog}>
								{prog?.completed ? 'Review →' : prog ? 'Continue →' : 'Start →'}
							</span>
						</span>
					</button>
				</li>
			{/snippet}

			{#if filteredCourses.length === 0}
				<p class="hint empty">
					No courses match “{search}”{levelFilter !== 'all' ? ` at ${levelFilter} level` : ''}.
					<button class="link" onclick={() => { search = ''; levelFilter = 'all'; }}>Clear filters</button>
				</p>
			{:else if groupByTopic}
				{#each groupedCourses as group (group.topic)}
					<section class="topic">
						<h3 class="topic__head">
							{group.topic} <span class="topic__count">{group.courses.length}</span>
						</h3>
						<ul class="catalogue">
							{#each group.courses as course (course.id)}{@render courseCard(course)}{/each}
						</ul>
					</section>
				{/each}
			{:else}
				<ul class="catalogue">
					{#each filteredCourses as course (course.id)}{@render courseCard(course)}{/each}
				</ul>
			{/if}
		{/if}

		<!-- Public certificate verification -->
		<section class="verify">
			<h2>Verify a certificate</h2>
			<p class="verify__hint">Paste a certificate ID to check it was genuinely issued.</p>
			<div class="verify__row">
				<div class="grow">
					<PixelInput placeholder="Certificate ID" bind:value={verifyId} ariaLabel="Certificate ID" />
				</div>
				<PixelButton
					variant="solid"
					size="sm"
					disabled={$verifying || !verifyId.trim()}
					onclick={() => vm.verify(verifyId.trim())}
				>
					{$verifying ? 'Checking…' : 'Verify'}
				</PixelButton>
			</div>
			{#if $verification}
				{#if $verification.valid && $verification.certificate}
					<p class="verify__result">
						<Badge variant="success" size="sm">Valid</Badge>
						Course <strong>{$verification.certificate.courseSlug}</strong>, issued
						{new Date($verification.certificate.issuedAt).toLocaleDateString()}.
					</p>
				{:else}
					<p class="verify__result">
						<Badge variant="danger" size="sm">Not valid</Badge>
						No certificate matches that ID.
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
</style>
