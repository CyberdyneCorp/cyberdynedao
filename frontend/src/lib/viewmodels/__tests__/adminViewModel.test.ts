import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import { createAdminViewModel, type AdminViewModelDeps } from '../adminViewModel';
import type { CourseDetail, CourseSummary } from '$lib/api/coursesApi';

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

const detail: CourseDetail = { ...draft, lessons: [] };

function fakeDeps(over: Partial<AdminViewModelDeps> = {}): AdminViewModelDeps {
	return {
		listCourses: vi.fn().mockResolvedValue([draft]),
		getCourse: vi.fn().mockResolvedValue(detail),
		createCourse: vi.fn().mockResolvedValue(detail),
		publishCourse: vi.fn().mockResolvedValue({ ...detail, status: 'published' }),
		unpublishCourse: vi.fn().mockResolvedValue(detail),
		deleteCourse: vi.fn().mockResolvedValue(undefined),
		addLesson: vi.fn().mockResolvedValue({
			id: 'l-1',
			courseId: 'c-1',
			title: 'Intro',
			lessonType: 'text',
			sortOrder: 0,
			contentUrl: null,
			textBody: 'hi',
			duration: null
		}),
		deleteLesson: vi.fn().mockResolvedValue(undefined),
		uploadFile: vi.fn().mockResolvedValue({
			id: 'u-1',
			url: 'https://cdn/x.mp4',
			originalFilename: 'x.mp4',
			contentType: 'video/mp4',
			sizeBytes: 10,
			category: 'video'
		}),
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

describe('adminViewModel — lesson editing', () => {
	it('openCourse loads the detail and closeCourse clears it', async () => {
		const vm = createAdminViewModel(fakeDeps());
		await vm.openCourse('solidity-101');
		expect(get(vm.selected)).toEqual(detail);
		vm.closeCourse();
		expect(get(vm.selected)).toBeNull();
	});

	it('addLesson posts then reloads the selected course', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.openCourse('solidity-101');
		const ok = await vm.addLesson({ title: 'Intro', lessonType: 'text', textBody: 'hi' });
		expect(ok).toBe(true);
		expect(deps.addLesson).toHaveBeenCalledWith('solidity-101', {
			title: 'Intro',
			lessonType: 'text',
			textBody: 'hi'
		});
		// getCourse called twice: once on open, once on reload after the mutation.
		expect((deps.getCourse as ReturnType<typeof vi.fn>).mock.calls.length).toBe(2);
	});

	it('addLesson without an open course is a no-op (false)', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		const ok = await vm.addLesson({ title: 'x', lessonType: 'text', textBody: 'y' });
		expect(ok).toBe(false);
		expect(deps.addLesson).not.toHaveBeenCalled();
	});

	it('removeLesson deletes then reloads the selected course', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.openCourse('solidity-101');
		await vm.removeLesson('l-1');
		expect(deps.deleteLesson).toHaveBeenCalledWith('solidity-101', 'l-1');
	});

	it('upload returns the result; null on failure', async () => {
		const vm = createAdminViewModel(fakeDeps());
		const file = new File(['x'], 'x.mp4', { type: 'video/mp4' });
		const res = await vm.upload(file);
		expect(res?.url).toBe('https://cdn/x.mp4');

		const failing = createAdminViewModel(
			fakeDeps({ uploadFile: vi.fn().mockRejectedValue(new Error('too big')) })
		);
		expect(await failing.upload(file)).toBeNull();
		expect(get(failing.error)).toBe('too big');
	});
});

describe('adminViewModel — defaults', () => {
	it('constructs with the real api deps', () => {
		const vm = createAdminViewModel();
		expect(get(vm.courses)).toEqual([]);
	});
});
