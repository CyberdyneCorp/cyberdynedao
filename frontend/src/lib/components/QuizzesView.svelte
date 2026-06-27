<script lang="ts">
	import { onMount } from 'svelte';
	import { PixelButton, Badge } from '@cyberdynecorp/svelte-ui-core';
	import { createQuizzesViewModel } from '$lib/viewmodels/quizzesViewModel';
	import type { QuizCatalogItem } from '$lib/api/coursesApi';
	import { authVM } from '$lib/auth/authViewModel.svelte';
	import { t, locale } from '$lib/i18n';
	import QuizPlayer from './QuizPlayer.svelte';

	const vm = createQuizzesViewModel();
	const { results, resultsCursor, browse, browseCursor, loadingResults, loadingBrowse, error } = vm;

	const authReady = $derived(authVM.isRestored && authVM.isAuthenticated);

	let subTab = $state<'results' | 'available'>('results');
	// Lesson id whose quiz is being taken inline.
	let takingLessonId = $state<string | null>(null);

	let loaded = $state(false);
	function loadAll(): void {
		void vm.loadResults();
		void vm.loadBrowse();
	}
	onMount(() => {
		if (authReady) {
			loaded = true;
			loadAll();
		}
	});
	$effect(() => {
		if (authReady && !loaded) {
			loaded = true;
			loadAll();
		}
	});

	// Available = not-yet-attempted quizzes from the loaded catalogue pages,
	// grouped by course (the backend has no un-attempted filter; we split
	// client-side, same as the iOS app).
	const availableByCourse = $derived(
		Object.entries(
			$browse
				.filter((q) => q.lastAttempt === null)
				.reduce<Record<string, QuizCatalogItem[]>>((acc, q) => {
					(acc[q.courseTitle] ??= []).push(q);
					return acc;
				}, {})
		).sort(([a], [b]) => a.localeCompare(b))
	);

	function takeQuiz(lessonId: string): void {
		takingLessonId = lessonId;
	}
	function onQuizDone(): void {
		takingLessonId = null;
		// A fresh attempt changes the Results list + attempted state.
		void vm.refreshResults();
		void vm.loadBrowse();
	}

	function fmtDate(iso: string): string {
		return new Date(iso).toLocaleDateString($locale);
	}
</script>

