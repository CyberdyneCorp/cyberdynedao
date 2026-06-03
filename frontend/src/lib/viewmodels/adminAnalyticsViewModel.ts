/**
 * Admin analytics view-model — the platform-wide overview the admin
 * dashboard renders. One read (`GET /admin/analytics/overview`), injected
 * so the logic stays unit-testable.
 */

import { writable, type Writable } from 'svelte/store';
import { fetchAdminOverview as apiFetchOverview, type AdminOverview } from '$lib/api/adminApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

export interface AdminAnalyticsViewModelDeps {
	fetchOverview: typeof apiFetchOverview;
}

const defaultDeps: AdminAnalyticsViewModelDeps = {
	fetchOverview: apiFetchOverview
};

export interface AdminAnalyticsViewModel {
	overview: Writable<AdminOverview | null>;
	loading: Writable<boolean>;
	error: Writable<string | null>;
	load: () => Promise<void>;
}

export function createAdminAnalyticsViewModel(
	deps: AdminAnalyticsViewModelDeps = defaultDeps
): AdminAnalyticsViewModel {
	const overview = writable<AdminOverview | null>(null);
	const loading = writable(false);
	const error = writable<string | null>(null);

	async function load(): Promise<void> {
		loading.set(true);
		error.set(null);
		try {
			overview.set(await deps.fetchOverview());
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	return { overview, loading, error, load };
}
