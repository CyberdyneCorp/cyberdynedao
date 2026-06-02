import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
	AdminApiError,
	createCourse,
	deleteCourse,
	publishCourse,
	reorderCourses,
	unpublishCourse,
	updateCourse
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