<div class="quizzes">
	{#if !authReady}
		<header class="hero">
			<h1>{$t('quizzes.hero.title')}</h1>
			<p>{$t('quizzes.hero.subtitle')}</p>
		</header>
		<p class="hint">{$t('quizzes.signIn')}</p>
	{:else if takingLessonId}
		<button class="link back" onclick={() => (takingLessonId = null)}>{$t('quizzes.back')}</button>
		<QuizPlayer lessonId={takingLessonId} onDone={onQuizDone} />
	{:else}
		<header class="hero">
			<h1>{$t('quizzes.hero.title')}</h1>
			<p>{$t('quizzes.hero.subtitle')}</p>
		</header>

		<nav class="subtabs" aria-label={$t('quizzes.tabs.aria')}>
			<button
				class="subtab"
				class:subtab--active={subTab === 'results'}
				aria-pressed={subTab === 'results'}
				onclick={() => (subTab = 'results')}
			>
				{$t('quizzes.tabs.results')}
			</button>
			<button
				class="subtab"
				class:subtab--active={subTab === 'available'}
				aria-pressed={subTab === 'available'}
				onclick={() => (subTab = 'available')}
			>
				{$t('quizzes.tabs.available')}
			</button>
		</nav>

		{#if $error}<p class="err">{$error}</p>{/if}

		{#if subTab === 'results'}
			{#if $loadingResults && $results.length === 0}
				<p class="hint">{$t('quizzes.loading')}</p>
			{:else if $results.length === 0}
				<p class="hint empty">{$t('quizzes.noResults')}</p>
			{:else}
				<ul class="list">
					{#each $results as quiz (quiz.quizId)}
						{@const a = quiz.lastAttempt}
						<li class="row">
							<div class="row__main">
								<span class="row__title">{quiz.lessonTitle}</span>
								<span class="row__sub">{quiz.courseTitle}</span>
							</div>
							{#if a}
								<div class="row__attempt">
									<Badge variant={a.passed ? 'success' : 'danger'} size="sm">
										{a.passed ? $t('quizzes.passed') : $t('quizzes.failed')}
									</Badge>
									<span class="row__score">{$t('quizzes.scorePct', { score: String(a.score) })}</span>
									<span class="row__date">{fmtDate(a.submittedAt)}</span>
								</div>
							{/if}
							<PixelButton variant="outline" size="sm" onclick={() => takeQuiz(quiz.lessonId)}>
								{$t('quizzes.retake')}
							</PixelButton>
						</li>
					{/each}
				</ul>
				{#if $resultsCursor}
					<div class="more">
						<PixelButton variant="ghost" size="sm" disabled={$loadingResults} onclick={() => vm.loadMoreResults()}>
							{$loadingResults ? $t('quizzes.loading') : $t('quizzes.loadMore')}
						</PixelButton>
					</div>
				{/if}
			{/if}
		{:else if $loadingBrowse && $browse.length === 0}
			<p class="hint">{$t('quizzes.loading')}</p>
		{:else if availableByCourse.length === 0}
			<p class="hint empty">{$t('quizzes.noAvailable')}</p>
		{:else}
			{#each availableByCourse as [course, quizzes] (course)}
				<section class="group">
					<h3 class="group__head">{course} <span class="group__count">{quizzes.length}</span></h3>
					<ul class="list">
						{#each quizzes as quiz (quiz.quizId)}
							<li class="row">
								<div class="row__main">
									<span class="row__title">{quiz.lessonTitle}</span>
									<span class="row__sub">{$t('quizzes.questionCount', { count: String(quiz.questionCount) })}</span>
								</div>
								<PixelButton variant="solid" size="sm" onclick={() => takeQuiz(quiz.lessonId)}>
									{$t('quizzes.take')}
								</PixelButton>
							</li>
						{/each}
					</ul>
				</section>
			{/each}
			{#if $browseCursor}
				<div class="more">
					<PixelButton variant="ghost" size="sm" disabled={$loadingBrowse} onclick={() => vm.loadMoreBrowse()}>
						{$loadingBrowse ? $t('quizzes.loading') : $t('quizzes.loadMore')}
					</PixelButton>
				</div>
			{/if}
		{/if}
	{/if}
</div>

<style>
	.quizzes {
		padding: 1rem 1.25rem 2rem;
		max-width: 880px;
		margin: 0 auto;
		color: #111827;
	}
	.hero h1 {
		margin: 0 0 0.25rem;
		font-size: 1.4rem;
		color: #111827;
	}
	.hero p {
		margin: 0 0 1rem;
		color: #374151;
	}
	.subtabs {
		display: flex;
		gap: 0.25rem;
		margin: 0 0 1rem;
		border-bottom: 2px solid #e5e7eb;
	}
	.subtab {
		background: none;
		border: none;
		border-bottom: 2px solid transparent;
		margin-bottom: -2px;
		padding: 0.4rem 0.8rem;
		color: #6b7280;
		cursor: pointer;
		font: inherit;
	}
	.subtab--active {
		color: #111827;
		border-bottom-color: #3b82f6;
	}
	.subtab:hover {
		color: #111827;
	}
	.list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.row {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.6rem 0.8rem;
		border: 2px solid #000000;
		border-radius: 8px;
		background: #ffffff;
		color: #111827;
		flex-wrap: wrap;
	}
	.row__main {
		display: flex;
		flex-direction: column;
		flex: 1;
		min-width: 160px;
	}
	.row__title {
		font-weight: bold;
		color: #111827;
	}
	.row__sub {
		font-size: 0.8rem;
		color: #6b7280;
	}
	.row__attempt {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.8rem;
		color: #374151;
	}
	.row__date {
		color: #6b7280;
	}
	.group {
		margin-bottom: 1.25rem;
	}
	.group__head {
		margin: 0 0 0.5rem;
		font-size: 1rem;
		display: flex;
		align-items: center;
		gap: 0.4rem;
		color: #111827;
	}
	.group__count {
		font-size: 0.75rem;
		color: #6b7280;
		border: 1px solid #d1d5db;
		border-radius: 999px;
		padding: 0 0.35rem;
	}
	.more {
		display: flex;
		justify-content: center;
		margin-top: 1rem;
	}
	.back,
	.link {
		background: none;
		border: none;
		color: #3b82f6;
		cursor: pointer;
		padding: 0;
		font: inherit;
		margin-bottom: 0.75rem;
	}
	.hint {
		color: #6b7280;
	}
	.empty {
		padding: 2rem 0;
		text-align: center;
	}
	.err {
		color: #991b1b;
	}
</style>
