/**
 * Quiz-player view-model — the learner's take-a-quiz flow over the
 * answer-blind player endpoints, with the backend calls injected so the
 * logic is unit-testable.
 *
 * Flow: `load(lessonId)` fetches the player view (no correct flags) →
 * the learner `select`s one option per question → `submit` grades it
 * server-side and returns the score/pass + per-question results
 * (explanations included post-grade) → `explain` fetches the optional
 * AI "why it's wrong" feedback.
 */

import { writable, type Writable } from 'svelte/store';
import {
	fetchLessonQuiz as apiFetchLessonQuiz,
	fetchQuizFeedback as apiFetchQuizFeedback,
	submitQuizAttempt as apiSubmitQuizAttempt,
	type PlayerQuiz,
	type QuizAnswerFeedback,
	type QuizAnswers,
	type QuizAttemptResult
} from '$lib/api/coursesApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

export interface QuizPlayerViewModelDeps {
	fetchLessonQuiz: typeof apiFetchLessonQuiz;
	submitQuizAttempt: typeof apiSubmitQuizAttempt;
	fetchQuizFeedback: typeof apiFetchQuizFeedback;
}

const defaultDeps: QuizPlayerViewModelDeps = {
	fetchLessonQuiz: apiFetchLessonQuiz,
	submitQuizAttempt: apiSubmitQuizAttempt,
	fetchQuizFeedback: apiFetchQuizFeedback
};

export interface QuizPlayerViewModel {
	quiz: Writable<PlayerQuiz | null>;
	answers: Writable<QuizAnswers>;
	result: Writable<QuizAttemptResult | null>;
	feedback: Writable<QuizAnswerFeedback[] | null>;
	loading: Writable<boolean>;
	busy: Writable<boolean>;
	error: Writable<string | null>;
	load: (lessonId: string) => Promise<void>;
	select: (questionId: string, optionId: string) => void;
	submit: (lessonId: string) => Promise<void>;
	explain: (lessonId: string) => Promise<void>;
	reset: () => void;
}

export function createQuizPlayerViewModel(
	deps: QuizPlayerViewModelDeps = defaultDeps
): QuizPlayerViewModel {
	const quiz = writable<PlayerQuiz | null>(null);
	const answers = writable<QuizAnswers>({});
	const result = writable<QuizAttemptResult | null>(null);
	const feedback = writable<QuizAnswerFeedback[] | null>(null);
	const loading = writable(false);
	const busy = writable(false);
	const error = writable<string | null>(null);

	let current: QuizAnswers = {};

	function reset(): void {
		quiz.set(null);
		answers.set({});
		current = {};
		result.set(null);
		feedback.set(null);
		error.set(null);
	}

	async function load(lessonId: string): Promise<void> {
		loading.set(true);
		error.set(null);
		result.set(null);
		feedback.set(null);
		current = {};
		answers.set({});
		try {
			quiz.set(await deps.fetchLessonQuiz(lessonId));
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	function select(questionId: string, optionId: string): void {
		current = { ...current, [questionId]: optionId };
		answers.set(current);
	}

	async function submit(lessonId: string): Promise<void> {
		busy.set(true);
		error.set(null);
		try {
			result.set(await deps.submitQuizAttempt(lessonId, current));
		} catch (err) {
			error.set(message(err));
		} finally {
			busy.set(false);
		}
	}

	async function explain(lessonId: string): Promise<void> {
		busy.set(true);
		error.set(null);
		try {
			feedback.set(await deps.fetchQuizFeedback(lessonId, current));
		} catch (err) {
			error.set(message(err));
		} finally {
			busy.set(false);
		}
	}

	return {
		quiz,
		answers,
		result,
		feedback,
		loading,
		busy,
		error,
		load,
		select,
		submit,
		explain,
		reset
	};
}
