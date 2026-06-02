import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import {
	createQuizPlayerViewModel,
	type QuizPlayerViewModelDeps
} from '../quizPlayerViewModel';
import type { PlayerQuiz, QuizAttemptResult } from '$lib/api/coursesApi';

const quiz: PlayerQuiz = {
	lessonId: 'l-1',
	passingScore: 70,
	questions: [
		{ id: 'q1', prompt: '2+2?', options: [{ id: 'o1', text: '3' }, { id: 'o2', text: '4' }] }
	]
};

const result: QuizAttemptResult = {
	attemptId: 'a-1',
	score: 100,
	passed: true,
	attemptNumber: 1,
	submittedAt: '2026-01-01T00:00:00Z',
	results: [
		{ questionId: 'q1', selectedOptionId: 'o2', correctOptionId: 'o2', isCorrect: true, explanation: 'yes' }
	]
};

function fakeDeps(over: Partial<QuizPlayerViewModelDeps> = {}): QuizPlayerViewModelDeps {
	return {
		fetchLessonQuiz: vi.fn().mockResolvedValue(quiz),
		submitQuizAttempt: vi.fn().mockResolvedValue(result),
		fetchQuizFeedback: vi.fn().mockResolvedValue([
			{
				questionId: 'q1',
				prompt: '2+2?',
				isCorrect: false,
				selectedOptionId: 'o1',
				correctOptionId: 'o2',
				staticExplanation: 'addition',
				aiExplanation: 'You picked 3; 2+2 is 4.'
			}
		]),
		...over
	};
}

beforeEach(() => vi.restoreAllMocks());

describe('quizPlayerViewModel', () => {
	it('load fetches the player quiz and clears prior result', async () => {
		const vm = createQuizPlayerViewModel(fakeDeps());
		await vm.load('l-1');
		expect(get(vm.quiz)).toEqual(quiz);
		expect(get(vm.result)).toBeNull();
		expect(get(vm.loading)).toBe(false);
	});

	it('load records errors', async () => {
		const vm = createQuizPlayerViewModel(
			fakeDeps({ fetchLessonQuiz: vi.fn().mockRejectedValue(new Error('404')) })
		);
		await vm.load('l-1');
		expect(get(vm.error)).toBe('404');
	});

	it('select accumulates answers', () => {
		const vm = createQuizPlayerViewModel(fakeDeps());
		vm.select('q1', 'o2');
		vm.select('q2', 'o5');
		expect(get(vm.answers)).toEqual({ q1: 'o2', q2: 'o5' });
	});

	it('submit grades the selected answers', async () => {
		const deps = fakeDeps();
		const vm = createQuizPlayerViewModel(deps);
		await vm.load('l-1');
		vm.select('q1', 'o2');
		await vm.submit('l-1');
		expect(deps.submitQuizAttempt).toHaveBeenCalledWith('l-1', { q1: 'o2' });
		expect(get(vm.result)?.passed).toBe(true);
	});

	it('submit records errors', async () => {
		const vm = createQuizPlayerViewModel(
			fakeDeps({ submitQuizAttempt: vi.fn().mockRejectedValue(new Error('bad')) })
		);
		vm.select('q1', 'o2');
		await vm.submit('l-1');
		expect(get(vm.error)).toBe('bad');
	});

	it('explain fetches AI feedback for the current answers', async () => {
		const deps = fakeDeps();
		const vm = createQuizPlayerViewModel(deps);
		vm.select('q1', 'o1');
		await vm.explain('l-1');
		expect(deps.fetchQuizFeedback).toHaveBeenCalledWith('l-1', { q1: 'o1' });
		expect(get(vm.feedback)?.[0].aiExplanation).toContain('2+2');
	});

	it('explain records errors', async () => {
		const vm = createQuizPlayerViewModel(
			fakeDeps({ fetchQuizFeedback: vi.fn().mockRejectedValue(new Error('llm down')) })
		);
		await vm.explain('l-1');
		expect(get(vm.error)).toBe('llm down');
	});

	it('reset clears everything', async () => {
		const vm = createQuizPlayerViewModel(fakeDeps());
		await vm.load('l-1');
		vm.select('q1', 'o2');
		await vm.submit('l-1');
		vm.reset();
		expect(get(vm.quiz)).toBeNull();
		expect(get(vm.result)).toBeNull();
		expect(get(vm.answers)).toEqual({});
	});

	it('constructs with the real api deps', () => {
		const vm = createQuizPlayerViewModel();
		expect(get(vm.quiz)).toBeNull();
	});
});
