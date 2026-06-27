import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import { createQuizzesViewModel, type QuizzesViewModelDeps } from '../quizzesViewModel';
import type { QuizCatalogItem, QuizCatalogPage } from '$lib/api/coursesApi';

function item(id: string, attempted: boolean): QuizCatalogItem {
	return {
		quizId: id,
		lessonId: `l-${id}`,
		lessonTitle: `Lesson ${id}`,
		courseSlug: 'c1',
		courseTitle: 'Course One',
		categorySlug: null,
		passingScore: 70,
		questionCount: 5,
		lastAttempt: attempted
			? { score: 90, passed: true, attemptNumber: 1, submittedAt: '2026-01-01T00:00:00Z' }
			: null
	};
}

function page(items: QuizCatalogItem[], nextCursor: string | null = null): QuizCatalogPage {
	return { items, nextCursor };
}

function fakeDeps(over: Partial<QuizzesViewModelDeps> = {}): QuizzesViewModelDeps {
	return {
		fetchCatalogue: vi.fn().mockResolvedValue(page([])),
		...over
	};
}

beforeEach(() => vi.restoreAllMocks());

describe('quizzesViewModel', () => {
	it('loadResults requests attempted=true and stores items + cursor', async () => {
		const fetchCatalogue = vi.fn().mockResolvedValue(page([item('a', true)], 'cur1'));
		const vm = createQuizzesViewModel(fakeDeps({ fetchCatalogue }));
		await vm.loadResults();
		expect(fetchCatalogue).toHaveBeenCalledWith({ attempted: true, limit: 10 });
		expect(get(vm.results)).toHaveLength(1);
		expect(get(vm.resultsCursor)).toBe('cur1');
	});

	it('loadMoreResults appends the next page using the cursor', async () => {
		const fetchCatalogue = vi
			.fn()
			.mockResolvedValueOnce(page([item('a', true)], 'cur1'))
			.mockResolvedValueOnce(page([item('b', true)], null));
		const vm = createQuizzesViewModel(fakeDeps({ fetchCatalogue }));
		await vm.loadResults();
		await vm.loadMoreResults();
		expect(fetchCatalogue).toHaveBeenLastCalledWith({ attempted: true, limit: 10, cursor: 'cur1' });
		expect(get(vm.results).map((q) => q.quizId)).toEqual(['a', 'b']);
		expect(get(vm.resultsCursor)).toBeNull();
	});

	it('loadMoreResults is a no-op when there is no cursor', async () => {
		const fetchCatalogue = vi.fn().mockResolvedValue(page([item('a', true)], null));
		const vm = createQuizzesViewModel(fakeDeps({ fetchCatalogue }));
		await vm.loadResults();
		fetchCatalogue.mockClear();
		await vm.loadMoreResults();
		expect(fetchCatalogue).not.toHaveBeenCalled();
	});

	it('loadBrowse requests the full catalogue (no attempted filter)', async () => {
		const fetchCatalogue = vi
			.fn()
			.mockResolvedValue(page([item('a', true), item('b', false)], 'b1'));
		const vm = createQuizzesViewModel(fakeDeps({ fetchCatalogue }));
		await vm.loadBrowse();
		expect(fetchCatalogue).toHaveBeenCalledWith({ limit: 20 });
		expect(get(vm.browse)).toHaveLength(2);
		expect(get(vm.browseCursor)).toBe('b1');
	});

	it('surfaces an error when a fetch fails', async () => {
		const fetchCatalogue = vi.fn().mockRejectedValue(new Error('boom'));
		const vm = createQuizzesViewModel(fakeDeps({ fetchCatalogue }));
		await vm.loadResults();
		expect(get(vm.error)).toBe('boom');
		expect(get(vm.loadingResults)).toBe(false);
	});

	it('refreshResults re-pulls the first attempted page', async () => {
		const fetchCatalogue = vi.fn().mockResolvedValue(page([item('a', true)], null));
		const vm = createQuizzesViewModel(fakeDeps({ fetchCatalogue }));
		await vm.refreshResults();
		expect(fetchCatalogue).toHaveBeenCalledWith({ attempted: true, limit: 10 });
		expect(get(vm.results)).toHaveLength(1);
	});
});
