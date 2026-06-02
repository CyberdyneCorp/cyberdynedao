import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
	CoursesApiError,
	claimCourseCertificate,
	courseCertificatePdfUrl,
	fetchCourse,
	fetchCourses,
	fetchLearnerDashboard,
	fetchLessonQuiz,
	fetchMyCourseProgress,
	fetchQuizFeedback,
	fetchRecommendations,
	setLessonProgress,
	submitQuizAttempt,
	verifyCourseCertificate
} from '../coursesApi';
import { clearAuthToken, setAuthToken } from '$lib/auth/authToken';

type FetchMock = ReturnType<typeof vi.fn>;

function mockJsonOnce(status: number, body: unknown): void {
	(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(
		new Response(JSON.stringify(body), {
			status,
			headers: { 'content-type': 'application/json' }
		})
	);
}

function lastCall(): [string, RequestInit] {
	const calls = (globalThis.fetch as unknown as FetchMock).mock.calls;
	return calls[calls.length - 1] as [string, RequestInit];
}

beforeEach(() => {
	globalThis.fetch = vi.fn() as unknown as typeof fetch;
});

afterEach(() => {
	clearAuthToken();
	vi.restoreAllMocks();
});

describe('coursesApi — catalogue (public)', () => {
	it('fetchCourses GETs the catalogue', async () => {
		mockJsonOnce(200, []);
		await fetchCourses();
		const [url, init] = lastCall();
		expect(String(url)).toMatch(/\/api\/v1\/courses$/);
		expect(init.method).toBe('GET');
	});

	it('fetchCourses passes the level filter as a query param', async () => {
		mockJsonOnce(200, []);
		await fetchCourses('Beginner');
		expect(String(lastCall()[0])).toMatch(/\/api\/v1\/courses\?level=Beginner$/);
	});

	it('fetchCourse URL-encodes the slug', async () => {
		mockJsonOnce(200, { slug: 'a/b', lessons: [] });
		await fetchCourse('a/b');
		expect(String(lastCall()[0])).toMatch(/\/api\/v1\/courses\/a%2Fb$/);
	});
});

describe('coursesApi — progress (me)', () => {
	it('fetchMyCourseProgress attaches the bearer', async () => {
		setAuthToken('tok');
		mockJsonOnce(200, { slug: 'x', lessons: [] });
		await fetchMyCourseProgress('x');
		const [url, init] = lastCall();
		expect(String(url)).toMatch(/\/api\/v1\/courses\/x\/progress$/);
		expect((init.headers as Headers).get('authorization')).toBe('Bearer tok');
	});

	it('setLessonProgress PUTs the percent body', async () => {
		mockJsonOnce(200, { slug: 'x', lessons: [] });
		await setLessonProgress('x', 'lesson-1', 100);
		const [url, init] = lastCall();
		expect(init.method).toBe('PUT');
		expect(String(url)).toMatch(/\/api\/v1\/courses\/x\/lessons\/lesson-1\/progress$/);
		expect(JSON.parse(init.body as string)).toEqual({ percent: 100 });
	});
});

describe('coursesApi — certificates', () => {
	it('claimCourseCertificate POSTs an empty body', async () => {
		mockJsonOnce(201, { id: 'c-1', courseSlug: 'x' });
		const cert = await claimCourseCertificate('x');
		expect(cert.id).toBe('c-1');
		const [url, init] = lastCall();
		expect(init.method).toBe('POST');
		expect(String(url)).toMatch(/\/api\/v1\/courses\/x\/certificate$/);
		expect(JSON.parse(init.body as string)).toEqual({});
	});

	it('verifyCourseCertificate GETs the public verify route', async () => {
		mockJsonOnce(200, { valid: true, certificate: { id: 'c-1' } });
		const result = await verifyCourseCertificate('c-1');
		expect(result.valid).toBe(true);
		expect(String(lastCall()[0])).toMatch(/\/api\/v1\/courses\/certificates\/c-1\/verify$/);
	});

	it('courseCertificatePdfUrl builds the download URL', () => {
		expect(courseCertificatePdfUrl('c-1')).toMatch(
			/\/api\/v1\/courses\/certificates\/c-1\/pdf$/
		);
	});
});

describe('coursesApi — recommendations + dashboard', () => {
	it('fetchRecommendations GETs /recommendations/me', async () => {
		mockJsonOnce(200, { summary: 's', courses: [] });
		await fetchRecommendations();
		expect(String(lastCall()[0])).toMatch(/\/api\/v1\/recommendations\/me$/);
	});

	it('fetchLearnerDashboard GETs /analytics/me', async () => {
		mockJsonOnce(200, { completedCourses: 1, inProgressCourses: 2 });
		const d = await fetchLearnerDashboard();
		expect(d.completedCourses).toBe(1);
		expect(String(lastCall()[0])).toMatch(/\/api\/v1\/analytics\/me$/);
	});
});

describe('coursesApi — quiz player', () => {
	it('fetchLessonQuiz GETs the player view', async () => {
		mockJsonOnce(200, { lessonId: 'l-1', passingScore: 70, questions: [] });
		await fetchLessonQuiz('l-1');
		expect(String(lastCall()[0])).toMatch(/\/api\/v1\/lessons\/l-1\/quiz$/);
	});

	it('submitQuizAttempt POSTs the answers map', async () => {
		mockJsonOnce(201, { attemptId: 'a-1', score: 100, passed: true, results: [] });
		await submitQuizAttempt('l-1', { q1: 'o2' });
		const [url, init] = lastCall();
		expect(init.method).toBe('POST');
		expect(String(url)).toMatch(/\/api\/v1\/lessons\/l-1\/quiz\/attempts$/);
		expect(JSON.parse(init.body as string)).toEqual({ answers: { q1: 'o2' } });
	});

	it('fetchQuizFeedback POSTs to the feedback route', async () => {
		mockJsonOnce(200, []);
		await fetchQuizFeedback('l-1', { q1: 'o1' });
		const [url, init] = lastCall();
		expect(init.method).toBe('POST');
		expect(String(url)).toMatch(/\/api\/v1\/lessons\/l-1\/quiz\/feedback$/);
		expect(JSON.parse(init.body as string)).toEqual({ answers: { q1: 'o1' } });
	});
});

describe('coursesApi — errors', () => {
	it('throws CoursesApiError with the detail field on non-2xx', async () => {
		mockJsonOnce(409, { detail: 'not eligible' });
		await expect(claimCourseCertificate('x')).rejects.toMatchObject({
			name: 'CoursesApiError',
			status: 409,
			message: 'not eligible'
		});
	});

	it('falls back to HTTP <status> on non-JSON error bodies', async () => {
		(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(
			new Response('nope', { status: 503 })
		);
		await expect(fetchCourses()).rejects.toMatchObject({
			name: 'CoursesApiError',
			status: 503,
			message: 'HTTP 503'
		});
	});
});
