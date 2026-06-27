/**
 * Quizzes view-model — the learner's quiz catalogue split into two
 * surfaces, both server-paged via the `/api/v1/quizzes` cursor:
 *
 *  - **Results**: `attempted=true`, the learner's most-recently-submitted
 *    quizzes (server-ordered, recent first), "load more" via the cursor.
 *  - **Available**: the full catalogue (paged), from which the component
 *    surfaces the not-yet-attempted quizzes grouped by course. The backend
 *    has no "un-attempted only" filter, so this pages the full catalogue
 *    and the not-taken split happens client-side (same as the iOS app).
 *
 * Async actions are injected so the orchestration is unit-testable.
 */

import { writable, type Writable } from 'svelte/store';
import {
	fetchQuizCatalogue as apiFetchCatalogue,
	type QuizCatalogItem
} from '$lib/api/coursesApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

const RESULTS_PAGE = 10;
const BROWSE_PAGE = 20;

export interface QuizzesViewModelDeps {
	fetchCatalogue: typeof apiFetchCatalogue;
}

const defaultDeps: QuizzesViewModelDeps = {
	fetchCatalogue: apiFetchCatalogue
};

export interface QuizzesViewModel {
	results: Writable<QuizCatalogItem[]>;
	resultsCursor: Writable<string | null>;
	browse: Writable<QuizCatalogItem[]>;
	browseCursor: Writable<string | null>;
	loadingResults: Writable<boolean>;
	loadingBrowse: Writable<boolean>;
	error: Writable<string | null>;
	/** First page of the learner's attempted quizzes (recent first). */
	loadResults: () => Promise<void>;
	loadMoreResults: () => Promise<void>;
	/** First page of the full catalogue (for the Available/browse split). */
	loadBrowse: () => Promise<void>;
	loadMoreBrowse: () => Promise<void>;
	/** Re-pull the first results page (e.g. after taking a quiz). */
	refreshResults: () => Promise<void>;
}

export function createQuizzesViewModel(
	deps: QuizzesViewModelDeps = defaultDeps
): QuizzesViewModel {
	const results = writable<QuizCatalogItem[]>([]);
	const resultsCursor = writable<string | null>(null);
	const browse = writable<QuizCatalogItem[]>([]);
	const browseCursor = writable<string | null>(null);
	const loadingResults = writable(false);
	const loadingBrowse = writable(false);
	const error = writable<string | null>(null);

	async function loadResults(): Promise<void> {
		loadingResults.set(true);
		error.set(null);
		try {
			const page = await deps.fetchCatalogue({ attempted: true, limit: RESULTS_PAGE });
			results.set(page.items);
			resultsCursor.set(page.nextCursor);
		} catch (err) {
			error.set(message(err));
		} finally {
			loadingResults.set(false);
		}
	}

	async function loadMoreResults(): Promise<void> {
		let cursor: string | null = null;
		resultsCursor.subscribe((c) => (cursor = c))();
		if (!cursor) return;
		loadingResults.set(true);
		try {
			const page = await deps.fetchCatalogue({
				attempted: true,
				limit: RESULTS_PAGE,
				cursor
			});
			results.update((cur) => [...cur, ...page.items]);
			resultsCursor.set(page.nextCursor);
		} catch (err) {
			error.set(message(err));
		} finally {
			loadingResults.set(false);
		}
	}

	async function refreshResults(): Promise<void> {
		await loadResults();
	}

	async function loadBrowse(): Promise<void> {
		loadingBrowse.set(true);
		error.set(null);
		try {
			const page = await deps.fetchCatalogue({ limit: BROWSE_PAGE });
			browse.set(page.items);
			browseCursor.set(page.nextCursor);
		} catch (err) {
			error.set(message(err));
		} finally {
			loadingBrowse.set(false);
		}
	}

	async function loadMoreBrowse(): Promise<void> {
		let cursor: string | null = null;
		browseCursor.subscribe((c) => (cursor = c))();
		if (!cursor) return;
		loadingBrowse.set(true);
		try {
			const page = await deps.fetchCatalogue({ limit: BROWSE_PAGE, cursor });
			browse.update((cur) => [...cur, ...page.items]);
			browseCursor.set(page.nextCursor);
		} catch (err) {
			error.set(message(err));
		} finally {
			loadingBrowse.set(false);
		}
	}

	return {
		results,
		resultsCursor,
		browse,
		browseCursor,
		loadingResults,
		loadingBrowse,
		error,
		loadResults,
		loadMoreResults,
		loadBrowse,
		loadMoreBrowse,
		refreshResults
	};
}
