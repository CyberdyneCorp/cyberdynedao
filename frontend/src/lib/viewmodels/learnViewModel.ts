import { writable, type Writable } from 'svelte/store';
import type { LearningModule, LearningPath } from '$lib/types/components';
import { learningModules as defaultModules, learningPaths as defaultPaths } from '$lib/data/learn';

export type LearnTab = 'modules' | 'paths' | 'resources';

export function getLevelColor(level: string): string {
	switch (level) {
		case 'Beginner': return 'text-green-600 bg-green-100';
		case 'Intermediate': return 'text-yellow-600 bg-yellow-100';
		case 'Advanced': return 'text-red-600 bg-red-100';
		default: return 'text-gray-600 bg-gray-100';
	}
}

export function getLearnCategoryColor(category: string): string {
	switch (category) {
		case 'Blockchain': return 'text-blue-600 bg-blue-100';
		case 'Development': return 'text-purple-600 bg-purple-100';
		case 'Governance': return 'text-indigo-600 bg-indigo-100';
		case 'DeFi': return 'text-green-600 bg-green-100';
		case 'Economics': return 'text-orange-600 bg-orange-100';
		case 'Infrastructure': return 'text-gray-600 bg-gray-100';
		case 'Security': return 'text-red-600 bg-red-100';
		default: return 'text-gray-600 bg-gray-100';
	}
}

export function resolvePathModules(path: LearningPath, modules: LearningModule[]): LearningModule[] {
	return path.modules
		.map(id => modules.find(m => m.id === id))
		.filter((m): m is LearningModule => m !== undefined);
}

export interface LearnViewModel {
	modules: LearningModule[];
	paths: LearningPath[];
	selectedModule: Writable<LearningModule | null>;
	selectedPath: Writable<LearningPath | null>;
	activeTab: Writable<LearnTab>;
	selectModule: (module: LearningModule) => void;
	selectPath: (path: LearningPath) => void;
	setTab: (tab: LearnTab) => void;
	reset: () => void;
}

export function createLearnViewModel(
	modules: LearningModule[] = defaultModules,
	paths: LearningPath[] = defaultPaths
): LearnViewModel {
	const selectedModule = writable<LearningModule | null>(null);
	const selectedPath = writable<LearningPath | null>(null);
	const activeTab = writable<LearnTab>('modules');

	return {
		modules,
		paths,
		selectedModule,
		selectedPath,
		activeTab,
		selectModule: (m) => {
			selectedModule.set(m);
			selectedPath.set(null);
		},
		selectPath: (p) => {
			selectedPath.set(p);
			selectedModule.set(null);
		},
		setTab: (t) => activeTab.set(t),
		reset: () => {
			selectedModule.set(null);
			selectedPath.set(null);
			activeTab.set('modules');
		}
	};
}
