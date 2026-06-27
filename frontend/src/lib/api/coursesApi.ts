/**
 * Cyberdyne Academy courses client.
 *
 * Talks to the backend's course-centric `/api/v1/courses/*`,
 * `/api/v1/lessons/*`, `/api/v1/recommendations/*`, and
 * `/api/v1/analytics/*` endpoints — the richer surface that sits beside
 * the older `/api/v1/learning/*` modules/paths catalogue in
 * `contentApi.ts`.
 *
 * Public reads (catalogue, certificate verify) are unauthenticated;
 * everything that acts on "me" (progress, certificate claim, quiz
 * attempts, recommendations, dashboard) auto-injects the bearer via
 * `withAuth()`. Backend responses are camelCase (pydantic
 * `alias_generator=to_camel`), so the types below match 1:1.
 */

import { withAuth } from '$lib/auth/authToken';
import { withLocale } from '$lib/api/localeHeader';

const API_BASE = (import.meta.env.VITE_BACKEND_API_URL ?? '').replace(/\/+$/, '');

// ── Types ─────────────────────────────────────────────────────────────

export type CourseLevel = 'Beginner' | 'Intermediate' | 'Advanced';
export type CourseStatus = 'draft' | 'published';
export type LessonType = 'video' | 'pdf' | 'presentation' | 'text' | 'quiz' | 'code';
export type DeadlineStatus = 'none' | 'upcoming' | 'urgent' | 'overdue';

export interface CourseLesson {
	id: string;
	courseId: string;
	title: string;
	lessonType: LessonType;
	sortOrder: number;
	contentUrl: string | null;
	textBody: string | null;
	duration: string | null;
}

export interface Category {
	id: string;
	slug: string;
	name: string;
	icon: string;
	sortOrder: number;
	/** Parent group id, or null for a top-level group. */
	parentId: string | null;
}

export interface CourseSummary {
	id: string;
	slug: string;
	title: string;
	description: string;
	level: CourseLevel;
	status: CourseStatus;
	mandatory: boolean;
	sortOrder: number;
	lessonCount: number;
	createdAt: string;
	publishedAt: string | null;
	dueAt: string | null;
	deadlineStatus: DeadlineStatus;
	daysRemaining: number | null;
	/** Assigned category, or null when uncategorized. */
	category: Category | null;
}

export interface CourseDetail extends CourseSummary {
	lessons: CourseLesson[];
}

export interface LessonProgressView {
	lessonId: string;
	title: string;
	percent: number;
	completed: boolean;
}

export interface CourseProgress {
	courseId: string;
	slug: string;
	totalLessons: number;
	completedLessons: number;
	percent: number;
	completed: boolean;
	lessons: LessonProgressView[];
}

/** Compact per-course progress for the catalogue (only started courses). */
export interface MyCourseProgress {
	slug: string;
	totalLessons: number;
	completedLessons: number;
	percent: number;
	completed: boolean;
}

export interface CourseCertificate {
	id: string;
	userId: string;
	courseSlug: string;
	issuedAt: string;
	verificationHash: string;
}

export interface CourseCertificateVerification {
	valid: boolean;
	certificate: CourseCertificate | null;
}

export interface CourseRecommendation {
	slug: string;
	title: string;
	level: CourseLevel;
	reason: string;
}

export interface LearningRecommendations {
	summary: string;
	courses: CourseRecommendation[];
}

export interface LearnerDashboard {
	enrolledPaths: number;
	completedPaths: number;
	activePaths: number;
	completedModules: number;
	inProgressModules: number;
	avgModulePercent: number;
	quizzesAttempted: number;
	quizzesPassed: number;
	quizPassRate: number;
	avgQuizScore: number;
	totalQuizAttempts: number;
	certificates: number;
	completedCourses: number;
	inProgressCourses: number;
}

// Quiz player (answers stripped until an attempt is graded).
export interface PlayerQuizOption {
	id: string;
	text: string;
}

export interface PlayerQuizQuestion {
	id: string;
	prompt: string;
	options: PlayerQuizOption[];
}

export interface PlayerQuiz {
	lessonId: string;
	passingScore: number;
	questions: PlayerQuizQuestion[];
}

