import { describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import { createAdminAnalyticsViewModel } from '../adminAnalyticsViewModel';
import type { AdminOverview } from '$lib/api/adminApi';

const overview: AdminOverview = {
	totalLearners: 12,
	totalEnrollments: 30,
	completedEnrollments: 9,
	enrollmentCompletionRate: 0.3,
	publishedCourses: 4,
	draftCourses: 2,
	totalModules: 18,
	totalPaths: 3,
	totalCertificates: 7,
	totalQuizAttempts: 40,
	quizPassRate: 0.75,
	avgQuizScore: 82.5
};

describe('adminAnalyticsViewModel', () => {
	it('loads the overview and clears loading', async () => {
		const vm = createAdminAnalyticsViewModel({ fetchOverview: vi.fn().mockResolvedValue(overview) });
		await vm.load();
		expect(get(vm.overview)).toEqual(overview);
		expect(get(vm.loading)).toBe(false);
		expect(get(vm.error)).toBeNull();
	});

	it('records an error and leaves overview null', async () => {
		const vm = createAdminAnalyticsViewModel({
			fetchOverview: vi.fn().mockRejectedValue(new Error('forbidden'))
		});
		await vm.load();
		expect(get(vm.overview)).toBeNull();
		expect(get(vm.error)).toBe('forbidden');
		expect(get(vm.loading)).toBe(false);
	});
});
