import { describe, it, expect, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import { reduceMotion } from '$lib/stores/settingsStore';

describe('settingsStore.reduceMotion', () => {
	beforeEach(() => {
		localStorage.clear();
		reduceMotion.set(false);
	});

	it('defaults to false', () => {
		expect(get(reduceMotion)).toBe(false);
	});

	it('persists changes to localStorage (survives reload)', () => {
		reduceMotion.set(true);
		expect(get(reduceMotion)).toBe(true);
		expect(JSON.parse(localStorage.getItem('cyberdyne.reduceMotion') as string)).toBe(true);
	});
});
