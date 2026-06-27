/**
 * Learning Tracks view-model — the learner-facing paths catalogue plus the
 * signed-in learner's enrollments, per-module progress, prerequisite
 * gating, and deadlines. Async actions are injected so the orchestration
 * is unit-testable without a live backend.
 *
 * Sits on top of `learningApi.ts`. A thin Svelte component renders these
 * stores and calls the actions; all orchestration + error handling lives
 * here (mirrors `coursesViewModel`).
 */

import { writable, type Writable } from 'svelte/store';
import {
	checkPathEligibility as apiCheckEligibility,
	enrollInPath as apiEnroll,
	fetchLearningModules as apiFetchModules,
	fetchLearningPaths as apiFetchPaths,
	fetchMyDeadlines as apiFetchDeadlines,
	fetchMyLearningState as apiFetchMyState,
	fetchPathGating as apiFetchGating,
	updateModuleProgress as apiUpdateProgress,
	type Eligibility,
	type EnrollmentDeadline,
	type LearningModule,
	type LearningPath,
	type ModuleGate,
	type MyLearningState
} from '$lib/api/learningApi';

function message(err: unknown): string {
	return err instanceof Error ? err.message : String(err);
}

const EMPTY_STATE: MyLearningState = { enrollments: [], progress: [], certificates: [] };

export interface LearningTracksViewModelDeps {
	fetchPaths: typeof apiFetchPaths;
	fetchModules: typeof apiFetchModules;
	fetchMyState: typeof apiFetchMyState;
	fetchDeadlines: typeof apiFetchDeadlines;
	fetchGating: typeof apiFetchGating;
	checkEligibility: typeof apiCheckEligibility;
	enroll: typeof apiEnroll;
	updateProgress: typeof apiUpdateProgress;
}

const defaultDeps: LearningTracksViewModelDeps = {
	fetchPaths: apiFetchPaths,
	fetchModules: apiFetchModules,
	fetchMyState: apiFetchMyState,
	fetchDeadlines: apiFetchDeadlines,
	fetchGating: apiFetchGating,
	checkEligibility: apiCheckEligibility,
	enroll: apiEnroll,
	updateProgress: apiUpdateProgress
};

export interface LearningTracksViewModel {
	paths: Writable<LearningPath[]>;
	modules: Writable<LearningModule[]>;
	myState: Writable<MyLearningState>;
	deadlines: Writable<EnrollmentDeadline[]>;
	selected: Writable<LearningPath | null>;
	gating: Writable<ModuleGate[]>;
	eligibility: Writable<Eligibility | null>;
	loading: Writable<boolean>;
	enrolling: Writable<boolean>;
	error: Writable<string | null>;
	/** Load the catalogue (paths + modules) and, if signed in, the
	 *  learner's state + deadlines (best-effort). */
	load: (opts?: { authed?: boolean }) => Promise<void>;
	/** Open a path: keep the summary and, if signed in, load its gating +
	 *  eligibility. */
	openPath: (slug: string, opts?: { authed?: boolean }) => Promise<void>;
	enrollInPath: (slug: string) => Promise<void>;
	markModuleComplete: (moduleSlug: string, pathSlug: string) => Promise<void>;
	close: () => void;
}

export function createLearningTracksViewModel(
	deps: LearningTracksViewModelDeps = defaultDeps
): LearningTracksViewModel {
	const paths = writable<LearningPath[]>([]);
	const modules = writable<LearningModule[]>([]);
	const myState = writable<MyLearningState>(EMPTY_STATE);
	const deadlines = writable<EnrollmentDeadline[]>([]);
	const selected = writable<LearningPath | null>(null);
	const gating = writable<ModuleGate[]>([]);
	const eligibility = writable<Eligibility | null>(null);
	const loading = writable(false);
	const enrolling = writable(false);
	const error = writable<string | null>(null);

	// Best-effort: the learner's enrollments/progress + deadlines. A lapsed
	// session (401) just leaves the panels empty rather than blocking the
	// public catalogue.
	async function loadMe(): Promise<void> {
		try {
			myState.set(await deps.fetchMyState());
		} catch {
			myState.set(EMPTY_STATE);
		}
		try {
			deadlines.set(await deps.fetchDeadlines());
		} catch {
			deadlines.set([]);
		}
	}

	async function load(opts: { authed?: boolean } = {}): Promise<void> {
		loading.set(true);
		error.set(null);
		try {
			const [p, m] = await Promise.all([deps.fetchPaths(), deps.fetchModules()]);
			paths.set(p);
			modules.set(m);
			if (opts.authed) await loadMe();
		} catch (err) {
			error.set(message(err));
		} finally {
			loading.set(false);
		}
	}

	// Gating + eligibility are per-learner, so only fetch them when signed
	// in; anonymous viewers still see the module list (without lock state).
	async function loadGating(slug: string): Promise<void> {
		try {
			gating.set(await deps.fetchGating(slug));
		} catch {
			gating.set([]);
		}
		try {
			eligibility.set(await deps.checkEligibility(slug));
		} catch {
			eligibility.set(null);
		}
	}

	async function openPath(slug: string, opts: { authed?: boolean } = {}): Promise<void> {
		error.set(null);
		gating.set([]);
		eligibility.set(null);
		let target: LearningPath | null = null;
		paths.subscribe((list) => (target = list.find((p) => p.slug === slug) ?? null))();
		selected.set(target);
		if (opts.authed) await loadGating(slug);
	}

	async function enrollInPath(slug: string): Promise<void> {
		enrolling.set(true);
		error.set(null);
		try {
			await deps.enroll(slug);
			await loadMe();
			await loadGating(slug);
		} catch (err) {
			error.set(message(err));
		} finally {
			enrolling.set(false);
		}
	}

	async function markModuleComplete(moduleSlug: string, pathSlug: string): Promise<void> {
		error.set(null);
		try {
			await deps.updateProgress(moduleSlug, 100);
			await loadMe();
			await loadGating(pathSlug);
		} catch (err) {
			error.set(message(err));
		}
	}

	function close(): void {
		selected.set(null);
		gating.set([]);
		eligibility.set(null);
		error.set(null);
	}

	return {
		paths,
		modules,
		myState,
		deadlines,
		selected,
		gating,
		eligibility,
		loading,
		enrolling,
		error,
		load,
		openPath,
		enrollInPath,
		markModuleComplete,
		close
	};
}
