/**
 * Courses view-model — catalogue + selected-course detail + the signed-in
 * learner's progress, with the async actions injected so the logic is
 * unit-testable without a live backend.
 *
 * Sits on top of `coursesApi.ts`. A thin Svelte component renders these
 * stores and calls the actions; all orchestration + error handling lives
 * here (unlike the older `learnViewModel`, which left API calls in the
 * component).
 */

import { writable, type Writable } from 'svelte/store';
import {
	fetchCourse as apiFetchCourse,
	fetchCourses as apiFetchCourses,
	fetchMyCourseProgress as apiFetchMyCourseProgress,
	setLessonProgress as apiSetLessonProgress,
	type CourseDetail,
	type CourseLevel,
	type CourseProgress,
	type CourseSummary
} from '$lib/api/coursesApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

export interface CoursesViewModelDeps {
	fetchCourses: typeof apiFetchCourses;
	fetchCourse: typeof apiFetchCourse;
	fetchMyCourseProgress: typeof apiFetchMyCourseProgress;
	setLessonProgress: typeof apiSetLessonProgress;
}

const defaultDeps: CoursesViewModelDeps = {
	fetchCourses: apiFetchCourses,
	fetchCourse: apiFetchCourse,
	fetchMyCourseProgress: apiFetchMyCourseProgress,
	setLessonProgress: apiSetLessonProgress
};

export interface CoursesViewModel {
	courses: Writable<CourseSummary[]>;
	selected: Writable<CourseDetail | null>;
	progress: Writable<CourseProgress | null>;
	loading: Writable<boolean>;
	error: Writable<string | null>;
	loadCatalogue: (level?: CourseLevel) => Promise<void>;
	open: (slug: string, opts?: { withProgress?: boolean }) => Promise<void>;
	refreshProgress: (slug: string) => Promise<void>;
	completeLesson: (slug: string, lessonId: string) => Promise<void>;
	close: () => void;
}

export function createCoursesViewModel(
	deps: CoursesViewModelDeps = defaultDeps
): CoursesViewModel {
	const courses = writable<CourseSummary[]>([]);
	const selected = writable<CourseDetail | null>(null);
	const progress = writable<CourseProgress | null>(null);
	const loading = writable(false);
	const error = writable<string | null>(null);

	async function loadCatalogue(level?: CourseLevel): Promise<void> {
		loading.set(true);
		error.set(null);
		try {
			courses.set(await deps.fetchCourses(level));
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	async function open(slug: string, opts: { withProgress?: boolean } = {}): Promise<void> {
		loading.set(true);
		error.set(null);
		try {
			selected.set(await deps.fetchCourse(slug));
			progress.set(opts.withProgress ? await deps.fetchMyCourseProgress(slug) : null);
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	async function refreshProgress(slug: string): Promise<void> {
		try {
			progress.set(await deps.fetchMyCourseProgress(slug));
		} catch (err) {
			error.set(message(err));
		}
	}

	async function completeLesson(slug: string, lessonId: string): Promise<void> {
		error.set(null);
		try {
			progress.set(await deps.setLessonProgress(slug, lessonId, 100));
		} catch (err) {
			error.set(message(err));
		}
	}

	function close(): void {
		selected.set(null);
		progress.set(null);
		error.set(null);
	}

	return {
		courses,
		selected,
		progress,
		loading,
		error,
		loadCatalogue,
		open,
		refreshProgress,
		completeLesson,
		close
	};
}
