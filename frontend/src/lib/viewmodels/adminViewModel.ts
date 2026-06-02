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
	addLesson as apiAddLesson,
	createCourse as apiCreateCourse,
	deleteCourse as apiDeleteCourse,
	deleteLesson as apiDeleteLesson,
	publishCourse as apiPublishCourse,
	unpublishCourse as apiUnpublishCourse,
	uploadFile as apiUploadFile,
	type AddLessonInput,
	type CreateCourseInput,
	type UploadResult
} from '$lib/api/adminApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
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
	uploadFile: apiUploadFile
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
		upload
	};
}
