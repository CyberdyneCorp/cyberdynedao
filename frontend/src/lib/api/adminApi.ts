/**
 * Admin authoring client (editor scope).
 *
 * Talks to the backend's `/api/v1/admin/courses/*` authoring endpoints —
 * course CRUD + publish/reorder. All calls require the `editor` scope;
 * the bearer is injected via `withAuth()`, and the UI gates entry on
 * `authVM.isEditor` (a 401/403 here still surfaces as a `AdminApiError`).
 *
 * Reuses the camelCase course types from `coursesApi` so the catalogue
 * and the editor speak the same shapes.
 */

import { withAuth } from '$lib/auth/authToken';
import type {
	Category,
	CourseDetail,
	CourseLesson,
	CourseLevel,
	CourseSummary,
	LessonType
} from './coursesApi';

const API_BASE = (import.meta.env.VITE_BACKEND_API_URL ?? '').replace(/\/+$/, '');

export interface CreateCourseInput {
	title: string;
	description?: string;
	level: CourseLevel;
	slug?: string;
	mandatory?: boolean;
	sortOrder?: number;
}

export interface UpdateCourseInput {
	title?: string;
	description?: string;
	mandatory?: boolean;
	sortOrder?: number;
}

export interface AddLessonInput {
	title: string;
	lessonType: LessonType;
	contentUrl?: string;
	textBody?: string;
	duration?: string;
	sortOrder?: number;
}

// Lesson type is fixed at creation; everything else is editable.
export interface UpdateLessonInput {
	title?: string;
	contentUrl?: string;
	textBody?: string;
	duration?: string;
	sortOrder?: number;
}

export interface UploadResult {
	id: string;
	url: string;
	originalFilename: string;
	contentType: string;
	sizeBytes: number;
	category: string;
}

// ── Quiz authoring (editor view: full tree incl. correct flags) ───────

export interface EditorQuizOption {
	id: string;
	text: string;
	isCorrect: boolean;
}

export interface EditorQuizQuestion {
	id: string;
	prompt: string;
	explanation: string;
	options: EditorQuizOption[];
}

export interface EditorQuiz {
	id: string;
	lessonId: string;
	passingScore: number;
	questions: EditorQuizQuestion[];
}

export interface UpsertQuizInput {
	passingScore?: number;
	questions: {
		prompt: string;
		explanation?: string;
		options: { text: string; isCorrect: boolean }[];
	}[];
}

