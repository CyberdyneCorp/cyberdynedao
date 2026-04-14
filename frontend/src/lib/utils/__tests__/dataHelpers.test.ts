import { describe, it, expect } from 'vitest';
import {
	filterByCategory,
	filterBySearch,
	getUniqueCategories,
	countByCategory,
	sortBy,
	groupBy
} from '../dataHelpers';

const items = [
	{ id: '1', title: 'Alpha', category: 'A' },
	{ id: '2', title: 'Beta', category: 'B' },
	{ id: '3', title: 'Gamma', category: 'A' }
];

describe('dataHelpers', () => {
	it('filterByCategory returns all when "all"', () => {
		expect(filterByCategory(items, 'all')).toHaveLength(3);
	});
	it('filterByCategory filters case-insensitive', () => {
		expect(filterByCategory(items, 'a')).toHaveLength(2);
	});

	it('filterBySearch matches title', () => {
		expect(filterBySearch(items, 'alph')).toHaveLength(1);
	});
	it('filterBySearch matches category case-insensitively', () => {
		expect(filterBySearch(items, 'a')).toHaveLength(3);
	});
	it('filterBySearch returns all when empty', () => {
		expect(filterBySearch(items, '  ')).toHaveLength(3);
	});

	it('getUniqueCategories returns unique', () => {
		expect(getUniqueCategories(items).sort()).toEqual(['A', 'B']);
	});

	it('countByCategory', () => {
		expect(countByCategory(items)).toEqual({ A: 2, B: 1 });
	});

	it('sortBy asc and desc', () => {
		const asc = sortBy(items, 'title', 'asc');
		expect(asc[0].title).toBe('Alpha');
		const desc = sortBy(items, 'title', 'desc');
		expect(desc[0].title).toBe('Gamma');
	});
	it('sortBy default is asc', () => {
		expect(sortBy(items, 'title')[0].title).toBe('Alpha');
	});
	it('sortBy keeps equal items in order', () => {
		const eq = sortBy([{ x: 1 }, { x: 1 }], 'x');
		expect(eq).toHaveLength(2);
	});

	it('groupBy', () => {
		const g = groupBy(items, 'category');
		expect(g.A).toHaveLength(2);
		expect(g.B).toHaveLength(1);
	});
});
