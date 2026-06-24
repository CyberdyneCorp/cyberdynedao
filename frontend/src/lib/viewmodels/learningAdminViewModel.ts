/**
 * Learning admin view-model — state + actions for the standalone learning
 * content (reusable modules and the ordered paths that group them), with
 * the backend calls injected so the logic is unit-testable.
 *
 * Mirrors `adminViewModel`: `writable` stores, a `mutate()` helper that
 * runs a backend call then reloads from the server (so the view reflects
 * server truth without optimistic bookkeeping), and methods that return a
 * boolean success so components can clear their forms.
 */

import { get, writable, type Writable } from 'svelte/store';
import {
	createLearningModule as apiCreateModule,
	createLearningPath as apiCreatePath,
	deleteLearningModule as apiDeleteModule,
	deleteLearningPath as apiDeletePath,
	listLearningModules as apiListModules,
	listLearningPaths as apiListPaths,
	reorderPathModules as apiReorderPathModules,
	updateLearningModule as apiUpdateModule,
	updateLearningPath as apiUpdatePath,
	type CreateModuleInput,
	type CreatePathInput,
	type LearningModule,
	type LearningPath,
	type UpdateModuleInput,
	type UpdatePathInput
} from '$lib/api/adminApi';
import { fetchCourses as apiListCourses, type CourseSummary } from '$lib/api/coursesApi';

/** Minimal course shape the picker needs (slug + label fields). */
export interface CourseOption {
	slug: string;
	title: string;
	level: string;
}

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

/**
 * Reorder `slugs` after moving `slug` one step `up`/`down`. Returns `null`
 * when the move is a no-op (slug absent or already at the boundary), so
 * callers can skip the request. e.g. moving "m2" up in [m1,m2,m3] → [m2,m1,m3].
 */
export function reorderedSlugs(
	slugs: string[],
	slug: string,
	dir: 'up' | 'down'
): string[] | null {
	const index = slugs.indexOf(slug);
	if (index < 0) return null;
	const target = dir === 'up' ? index - 1 : index + 1;
	if (target < 0 || target >= slugs.length) return null;
	const next = [...slugs];
	[next[index], next[target]] = [next[target], next[index]];
	return next;
}

export interface AdminLearningViewModelDeps {
	listModules: typeof apiListModules;
	createModule: typeof apiCreateModule;
	updateModule: typeof apiUpdateModule;
	deleteModule: typeof apiDeleteModule;
	listPaths: typeof apiListPaths;
	createPath: typeof apiCreatePath;
	updatePath: typeof apiUpdatePath;
	deletePath: typeof apiDeletePath;
	reorderPathModules: typeof apiReorderPathModules;
	listCourses: typeof apiListCourses;
}

const defaultDeps: AdminLearningViewModelDeps = {
	listModules: apiListModules,
	createModule: apiCreateModule,
	updateModule: apiUpdateModule,
	deleteModule: apiDeleteModule,
	listPaths: apiListPaths,
	createPath: apiCreatePath,
	updatePath: apiUpdatePath,
	deletePath: apiDeletePath,
	reorderPathModules: apiReorderPathModules,
	listCourses: apiListCourses
};

export interface AdminLearningViewModel {
	modules: Writable<LearningModule[]>;
	paths: Writable<LearningPath[]>;
	/** Published courses available to assign to a stage. */
	courses: Writable<CourseOption[]>;
	loading: Writable<boolean>;
	busy: Writable<boolean>;
	error: Writable<string | null>;
	/** Transient success message after a mutation (e.g. "Module created"). */
	notice: Writable<string | null>;
	clearNotice: () => void;
	load: () => Promise<void>;
	createModule: (input: CreateModuleInput) => Promise<boolean>;
	editModule: (slug: string, input: UpdateModuleInput) => Promise<boolean>;
	removeModule: (slug: string) => Promise<boolean>;
	createPath: (input: CreatePathInput) => Promise<boolean>;
	editPath: (slug: string, input: UpdatePathInput) => Promise<boolean>;
	removePath: (slug: string) => Promise<boolean>;
	movePathModule: (pathSlug: string, moduleSlug: string, dir: 'up' | 'down') => Promise<boolean>;
}

export function createLearningAdminViewModel(
	deps: AdminLearningViewModelDeps = defaultDeps
): AdminLearningViewModel {
	const modules = writable<LearningModule[]>([]);
	const paths = writable<LearningPath[]>([]);
	const courses = writable<CourseOption[]>([]);
	const loading = writable(false);
	const busy = writable(false);
	const error = writable<string | null>(null);
	const notice = writable<string | null>(null);

	async function load(): Promise<void> {
		loading.set(true);
		error.set(null);
		try {
			const [moduleList, pathList, courseList] = await Promise.all([
				deps.listModules(),
				deps.listPaths(),
				deps.listCourses()
			]);
			modules.set(moduleList);
			paths.set(pathList);
			courses.set(courseList.map((c: CourseSummary) => ({ slug: c.slug, title: c.title, level: c.level })));
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	// Mutation + reload both lists. On failure the error store is set, the
	// success notice is skipped, and the lists are NOT reloaded.
	async function mutate(run: () => Promise<unknown>, successMsg?: string): Promise<boolean> {
		busy.set(true);
		error.set(null);
		notice.set(null);
		try {
			await run();
			await load();
			if (successMsg) notice.set(successMsg);
			return true;
		} catch (err) {
			error.set(message(err));
			return false;
		} finally {
			busy.set(false);
		}
	}

	return {
		modules,
		paths,
		courses,
		loading,
		busy,
		error,
		notice,
		clearNotice: () => notice.set(null),
		load,
		createModule: (input) => mutate(() => deps.createModule(input), 'Module created'),
		editModule: (slug, input) => mutate(() => deps.updateModule(slug, input), 'Module updated'),
		removeModule: (slug) => mutate(() => deps.deleteModule(slug), 'Module deleted'),
		createPath: (input) => mutate(() => deps.createPath(input), 'Path created'),
		editPath: (slug, input) => mutate(() => deps.updatePath(slug, input), 'Path updated'),
		removePath: (slug) => mutate(() => deps.deletePath(slug), 'Path deleted'),
		movePathModule: (pathSlug, moduleSlug, dir) => {
			const path = get(paths).find((p) => p.slug === pathSlug);
			if (!path) return Promise.resolve(false);
			const next = reorderedSlugs(path.moduleSlugs, moduleSlug, dir);
			if (!next) return Promise.resolve(false);
			return mutate(() => deps.reorderPathModules(pathSlug, next));
		}
	};
}
