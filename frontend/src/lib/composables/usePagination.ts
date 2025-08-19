/**
 * Composable for pagination functionality
 */

import { writable, derived, type Readable } from 'svelte/store';
import { UI_CONSTANTS } from '$lib/constants/app';

export function usePagination<T>(
	items: Readable<T[]>,
	pageSize = UI_CONSTANTS.DEFAULT_PAGE_SIZE
) {
	const currentPage = writable(1);
	const itemsPerPage = writable(pageSize);

	// Calculate total pages
	const totalPages = derived(
		[items, itemsPerPage],
		([$items, $itemsPerPage]) => Math.ceil($items.length / $itemsPerPage)
	);

	// Get current page items
	const paginatedItems = derived(
		[items, currentPage, itemsPerPage],
		([$items, $currentPage, $itemsPerPage]) => {
			const startIndex = ($currentPage - 1) * $itemsPerPage;
			const endIndex = startIndex + $itemsPerPage;
			return $items.slice(startIndex, endIndex);
		}
	);

	// Pagination info
	const paginationInfo = derived(
		[items, currentPage, itemsPerPage, totalPages],
		([$items, $currentPage, $itemsPerPage, $totalPages]) => ({
			currentPage: $currentPage,
			totalPages: $totalPages,
			itemsPerPage: $itemsPerPage,
			totalItems: $items.length,
			hasNext: $currentPage < $totalPages,
			hasPrev: $currentPage > 1,
			startIndex: ($currentPage - 1) * $itemsPerPage + 1,
			endIndex: Math.min($currentPage * $itemsPerPage, $items.length)
		})
	);

	return {
		currentPage,
		itemsPerPage,
		totalPages,
		paginatedItems,
		paginationInfo,
		
		// Actions
		goToPage: (page: number) => {
			currentPage.update(current => {
				const newPage = Math.max(1, Math.min(page, get(totalPages)));
				return newPage;
			});
		},
		
		nextPage: () => {
			currentPage.update(current => {
				const max = get(totalPages);
				return current < max ? current + 1 : current;
			});
		},
		
		prevPage: () => {
			currentPage.update(current => current > 1 ? current - 1 : current);
		},
		
		setPageSize: (size: number) => {
			const validSize = Math.max(1, Math.min(size, UI_CONSTANTS.MAX_PAGE_SIZE));
			itemsPerPage.set(validSize);
			currentPage.set(1); // Reset to first page
		},
		
		reset: () => {
			currentPage.set(1);
			itemsPerPage.set(pageSize);
		}
	};
}

// Helper function to get store value (for derived calculations)
function get<T>(store: Readable<T>): T {
	let value: T;
	const unsubscribe = store.subscribe(val => value = val);
	unsubscribe();
	return value!;
}