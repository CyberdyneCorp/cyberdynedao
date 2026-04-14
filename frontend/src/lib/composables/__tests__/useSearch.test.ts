import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { get } from 'svelte/store';
import { useSearch } from '../useSearch';

const items = [
	{ id: '1', title: 'Alpha Widget', category: 'Tools' },
	{ id: '2', title: 'Beta Toy', category: 'Games' },
	{ id: '3', title: 'Alpha Book', category: 'Education' }
];

describe('useSearch', () => {
	beforeEach(() => {
		vi.useFakeTimers();
	});
	afterEach(() => {
		vi.useRealTimers();
	});

	it('returns all items initially', () => {
		const s = useSearch(items);
		expect(get(s.filteredItems)).toHaveLength(3);
	});

	it('filters after debounce by title', () => {
		const s = useSearch(items);
		s.setSearchTerm('alpha');
		vi.advanceTimersByTime(500);
		expect(get(s.filteredItems)).toHaveLength(2);
	});

	it('filters after debounce by category', () => {
		const s = useSearch(items);
		s.setSearchTerm('games');
		vi.advanceTimersByTime(500);
		expect(get(s.filteredItems)).toHaveLength(1);
	});

	it('empty search restores all', () => {
		const s = useSearch(items);
		s.setSearchTerm('alpha');
		vi.advanceTimersByTime(500);
		s.setSearchTerm('');
		vi.advanceTimersByTime(500);
		expect(get(s.filteredItems)).toHaveLength(3);
	});

	it('clearSearch resets', () => {
		const s = useSearch(items);
		s.setSearchTerm('alpha');
		vi.advanceTimersByTime(500);
		s.clearSearch();
		vi.advanceTimersByTime(500);
		expect(get(s.searchTerm)).toBe('');
	});

	it('rejects too-long search terms', () => {
		const s = useSearch(items);
		s.setSearchTerm('x'.repeat(1000));
		expect(get(s.searchTerm)).toBe('');
	});
});
