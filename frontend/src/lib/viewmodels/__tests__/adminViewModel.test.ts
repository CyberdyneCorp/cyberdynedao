import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import { createAdminViewModel, type AdminViewModelDeps } from '../adminViewModel';
import type { CourseSummary } from '$lib/api/coursesApi';

const draft: CourseSummary = {
	id: 'c-1',
	slug: 'solidity-101',
	title: 'Solidity 101',
	description: 'd',
	level: 'Beginner',
	status: 'draft',
	mandatory: false,
	sortOrder: 0,
	lessonCount: 0,
	createdAt: '2026-01-01T00:00:00Z',
	publishedAt: null,
	dueAt: null,
	deadlineStatus: 'none',
	daysRemaining: null
};

function fakeDeps(over: Partial<AdminViewModelDeps> = {}): AdminViewModelDeps {
	return {
		listCourses: vi.fn().mockResolvedValue([draft]),
		createCourse: vi.fn().mockResolvedValue({ ...draft, lessons: [] }),
		publishCourse: vi.fn().mockResolvedValue({ ...draft, status: 'published', lessons: [] }),
		unpublishCourse: vi.fn().mockResolvedValue({ ...draft, lessons: [] }),
		deleteCourse: vi.fn().mockResolvedValue(undefined),
		...over
	};
}

beforeEach(() => vi.restoreAllMocks());

describe('adminViewModel — load', () => {
	it('lists courses (drafts included) and clears loading', async () => {
		const vm = createAdminViewModel(fakeDeps());
		await vm.load();
		expect(get(vm.courses)).toEqual([draft]);
		expect(get(vm.loading)).toBe(false);
		expect(get(vm.error)).toBeNull();
	});

	it('records load errors', async () => {
		const vm = createAdminViewModel(
			fakeDeps({ listCourses: vi.fn().mockRejectedValue(new Error('boom')) })
		);
		await vm.load();
		expect(get(vm.error)).toBe('boom');
		expect(get(vm.loading)).toBe(false);
	});
});

describe('adminViewModel — create', () => {
	it('creates then reloads, returning true', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		const ok = await vm.create({ title: 'Solidity 101', level: 'Beginner' });
		expect(ok).toBe(true);
		expect(deps.createCourse).toHaveBeenCalledWith({ title: 'Solidity 101', level: 'Beginner' });
		expect(deps.listCourses).toHaveBeenCalled(); // reloaded
		expect(get(vm.busy)).toBe(false);
	});

	it('returns false and records error on failure', async () => {
		const deps = fakeDeps({
			createCourse: vi.fn().mockRejectedValue(new Error('slug already exists'))
		});
		const vm = createAdminViewModel(deps);
		const ok = await vm.create({ title: 'Dup', level: 'Beginner' });
		expect(ok).toBe(false);
		expect(get(vm.error)).toBe('slug already exists');
		expect(deps.listCourses).not.toHaveBeenCalled(); // no reload on failure
	});
});

describe('adminViewModel — publish/unpublish/remove', () => {
	it('publish calls the api then reloads', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.publish('solidity-101');
		expect(deps.publishCourse).toHaveBeenCalledWith('solidity-101');
		expect(deps.listCourses).toHaveBeenCalled();
	});

	it('unpublish calls the api', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.unpublish('solidity-101');
		expect(deps.unpublishCourse).toHaveBeenCalledWith('solidity-101');
	});

	it('remove deletes then reloads', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.remove('solidity-101');
		expect(deps.deleteCourse).toHaveBeenCalledWith('solidity-101');
		expect(deps.listCourses).toHaveBeenCalled();
	});

	it('records errors from a mutation', async () => {
		const vm = createAdminViewModel(
			fakeDeps({ publishCourse: vi.fn().mockRejectedValue(new Error('nope')) })
		);
		await vm.publish('x');
		expect(get(vm.error)).toBe('nope');
	});
});

describe('adminViewModel — defaults', () => {
	it('constructs with the real api deps', () => {
		const vm = createAdminViewModel();
		expect(get(vm.courses)).toEqual([]);
	});
});
