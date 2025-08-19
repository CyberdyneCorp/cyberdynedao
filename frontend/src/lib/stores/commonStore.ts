/**
 * Common store utilities and patterns
 */

import { writable, type Writable } from 'svelte/store';
import { getStorageItem, setStorageItem } from '$lib/utils/storage';

/**
 * Creates a store that persists to localStorage
 */
export function createPersistedStore<T>(
	key: string, 
	initialValue: T
): Writable<T> {
	const storedValue = getStorageItem(key, initialValue);
	const store = writable<T>(storedValue);

	store.subscribe((value) => {
		setStorageItem(key, value);
	});

	return store;
}

/**
 * Creates a loading state store with common loading patterns
 */
export function createLoadingStore() {
	const { subscribe, set, update } = writable({
		isLoading: false,
		error: null as string | null,
		lastUpdated: null as Date | null
	});

	return {
		subscribe,
		setLoading: (loading: boolean) => update(state => ({
			...state,
			isLoading: loading,
			error: loading ? null : state.error
		})),
		setError: (error: string | null) => update(state => ({
			...state,
			isLoading: false,
			error
		})),
		setSuccess: () => update(state => ({
			...state,
			isLoading: false,
			error: null,
			lastUpdated: new Date()
		})),
		reset: () => set({
			isLoading: false,
			error: null,
			lastUpdated: null
		})
	};
}

/**
 * Creates a pagination store
 */
export function createPaginationStore(initialPageSize = 10) {
	const { subscribe, set, update } = writable({
		currentPage: 1,
		pageSize: initialPageSize,
		totalItems: 0
	});

	return {
		subscribe,
		setPage: (page: number) => update(state => ({
			...state,
			currentPage: Math.max(1, page)
		})),
		setPageSize: (size: number) => update(state => ({
			...state,
			pageSize: Math.max(1, size),
			currentPage: 1 // Reset to first page
		})),
		setTotalItems: (total: number) => update(state => ({
			...state,
			totalItems: Math.max(0, total)
		})),
		nextPage: () => update(state => ({
			...state,
			currentPage: state.currentPage + 1
		})),
		prevPage: () => update(state => ({
			...state,
			currentPage: Math.max(1, state.currentPage - 1)
		})),
		reset: () => set({
			currentPage: 1,
			pageSize: initialPageSize,
			totalItems: 0
		})
	};
}