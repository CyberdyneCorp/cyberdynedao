<script lang="ts">
	import { onMount } from 'svelte';
	import { createCoursesViewModel } from '$lib/viewmodels/coursesViewModel';
	import {
		courseCertificatePdfUrl,
		type CourseLevel,
		type DeadlineStatus
	} from '$lib/api/coursesApi';
	import { authVM } from '$lib/auth/authViewModel.svelte';
	import QuizPlayer from './QuizPlayer.svelte';
	import LessonContent from './LessonContent.svelte';

	// The view-model owns all backend orchestration (catalogue, detail,
	// progress, mark-complete, certificate) over the new /api/v1/courses
	// endpoints.
	const vm = createCoursesViewModel();
	const { courses, selected, progress, certificate, loading, error } = vm;

	const authReady = $derived(authVM.isRestored && authVM.isAuthenticated);

	// Lesson id whose quiz the learner is currently taking (inline player).
	let takingQuiz = $state<string | null>(null);
	// Lesson id whose content is expanded for viewing.
	let openLesson = $state<string | null>(null);

	onMount(() => {
		void vm.loadCatalogue();
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

	const levelClass: Record<CourseLevel, string> = {
		Beginner: 'lvl lvl--beg',
		Intermediate: 'lvl lvl--int',
		Advanced: 'lvl lvl--adv'
	};

	const deadlineLabel: Record<DeadlineStatus, string> = {
		none: '',
		upcoming: 'Due soon',
		urgent: 'Due urgently',
		overdue: 'Overdue'
	};
</script>

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
		<button class="back" onclick={() => vm.close()}>← All courses</button>

		<article class="detail">
			<div class="detail__head">
				<h2>{course.title}</h2>
				<span class={levelClass[course.level]}>{course.level}</span>
				{#if course.deadlineStatus !== 'none'}
					<span class="deadline deadline--{course.deadlineStatus}">
						{deadlineLabel[course.deadlineStatus]}
						{#if course.daysRemaining !== null}({course.daysRemaining}d){/if}
					</span>
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
					<button class="cert__claim" onclick={() => vm.claimCertificate(course.slug)}>
						🎓 Claim your certificate
					</button>
				{/if}
			{/if}

			<ol class="lessons">
				{#each course.lessons as lesson (lesson.id)}
					<li class="lesson-wrap">
						<div class="lesson" class:lesson--done={lessonCompleted(lesson.id)}>
							<span class="lesson__type">{lesson.lessonType}</span>
							<span class="lesson__title">{lesson.title}</span>
							{#if lesson.duration}<span class="lesson__dur">{lesson.duration}</span>{/if}
							{#if lesson.lessonType !== 'quiz'}
								<button
									class="lesson__btn"
									onclick={() => (openLesson = openLesson === lesson.id ? null : lesson.id)}
								>
									{openLesson === lesson.id ? 'Hide' : 'View'}
								</button>
							{/if}
							{#if authReady}
								{#if lesson.lessonType === 'quiz'}
									<button
										class="lesson__btn"
										onclick={() => (takingQuiz = takingQuiz === lesson.id ? null : lesson.id)}
									>
										{takingQuiz === lesson.id ? 'Hide quiz' : 'Take quiz'}
									</button>
								{/if}
								{#if lessonCompleted(lesson.id)}
									<span class="lesson__done">✓ done</span>
								{:else if lesson.lessonType !== 'quiz'}
									<button class="lesson__btn" onclick={() => markComplete(lesson.id)}>
										Mark complete
									</button>
								{/if}
							{/if}
						</div>
						{#if openLesson === lesson.id}
							<LessonContent {lesson} />
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
		{#if $loading && $courses.length === 0}
			<p class="hint">Loading courses…</p>
		{:else if $courses.length === 0}
			<p class="hint">No published courses yet — check back soon.</p>
		{:else}
			<ul class="catalogue">
				{#each $courses as course (course.id)}
					<li>
						<button class="card" onclick={() => openCourse(course.slug)}>
							<div class="card__top">
								<span class={levelClass[course.level]}>{course.level}</span>
								{#if course.mandatory}<span class="badge">Required</span>{/if}
								{#if course.deadlineStatus !== 'none'}
									<span class="deadline deadline--{course.deadlineStatus}">
										{deadlineLabel[course.deadlineStatus]}
									</span>
								{/if}
							</div>
							<h3>{course.title}</h3>
							<p>{course.description}</p>
							<span class="card__meta">{course.lessonCount} lessons</span>
						</button>
					</li>
				{/each}
			</ul>
		{/if}
	{/if}
</div>

<style>
	.courses-view {
		padding: 1.25rem;
		color: #e5e7eb;
		font-family: system-ui, sans-serif;
		overflow-y: auto;
		height: 100%;
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
		color: #9ca3af;
	}
	.banner--error {
		background: #7f1d1d;
		color: #fecaca;
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		font-size: 0.85rem;
	}
	.catalogue {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
		gap: 0.75rem;
	}
	.card {
		width: 100%;
		text-align: left;
		background: #111827;
		border: 1px solid #1f2937;
		border-radius: 8px;
		padding: 0.85rem;
		cursor: pointer;
		color: inherit;
	}
	.card:hover {
		border-color: #3b82f6;
	}
	.card__top {
		display: flex;
		gap: 0.4rem;
		flex-wrap: wrap;
		margin-bottom: 0.4rem;
	}
	.card h3 {
		margin: 0 0 0.25rem;
		font-size: 1rem;
	}
	.card p {
		margin: 0 0 0.5rem;
		font-size: 0.8rem;
		color: #9ca3af;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
	.card__meta {
		font-size: 0.75rem;
		color: #6b7280;
	}
	.lvl {
		font-size: 0.7rem;
		padding: 0.1rem 0.45rem;
		border-radius: 999px;
		font-weight: 600;
	}
	.lvl--beg {
		background: #064e3b;
		color: #6ee7b7;
	}
	.lvl--int {
		background: #1e3a8a;
		color: #93c5fd;
	}
	.lvl--adv {
		background: #7f1d1d;
		color: #fca5a5;
	}
	.badge {
		font-size: 0.7rem;
		padding: 0.1rem 0.45rem;
		border-radius: 999px;
		background: #374151;
		color: #d1d5db;
	}
	.deadline {
		font-size: 0.7rem;
		padding: 0.1rem 0.45rem;
		border-radius: 999px;
		font-weight: 600;
	}
	.deadline--upcoming {
		background: #1e3a8a;
		color: #93c5fd;
	}
	.deadline--urgent {
		background: #78350f;
		color: #fcd34d;
	}
	.deadline--overdue {
		background: #7f1d1d;
		color: #fca5a5;
	}
	.back {
		background: none;
		border: none;
		color: #93c5fd;
		cursor: pointer;
		padding: 0;
		font-size: 0.85rem;
		margin-bottom: 0.75rem;
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
		color: #9ca3af;
		font-size: 0.88rem;
	}
	.progress {
		margin: 0.75rem 0;
	}
	.progress__bar {
		height: 8px;
		background: #1f2937;
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
		color: #9ca3af;
	}
	.cert {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		background: #064e3b;
		color: #6ee7b7;
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
		color: #6ee7b7;
		font-weight: 600;
	}
	.cert__claim {
		background: #1d4ed8;
		border: 1px solid #2563eb;
		color: #fff;
		border-radius: 6px;
		padding: 0.45rem 0.7rem;
		font-size: 0.85rem;
		cursor: pointer;
		margin: 0.5rem 0;
	}
	.hint {
		color: #9ca3af;
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
		gap: 0.6rem;
		align-items: center;
		background: #111827;
		border: 1px solid #1f2937;
		border-radius: 6px;
		padding: 0.5rem 0.7rem;
	}
	.lesson--done {
		border-color: #14532d;
	}
	.lesson__type {
		font-size: 0.65rem;
		text-transform: uppercase;
		color: #6b7280;
		min-width: 70px;
	}
	.lesson__title {
		flex: 1;
		font-size: 0.85rem;
	}
	.lesson__dur {
		font-size: 0.72rem;
		color: #6b7280;
	}
	.lesson__done {
		font-size: 0.75rem;
		color: #6ee7b7;
	}
	.lesson__btn {
		font-size: 0.72rem;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		border: 1px solid #3b82f6;
		background: none;
		color: #93c5fd;
		cursor: pointer;
	}
</style>
