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

import { writable, type Writable } from 'svelte/store';
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
	unpublishCourse as apiUnpublishCourse,
	upsertQuiz as apiUpsertQuiz,
	uploadFile as apiUploadFile,
	type AddLessonInput,
	type CreateCourseInput,
	type EditorQuiz,
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

export interface AdminViewModelDeps {
	listCourses: typeof apiFetchCourses;
	getCourse: typeof apiFetchCourse;
	createCourse: typeof apiCreateCourse;
	publishCourse: typeof apiPublishCourse;
	unpublishCourse: typeof apiUnpublishCourse;
	deleteCourse: typeof apiDeleteCourse;
	addLesson: typeof apiAddLesson;
	deleteLesson: typeof apiDeleteLesson;
	uploadFile: typeof apiUploadFile;
	getQuiz: typeof apiGetQuiz;
	upsertQuiz: typeof apiUpsertQuiz;
	deleteQuiz: typeof apiDeleteQuiz;
}

const defaultDeps: AdminViewModelDeps = {
	listCourses: apiFetchCourses,
	getCourse: apiFetchCourse,
	createCourse: apiCreateCourse,
	publishCourse: apiPublishCourse,
	unpublishCourse: apiUnpublishCourse,
	deleteCourse: apiDeleteCourse,
	addLesson: apiAddLesson,
	deleteLesson: apiDeleteLesson,
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
