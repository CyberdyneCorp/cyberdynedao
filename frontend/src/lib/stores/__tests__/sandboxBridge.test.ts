import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { get } from 'svelte/store';
import { registerSandbox, sendToSandbox, sandboxTargetForLang } from '../sandboxBridge';
import { windows, closeAllWindows } from '../windowStore';

beforeEach(() => {
	closeAllWindows();
});
afterEach(() => {
	closeAllWindows();
});

describe('sandboxTargetForLang', () => {
	it('maps python/py to the interpreter sandbox', () => {
		expect(sandboxTargetForLang('python')).toBe('interpreter');
		expect(sandboxTargetForLang('PY')).toBe('interpreter');
	});
	it('maps matlab/octave to the matlab sandbox', () => {
		expect(sandboxTargetForLang('matlab')).toBe('matlab');
		expect(sandboxTargetForLang('Octave')).toBe('matlab');
	});
	it('returns null for languages without a sandbox', () => {
		expect(sandboxTargetForLang('javascript')).toBeNull();
		expect(sandboxTargetForLang('')).toBeNull();
	});
});

describe('sendToSandbox', () => {
	it('delivers to a live sink and focuses the existing window', () => {
		const received: string[] = [];
		const unregister = registerSandbox('interpreter', (code) => received.push(code));
		// Pretend a Python window is already open.
		windows.set([
			{
				id: 'w1',
				title: 'Python',
				x: 0,
				y: 0,
				width: 800,
				height: 600,
				zIndex: 100,
				minimized: false,
				maximized: false,
				isSlideHidden: false,
				content: 'interpreter'
			}
		]);

		sendToSandbox('interpreter', 'print(1)');

		expect(received).toEqual(['print(1)']);
		// No new window created — the existing one is reused.
		expect(get(windows)).toHaveLength(1);
		unregister();
	});

	it('opens a window when none is live and drains the code on register', () => {
		// No sink registered yet, no window open → the code is queued and the
		// bridge opens the matching window.
		sendToSandbox('matlab', 'disp(1)');
		expect(get(windows).map((w) => w.content)).toEqual(['matlab']);

		// The freshly-mounted view registers and drains the queued code.
		const received: string[] = [];
		const unregister = registerSandbox('matlab', (code) => received.push(code));
		expect(received).toEqual(['disp(1)']);

		// Queue is one-shot: a later window does NOT re-receive it.
		const later: string[] = [];
		const unregister2 = registerSandbox('matlab', (code) => later.push(code));
		expect(later).toEqual([]);
		unregister();
		unregister2();
	});

	it('unminimizes a minimized target window', () => {
		windows.set([
			{
				id: 'w2',
				title: 'Python',
				x: 0,
				y: 0,
				width: 800,
				height: 600,
				zIndex: 100,
				minimized: true,
				maximized: false,
				isSlideHidden: false,
				content: 'interpreter'
			}
		]);
		const unregister = registerSandbox('interpreter', () => {});
		sendToSandbox('interpreter', 'x = 1');
		expect(get(windows)[0].minimized).toBe(false);
		unregister();
	});
});
