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
	CoursesApiError,
	claimCourseCertificate as apiClaimCertificate,
	fetchCourse as apiFetchCourse,
	fetchCourses as apiFetchCourses,
	fetchLearnerDashboard as apiFetchDashboard,
	fetchMyCourseCertificate as apiFetchMyCertificate,
	fetchMyCourseProgress as apiFetchMyCourseProgress,
	fetchRecommendations as apiFetchRecommendations,
	setLessonProgress as apiSetLessonProgress,
	verifyCourseCertificate as apiVerifyCertificate,
	type CourseCertificate,
	type CourseCertificateVerification,
	type CourseDetail,
	type CourseLevel,
	type CourseProgress,
	type CourseSummary,
	type LearnerDashboard,
	type LearningRecommendations
} from '$lib/api/coursesApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

export interface CoursesViewModelDeps {
	fetchCourses: typeof apiFetchCourses;
	fetchCourse: typeof apiFetchCourse;
	fetchMyCourseProgress: typeof apiFetchMyCourseProgress;
	setLessonProgress: typeof apiSetLessonProgress;
	fetchMyCertificate: typeof apiFetchMyCertificate;
	claimCertificate: typeof apiClaimCertificate;
	fetchDashboard: typeof apiFetchDashboard;
	fetchRecommendations: typeof apiFetchRecommendations;
	verifyCertificate: typeof apiVerifyCertificate;
}

const defaultDeps: CoursesViewModelDeps = {
	fetchCourses: apiFetchCourses,
	fetchCourse: apiFetchCourse,
	fetchMyCourseProgress: apiFetchMyCourseProgress,
	setLessonProgress: apiSetLessonProgress,
	fetchMyCertificate: apiFetchMyCertificate,
	claimCertificate: apiClaimCertificate,
	fetchDashboard: apiFetchDashboard,
	fetchRecommendations: apiFetchRecommendations,
	verifyCertificate: apiVerifyCertificate
};

export interface CoursesViewModel {
	courses: Writable<CourseSummary[]>;
	selected: Writable<CourseDetail | null>;
	progress: Writable<CourseProgress | null>;
	certificate: Writable<CourseCertificate | null>;
	dashboard: Writable<LearnerDashboard | null>;
	recommendations: Writable<LearningRecommendations | null>;
	verification: Writable<CourseCertificateVerification | null>;
	verifying: Writable<boolean>;
	loading: Writable<boolean>;
	error: Writable<string | null>;
	loadCatalogue: (level?: CourseLevel) => Promise<void>;
	/** Public certificate authenticity check by id. */
	verify: (certificateId: string) => Promise<void>;
	/** Load the signed-in learner's dashboard + recommendations (best-effort). */
	loadMe: () => Promise<void>;
	open: (slug: string, opts?: { withProgress?: boolean }) => Promise<void>;
	refreshProgress: (slug: string) => Promise<void>;
	completeLesson: (slug: string, lessonId: string) => Promise<void>;
	claimCertificate: (slug: string) => Promise<void>;
	close: () => void;
}

export function createCoursesViewModel(
	deps: CoursesViewModelDeps = defaultDeps
): CoursesViewModel {
	const courses = writable<CourseSummary[]>([]);
	const selected = writable<CourseDetail | null>(null);
	const progress = writable<CourseProgress | null>(null);
	const certificate = writable<CourseCertificate | null>(null);
	const dashboard = writable<LearnerDashboard | null>(null);
	const recommendations = writable<LearningRecommendations | null>(null);
	const verification = writable<CourseCertificateVerification | null>(null);
	const verifying = writable(false);
	const loading = writable(false);
	const error = writable<string | null>(null);

	// Best-effort: the learner's dashboard + recommendations for the
	// catalogue header. Failures (e.g. 401 when the session lapsed) leave
	// the panels hidden rather than blocking the catalogue.
	async function loadMe(): Promise<void> {
		try {
			dashboard.set(await deps.fetchDashboard());
		} catch {
			dashboard.set(null);
		}
		try {
			recommendations.set(await deps.fetchRecommendations());
		} catch {
			recommendations.set(null);
		}
	}

	// Best-effort: the learner's certificate for a course (auto-issued on
	// completion). A 404 just means "not earned yet" — not an error.
	async function loadCertificate(slug: string): Promise<void> {
		try {
			certificate.set(await deps.fetchMyCertificate(slug));
		} catch (err) {
			if (err instanceof CoursesApiError && err.status === 404) {
				certificate.set(null);
				return;
			}
			error.set(message(err));
			certificate.set(null);
		}
	}

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
			if (opts.withProgress) {
				progress.set(await deps.fetchMyCourseProgress(slug));
				await loadCertificate(slug);
			} else {
				progress.set(null);
				certificate.set(null);
			}
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	async function refreshProgress(slug: string): Promise<void> {
		try {
			progress.set(await deps.fetchMyCourseProgress(slug));
			await loadCertificate(slug);
		} catch (err) {
			error.set(message(err));
		}
	}

	async function completeLesson(slug: string, lessonId: string): Promise<void> {
		error.set(null);
		try {
			progress.set(await deps.setLessonProgress(slug, lessonId, 100));
			await loadCertificate(slug);
		} catch (err) {
			error.set(message(err));
		}
	}

	async function claimCertificate(slug: string): Promise<void> {
		error.set(null);
		try {
			certificate.set(await deps.claimCertificate(slug));
		} catch (err) {
			error.set(message(err));
		}
	}

	// Public verification: anyone can check a certificate id. A 404 means
	// no such certificate — report it as "not valid" rather than an error.
	async function verify(certificateId: string): Promise<void> {
		verifying.set(true);
		error.set(null);
		try {
			verification.set(await deps.verifyCertificate(certificateId));
		} catch (err) {
			if (err instanceof CoursesApiError && err.status === 404) {
				verification.set({ valid: false, certificate: null });
			} else {
				error.set(message(err));
				verification.set(null);
			}
		} finally {
			verifying.set(false);
		}
	}

	function close(): void {
		selected.set(null);
		progress.set(null);
		certificate.set(null);
		error.set(null);
	}

	return {
		courses,
		selected,
		progress,
		certificate,
		dashboard,
		recommendations,
		verification,
		verifying,
		loading,
		error,
		loadCatalogue,
		loadMe,
		open,
		refreshProgress,
		completeLesson,
		claimCertificate,
		verify,
		close
	};
}
