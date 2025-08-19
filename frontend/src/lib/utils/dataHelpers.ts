/**
 * Utility functions for data manipulation and filtering
 */

import type { BaseItem } from '$lib/types/components';

/**
 * Filters items by category
 */
export function filterByCategory<T extends BaseItem>(
	items: T[], 
	category: string
): T[] {
	if (category === 'all') {
		return items;
	}
	return items.filter(item => 
		item.category.toLowerCase() === category.toLowerCase()
	);
}

/**
 * Filters items by search term (searches title and category)
 */
export function filterBySearch<T extends BaseItem>(
	items: T[], 
	searchTerm: string
): T[] {
	if (!searchTerm.trim()) {
		return items;
	}
	
	const term = searchTerm.toLowerCase();
	return items.filter(item =>
		item.title.toLowerCase().includes(term) ||
		item.category.toLowerCase().includes(term)
	);
}

/**
 * Gets unique categories from a list of items
 */
export function getUniqueCategories<T extends BaseItem>(items: T[]): string[] {
	const categories = items.map(item => item.category);
	return Array.from(new Set(categories));
}

/**
 * Counts items by category
 */
export function countByCategory<T extends BaseItem>(
	items: T[]
): Record<string, number> {
	return items.reduce((acc, item) => {
		acc[item.category] = (acc[item.category] || 0) + 1;
		return acc;
	}, {} as Record<string, number>);
}

/**
 * Sorts items by a specified field
 */
export function sortBy<T>(
	items: T[], 
	field: keyof T, 
	direction: 'asc' | 'desc' = 'asc'
): T[] {
	return [...items].sort((a, b) => {
		const aVal = a[field];
		const bVal = b[field];
		
		if (aVal < bVal) return direction === 'asc' ? -1 : 1;
		if (aVal > bVal) return direction === 'asc' ? 1 : -1;
		return 0;
	});
}

/**
 * Groups items by a specified field
 */
export function groupBy<T>(
	items: T[], 
	field: keyof T
): Record<string, T[]> {
	return items.reduce((acc, item) => {
		const key = String(item[field]);
		if (!acc[key]) {
			acc[key] = [];
		}
		acc[key].push(item);
		return acc;
	}, {} as Record<string, T[]>);
}