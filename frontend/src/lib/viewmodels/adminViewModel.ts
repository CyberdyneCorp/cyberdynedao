/**
 * Admin authoring view-model — the course CMS state + actions, with the
 * backend calls injected so the logic is unit-testable.
 *
 * Listing reuses `coursesApi.fetchCourses` (the editor bearer makes the
 * backend include drafts); mutations go through `adminApi`. After every
 * mutation we reload the list so the view reflects server truth
 * (statuses, new slugs) without optimistic bookkeeping.
 */

import { writable, type Writable } from 'svelte/store';
import { fetchCourses as apiFetchCourses, type CourseSummary } from '$lib/api/coursesApi';
import {
	createCourse as apiCreateCourse,
	deleteCourse as apiDeleteCourse,
	publishCourse as apiPublishCourse,
	unpublishCourse as apiUnpublishCourse,
	type CreateCourseInput
} from '$lib/api/adminApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

export interface AdminViewModelDeps {
	listCourses: typeof apiFetchCourses;
	createCourse: typeof apiCreateCourse;
	publishCourse: typeof apiPublishCourse;
	unpublishCourse: typeof apiUnpublishCourse;
	deleteCourse: typeof apiDeleteCourse;
}

const defaultDeps: AdminViewModelDeps = {
	listCourses: apiFetchCourses,
	createCourse: apiCreateCourse,
	publishCourse: apiPublishCourse,
	unpublishCourse: apiUnpublishCourse,
	deleteCourse: apiDeleteCourse
};

export interface AdminViewModel {
	courses: Writable<CourseSummary[]>;
	loading: Writable<boolean>;
	busy: Writable<boolean>;
	error: Writable<string | null>;
	load: () => Promise<void>;
	create: (input: CreateCourseInput) => Promise<boolean>;
	publish: (slug: string) => Promise<void>;
	unpublish: (slug: string) => Promise<void>;
	remove: (slug: string) => Promise<void>;
}

export function createAdminViewModel(deps: AdminViewModelDeps = defaultDeps): AdminViewModel {
	const courses = writable<CourseSummary[]>([]);
	const loading = writable(false);
	const busy = writable(false);
	const error = writable<string | null>(null);

	async function load(): Promise<void> {
		loading.set(true);
		error.set(null);
		try {
			courses.set(await deps.listCourses());
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	// Runs a mutation with the busy guard, then reloads. Returns whether
	// the mutation succeeded (callers like `create` use it to reset forms).
	async function mutate(run: () => Promise<unknown>): Promise<boolean> {
		busy.set(true);
		error.set(null);
		try {
			await run();
			await load();
			return true;
		} catch (err) {
			error.set(message(err));
			return false;
		} finally {
			busy.set(false);
		}
	}

	return {
		courses,
		loading,
		busy,
		error,
		load,
		create: (input) => mutate(() => deps.createCourse(input)),
		publish: async (slug) => {
			await mutate(() => deps.publishCourse(slug));
		},
		unpublish: async (slug) => {
			await mutate(() => deps.unpublishCourse(slug));
		},
		remove: async (slug) => {
			await mutate(() => deps.deleteCourse(slug));
		}
	};
}
