/**
 * Admin authoring view-model — the course CMS state + actions, with the
 * backend calls injected so the logic is unit-testable.
 *
 * Listing reuses `coursesApi.fetchCourses` (the editor bearer makes the
 * backend include drafts); a selected course's detail (incl. its lessons)
 * comes from `coursesApi.fetchCourse`; mutations go through `adminApi`.
 * After every mutation we reload from the server (list or the selected
 * course) so the view reflects server truth without optimistic bookkeeping.
 */

import { get, writable, type Writable } from 'svelte/store';
import {
	fetchCourse as apiFetchCourse,
	fetchCourses as apiFetchCourses,
	type CourseDetail,
	type CourseSummary
} from '$lib/api/coursesApi';
import {
	AdminApiError,
	addLesson as apiAddLesson,
	createCourse as apiCreateCourse,
	deleteCourse as apiDeleteCourse,
	deleteLesson as apiDeleteLesson,
	deleteQuiz as apiDeleteQuiz,
	getQuiz as apiGetQuiz,
	publishCourse as apiPublishCourse,
	reorderCourses as apiReorderCourses,
	reorderLessons as apiReorderLessons,
	setCourseDeadline as apiSetCourseDeadline,
	unpublishCourse as apiUnpublishCourse,
	updateCourse as apiUpdateCourse,
	updateLesson as apiUpdateLesson,
	upsertQuiz as apiUpsertQuiz,
	uploadFile as apiUploadFile,
	type AddLessonInput,
	type CreateCourseInput,
	type EditorQuiz,
	type UpdateCourseInput,
	type UpdateLessonInput,
	type UploadResult,
	type UpsertQuizInput
} from '$lib/api/adminApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

/**
 * Whether the admin view should kick off its one-time initial course
 * load. Deliberately independent of how many courses came back: an empty
 * list is a valid result, so gating on `courses.length === 0` would
 * re-trigger the load forever and leave the UI stuck on "Loading…".
 * Callers track `attempted` and flip it before loading.
 */
export function shouldAutoLoad(canEdit: boolean, attempted: boolean, loading: boolean): boolean {
	return canEdit && !attempted && !loading;
}

/**
 * Build the `{id: sortOrder}` payload for a reorder endpoint after moving
 * the item at `index` one step `up`/`down`. Returns `null` when the move
 * is a no-op (out of bounds), so callers can skip the request. Order is
 * re-densified to 0..n-1 so sort positions stay contiguous.
 */
export function reorderedMap(
	ids: string[],
	index: number,
	dir: 'up' | 'down'
): Record<string, number> | null {
	const target = dir === 'up' ? index - 1 : index + 1;
	if (index < 0 || target < 0 || target >= ids.length) return null;
	const next = [...ids];
	[next[index], next[target]] = [next[target], next[index]];
	return Object.fromEntries(next.map((id, i) => [id, i]));
}

export interface AdminViewModelDeps {
	listCourses: typeof apiFetchCourses;
	getCourse: typeof apiFetchCourse;
	createCourse: typeof apiCreateCourse;
	updateCourse: typeof apiUpdateCourse;
	setCourseDeadline: typeof apiSetCourseDeadline;
	publishCourse: typeof apiPublishCourse;
	unpublishCourse: typeof apiUnpublishCourse;
	deleteCourse: typeof apiDeleteCourse;
	reorderCourses: typeof apiReorderCourses;
	addLesson: typeof apiAddLesson;
	updateLesson: typeof apiUpdateLesson;
	deleteLesson: typeof apiDeleteLesson;
	reorderLessons: typeof apiReorderLessons;
	uploadFile: typeof apiUploadFile;
	getQuiz: typeof apiGetQuiz;
	upsertQuiz: typeof apiUpsertQuiz;
	deleteQuiz: typeof apiDeleteQuiz;
}

const defaultDeps: AdminViewModelDeps = {
	listCourses: apiFetchCourses,
	getCourse: apiFetchCourse,
	createCourse: apiCreateCourse,
	updateCourse: apiUpdateCourse,
	setCourseDeadline: apiSetCourseDeadline,
	publishCourse: apiPublishCourse,
	unpublishCourse: apiUnpublishCourse,
	deleteCourse: apiDeleteCourse,
	reorderCourses: apiReorderCourses,
	addLesson: apiAddLesson,
	updateLesson: apiUpdateLesson,
	deleteLesson: apiDeleteLesson,
	reorderLessons: apiReorderLessons,
	uploadFile: apiUploadFile,
	getQuiz: apiGetQuiz,
	upsertQuiz: apiUpsertQuiz,
	deleteQuiz: apiDeleteQuiz
};