export interface QuizQuestionResult {
	questionId: string;
	selectedOptionId: string | null;
	correctOptionId: string;
	isCorrect: boolean;
	explanation: string;
}

export interface QuizAttemptResult {
	attemptId: string;
	score: number;
	passed: boolean;
	attemptNumber: number;
	submittedAt: string;
	results: QuizQuestionResult[];
}

export interface QuizAnswerFeedback {
	questionId: string;
	prompt: string;
	isCorrect: boolean;
	selectedOptionId: string | null;
	correctOptionId: string;
	staticExplanation: string;
	aiExplanation: string | null;
}

/** Map of `questionId -> optionId` for a quiz submission. */
export type QuizAnswers = Record<string, string>;

// Code-interpreter (code lessons run on the MATLAB engine).
export interface RunCodeResult {
	ok: boolean;
	stdout: string;
	stderr: string;
	artifacts: string[];
	sessionId: string;
	timedOut: boolean;
}

// ── Client ────────────────────────────────────────────────────────────

export class CoursesApiError extends Error {
	constructor(
		public readonly status: number,
		message: string
	) {
		super(message);
		this.name = 'CoursesApiError';
	}
}

async function readError(res: Response): Promise<string> {
	try {
		const body = (await res.json()) as { detail?: unknown };
		if (typeof body.detail === 'string') return body.detail;
		return `HTTP ${res.status}`;
	} catch {
		return `HTTP ${res.status}`;
	}
}

