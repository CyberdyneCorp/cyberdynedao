/**
 * Composable for search functionality
 */

import { writable } from 'svelte/store';
import { UI_CONSTANTS } from '$lib/constants/app';
import type { BaseItem } from '$lib/types/components';

export function useSearch<T extends BaseItem>(items: T[]) {
	const searchTerm = writable('');
	const filteredItems = writable<T[]>(items);
	let debounceTimer: ReturnType<typeof setTimeout>;

	// Update filtered items when search term changes
	searchTerm.subscribe(term => {
		clearTimeout(debounceTimer);
		
		debounceTimer = setTimeout(() => {
			if (!term.trim()) {
				filteredItems.set(items);
				return;
			}

			const lowercaseTerm = term.toLowerCase();
			const filtered = items.filter(item =>
				item.title.toLowerCase().includes(lowercaseTerm) ||
				item.category.toLowerCase().includes(lowercaseTerm)
			);
			
			filteredItems.set(filtered);
		}, UI_CONSTANTS.DEBOUNCE_DELAY);
	});

	return {
		searchTerm,
		filteredItems,
		setSearchTerm: (term: string) => {
			if (term.length <= UI_CONSTANTS.MAX_SEARCH_LENGTH) {
				searchTerm.set(term);
			}
		},
		clearSearch: () => {
			searchTerm.set('');
		}
	};
}