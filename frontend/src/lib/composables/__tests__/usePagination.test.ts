import { describe, it, expect } from 'vitest';
import { get, writable } from 'svelte/store';
import { usePagination } from '../usePagination';

describe('usePagination', () => {
	it('paginates items correctly', () => {
		const items = writable(Array.from({ length: 25 }, (_, i) => i));
		const p = usePagination(items, 10);
		expect(get(p.totalPages)).toBe(3);
		expect(get(p.paginatedItems)).toHaveLength(10);
		const info = get(p.paginationInfo);
		expect(info.hasNext).toBe(true);
		expect(info.hasPrev).toBe(false);
		expect(info.startIndex).toBe(1);
		expect(info.endIndex).toBe(10);
	});

	it('nextPage advances and bounds at max', () => {
		const items = writable([1, 2, 3]);
		const p = usePagination(items, 2);
		p.nextPage();
		expect(get(p.currentPage)).toBe(2);
		p.nextPage();
		expect(get(p.currentPage)).toBe(2);
	});

	it('prevPage decrements and stops at 1', () => {
		const items = writable([1, 2, 3, 4]);
		const p = usePagination(items, 2);
		p.nextPage();
		p.prevPage();
		expect(get(p.currentPage)).toBe(1);
		p.prevPage();
		expect(get(p.currentPage)).toBe(1);
	});

	it('goToPage clamps to bounds', () => {
		const items = writable([1, 2, 3, 4]);
		const p = usePagination(items, 2);
		p.goToPage(99);
		expect(get(p.currentPage)).toBe(2);
		p.goToPage(-5);
		expect(get(p.currentPage)).toBe(1);
	});

	it('setPageSize resets to first page and clamps', () => {
		const items = writable(Array.from({ length: 30 }, (_, i) => i));
		const p = usePagination(items, 5);
		p.nextPage();
		p.setPageSize(10);
		expect(get(p.currentPage)).toBe(1);
		expect(get(p.itemsPerPage)).toBe(10);
		p.setPageSize(0);
		expect(get(p.itemsPerPage)).toBe(1);
		p.setPageSize(9999);
		expect(get(p.itemsPerPage)).toBeLessThanOrEqual(200);
	});

	it('reset restores defaults', () => {
		const items = writable([1, 2, 3]);
		const p = usePagination(items, 2);
		p.nextPage();
		p.setPageSize(1);
		p.reset();
		expect(get(p.currentPage)).toBe(1);
		expect(get(p.itemsPerPage)).toBe(2);
	});

	it('default page size from UI_CONSTANTS', () => {
		const items = writable([1, 2]);
		const p = usePagination(items);
		expect(get(p.itemsPerPage)).toBeGreaterThan(0);
	});
});