async function getJson<T>(path: string): Promise<T> {
	if (!API_BASE) throw new CoursesApiError(0, 'VITE_BACKEND_API_URL is not configured');
	const res = await fetch(`${API_BASE}${path}`, {
		method: 'GET',
		headers: withLocale(withAuth({ accept: 'application/json' }))
	});
	if (!res.ok) throw new CoursesApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function sendJson<T>(method: 'POST' | 'PUT', path: string, body: unknown): Promise<T> {
	if (!API_BASE) throw new CoursesApiError(0, 'VITE_BACKEND_API_URL is not configured');
	const res = await fetch(`${API_BASE}${path}`, {
		method,
		headers: withLocale(withAuth({ 'content-type': 'application/json', accept: 'application/json' })),
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new CoursesApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

const enc = encodeURIComponent;

// ── Catalogue (public) ────────────────────────────────────────────────

export interface CoursePageParams {
	limit?: number;
	offset?: number;
}

export function fetchCourses(
	level?: CourseLevel,
	page: CoursePageParams = {}
): Promise<CourseSummary[]> {
	const q = new URLSearchParams();
	if (level) q.set('level', level);
	if (page.limit !== undefined) q.set('limit', String(page.limit));
	if (page.offset !== undefined) q.set('offset', String(page.offset));
	const qs = q.toString();
	return getJson<CourseSummary[]>(`/api/v1/courses${qs ? `?${qs}` : ''}`);
}

export function fetchCourse(slug: string): Promise<CourseDetail> {
	return getJson<CourseDetail>(`/api/v1/courses/${enc(slug)}`);
}

export function fetchCategories(): Promise<Category[]> {
	return getJson<Category[]>('/api/v1/categories');
}

// ── Progress (me) ─────────────────────────────────────────────────────

export function fetchMyCourseProgress(slug: string): Promise<CourseProgress> {
	return getJson<CourseProgress>(`/api/v1/courses/${enc(slug)}/progress`);
}

/** The signed-in learner's progress across every started course (one call). */
export function fetchMyCoursesProgress(): Promise<MyCourseProgress[]> {
	return getJson<MyCourseProgress[]>('/api/v1/courses/me/progress');
}

export function setLessonProgress(
	slug: string,
	lessonId: string,
	percent: number
): Promise<CourseProgress> {
	return sendJson<CourseProgress>(
		'PUT',
		`/api/v1/courses/${enc(slug)}/lessons/${enc(lessonId)}/progress`,
		{ percent }
	);
}

// ── Certificates ──────────────────────────────────────────────────────

export function claimCourseCertificate(slug: string): Promise<CourseCertificate> {
	return sendJson<CourseCertificate>('POST', `/api/v1/courses/${enc(slug)}/certificate`, {});
}

export function fetchMyCourseCertificate(slug: string): Promise<CourseCertificate> {
	return getJson<CourseCertificate>(`/api/v1/courses/${enc(slug)}/certificate`);
}

export function verifyCourseCertificate(
	certificateId: string
): Promise<CourseCertificateVerification> {
	return getJson<CourseCertificateVerification>(
		`/api/v1/courses/certificates/${enc(certificateId)}/verify`
	);
}

/** Public PDF download URL (the id is the bearer, like verify). */
export function courseCertificatePdfUrl(certificateId: string): string {
	return `${API_BASE}/api/v1/courses/certificates/${enc(certificateId)}/pdf`;
}

// ── Recommendations + dashboard (me) ──────────────────────────────────

export function fetchRecommendations(): Promise<LearningRecommendations> {
	return getJson<LearningRecommendations>('/api/v1/recommendations/me');
}

export function fetchLearnerDashboard(): Promise<LearnerDashboard> {
	return getJson<LearnerDashboard>('/api/v1/analytics/me');
}

// ── Quiz player (me) ──────────────────────────────────────────────────

export function fetchLessonQuiz(lessonId: string): Promise<PlayerQuiz> {
	return getJson<PlayerQuiz>(`/api/v1/lessons/${enc(lessonId)}/quiz`);
}

export function submitQuizAttempt(
	lessonId: string,
	answers: QuizAnswers
): Promise<QuizAttemptResult> {
	return sendJson<QuizAttemptResult>('POST', `/api/v1/lessons/${enc(lessonId)}/quiz/attempts`, {
		answers
	});
}

export function fetchQuizFeedback(
	lessonId: string,
	answers: QuizAnswers
): Promise<QuizAnswerFeedback[]> {
	return sendJson<QuizAnswerFeedback[]>('POST', `/api/v1/lessons/${enc(lessonId)}/quiz/feedback`, {
		answers
	});
}

// ── Quiz catalogue / browse (me) ──────────────────────────────────────

export interface QuizLastAttempt {
	score: number;
	passed: boolean;
	attemptNumber: number;
	submittedAt: string;
}

export interface QuizCatalogItem {
	quizId: string;
	lessonId: string;
	lessonTitle: string;
	courseSlug: string;
	courseTitle: string;
	categorySlug: string | null;
	passingScore: number;
	questionCount: number;
	/** The learner's most-recent attempt, or null if never taken. */
	lastAttempt: QuizLastAttempt | null;
}

export interface QuizCatalogPage {
	items: QuizCatalogItem[];
	nextCursor: string | null;
}

export interface QuizCatalogParams {
	/** true → only the learner's attempted quizzes, most-recent first. */
	attempted?: boolean;
	courseSlug?: string;
	domain?: string;
	cursor?: string;
	limit?: number;
}

export function fetchQuizCatalogue(params: QuizCatalogParams = {}): Promise<QuizCatalogPage> {
	const q = new URLSearchParams();
	if (params.attempted !== undefined) q.set('attempted', String(params.attempted));
	if (params.courseSlug) q.set('courseSlug', params.courseSlug);
	if (params.domain) q.set('domain', params.domain);
	if (params.cursor) q.set('cursor', params.cursor);
	if (params.limit !== undefined) q.set('limit', String(params.limit));
	const qs = q.toString();
	return getJson<QuizCatalogPage>(`/api/v1/quizzes${qs ? `?${qs}` : ''}`);
}

// ── Code lessons (me) ─────────────────────────────────────────────────

export type CodeLanguage = 'matlab' | 'python';

export function runLessonCode(
	lessonId: string,
	source: string,
	language: CodeLanguage = 'matlab'
): Promise<RunCodeResult> {
	return sendJson<RunCodeResult>('POST', `/api/v1/lessons/${enc(lessonId)}/code/run`, {
		source,
		language
	});
}

/** Infer a code lesson's language from its course (no per-lesson language
 *  field yet): only explicitly-MATLAB courses run on the MATLAB engine;
 *  everything else (Python, Blockchain toys, …) runs Python. */
export function courseCodeLanguage(slugOrTitle: string): CodeLanguage {
	return /matlab/i.test(slugOrTitle) ? 'matlab' : 'python';
}
