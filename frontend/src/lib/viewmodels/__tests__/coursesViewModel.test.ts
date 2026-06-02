import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import { createCoursesViewModel, type CoursesViewModelDeps } from '../coursesViewModel';
import type { CourseDetail, CourseProgress, CourseSummary } from '$lib/api/coursesApi';

const summary: CourseSummary = {
	id: 'c-1',
	slug: 'solidity-101',
	title: 'Solidity 101',
	description: 'd',
	level: 'Beginner',
	status: 'published',
	mandatory: false,
	sortOrder: 0,
	lessonCount: 2,
	createdAt: '2026-01-01T00:00:00Z',
	publishedAt: '2026-01-01T00:00:00Z',
	dueAt: null,
	deadlineStatus: 'none',
	daysRemaining: null
};

const detail: CourseDetail = {
	...summary,
	lessons: [
		{
			id: 'l-1',
			courseId: 'c-1',
			title: 'Intro',
			lessonType: 'text',
			sortOrder: 0,
			contentUrl: null,
			textBody: 'hi',
			duration: null
		}
	]
};

const progress: CourseProgress = {
	courseId: 'c-1',
	slug: 'solidity-101',
	totalLessons: 2,
	completedLessons: 1,
	percent: 50,
	completed: false,
	lessons: [{ lessonId: 'l-1', title: 'Intro', percent: 100, completed: true }]
};

function fakeDeps(over: Partial<CoursesViewModelDeps> = {}): CoursesViewModelDeps {
	return {
		fetchCourses: vi.fn().mockResolvedValue([summary]),
		fetchCourse: vi.fn().mockResolvedValue(detail),
		fetchMyCourseProgress: vi.fn().mockResolvedValue(progress),
		setLessonProgress: vi.fn().mockResolvedValue({ ...progress, completedLessons: 2, completed: true }),
		...over
	};
}

describe('coursesViewModel — loadCatalogue', () => {
	it('populates courses and toggles loading', async () => {
		const vm = createCoursesViewModel(fakeDeps());
		await vm.loadCatalogue();
		expect(get(vm.courses)).toEqual([summary]);
		expect(get(vm.loading)).toBe(false);
		expect(get(vm.error)).toBeNull();
	});

	it('passes the level filter through', async () => {
		const deps = fakeDeps();
		const vm = createCoursesViewModel(deps);
		await vm.loadCatalogue('Advanced');
		expect(deps.fetchCourses).toHaveBeenCalledWith('Advanced');
	});

	it('captures the error message and clears loading', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ fetchCourses: vi.fn().mockRejectedValue(new Error('boom')) })
		);
		await vm.loadCatalogue();
		expect(get(vm.error)).toBe('boom');
		expect(get(vm.loading)).toBe(false);
		expect(get(vm.courses)).toEqual([]);
	});

	it('stringifies non-Error throwables', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ fetchCourses: vi.fn().mockRejectedValue('plain') })
		);
		await vm.loadCatalogue();
		expect(get(vm.error)).toBe('plain');
	});
});

describe('coursesViewModel — open', () => {
	it('loads detail without progress by default', async () => {
		const deps = fakeDeps();
		const vm = createCoursesViewModel(deps);
		await vm.open('solidity-101');
		expect(get(vm.selected)).toEqual(detail);
		expect(get(vm.progress)).toBeNull();
		expect(deps.fetchMyCourseProgress).not.toHaveBeenCalled();
	});

	it('loads progress when withProgress is set', async () => {
		const vm = createCoursesViewModel(fakeDeps());
		await vm.open('solidity-101', { withProgress: true });
		expect(get(vm.selected)).toEqual(detail);
		expect(get(vm.progress)).toEqual(progress);
	});

	it('records errors from detail load', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ fetchCourse: vi.fn().mockRejectedValue(new Error('404')) })
		);
		await vm.open('ghost');
		expect(get(vm.error)).toBe('404');
		expect(get(vm.selected)).toBeNull();
	});
});

describe('coursesViewModel — progress actions', () => {
	it('refreshProgress sets the progress store', async () => {
		const vm = createCoursesViewModel(fakeDeps());
		await vm.refreshProgress('solidity-101');
		expect(get(vm.progress)).toEqual(progress);
	});

	it('refreshProgress records errors', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ fetchMyCourseProgress: vi.fn().mockRejectedValue(new Error('401')) })
		);
		await vm.refreshProgress('x');
		expect(get(vm.error)).toBe('401');
	});

	it('completeLesson marks the lesson and updates progress', async () => {
		const deps = fakeDeps();
		const vm = createCoursesViewModel(deps);
		await vm.completeLesson('solidity-101', 'l-1');
		expect(deps.setLessonProgress).toHaveBeenCalledWith('solidity-101', 'l-1', 100);
		expect(get(vm.progress)?.completed).toBe(true);
	});

	it('completeLesson records errors', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ setLessonProgress: vi.fn().mockRejectedValue(new Error('nope')) })
		);
		await vm.completeLesson('x', 'l-1');
		expect(get(vm.error)).toBe('nope');
	});
});

describe('coursesViewModel — close', () => {
	it('clears selected, progress and error', async () => {
		const vm = createCoursesViewModel(fakeDeps());
		await vm.open('solidity-101', { withProgress: true });
		vm.close();
		expect(get(vm.selected)).toBeNull();
		expect(get(vm.progress)).toBeNull();
		expect(get(vm.error)).toBeNull();
	});
});

describe('coursesViewModel — defaults', () => {
	it('constructs with the real api deps', () => {
		const vm = createCoursesViewModel();
		expect(get(vm.courses)).toEqual([]);
		expect(get(vm.loading)).toBe(false);
	});
});

beforeEach(() => {
	vi.restoreAllMocks();
});
