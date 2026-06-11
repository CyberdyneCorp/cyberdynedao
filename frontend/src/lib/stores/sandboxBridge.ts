/**
 * Bridge that lets one view push code into a sandbox window (Python or
 * MATLAB) belonging to a *different* window. The Agent uses it to drop the
 * code it wrote into the matching sandbox editor, ready to run.
 *
 * A live sandbox view registers a `sink` (its VM's `appendToInput`). A send
 * either delivers to every live sink of that target, or — when no such
 * window is open yet — queues the code so the freshly-opened view drains it
 * on mount. The queue is one-shot, so reopening a sandbox later never
 * re-injects stale code.
 */

import { get } from 'svelte/store';
import { windows, createWindow, bringToFront, updateWindow } from '$lib/stores/windowStore';

/** Sandbox windows the agent can push code into. Values match
 *  {@link WindowState.content}. */
export type SandboxTarget = 'interpreter' | 'matlab';

/** Window titles, kept in sync with the navigation labels. */
const TITLES: Record<SandboxTarget, string> = {
	interpreter: 'Python',
	matlab: 'MATLAB'
};

type Sink = (code: string) => void;

const sinks: Record<SandboxTarget, Set<Sink>> = {
	interpreter: new Set(),
	matlab: new Set()
};
const pending: Record<SandboxTarget, string[]> = {
	interpreter: [],
	matlab: []
};

/**
 * Register a sandbox view as a delivery target. Drains anything queued
 * before the view mounted. Returns an unregister function for `onDestroy`.
 */
export function registerSandbox(target: SandboxTarget, sink: Sink): () => void {
	sinks[target].add(sink);
	if (pending[target].length > 0) {
		const queued = pending[target].splice(0);
		for (const code of queued) sink(code);
	}
	return () => {
		sinks[target].delete(sink);
	};
}

/** Open (or focus) the target sandbox window and drop `code` into its editor. */
export function sendToSandbox(target: SandboxTarget, code: string): void {
	const live = sinks[target];
	if (live.size > 0) {
		for (const sink of live) sink(code);
	} else {
		pending[target].push(code);
	}
	focusOrOpen(target);
}

/** Map a fenced-code language to the sandbox that can run it, or null. */
export function sandboxTargetForLang(lang: string): SandboxTarget | null {
	const l = lang.trim().toLowerCase();
	if (l === 'python' || l === 'py') return 'interpreter';
	if (l === 'matlab' || l === 'octave') return 'matlab';
	return null;
}

function focusOrOpen(target: SandboxTarget): void {
	const open = get(windows).find((w) => w.content === target);
	if (open) {
		if (open.minimized) updateWindow(open.id, { minimized: false });
		bringToFront(open.id);
	} else {
		createWindow(target, TITLES[target]);
	}
}
