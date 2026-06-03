import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import { createCoursesViewModel, type CoursesViewModelDeps } from '../coursesViewModel';
import { CoursesApiError } from '$lib/api/coursesApi';
import type {
	CourseCertificate,
	CourseDetail,
	CourseProgress,
	CourseSummary
} from '$lib/api/coursesApi';

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

const certificate: CourseCertificate = {
	id: 'cert-1',
	userId: 'u-1',
	courseSlug: 'solidity-101',
	issuedAt: '2026-01-02T00:00:00Z',
	verificationHash: 'abc'
};

function fakeDeps(over: Partial<CoursesViewModelDeps> = {}): CoursesViewModelDeps {
	return {
		fetchCourses: vi.fn().mockResolvedValue([summary]),
		fetchCourse: vi.fn().mockResolvedValue(detail),
		fetchMyCourseProgress: vi.fn().mockResolvedValue(progress),
		setLessonProgress: vi.fn().mockResolvedValue({ ...progress, completedLessons: 2, completed: true }),
		fetchMyCertificate: vi.fn().mockRejectedValue(new CoursesApiError(404, 'certificate not found')),
		claimCertificate: vi.fn().mockResolvedValue(certificate),
		fetchDashboard: vi.fn().mockResolvedValue({
			enrolledPaths: 0,
			completedPaths: 0,
			activePaths: 0,
			completedModules: 0,
			inProgressModules: 0,
			avgModulePercent: 0,
			quizzesAttempted: 2,
			quizzesPassed: 1,
			quizPassRate: 50,
			avgQuizScore: 65,
			totalQuizAttempts: 3,
			certificates: 1,
			completedCourses: 1,
			inProgressCourses: 2
		}),
		fetchRecommendations: vi.fn().mockResolvedValue({
			summary: 'Try these next.',
			courses: [{ slug: 'advanced', title: 'Advanced', level: 'Advanced', reason: 'next step' }]
		}),
		verifyCertificate: vi.fn().mockResolvedValue({ valid: true, certificate }),
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

describe('coursesViewModel — certificate', () => {
	it('open loads an existing certificate when present', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ fetchMyCertificate: vi.fn().mockResolvedValue(certificate) })
		);
		await vm.open('solidity-101', { withProgress: true });
		expect(get(vm.certificate)).toEqual(certificate);
	});

	it('a 404 certificate is treated as "not earned", not an error', async () => {
		const vm = createCoursesViewModel(fakeDeps()); // default cert dep → 404
		await vm.open('solidity-101', { withProgress: true });
		expect(get(vm.certificate)).toBeNull();
		expect(get(vm.error)).toBeNull();
	});

	it('does not load a certificate when anonymous (no progress)', async () => {
		const deps = fakeDeps();
		const vm = createCoursesViewModel(deps);
		await vm.open('solidity-101');
		expect(deps.fetchMyCertificate).not.toHaveBeenCalled();
		expect(get(vm.certificate)).toBeNull();
	});

	it('claimCertificate sets the certificate', async () => {
		const deps = fakeDeps();
		const vm = createCoursesViewModel(deps);
		await vm.claimCertificate('solidity-101');
		expect(deps.claimCertificate).toHaveBeenCalledWith('solidity-101');
		expect(get(vm.certificate)).toEqual(certificate);
	});

	it('claimCertificate records errors (e.g. 409 not eligible)', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ claimCertificate: vi.fn().mockRejectedValue(new Error('not eligible')) })
		);
		await vm.claimCertificate('x');
		expect(get(vm.error)).toBe('not eligible');
	});

	it('completeLesson refreshes the certificate (auto-issued on completion)', async () => {
		const deps = fakeDeps({ fetchMyCertificate: vi.fn().mockResolvedValue(certificate) });
		const vm = createCoursesViewModel(deps);
		await vm.completeLesson('solidity-101', 'l-1');
		expect(deps.fetchMyCertificate).toHaveBeenCalledWith('solidity-101');
		expect(get(vm.certificate)).toEqual(certificate);
	});
});

describe('coursesViewModel — loadMe (dashboard + recommendations)', () => {
	it('loads both stores', async () => {
		const vm = createCoursesViewModel(fakeDeps());
		await vm.loadMe();
		expect(get(vm.dashboard)?.completedCourses).toBe(1);
		expect(get(vm.recommendations)?.courses[0].slug).toBe('advanced');
	});

	it('is best-effort — a failing dashboard leaves it null without throwing', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ fetchDashboard: vi.fn().mockRejectedValue(new Error('401')) })
		);
		await vm.loadMe();
		expect(get(vm.dashboard)).toBeNull();
		// recommendations still load independently
		expect(get(vm.recommendations)?.summary).toBe('Try these next.');
	});
});

describe('coursesViewModel — close', () => {
	it('clears selected, progress, certificate and error', async () => {
		const vm = createCoursesViewModel(fakeDeps());
		await vm.open('solidity-101', { withProgress: true });
		vm.close();
		expect(get(vm.selected)).toBeNull();
		expect(get(vm.progress)).toBeNull();
		expect(get(vm.certificate)).toBeNull();
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

describe('coursesViewModel — verify', () => {
	it('stores a valid verification result', async () => {
		const vm = createCoursesViewModel(fakeDeps());
		await vm.verify('cert-123');
		expect(get(vm.verification)).toEqual({ valid: true, certificate });
		expect(get(vm.verifying)).toBe(false);
	});

	it('treats a 404 as "not valid" rather than an error', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ verifyCertificate: vi.fn().mockRejectedValue(new CoursesApiError(404, 'nope')) })
		);
		await vm.verify('missing');
		expect(get(vm.verification)).toEqual({ valid: false, certificate: null });
		expect(get(vm.error)).toBeNull();
	});

	it('records a non-404 failure as an error', async () => {
		const vm = createCoursesViewModel(
			fakeDeps({ verifyCertificate: vi.fn().mockRejectedValue(new Error('boom')) })
		);
		await vm.verify('x');
		expect(get(vm.verification)).toBeNull();
		expect(get(vm.error)).toBe('boom');
	});
});

beforeEach(() => {
	vi.restoreAllMocks();
});
