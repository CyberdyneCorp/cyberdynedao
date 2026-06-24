import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';
import {
	createLearningAdminViewModel,
	reorderedSlugs,
	type AdminLearningViewModelDeps
} from '../learningAdminViewModel';
import { AdminApiError, type LearningModule, type LearningPath } from '$lib/api/adminApi';

const moduleA: LearningModule = {
	slug: 'm1',
	title: 'Module 1',
	category: 'Robotics',
	description: 'd',
	level: 'Beginner',
	duration: '2h',
	icon: '🤖',
	topics: ['intro']
};
const moduleB: LearningModule = { ...moduleA, slug: 'm2', title: 'Module 2' };
const moduleC: LearningModule = { ...moduleA, slug: 'm3', title: 'Module 3' };

const path: LearningPath = {
	slug: 'p1',
	title: 'Path 1',
	description: 'd',
	moduleSlugs: ['m1', 'm2', 'm3'],
	estimatedTime: '6h',
	icon: '🛤️'
};

function fakeDeps(over: Partial<AdminLearningViewModelDeps> = {}): AdminLearningViewModelDeps {
	return {
		listModules: vi.fn().mockResolvedValue([moduleA, moduleB, moduleC]),
		createModule: vi.fn().mockResolvedValue(moduleA),
		updateModule: vi.fn().mockResolvedValue(moduleA),
		deleteModule: vi.fn().mockResolvedValue(undefined),
		listPaths: vi.fn().mockResolvedValue([path]),
		createPath: vi.fn().mockResolvedValue(path),
		updatePath: vi.fn().mockResolvedValue(path),
		deletePath: vi.fn().mockResolvedValue(undefined),
		reorderPathModules: vi.fn().mockResolvedValue(path),
		...over
	};
}

beforeEach(() => vi.restoreAllMocks());

describe('learningAdminViewModel — load', () => {
	it('populates modules and paths and clears loading', async () => {
		const vm = createLearningAdminViewModel(fakeDeps());
		await vm.load();
		expect(get(vm.modules)).toEqual([moduleA, moduleB, moduleC]);
		expect(get(vm.paths)).toEqual([path]);
		expect(get(vm.loading)).toBe(false);
		expect(get(vm.error)).toBeNull();
	});

	it('records load errors', async () => {
		const vm = createLearningAdminViewModel(
			fakeDeps({ listModules: vi.fn().mockRejectedValue(new Error('boom')) })
		);
		await vm.load();
		expect(get(vm.error)).toBe('boom');
		expect(get(vm.loading)).toBe(false);
	});

	it('empty lists are a valid result', async () => {
		const vm = createLearningAdminViewModel(
			fakeDeps({
				listModules: vi.fn().mockResolvedValue([]),
				listPaths: vi.fn().mockResolvedValue([])
			})
		);
		await vm.load();
		expect(get(vm.modules)).toEqual([]);
		expect(get(vm.paths)).toEqual([]);
		expect(get(vm.error)).toBeNull();
	});
});

describe('learningAdminViewModel — modules', () => {
	it('createModule calls the dep and reloads, returning true', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		const input = {
			title: 'Module 1',
			category: 'Robotics',
			description: 'd',
			level: 'Beginner' as const,
			duration: '2h',
			icon: '🤖',
			topics: ['intro']
		};
		const ok = await vm.createModule(input);
		expect(ok).toBe(true);
		expect(deps.createModule).toHaveBeenCalledWith(input);
		expect(deps.listModules).toHaveBeenCalled(); // reloaded after mutation
		expect(get(vm.notice)).toBe('Module created');
		expect(get(vm.busy)).toBe(false);
	});

	it('a rejected createModule sets the error store and returns false', async () => {
		const deps = fakeDeps({
			createModule: vi.fn().mockRejectedValue(new AdminApiError(409, 'slug already exists'))
		});
		const vm = createLearningAdminViewModel(deps);
		const ok = await vm.createModule({
			title: 'Dup',
			category: 'Robotics',
			description: 'd',
			level: 'Beginner',
			duration: '2h',
			icon: '🤖',
			topics: []
		});
		expect(ok).toBe(false);
		expect(get(vm.error)).toBe('slug already exists');
		expect(get(vm.notice)).toBeNull();
		expect(deps.listModules).not.toHaveBeenCalled(); // no reload on failure
	});

	it('editModule forwards the subset and reloads', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		await vm.editModule('m1', { title: 'Renamed', topics: ['a', 'b'] });
		expect(deps.updateModule).toHaveBeenCalledWith('m1', { title: 'Renamed', topics: ['a', 'b'] });
		expect(deps.listModules).toHaveBeenCalled();
	});

	it('removeModule deletes then reloads', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		const ok = await vm.removeModule('m1');
		expect(ok).toBe(true);
		expect(deps.deleteModule).toHaveBeenCalledWith('m1');
		expect(deps.listModules).toHaveBeenCalled();
	});
});

