import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
	AdminApiError,
	addLesson,
	createCourse,
	deleteCourse,
	deleteLesson,
	deleteQuiz,
	getQuiz,
	publishCourse,
	reorderCourses,
	unpublishCourse,
	updateCourse,
	uploadFile,
	upsertQuiz
} from '../adminApi';
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

describe('adminApi — course authoring', () => {
	it('createCourse POSTs the body with bearer', async () => {
		setAuthToken('ed');
		mockJsonOnce(201, { slug: 'solidity-101', lessons: [] });
		await createCourse({ title: 'Solidity 101', level: 'Beginner' });
		const [url, init] = lastCall();
		expect(init.method).toBe('POST');
		expect(String(url)).toMatch(/\/api\/v1\/admin\/courses$/);
		expect((init.headers as Headers).get('authorization')).toBe('Bearer ed');
		expect(JSON.parse(init.body as string)).toEqual({ title: 'Solidity 101', level: 'Beginner' });
	});

	it('updateCourse PATCHes the slug', async () => {
		mockJsonOnce(200, { slug: 'x', lessons: [] });
		await updateCourse('x', { title: 'New' });
		const [url, init] = lastCall();
		expect(init.method).toBe('PATCH');
		expect(String(url)).toMatch(/\/api\/v1\/admin\/courses\/x$/);
		expect(JSON.parse(init.body as string)).toEqual({ title: 'New' });
	});

	it('publishCourse / unpublishCourse hit the right routes', async () => {
		mockJsonOnce(200, { slug: 'x', status: 'published', lessons: [] });
		await publishCourse('x');
		expect(String(lastCall()[0])).toMatch(/\/api\/v1\/admin\/courses\/x\/publish$/);

		mockJsonOnce(200, { slug: 'x', status: 'draft', lessons: [] });
		await unpublishCourse('x');
		expect(String(lastCall()[0])).toMatch(/\/api\/v1\/admin\/courses\/x\/unpublish$/);
	});

	it('deleteCourse DELETEs and resolves void on 204', async () => {
		(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(new Response(null, { status: 204 }));
		await expect(deleteCourse('x')).resolves.toBeUndefined();
		expect(lastCall()[1].method).toBe('DELETE');
	});

	it('reorderCourses POSTs the order map', async () => {
		mockJsonOnce(200, []);
		await reorderCourses({ a: 0, b: 1 });
		const [url, init] = lastCall();
		expect(String(url)).toMatch(/\/api\/v1\/admin\/courses\/reorder$/);
		expect(JSON.parse(init.body as string)).toEqual({ order: { a: 0, b: 1 } });
	});

	it('throws AdminApiError with the detail field on non-2xx', async () => {
		mockJsonOnce(403, { detail: 'editor scope required' });
		await expect(createCourse({ title: 't', level: 'Beginner' })).rejects.toMatchObject({
			name: 'AdminApiError',
			status: 403,
			message: 'editor scope required'
		});
	});

	it('surfaces a 409 duplicate-slug error', async () => {
		mockJsonOnce(409, { detail: 'slug already exists: dup' });
		await expect(createCourse({ title: 'Dup', level: 'Beginner' })).rejects.toMatchObject({
			status: 409
		});
	});
});

describe('adminApi — lessons + uploads', () => {
	it('addLesson POSTs to the course lessons route', async () => {
		mockJsonOnce(201, { id: 'l-1', title: 'Intro', lessonType: 'text' });
		await addLesson('solidity-101', { title: 'Intro', lessonType: 'text', textBody: 'hi' });
		const [url, init] = lastCall();
		expect(init.method).toBe('POST');
		expect(String(url)).toMatch(/\/api\/v1\/admin\/courses\/solidity-101\/lessons$/);
		expect(JSON.parse(init.body as string)).toEqual({
			title: 'Intro',
			lessonType: 'text',
			textBody: 'hi'
		});
	});

	it('deleteLesson DELETEs the lesson', async () => {
		(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(new Response(null, { status: 204 }));
		await deleteLesson('solidity-101', 'l-1');
		const [url, init] = lastCall();
		expect(init.method).toBe('DELETE');
		expect(String(url)).toMatch(/\/courses\/solidity-101\/lessons\/l-1$/);
	});

	it('uploadFile POSTs multipart form-data with the bearer (no JSON content-type)', async () => {
		setAuthToken('ed');
		mockJsonOnce(201, { id: 'u-1', url: 'https://cdn/x.mp4', originalFilename: 'x.mp4' });
		const file = new File(['data'], 'x.mp4', { type: 'video/mp4' });
		const res = await uploadFile(file);
		expect(res.url).toBe('https://cdn/x.mp4');
		const [url, init] = lastCall();
		expect(String(url)).toMatch(/\/api\/v1\/admin\/uploads$/);
		expect(init.method).toBe('POST');
		expect(init.body).toBeInstanceOf(FormData);
		const headers = init.headers as Headers;
		expect(headers.get('authorization')).toBe('Bearer ed');
		// Must NOT pin JSON — the browser sets the multipart boundary.
		expect(headers.get('content-type')).toBeNull();
	});
});

describe('adminApi — quiz authoring', () => {
	it('getQuiz GETs the admin editor quiz route', async () => {
		mockJsonOnce(200, { id: 'q-1', lessonId: 'l-1', passingScore: 70, questions: [] });
		await getQuiz('l-1');
		const [url, init] = lastCall();
		expect(init.method).toBe('GET');
		expect(String(url)).toMatch(/\/api\/v1\/admin\/lessons\/l-1\/quiz$/);
	});

	it('getQuiz throws AdminApiError 404 when the lesson has no quiz', async () => {
		mockJsonOnce(404, { detail: 'quiz not found' });
		await expect(getQuiz('l-1')).rejects.toMatchObject({ name: 'AdminApiError', status: 404 });
	});

	it('upsertQuiz PUTs the questions body', async () => {
		mockJsonOnce(200, { id: 'q-1', lessonId: 'l-1', passingScore: 80, questions: [] });
		await upsertQuiz('l-1', {
			passingScore: 80,
			questions: [{ prompt: '2+2?', options: [{ text: '4', isCorrect: true }] }]
		});
		const [url, init] = lastCall();
		expect(init.method).toBe('PUT');
		expect(String(url)).toMatch(/\/api\/v1\/admin\/lessons\/l-1\/quiz$/);
		expect(JSON.parse(init.body as string)).toEqual({
			passingScore: 80,
			questions: [{ prompt: '2+2?', options: [{ text: '4', isCorrect: true }] }]
		});
	});

	it('deleteQuiz DELETEs the quiz', async () => {
		(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(new Response(null, { status: 204 }));
		await deleteQuiz('l-1');
		const [url, init] = lastCall();
		expect(init.method).toBe('DELETE');
		expect(String(url)).toMatch(/\/api\/v1\/admin\/lessons\/l-1\/quiz$/);
	});
});
