import { describe, it, expect } from 'vitest';
import { get } from 'svelte/store';
import {
	createLearnViewModel,
	getLevelColor,
	getLearnCategoryColor,
	resolvePathModules
} from '../learnViewModel';
import type { LearningModule, LearningPath } from '$lib/types/components';

const modules: LearningModule[] = [
	{ id: 'm1', title: 'Mod 1', category: 'Blockchain', description: 'd', level: 'Beginner', duration: '1h', icon: '🔗', topics: [] },
	{ id: 'm2', title: 'Mod 2', category: 'Security', description: 'd', level: 'Advanced', duration: '2h', icon: '🛡️', topics: [] }
];
const paths: LearningPath[] = [
	{ id: 'p1', title: 'Path', description: 'd', modules: ['m1', 'missing'], icon: '👨', estimatedTime: '4w' }
];

describe('learnViewModel helpers', () => {
	it('getLevelColor covers branches', () => {
		for (const l of ['Beginner', 'Intermediate', 'Advanced', 'X']) {
			expect(getLevelColor(l)).toContain('bg-');
		}
	});
	it('getLearnCategoryColor covers branches', () => {
		for (const c of ['Blockchain', 'Development', 'Governance', 'DeFi', 'Economics', 'Infrastructure', 'Security', 'Other']) {
			expect(getLearnCategoryColor(c)).toContain('bg-');
		}
	});
	it('resolvePathModules filters missing module ids', () => {
		const r = resolvePathModules(paths[0], modules);
		expect(r).toHaveLength(1);
		expect(r[0].id).toBe('m1');
	});
});

describe('learnViewModel factory', () => {
	it('initial state', () => {
		const vm = createLearnViewModel(modules, paths);
		expect(get(vm.selectedModule)).toBeNull();
		expect(get(vm.selectedPath)).toBeNull();
		expect(get(vm.activeTab)).toBe('modules');
	});
	it('selectModule clears path and vice versa', () => {
		const vm = createLearnViewModel(modules, paths);
		vm.selectPath(paths[0]);
		vm.selectModule(modules[0]);
		expect(get(vm.selectedModule)).toEqual(modules[0]);
		expect(get(vm.selectedPath)).toBeNull();

		vm.selectPath(paths[0]);
		expect(get(vm.selectedPath)).toEqual(paths[0]);
		expect(get(vm.selectedModule)).toBeNull();
	});
	it('setTab changes active tab', () => {
		const vm = createLearnViewModel(modules, paths);
		vm.setTab('resources');
		expect(get(vm.activeTab)).toBe('resources');
	});
	it('reset restores defaults', () => {
		const vm = createLearnViewModel(modules, paths);
		vm.selectModule(modules[0]);
		vm.setTab('paths');
		vm.reset();
		expect(get(vm.selectedModule)).toBeNull();
		expect(get(vm.activeTab)).toBe('modules');
	});
	it('defaults to built-in data', () => {
		const vm = createLearnViewModel();
		expect(vm.modules.length).toBeGreaterThan(0);
		expect(vm.paths.length).toBeGreaterThan(0);
	});
});