describe('learningAdminViewModel — paths', () => {
	it('createPath calls the dep and reloads', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		const input = {
			title: 'Path 1',
			description: 'd',
			moduleSlugs: ['m1', 'm2'],
			estimatedTime: '6h',
			icon: '🛤️'
		};
		const ok = await vm.createPath(input);
		expect(ok).toBe(true);
		expect(deps.createPath).toHaveBeenCalledWith(input);
		expect(deps.listPaths).toHaveBeenCalled();
	});

	it('a rejected createPath sets the error store and returns false', async () => {
		const deps = fakeDeps({
			createPath: vi.fn().mockRejectedValue(new AdminApiError(422, 'unknown module slug'))
		});
		const vm = createLearningAdminViewModel(deps);
		const ok = await vm.createPath({
			title: 'Bad',
			description: 'd',
			moduleSlugs: ['nope'],
			estimatedTime: '1h',
			icon: '🛤️'
		});
		expect(ok).toBe(false);
		expect(get(vm.error)).toBe('unknown module slug');
	});

	it('editPath forwards the subset and reloads', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		await vm.editPath('p1', { title: 'Renamed path' });
		expect(deps.updatePath).toHaveBeenCalledWith('p1', { title: 'Renamed path' });
		expect(deps.listPaths).toHaveBeenCalled();
	});

	it('removePath deletes then reloads', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		const ok = await vm.removePath('p1');
		expect(ok).toBe(true);
		expect(deps.deletePath).toHaveBeenCalledWith('p1');
		expect(deps.listPaths).toHaveBeenCalled();
	});
});

describe('learningAdminViewModel — movePathModule', () => {
	it('moving m2 up in [m1,m2,m3] sends [m2,m1,m3]', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		await vm.load();
		const ok = await vm.movePathModule('p1', 'm2', 'up');
		expect(ok).toBe(true);
		expect(deps.reorderPathModules).toHaveBeenCalledWith('p1', ['m2', 'm1', 'm3']);
	});

	it('moving m2 down in [m1,m2,m3] sends [m1,m3,m2]', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		await vm.load();
		await vm.movePathModule('p1', 'm2', 'down');
		expect(deps.reorderPathModules).toHaveBeenCalledWith('p1', ['m1', 'm3', 'm2']);
	});

	it('moving the first module up is a no-op (false)', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		await vm.load();
		const ok = await vm.movePathModule('p1', 'm1', 'up');
		expect(ok).toBe(false);
		expect(deps.reorderPathModules).not.toHaveBeenCalled();
	});

	it('an unknown path is a no-op (false)', async () => {
		const deps = fakeDeps();
		const vm = createLearningAdminViewModel(deps);
		await vm.load();
		const ok = await vm.movePathModule('nope', 'm1', 'down');
		expect(ok).toBe(false);
		expect(deps.reorderPathModules).not.toHaveBeenCalled();
	});
});

describe('reorderedSlugs', () => {
	it('moves up', () => {
		expect(reorderedSlugs(['m1', 'm2', 'm3'], 'm2', 'up')).toEqual(['m2', 'm1', 'm3']);
	});
	it('moves down', () => {
		expect(reorderedSlugs(['m1', 'm2', 'm3'], 'm2', 'down')).toEqual(['m1', 'm3', 'm2']);
	});
	it('returns null at the boundaries', () => {
		expect(reorderedSlugs(['m1', 'm2'], 'm1', 'up')).toBeNull();
		expect(reorderedSlugs(['m1', 'm2'], 'm2', 'down')).toBeNull();
	});
	it('returns null for an absent slug', () => {
		expect(reorderedSlugs(['m1', 'm2'], 'x', 'up')).toBeNull();
	});
});

describe('learningAdminViewModel — defaults', () => {
	it('constructs with the real api deps', () => {
		const vm = createLearningAdminViewModel();
		expect(get(vm.modules)).toEqual([]);
		expect(get(vm.paths)).toEqual([]);
	});
});
