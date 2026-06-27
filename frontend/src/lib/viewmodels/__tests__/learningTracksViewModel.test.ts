import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import {
	createLearningTracksViewModel,
	type LearningTracksViewModelDeps
} from '../learningTracksViewModel';
import type {
	Eligibility,
	Enrollment,
	EnrollmentDeadline,
	LearningModule,
	LearningPath,
	ModuleGate,
	MyLearningState
} from '$lib/api/learningApi';

const paths: LearningPath[] = [
	{
		slug: 'foundations',
		title: 'Foundations',
		description: 'Start here',
		moduleSlugs: ['m1', 'm2'],
		estimatedTime: '6h',
		icon: '🧭'
	}
];

const modules: LearningModule[] = [
	{
		slug: 'm1',
		title: 'Module One',
		category: 'core',
		description: 'first',
		level: 'Beginner',
		duration: '2h',
		icon: '📦',
		topics: ['intro'],
		courseSlugs: ['c1'],
		courses: [{ slug: 'c1', title: 'Course One', level: 'Beginner' }]
	},
	{
		slug: 'm2',
		title: 'Module Two',
		category: 'core',
		description: 'second',
		level: 'Intermediate',
		duration: '4h',
		icon: '📦',
		topics: [],
		courseSlugs: [],
		courses: []
	}
];

const myState: MyLearningState = {
	enrollments: [
		{
			id: 'e1',
			userId: 'u1',
			pathSlug: 'foundations',
			startedAt: '2026-01-01T00:00:00Z',
			status: 'active',
			dueAt: null
		} satisfies Enrollment
	],
	progress: [{ moduleSlug: 'm1', percent: 100, startedAt: '2026-01-01T00:00:00Z', completedAt: '2026-01-02T00:00:00Z' }],
	certificates: []
};

const deadlines: EnrollmentDeadline[] = [
	{ pathSlug: 'foundations', dueAt: null, status: 'upcoming', daysRemaining: 5 }
];

const gating: ModuleGate[] = [
	{ moduleSlug: 'm1', level: 'Beginner', position: 0, unlocked: true, completed: true, blockedBy: null, reason: null },
	{ moduleSlug: 'm2', level: 'Intermediate', position: 1, unlocked: false, completed: false, blockedBy: 'm1', reason: 'sequential' }
];

const eligibility: Eligibility = {
	eligible: true,
	alreadyEnrolled: true,
	nextModule: 'm2',
	reason: null
};

function fakeDeps(over: Partial<LearningTracksViewModelDeps> = {}): LearningTracksViewModelDeps {
	return {
		fetchPaths: vi.fn().mockResolvedValue(paths),
		fetchModules: vi.fn().mockResolvedValue(modules),
		fetchMyState: vi.fn().mockResolvedValue(myState),
		fetchDeadlines: vi.fn().mockResolvedValue(deadlines),
		fetchGating: vi.fn().mockResolvedValue(gating),
		checkEligibility: vi.fn().mockResolvedValue(eligibility),
		enroll: vi.fn().mockResolvedValue(myState.enrollments[0]),
		updateProgress: vi
			.fn()
			.mockResolvedValue({ moduleSlug: 'm2', percent: 100, startedAt: 'x', completedAt: 'y' }),
		...over
	};
}

beforeEach(() => vi.restoreAllMocks());

describe('learningTracksViewModel', () => {
	it('load (anonymous) fetches catalogue only, not me-state', async () => {
		const deps = fakeDeps();
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: false });
		expect(get(vm.paths)).toEqual(paths);
		expect(get(vm.modules)).toEqual(modules);
		expect(deps.fetchMyState).not.toHaveBeenCalled();
		expect(get(vm.loading)).toBe(false);
	});

	it('load (authed) also fetches enrollments + deadlines', async () => {
		const deps = fakeDeps();
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: true });
		expect(deps.fetchMyState).toHaveBeenCalledOnce();
		expect(get(vm.myState).enrollments).toHaveLength(1);
		expect(get(vm.deadlines)).toEqual(deadlines);
	});

	it('load surfaces an error when the catalogue fetch fails', async () => {
		const deps = fakeDeps({ fetchPaths: vi.fn().mockRejectedValue(new Error('boom')) });
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: false });
		expect(get(vm.error)).toBe('boom');
	});

	it('me-state failure is best-effort (no error, empty panels)', async () => {
		const deps = fakeDeps({ fetchMyState: vi.fn().mockRejectedValue(new Error('401')) });
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: true });
		expect(get(vm.error)).toBeNull();
		expect(get(vm.myState).enrollments).toHaveLength(0);
	});

	it('openPath selects the path and loads gating + eligibility when authed', async () => {
		const deps = fakeDeps();
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: true });
		await vm.openPath('foundations', { authed: true });
		expect(get(vm.selected)?.slug).toBe('foundations');
		expect(get(vm.gating)).toEqual(gating);
		expect(get(vm.eligibility)).toEqual(eligibility);
	});

	it('openPath when anonymous selects but skips gating', async () => {
		const deps = fakeDeps();
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: false });
		await vm.openPath('foundations', { authed: false });
		expect(get(vm.selected)?.slug).toBe('foundations');
		expect(deps.fetchGating).not.toHaveBeenCalled();
		expect(get(vm.gating)).toEqual([]);
	});

	it('enrollInPath enrolls then refreshes me-state + gating', async () => {
		const deps = fakeDeps();
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: true });
		await vm.openPath('foundations', { authed: true });
		await vm.enrollInPath('foundations');
		expect(deps.enroll).toHaveBeenCalledWith('foundations');
		expect(deps.fetchMyState).toHaveBeenCalledTimes(2); // load + after enroll
		expect(get(vm.enrolling)).toBe(false);
	});

	it('markModuleComplete posts 100% then refreshes', async () => {
		const deps = fakeDeps();
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: true });
		await vm.markModuleComplete('m2', 'foundations');
		expect(deps.updateProgress).toHaveBeenCalledWith('m2', 100);
		expect(deps.fetchGating).toHaveBeenCalledWith('foundations');
	});

	it('close clears the selection + gating', async () => {
		const deps = fakeDeps();
		const vm = createLearningTracksViewModel(deps);
		await vm.load({ authed: true });
		await vm.openPath('foundations', { authed: true });
		vm.close();
		expect(get(vm.selected)).toBeNull();
		expect(get(vm.gating)).toEqual([]);
	});
});
