<script lang="ts">
	import { onMount } from 'svelte';
	import { PixelButton, Badge } from '@cyberdynecorp/svelte-ui-core';
	import { createQuizPlayerViewModel } from '$lib/viewmodels/quizPlayerViewModel';

	let { lessonId, onDone }: { lessonId: string; onDone?: () => void } = $props();

	const vm = createQuizPlayerViewModel();
	const { quiz, answers, result, feedback, loading, busy, error } = vm;

	onMount(() => {
		void vm.load(lessonId);
	});

	const allAnswered = $derived(
		!!$quiz && $quiz.questions.every((q) => $answers[q.id] !== undefined)
	);

	function aiFor(questionId: string): string | null {
		return $feedback?.find((f) => f.questionId === questionId)?.aiExplanation ?? null;
	}
</script>

<div class="quiz">
	<div class="quiz__head">
		<h3>Quiz</h3>
		<PixelButton variant="ghost" size="sm" onclick={() => onDone?.()}>Close</PixelButton>
	</div>

	{#if $error}
		<p class="banner banner--error" role="alert">{$error}</p>
	{/if}

	{#if $loading}
		<p class="hint">Loading quiz…</p>
	{:else if !$quiz}
		<p class="hint">No quiz available.</p>
	{:else if $result}
		{@const res = $result}
		<!-- Graded result -->
		<div class="score" class:score--pass={res.passed}>
			{res.passed ? '✓ Passed' : '✗ Not passed'} — {res.score}% (attempt {res.attemptNumber})
		</div>
		<ol class="qlist">
			{#each $quiz.questions as q (q.id)}
				{@const r = res.results.find((x) => x.questionId === q.id)}
				<li class="q" class:q--wrong={r && !r.isCorrect}>
					<p class="q__prompt">{q.prompt}</p>
					{#each q.options as opt (opt.id)}
						<div
							class="opt"
							class:opt--correct={r && opt.id === r.correctOptionId}
							class:opt--chosen={r && opt.id === r.selectedOptionId}
						>
							{opt.text}
							{#if r && opt.id === r.correctOptionId}<Badge variant="success" size="sm">correct</Badge>{/if}
							{#if r && opt.id === r.selectedOptionId && !r.isCorrect}<Badge variant="danger" size="sm">your answer</Badge>{/if}
						</div>
					{/each}
					{#if r?.explanation}<p class="explain">{r.explanation}</p>{/if}
					{#if aiFor(q.id)}<p class="explain explain--ai">💡 {aiFor(q.id)}</p>{/if}
				</li>
			{/each}
		</ol>
		<div class="row">
			{#if !$feedback}
				<PixelButton variant="outline" size="sm" disabled={$busy} onclick={() => vm.explain(lessonId)}>
					{$busy ? 'Thinking…' : 'Explain my answers (AI)'}
				</PixelButton>
			{/if}
			<PixelButton variant="outline" size="sm" disabled={$busy} onclick={() => vm.load(lessonId)}>
				Try again
			</PixelButton>
			<PixelButton variant="solid" size="sm" onclick={() => onDone?.()}>Done</PixelButton>
		</div>
	{:else}
		<!-- Taking the quiz -->
		<ol class="qlist">
			{#each $quiz.questions as q, qi (q.id)}
				<li class="q">
					<p class="q__prompt">{qi + 1}. {q.prompt}</p>
					{#each q.options as opt (opt.id)}
						<label class="opt opt--pick">
							<input
								type="radio"
								name="q-{q.id}"
								value={opt.id}
								checked={$answers[q.id] === opt.id}
								onchange={() => vm.select(q.id, opt.id)}
							/>
							{opt.text}
						</label>
					{/each}
				</li>
			{/each}
		</ol>
		<PixelButton variant="solid" size="sm" disabled={$busy || !allAnswered} onclick={() => vm.submit(lessonId)}>
			{$busy ? 'Submitting…' : 'Submit answers'}
		</PixelButton>
	{/if}
</div>

<style>
	.quiz {
		background: #0b1220;
		border: 1px solid #1f2937;
		border-radius: 8px;
		padding: 0.85rem;
		margin-top: 0.6rem;
	}
	.quiz__head {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.quiz__head h3 {
		margin: 0;
		font-size: 1rem;
	}
	.banner--error {
		background: #7f1d1d;
		color: #fecaca;
		padding: 0.4rem 0.6rem;
		border-radius: 6px;
		font-size: 0.82rem;
	}
	.hint {
		color: #9ca3af;
		font-size: 0.85rem;
	}
	.qlist {
		list-style: none;
		margin: 0.5rem 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}
	.q {
		border: 1px solid #1f2937;
		border-radius: 6px;
		padding: 0.55rem 0.7rem;
	}
	.q--wrong {
		border-color: #7f1d1d;
	}
	.q__prompt {
		margin: 0 0 0.4rem;
		font-size: 0.88rem;
	}
	.opt {
		font-size: 0.82rem;
		padding: 0.2rem 0.35rem;
		border-radius: 4px;
		color: #d1d5db;
	}
	.opt--pick {
		display: flex;
		gap: 0.45rem;
		align-items: center;
		cursor: pointer;
	}
	.opt--correct {
		background: #064e3b;
		color: #6ee7b7;
	}
	.opt--chosen {
		outline: 1px solid #64748b;
	}
	.explain {
		margin: 0.35rem 0 0;
		font-size: 0.78rem;
		color: #9ca3af;
	}
	.explain--ai {
		color: #c4b5fd;
	}
	.score {
		font-weight: 600;
		font-size: 0.95rem;
		color: #fca5a5;
		margin-bottom: 0.4rem;
	}
	.score--pass {
		color: #6ee7b7;
	}
	.row {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		margin-top: 0.5rem;
	}
</style>
