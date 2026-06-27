/**
 * Learner-facing Learning Tracks client.
 *
 * Talks to the backend's `/api/v1/learning/*` learner surface — the
 * modules/paths catalogue plus the signed-in learner's enrollments,
 * per-module progress, prerequisite gating, eligibility, and deadlines.
 * (Admin CRUD over the same catalogue lives in `adminApi.ts`.)
 *
 * Public reads (catalogue) are unauthenticated; everything that acts on
 * "me" (state, enroll, progress, gating, eligibility, deadlines)
 * auto-injects the bearer via `withAuth()`. Responses are camelCase
 * (pydantic `alias_generator=to_camel`), so the types match 1:1.
 */

import { withAuth } from '$lib/auth/authToken';
import { withLocale } from '$lib/api/localeHeader';

const API_BASE = (import.meta.env.VITE_BACKEND_API_URL ?? '').replace(/\/+$/, '');

// ── Types ─────────────────────────────────────────────────────────────

export type LearningLevel = 'Beginner' | 'Intermediate' | 'Advanced';
export type EnrollmentStatus = 'active' | 'completed' | 'dropped';
export type DeadlineStatus = 'none' | 'upcoming' | 'urgent' | 'overdue';
export type GateReason = 'level' | 'sequential';

/** A course card a module bundles (resolved, locale-aware). */
export interface LinkedCourse {
	slug: string;
	title: string;
	level: string;
}

export interface LearningModule {
	slug: string;
	title: string;
	category: string;
	description: string;
	level: LearningLevel | string;
	duration: string;
	icon: string;
	topics: string[];
	courseSlugs: string[];
	courses: LinkedCourse[];
}

export interface LearningPath {
	slug: string;
	title: string;
	description: string;
	moduleSlugs: string[];
	estimatedTime: string;
	icon: string;
}

export interface Enrollment {
	id: string;
	userId: string;
	pathSlug: string;
	startedAt: string;
	status: EnrollmentStatus;
	dueAt: string | null;
}

export interface ModuleProgress {
	moduleSlug: string;
	percent: number;
	startedAt: string;
	completedAt: string | null;
}

export interface LearningCertificate {
	id: string;
	userId: string;
	pathSlug: string;
	issuedAt: string;
	verificationHash: string;
	signedPayload: string;
}

export interface MyLearningState {
	enrollments: Enrollment[];
	progress: ModuleProgress[];
	certificates: LearningCertificate[];
}

export interface EnrollmentDeadline {
	pathSlug: string;
	dueAt: string | null;
	status: DeadlineStatus;
	daysRemaining: number | null;
}

export interface ModuleGate {
	moduleSlug: string;
	level: string;
	position: number;
	unlocked: boolean;
	completed: boolean;
	blockedBy: string | null;
	reason: GateReason | null;
}

export interface Eligibility {
	eligible: boolean;
	alreadyEnrolled: boolean;
	nextModule: string | null;
	reason: string | null;
}

// ── Client ────────────────────────────────────────────────────────────

export class LearningApiError extends Error {
	constructor(
		public readonly status: number,
		message: string
	) {
		super(message);
		this.name = 'LearningApiError';
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
	if (!API_BASE) throw new LearningApiError(0, 'VITE_BACKEND_API_URL is not configured');
	const res = await fetch(`${API_BASE}${path}`, {
		method: 'GET',
		headers: withLocale(withAuth({ accept: 'application/json' }))
	});
	if (!res.ok) throw new LearningApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

async function sendJson<T>(
	method: 'POST' | 'PATCH',
	path: string,
	body?: unknown
): Promise<T> {
	if (!API_BASE) throw new LearningApiError(0, 'VITE_BACKEND_API_URL is not configured');
	const res = await fetch(`${API_BASE}${path}`, {
		method,
		headers: withLocale(
			withAuth({ 'content-type': 'application/json', accept: 'application/json' })
		),
		body: body === undefined ? undefined : JSON.stringify(body)
	});
	if (!res.ok) throw new LearningApiError(res.status, await readError(res));
	return (await res.json()) as T;
}

const enc = encodeURIComponent;

// ── Catalogue (public) ────────────────────────────────────────────────

export function fetchLearningPaths(): Promise<LearningPath[]> {
	return getJson<LearningPath[]>('/api/v1/learning/paths');
}

export function fetchLearningModules(): Promise<LearningModule[]> {
	return getJson<LearningModule[]>('/api/v1/learning/modules');
}

// ── Me (authenticated) ────────────────────────────────────────────────

export function fetchMyLearningState(): Promise<MyLearningState> {
	return getJson<MyLearningState>('/api/v1/learning/me');
}

export function fetchMyDeadlines(): Promise<EnrollmentDeadline[]> {
	return getJson<EnrollmentDeadline[]>('/api/v1/learning/deadlines');
}

export function enrollInPath(slug: string): Promise<Enrollment> {
	return sendJson<Enrollment>('POST', `/api/v1/learning/paths/${enc(slug)}/enroll`);
}

export function updateModuleProgress(slug: string, percent: number): Promise<ModuleProgress> {
	return sendJson<ModuleProgress>('PATCH', `/api/v1/learning/modules/${enc(slug)}/progress`, {
		percent
	});
}

export function fetchPathGating(slug: string): Promise<ModuleGate[]> {
	return getJson<ModuleGate[]>(`/api/v1/learning/paths/${enc(slug)}/gating`);
}

export function checkPathEligibility(slug: string): Promise<Eligibility> {
	return getJson<Eligibility>(`/api/v1/learning/paths/${enc(slug)}/eligibility`);
}
