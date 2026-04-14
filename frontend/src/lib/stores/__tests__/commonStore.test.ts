import { describe, it, expect, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import { createPersistedStore, createLoadingStore, createPaginationStore } from '../commonStore';

describe('commonStore', () => {
	beforeEach(() => localStorage.clear());

	describe('createPersistedStore', () => {
		it('initializes with initialValue when storage empty', () => {
			const s = createPersistedStore('k', { x: 1 });
			expect(get(s)).toEqual({ x: 1 });
		});
		it('persists writes to localStorage', () => {
			const s = createPersistedStore('k', 0);
			s.set(42);
			expect(JSON.parse(localStorage.getItem('k')!)).toBe(42);
		});
		it('loads persisted value on init', () => {
			localStorage.setItem('k', JSON.stringify('hello'));
			const s = createPersistedStore('k', 'default');
			expect(get(s)).toBe('hello');
		});
	});

	describe('createLoadingStore', () => {
		it('has initial state', () => {
			const s = createLoadingStore();
			expect(get(s)).toEqual({ isLoading: false, error: null, lastUpdated: null });
		});
		it('setLoading clears error when starting', () => {
			const s = createLoadingStore();
			s.setError('oops');
			s.setLoading(true);
			expect(get(s).error).toBeNull();
			expect(get(s).isLoading).toBe(true);
		});
		it('setLoading(false) preserves existing error', () => {
			const s = createLoadingStore();
			s.setError('stay');
			s.setLoading(false);
			expect(get(s).error).toBe('stay');
		});
		it('setError stops loading', () => {
			const s = createLoadingStore();
			s.setLoading(true);
			s.setError('x');
			expect(get(s).isLoading).toBe(false);
			expect(get(s).error).toBe('x');
		});
		it('setSuccess updates lastUpdated and clears loading/error', () => {
			const s = createLoadingStore();
			s.setLoading(true);
			s.setSuccess();
			const state = get(s);
			expect(state.isLoading).toBe(false);
			expect(state.error).toBeNull();
			expect(state.lastUpdated).toBeInstanceOf(Date);
		});
		it('reset clears state', () => {
			const s = createLoadingStore();
			s.setSuccess();
			s.reset();
			expect(get(s).lastUpdated).toBeNull();
		});
	});

	describe('createPaginationStore', () => {
		it('initial state uses defaults', () => {
			const s = createPaginationStore(5);
			expect(get(s)).toEqual({ currentPage: 1, pageSize: 5, totalItems: 0 });
		});
		it('setPage clamps to min 1', () => {
			const s = createPaginationStore();
			s.setPage(0);
			expect(get(s).currentPage).toBe(1);
			s.setPage(3);
			expect(get(s).currentPage).toBe(3);
		});
		it('setPageSize clamps and resets page', () => {
			const s = createPaginationStore();
			s.setPage(5);
			s.setPageSize(0);
			expect(get(s).pageSize).toBe(1);
			expect(get(s).currentPage).toBe(1);
		});
		it('setTotalItems clamps to >= 0', () => {
			const s = createPaginationStore();
			s.setTotalItems(-10);
			expect(get(s).totalItems).toBe(0);
			s.setTotalItems(50);
			expect(get(s).totalItems).toBe(50);
		});
		it('nextPage and prevPage', () => {
			const s = createPaginationStore();
			s.nextPage();
			expect(get(s).currentPage).toBe(2);
			s.prevPage();
			expect(get(s).currentPage).toBe(1);
			s.prevPage();
			expect(get(s).currentPage).toBe(1);
		});
		it('reset', () => {
			const s = createPaginationStore(3);
			s.nextPage();
			s.setTotalItems(99);
			s.reset();
			expect(get(s)).toEqual({ currentPage: 1, pageSize: 3, totalItems: 0 });
		});
	});
});
