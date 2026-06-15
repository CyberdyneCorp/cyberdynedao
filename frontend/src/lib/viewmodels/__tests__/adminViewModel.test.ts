import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import {
	createAdminViewModel,
	reorderedMap,
	shouldAutoLoad,
	type AdminViewModelDeps
} from '../adminViewModel';
import { AdminApiError } from '$lib/api/adminApi';
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
	daysRemaining: null,
	category: null
};

const detail: CourseDetail = { ...draft, lessons: [] };

function fakeDeps(over: Partial<AdminViewModelDeps> = {}): AdminViewModelDeps {
	return {
		listCourses: vi.fn().mockResolvedValue([draft]),
		getCourse: vi.fn().mockResolvedValue(detail),
		createCourse: vi.fn().mockResolvedValue(detail),
		updateCourse: vi.fn().mockResolvedValue(detail),
		setCourseDeadline: vi.fn().mockResolvedValue(detail),
		publishCourse: vi.fn().mockResolvedValue({ ...detail, status: 'published' }),
		unpublishCourse: vi.fn().mockResolvedValue(detail),
		deleteCourse: vi.fn().mockResolvedValue(undefined),
		reorderCourses: vi.fn().mockResolvedValue([draft]),
		updateLesson: vi.fn().mockResolvedValue({
			id: 'l-1',
			courseId: 'c-1',
			title: 'Intro (edited)',
			lessonType: 'text',
			sortOrder: 0,
			contentUrl: null,
			textBody: 'hi',
			duration: null
		}),
		reorderLessons: vi.fn().mockResolvedValue(detail),
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
		getQuiz: vi.fn().mockResolvedValue({ id: 'q-1', lessonId: 'l-1', passingScore: 70, questions: [] }),
		upsertQuiz: vi
			.fn()
			.mockResolvedValue({ id: 'q-1', lessonId: 'l-1', passingScore: 70, questions: [] }),
		deleteQuiz: vi.fn().mockResolvedValue(undefined),
		listCategories: vi.fn().mockResolvedValue([]),
		createCategory: vi.fn().mockResolvedValue({
			id: 'cat-1',
			slug: 'robotics',
			name: 'Robotics',
			icon: '🤖',
			sortOrder: 0,
			parentId: null
		}),
		updateCategory: vi.fn().mockResolvedValue({
			id: 'cat-1',
			slug: 'robotics',
			name: 'Robotics',
			icon: '🤖',
			sortOrder: 0,
			parentId: null
		}),
		deleteCategory: vi.fn().mockResolvedValue(undefined),
		setCourseCategory: vi.fn().mockResolvedValue(detail),
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

	it('an empty course list is a valid result (no error, not loading)', async () => {
		const vm = createAdminViewModel(fakeDeps({ listCourses: vi.fn().mockResolvedValue([]) }));
		await vm.load();
		expect(get(vm.courses)).toEqual([]);
		expect(get(vm.loading)).toBe(false);
		expect(get(vm.error)).toBeNull();
	});

	it('loads categories alongside courses', async () => {
		const cats = [
			{ id: 'cat-1', slug: 'robotics', name: 'Robotics', icon: '🤖', sortOrder: 0, parentId: null }
		];
		const vm = createAdminViewModel(
			fakeDeps({ listCategories: vi.fn().mockResolvedValue(cats) })
		);
		await vm.load();
		expect(get(vm.categories)).toEqual(cats);
	});

	it('a category load failure does not blank the catalogue', async () => {
		const vm = createAdminViewModel(
			fakeDeps({ listCategories: vi.fn().mockRejectedValue(new Error('nope')) })
		);
		await vm.load();
		expect(get(vm.courses)).toEqual([draft]); // courses still load
		expect(get(vm.categories)).toEqual([]);
	});
});

