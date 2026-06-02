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
import type { CourseDetail, CourseLevel, CourseSummary } from './coursesApi';

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
	method: 'POST' | 'PATCH',
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
