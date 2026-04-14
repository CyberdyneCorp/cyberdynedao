import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
	getStorageItem,
	setStorageItem,
	removeStorageItem,
	clearStorage,
	isStorageAvailable
} from '../storage';

describe('storage', () => {
	beforeEach(() => {
		localStorage.clear();
	});

	it('sets and gets items with JSON', () => {
		setStorageItem('key', { a: 1 });
		expect(getStorageItem('key', null)).toEqual({ a: 1 });
	});

	it('returns default when key missing', () => {
		expect(getStorageItem('missing', 'fallback')).toBe('fallback');
	});

	it('returns default when JSON is invalid', () => {
		localStorage.setItem('bad', 'not-json{');
		expect(getStorageItem('bad', 'fallback')).toBe('fallback');
	});

	it('removes items', () => {
		setStorageItem('x', 1);
		expect(removeStorageItem('x')).toBe(true);
		expect(getStorageItem('x', null)).toBe(null);
	});

	it('clears all items', () => {
		setStorageItem('a', 1);
		setStorageItem('b', 2);
		expect(clearStorage()).toBe(true);
	});

	it('reports storage available', () => {
		expect(isStorageAvailable()).toBe(true);
	});

	it('setStorageItem returns false on error', () => {
		const spy = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
			throw new Error('quota');
		});
		expect(setStorageItem('x', 1)).toBe(false);
		spy.mockRestore();
	});

	it('removeStorageItem returns false on error', () => {
		const spy = vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(() => {
			throw new Error('fail');
		});
		expect(removeStorageItem('x')).toBe(false);
		spy.mockRestore();
	});

	it('clearStorage returns false on error', () => {
		const spy = vi.spyOn(Storage.prototype, 'clear').mockImplementation(() => {
			throw new Error('fail');
		});
		expect(clearStorage()).toBe(false);
		spy.mockRestore();
	});

	it('isStorageAvailable returns false on error', () => {
		const spy = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
			throw new Error('fail');
		});
		expect(isStorageAvailable()).toBe(false);
		spy.mockRestore();
	});
});