describe('adminViewModel — categories', () => {
	it('makeCategory creates then reloads', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		const ok = await vm.makeCategory({ name: 'Robotics' });
		expect(ok).toBe(true);
		expect(deps.createCategory).toHaveBeenCalledWith({ name: 'Robotics' });
		expect(deps.listCourses).toHaveBeenCalled(); // reloaded after mutation
	});

	it('editCategory updates (rename / reparent) then reloads', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.editCategory('cat-1', { name: 'Robots', parentId: 'grp-1' });
		expect(deps.updateCategory).toHaveBeenCalledWith('cat-1', { name: 'Robots', parentId: 'grp-1' });
		expect(deps.listCourses).toHaveBeenCalled();
	});

	it('removeCategory deletes then reloads', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.removeCategory('cat-1');
		expect(deps.deleteCategory).toHaveBeenCalledWith('cat-1');
		expect(deps.listCourses).toHaveBeenCalled();
	});

	it('assignCategory assigns (and clears with null) then reloads', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.assignCategory('solidity-101', 'cat-1');
		expect(deps.setCourseCategory).toHaveBeenCalledWith('solidity-101', 'cat-1');
		await vm.assignCategory('solidity-101', null);
		expect(deps.setCourseCategory).toHaveBeenCalledWith('solidity-101', null);
	});
});

describe('shouldAutoLoad — the initial-load guard', () => {
	// Regression: the admin view auto-loaded whenever the course list was
	// empty, so an empty (but successful) result re-triggered the load
	// forever and the UI was stuck on "Loading…". The guard must fire at
	// most once and must NOT depend on how many courses came back.
	it('loads once when editable and not yet attempted', () => {
		expect(shouldAutoLoad(true, false, false)).toBe(true);
	});

	it('does not load again after the first attempt — even with zero courses', () => {
		expect(shouldAutoLoad(true, true, false)).toBe(false);
	});

	it('does not load while a load is in flight', () => {
		expect(shouldAutoLoad(true, false, true)).toBe(false);
	});

	it('does not load when the user cannot edit', () => {
		expect(shouldAutoLoad(false, false, false)).toBe(false);
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

	it('sets a success notice on create and clears it on the next mutation', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.create({ title: 'X', level: 'Beginner' });
		expect(get(vm.notice)).toBe('Draft created');
		await vm.publish('solidity-101');
		expect(get(vm.notice)).toBe('Course published');
		vm.clearNotice();
		expect(get(vm.notice)).toBeNull();
	});

	it('does not set a notice when the mutation fails', async () => {
		const deps = fakeDeps({ createCourse: vi.fn().mockRejectedValue(new Error('boom')) });
		const vm = createAdminViewModel(deps);
		await vm.create({ title: 'X', level: 'Beginner' });
		expect(get(vm.notice)).toBeNull();
	});
});

describe('adminViewModel — edit course & deadline', () => {
	it('editCourse updates, refreshes the open course, and reloads the list', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.openCourse('solidity-101');
		const ok = await vm.editCourse('solidity-101', { title: 'New title', mandatory: true });
		expect(ok).toBe(true);
		expect(deps.updateCourse).toHaveBeenCalledWith('solidity-101', {
			title: 'New title',
			mandatory: true
		});
		expect(deps.getCourse).toHaveBeenCalled(); // open course refreshed
		expect(deps.listCourses).toHaveBeenCalled(); // catalogue reloaded
	});

	it('setDeadline forwards the ISO string and null to clear', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		await vm.openCourse('solidity-101');
		await vm.setDeadline('solidity-101', '2099-01-01T00:00:00.000Z');
		expect(deps.setCourseDeadline).toHaveBeenCalledWith('solidity-101', '2099-01-01T00:00:00.000Z');
		await vm.setDeadline('solidity-101', null);
		expect(deps.setCourseDeadline).toHaveBeenCalledWith('solidity-101', null);
	});

	it('editCourse without an open course is a no-op', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		const ok = await vm.editCourse('solidity-101', { title: 'x' });
		expect(ok).toBe(false);
		expect(deps.updateCourse).not.toHaveBeenCalled();
	});
});