export class AdminApiError extends Error {
	constructor(
		public readonly status: number,
		message: string
	) {
		super(message);
		this.name = 'AdminApiError';
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

function ensureBase(): void {
	if (!API_BASE) throw new AdminApiError(0, 'VITE_BACKEND_API_URL is not configured');
}

async function sendJson<T>(
	method: 'POST' | 'PATCH' | 'PUT',
	path: string,
	body: unknown
): Promise<T> {
	ensureBase();
	const res = await fetch(`${API_BASE}${path}`, {
		method,
		headers: withAuth({ 'content-type': 'application/json', accept: 'application/json' }),
		body: JSON.stringify(body)
	});
	if (!res.ok) throw new AdminApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function getJson<T>(path: string): Promise<T> {
	ensureBase();
	const res = await fetch(`${API_BASE}${path}`, {
		method: 'GET',
		headers: withAuth({ accept: 'application/json' })
	});
	if (!res.ok) throw new AdminApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function del(path: string): Promise<void> {
	ensureBase();
	const res = await fetch(`${API_BASE}${path}`, {
		method: 'DELETE',
		headers: withAuth({ accept: 'application/json' })
	});
	if (!res.ok) throw new AdminApiError(res.status, await readError(res));
}

const enc = encodeURIComponent;

export function createCourse(input: CreateCourseInput): Promise<CourseDetail> {
	return sendJson<CourseDetail>('POST', '/api/v1/admin/courses', input);
}

export function updateCourse(slug: string, input: UpdateCourseInput): Promise<CourseDetail> {
	return sendJson<CourseDetail>('PATCH', `/api/v1/admin/courses/${enc(slug)}`, input);
}

/** Set or clear a course deadline. `dueAt` is an ISO-8601 string, or
 * `null` to clear it. */
export function setCourseDeadline(slug: string, dueAt: string | null): Promise<CourseDetail> {
	return sendJson<CourseDetail>('PUT', `/api/v1/admin/courses/${enc(slug)}/deadline`, { dueAt });
}

export function publishCourse(slug: string): Promise<CourseDetail> {
	return sendJson<CourseDetail>('POST', `/api/v1/admin/courses/${enc(slug)}/publish`, {});
}

export function unpublishCourse(slug: string): Promise<CourseDetail> {
	return sendJson<CourseDetail>('POST', `/api/v1/admin/courses/${enc(slug)}/unpublish`, {});
}

export function deleteCourse(slug: string): Promise<void> {
	return del(`/api/v1/admin/courses/${enc(slug)}`);
}

export function reorderCourses(order: Record<string, number>): Promise<CourseSummary[]> {
	return sendJson<CourseSummary[]>('POST', '/api/v1/admin/courses/reorder', { order });
}

// ── Categories ────────────────────────────────────────────────────────

export interface CreateCategoryInput {
	name: string;
	slug?: string;
	icon?: string;
	sortOrder?: number;
	/** Optional parent group (must be a top-level category). */
	parentId?: string | null;
}

export interface UpdateCategoryInput {
	name?: string;
	icon?: string;
	sortOrder?: number;
	/** Include (even as null) to reparent; null = top-level. */
	parentId?: string | null;
}

export function createCategory(input: CreateCategoryInput): Promise<Category> {
	return sendJson<Category>('POST', '/api/v1/admin/categories', input);
}

export function updateCategory(categoryId: string, input: UpdateCategoryInput): Promise<Category> {
	return sendJson<Category>('PATCH', `/api/v1/admin/categories/${enc(categoryId)}`, input);
}

export function deleteCategory(categoryId: string): Promise<void> {
	return del(`/api/v1/admin/categories/${enc(categoryId)}`);
}

/** Assign (or clear, with `categoryId: null`) a course's category. */
export function setCourseCategory(
	slug: string,
	categoryId: string | null
): Promise<CourseDetail> {
	return sendJson<CourseDetail>('PUT', `/api/v1/admin/courses/${enc(slug)}/category`, {
		categoryId
	});
}

// ── Translations ──────────────────────────────────────────────────────

export interface CourseLanguages {
	/** Languages the course is available in (always includes "en"). */
	available: string[];
	/** Every language the platform supports. */
	supported: string[];
	/** Whether a translation can be triggered now (OpenAI configured). */
	canTranslate: boolean;
}

export interface CourseTranslationStarted {
	slug: string;
	language: string;
	status: string;
}

/** Which languages a course currently has content for. */
export function fetchCourseLanguages(slug: string): Promise<CourseLanguages> {
	return getJson<CourseLanguages>(`/api/v1/admin/courses/${enc(slug)}/translations`);
}

/**
 * Kick off a background translation of the course into `language`. Resolves
 * once the job is accepted (202) — the language appears in
 * `fetchCourseLanguages().available` once it finishes, so callers poll.
 */
export function translateCourse(slug: string, language: string): Promise<CourseTranslationStarted> {
	return sendJson<CourseTranslationStarted>(
		'POST',
		`/api/v1/admin/courses/${enc(slug)}/translations/${enc(language)}`,
		{}
	);
}

// ── Lessons ───────────────────────────────────────────────────────────

export function addLesson(slug: string, input: AddLessonInput): Promise<CourseLesson> {
	return sendJson<CourseLesson>('POST', `/api/v1/admin/courses/${enc(slug)}/lessons`, input);
}

export function updateLesson(
	slug: string,
	lessonId: string,
	input: UpdateLessonInput
): Promise<CourseLesson> {
	return sendJson<CourseLesson>(
		'PATCH',
		`/api/v1/admin/courses/${enc(slug)}/lessons/${enc(lessonId)}`,
		input
	);
}

export function deleteLesson(slug: string, lessonId: string): Promise<void> {
	return del(`/api/v1/admin/courses/${enc(slug)}/lessons/${enc(lessonId)}`);
}

export function reorderLessons(
	slug: string,
	order: Record<string, number>
): Promise<CourseDetail> {
	return sendJson<CourseDetail>(
		'POST',
		`/api/v1/admin/courses/${enc(slug)}/lessons/reorder`,
		{ order }
	);
}

// ── Uploads (multipart) ───────────────────────────────────────────────

/** Upload a single file → its stored metadata incl. the `url` to use as
 * a lesson's `contentUrl`. Content-type is left unset so the browser
 * adds the multipart boundary. */
export async function uploadFile(file: File): Promise<UploadResult> {
	ensureBase();
	const form = new FormData();
	form.append('file', file);
	const res = await fetch(`${API_BASE}/api/v1/admin/uploads`, {
		method: 'POST',
		headers: withAuth({ accept: 'application/json' }),
		body: form
	});
	if (!res.ok) throw new AdminApiError(res.status, await readError(res));
	return (await res.json()) as UploadResult;
}

// ── Quiz authoring ────────────────────────────────────────────────────

/** Load a lesson's quiz (editor view). Throws `AdminApiError` 404 when
 * the lesson has no quiz yet — callers treat that as "author a new one". */
export function getQuiz(lessonId: string): Promise<EditorQuiz> {
	ensureBase();
	return fetch(`${API_BASE}/api/v1/admin/lessons/${enc(lessonId)}/quiz`, {
		method: 'GET',
		headers: withAuth({ accept: 'application/json' })
	}).then(async (res) => {
		if (!res.ok) throw new AdminApiError(res.status, await readError(res));
		return (await res.json()) as EditorQuiz;
	});
}

export function upsertQuiz(lessonId: string, input: UpsertQuizInput): Promise<EditorQuiz> {
	return sendJson<EditorQuiz>('PUT', `/api/v1/admin/lessons/${enc(lessonId)}/quiz`, input);
}

export function deleteQuiz(lessonId: string): Promise<void> {
	return del(`/api/v1/admin/lessons/${enc(lessonId)}/quiz`);
}

// ── Analytics (admin overview) ────────────────────────────────────────

export interface AdminOverview {
	totalLearners: number;
	totalEnrollments: number;
	completedEnrollments: number;
	enrollmentCompletionRate: number;
	publishedCourses: number;
	draftCourses: number;
	totalModules: number;
	totalPaths: number;
	totalCertificates: number;
	totalQuizAttempts: number;
	quizPassRate: number;
	avgQuizScore: number;
}

export function fetchAdminOverview(): Promise<AdminOverview> {
	return getJson<AdminOverview>('/api/v1/admin/analytics/overview');
}

// ── Learning paths & modules ──────────────────────────────────────────
//
// Standalone learning content (separate from the course catalogue):
// reusable modules, grouped into ordered learning paths. camelCase JSON;
// all routes require the `editor` scope, same as the course endpoints.

export interface LearningModule {
	slug: string;
	title: string;
	category: string;
	description: string;
	level: CourseLevel;
	duration: string;
	icon: string;
	topics: string[];
}

export interface LearningPath {
	slug: string;
	title: string;
	description: string;
	moduleSlugs: string[];
	estimatedTime: string;
	icon: string;
}

export interface CreateModuleInput {
	slug?: string;
	title: string;
	category: string;
	description: string;
	level: CourseLevel;
	duration: string;
	icon: string;
	topics: string[];
}

export interface UpdateModuleInput {
	title?: string;
	category?: string;
	description?: string;
	level?: CourseLevel;
	duration?: string;
	icon?: string;
	topics?: string[];
}

export interface CreatePathInput {
	slug?: string;
	title: string;
	description: string;
	moduleSlugs: string[];
	estimatedTime: string;
	icon: string;
}

export interface UpdatePathInput {
	title?: string;
	description?: string;
	moduleSlugs?: string[];
	estimatedTime?: string;
	icon?: string;
}

export function listLearningModules(): Promise<LearningModule[]> {
	return getJson<LearningModule[]>('/api/v1/admin/learning/modules');
}

export function createLearningModule(input: CreateModuleInput): Promise<LearningModule> {
	return sendJson<LearningModule>('POST', '/api/v1/admin/learning/modules', input);
}

export function updateLearningModule(
	slug: string,
	input: UpdateModuleInput
): Promise<LearningModule> {
	return sendJson<LearningModule>('PATCH', `/api/v1/admin/learning/modules/${enc(slug)}`, input);
}

export function deleteLearningModule(slug: string): Promise<void> {
	return del(`/api/v1/admin/learning/modules/${enc(slug)}`);
}

export function listLearningPaths(): Promise<LearningPath[]> {
	return getJson<LearningPath[]>('/api/v1/admin/learning/paths');
}

export function createLearningPath(input: CreatePathInput): Promise<LearningPath> {
	return sendJson<LearningPath>('POST', '/api/v1/admin/learning/paths', input);
}

export function updateLearningPath(slug: string, input: UpdatePathInput): Promise<LearningPath> {
	return sendJson<LearningPath>('PATCH', `/api/v1/admin/learning/paths/${enc(slug)}`, input);
}

export function deleteLearningPath(slug: string): Promise<void> {
	return del(`/api/v1/admin/learning/paths/${enc(slug)}`);
}

export function reorderPathModules(slug: string, moduleSlugs: string[]): Promise<LearningPath> {
	return sendJson<LearningPath>(
		'POST',
		`/api/v1/admin/learning/paths/${enc(slug)}/modules/reorder`,
		{ moduleSlugs }
	);
}