export interface AdminViewModel {
	courses: Writable<CourseSummary[]>;
	selected: Writable<CourseDetail | null>;
	loading: Writable<boolean>;
	busy: Writable<boolean>;
	error: Writable<string | null>;
	load: () => Promise<void>;
	create: (input: CreateCourseInput) => Promise<boolean>;
	editCourse: (slug: string, input: UpdateCourseInput) => Promise<boolean>;
	setDeadline: (slug: string, dueAt: string | null) => Promise<boolean>;
	moveCourse: (slug: string, dir: 'up' | 'down') => Promise<boolean>;
	editLesson: (lessonId: string, input: UpdateLessonInput) => Promise<boolean>;
	moveLesson: (lessonId: string, dir: 'up' | 'down') => Promise<boolean>;
	publish: (slug: string) => Promise<void>;
	unpublish: (slug: string) => Promise<void>;
	remove: (slug: string) => Promise<void>;
	openCourse: (slug: string) => Promise<void>;
	closeCourse: () => void;
	addLesson: (input: AddLessonInput) => Promise<boolean>;
	removeLesson: (lessonId: string) => Promise<void>;
	upload: (file: File) => Promise<UploadResult | null>;
	/** Load a lesson's quiz, or `null` when it has none yet (author fresh). */
	loadQuiz: (lessonId: string) => Promise<EditorQuiz | null>;
	saveQuiz: (lessonId: string, input: UpsertQuizInput) => Promise<boolean>;
	removeQuiz: (lessonId: string) => Promise<boolean>;
}

export function createAdminViewModel(deps: AdminViewModelDeps = defaultDeps): AdminViewModel {
	const courses = writable<CourseSummary[]>([]);
	const selected = writable<CourseDetail | null>(null);
	const loading = writable(false);
	const busy = writable(false);
	const error = writable<string | null>(null);

	let selectedSlug: string | null = null;

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

	// Mutation + reload the course LIST (course-level changes).
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

	// Mutation + reload the SELECTED course detail (lesson-level changes).
	async function mutateSelected(run: () => Promise<unknown>): Promise<boolean> {
		if (!selectedSlug) return false;
		busy.set(true);
		error.set(null);
		try {
			await run();
			selected.set(await deps.getCourse(selectedSlug));
			return true;
		} catch (err) {
			error.set(message(err));
			return false;
		} finally {
			busy.set(false);
		}
	}

	async function openCourse(slug: string): Promise<void> {
		loading.set(true);
		error.set(null);
		try {
			const detail = await deps.getCourse(slug);
			selected.set(detail);
			selectedSlug = slug;
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	function closeCourse(): void {
		selected.set(null);
		selectedSlug = null;
	}

	async function upload(file: File): Promise<UploadResult | null> {
		busy.set(true);
		error.set(null);
		try {
			return await deps.uploadFile(file);
		} catch (err) {
			error.set(message(err));
			return null;
		} finally {
			busy.set(false);
		}
	}

	async function loadQuiz(lessonId: string): Promise<EditorQuiz | null> {
		busy.set(true);
		error.set(null);
		try {
			return await deps.getQuiz(lessonId);
		} catch (err) {
			// A lesson with no quiz yet is the "author a fresh one" case,
			// not an error to surface.
			if (err instanceof AdminApiError && err.status === 404) return null;
			error.set(message(err));
			return null;
		} finally {
			busy.set(false);
		}
	}

	async function saveQuiz(lessonId: string, input: UpsertQuizInput): Promise<boolean> {
		busy.set(true);
		error.set(null);
		try {
			await deps.upsertQuiz(lessonId, input);
			return true;
		} catch (err) {
			error.set(message(err));
			return false;
		} finally {
			busy.set(false);
		}
	}

	async function removeQuiz(lessonId: string): Promise<boolean> {
		busy.set(true);
		error.set(null);
		try {
			await deps.deleteQuiz(lessonId);
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
		selected,
		loading,
		busy,
		error,
		load,
		create: (input) => mutate(() => deps.createCourse(input)),
		// Course-level edits happen while a course is open: refresh the
		// open detail AND the list (so the catalogue reflects the new
		// title/status/deadline once the editor closes).
		editCourse: async (slug, input) => {
			const ok = await mutateSelected(() => deps.updateCourse(slug, input));
			if (ok) await load();
			return ok;
		},
		setDeadline: async (slug, dueAt) => {
			const ok = await mutateSelected(() => deps.setCourseDeadline(slug, dueAt));
			if (ok) await load();
			return ok;
		},
		moveCourse: async (slug, dir) => {
			const list = get(courses);
			const map = reorderedMap(
				list.map((c) => c.slug),
				list.findIndex((c) => c.slug === slug),
				dir
			);
			if (!map) return false;
			return mutate(() => deps.reorderCourses(map));
		},
		editLesson: (lessonId, input) =>
			mutateSelected(() => deps.updateLesson(selectedSlug as string, lessonId, input)),
		moveLesson: async (lessonId, dir) => {
			const sel = get(selected);
			if (!sel) return false;
			const map = reorderedMap(
				sel.lessons.map((l) => l.id),
				sel.lessons.findIndex((l) => l.id === lessonId),
				dir
			);
			if (!map) return false;
			return mutateSelected(() => deps.reorderLessons(sel.slug, map));
		},
		publish: async (slug) => {
			await mutate(() => deps.publishCourse(slug));
		},
		unpublish: async (slug) => {
			await mutate(() => deps.unpublishCourse(slug));
		},
		remove: async (slug) => {
			await mutate(() => deps.deleteCourse(slug));
		},
		openCourse,
		closeCourse,
		addLesson: (input) => mutateSelected(() => deps.addLesson(selectedSlug as string, input)),
		removeLesson: async (lessonId) => {
			await mutateSelected(() => deps.deleteLesson(selectedSlug as string, lessonId));
		},
		upload,
		loadQuiz,
		saveQuiz,
		removeQuiz
	};
}