describe('adminViewModel — edit lesson & reorder', () => {
	const draftB: CourseSummary = { ...draft, id: 'c-2', slug: 'rust-101', title: 'Rust 101' };
	const twoLessons: CourseDetail = {
		...detail,
		lessons: [
			{ ...detail.lessons[0], id: 'l-1', title: 'One', sortOrder: 0 } as never,
			{
				id: 'l-2',
				courseId: 'c-1',
				title: 'Two',
				lessonType: 'text',
				sortOrder: 1,
				contentUrl: null,
				textBody: 'two',
				duration: null
			} as never
		]
	};

	it('editLesson updates the lesson within the open course', async () => {
		const deps = fakeDeps({ getCourse: vi.fn().mockResolvedValue(twoLessons) });
		const vm = createAdminViewModel(deps);
		await vm.openCourse('solidity-101');
		const ok = await vm.editLesson('l-1', { title: 'One (edited)' });
		expect(ok).toBe(true);
		expect(deps.updateLesson).toHaveBeenCalledWith('solidity-101', 'l-1', { title: 'One (edited)' });
	});

	it('moveCourse down sends a re-densified order map', async () => {
		const deps = fakeDeps({ listCourses: vi.fn().mockResolvedValue([draft, draftB]) });
		const vm = createAdminViewModel(deps);
		await vm.load();
		await vm.moveCourse('solidity-101', 'down');
		expect(deps.reorderCourses).toHaveBeenCalledWith({ 'rust-101': 0, 'solidity-101': 1 });
	});

	it('moveCourse up at the top is a no-op', async () => {
		const deps = fakeDeps({ listCourses: vi.fn().mockResolvedValue([draft, draftB]) });
		const vm = createAdminViewModel(deps);
		await vm.load();
		const ok = await vm.moveCourse('solidity-101', 'up');
		expect(ok).toBe(false);
		expect(deps.reorderCourses).not.toHaveBeenCalled();
	});

	it('moveLesson down reorders within the open course', async () => {
		const deps = fakeDeps({ getCourse: vi.fn().mockResolvedValue(twoLessons) });
		const vm = createAdminViewModel(deps);
		await vm.openCourse('solidity-101');
		await vm.moveLesson('l-1', 'down');
		expect(deps.reorderLessons).toHaveBeenCalledWith('solidity-101', { 'l-2': 0, 'l-1': 1 });
	});
});

describe('reorderedMap', () => {
	it('swaps down and re-densifies', () => {
		expect(reorderedMap(['a', 'b', 'c'], 0, 'down')).toEqual({ b: 0, a: 1, c: 2 });
	});
	it('swaps up and re-densifies', () => {
		expect(reorderedMap(['a', 'b', 'c'], 2, 'up')).toEqual({ a: 0, c: 1, b: 2 });
	});
	it('returns null at the boundaries', () => {
		expect(reorderedMap(['a', 'b'], 0, 'up')).toBeNull();
		expect(reorderedMap(['a', 'b'], 1, 'down')).toBeNull();
		expect(reorderedMap(['a', 'b'], -1, 'down')).toBeNull();
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

describe('adminViewModel — quiz authoring', () => {
	it('loadQuiz returns the editor quiz', async () => {
		const vm = createAdminViewModel(fakeDeps());
		const quiz = await vm.loadQuiz('l-1');
		expect(quiz?.id).toBe('q-1');
	});

	it('loadQuiz returns null (not an error) on 404', async () => {
		const vm = createAdminViewModel(
			fakeDeps({ getQuiz: vi.fn().mockRejectedValue(new AdminApiError(404, 'quiz not found')) })
		);
		expect(await vm.loadQuiz('l-1')).toBeNull();
		expect(get(vm.error)).toBeNull();
	});

	it('loadQuiz surfaces non-404 errors', async () => {
		const vm = createAdminViewModel(
			fakeDeps({ getQuiz: vi.fn().mockRejectedValue(new AdminApiError(500, 'boom')) })
		);
		expect(await vm.loadQuiz('l-1')).toBeNull();
		expect(get(vm.error)).toBe('boom');
	});

	it('saveQuiz returns true and forwards the input', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		const input = {
			passingScore: 80,
			questions: [{ prompt: '2+2?', options: [{ text: '4', isCorrect: true }] }]
		};
		expect(await vm.saveQuiz('l-1', input)).toBe(true);
		expect(deps.upsertQuiz).toHaveBeenCalledWith('l-1', input);
	});

	it('saveQuiz returns false + records error on failure', async () => {
		const vm = createAdminViewModel(
			fakeDeps({ upsertQuiz: vi.fn().mockRejectedValue(new Error('exactly one correct')) })
		);
		expect(await vm.saveQuiz('l-1', { questions: [] })).toBe(false);
		expect(get(vm.error)).toBe('exactly one correct');
	});

	it('removeQuiz deletes', async () => {
		const deps = fakeDeps();
		const vm = createAdminViewModel(deps);
		expect(await vm.removeQuiz('l-1')).toBe(true);
		expect(deps.deleteQuiz).toHaveBeenCalledWith('l-1');
	});
});

describe('adminViewModel — defaults', () => {
	it('constructs with the real api deps', () => {
		const vm = createAdminViewModel();
		expect(get(vm.courses)).toEqual([]);
	});
});
