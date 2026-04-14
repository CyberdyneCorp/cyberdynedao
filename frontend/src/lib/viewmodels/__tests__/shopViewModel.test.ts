import { describe, it, expect, vi } from 'vitest';
import { get } from 'svelte/store';
import {
	createShopViewModel,
	getCategoryColor,
	getStatusColor,
	getStatusText,
	formatMarketplacePrice,
	filterByCategorySlug,
	getSelectedItemSnapshot
} from '../shopViewModel';
import type { MarketplaceItem } from '$lib/types/components';

const items: MarketplaceItem[] = [
	{ id: 'a', title: 'A', description: 'd', category: 'Services', price: 100, features: [], image: 'x', status: 'available', popular: true },
	{ id: 'b', title: 'B', description: 'd', category: 'Training Material', price: 50, features: [], image: 'x', status: 'available' },
	{ id: 'c', title: 'C', description: 'd', category: 'Licenses', price: 2000, features: [], image: 'x', status: 'coming-soon', popular: true }
];

describe('shopViewModel helpers', () => {
	it('getCategoryColor covers known + default', () => {
		expect(getCategoryColor('Services')).toMatch(/blue/);
		expect(getCategoryColor('Training Material')).toMatch(/green/);
		expect(getCategoryColor('Licenses')).toMatch(/purple/);
		expect(getCategoryColor('Other')).toMatch(/gray/);
	});
	it('getStatusColor covers all branches', () => {
		expect(getStatusColor('available')).toMatch(/green/);
		expect(getStatusColor('beta')).toMatch(/yellow/);
		expect(getStatusColor('coming-soon')).toMatch(/orange/);
		expect(getStatusColor('other')).toMatch(/gray/);
	});
	it('getStatusText covers all branches', () => {
		expect(getStatusText('available')).toBe('Available');
		expect(getStatusText('beta')).toBe('Beta');
		expect(getStatusText('coming-soon')).toBe('Coming Soon');
		expect(getStatusText('other')).toBe('Unknown');
	});
	it('formatMarketplacePrice handles both ranges', () => {
		expect(formatMarketplacePrice(500)).toBe('$500');
		expect(formatMarketplacePrice(1500)).toBe('$1.5k');
	});
	it('filterByCategorySlug returns all on all', () => {
		expect(filterByCategorySlug(items, 'all')).toHaveLength(3);
		expect(filterByCategorySlug(items, 'services')).toHaveLength(1);
		expect(filterByCategorySlug(items, 'trainingmaterial')).toHaveLength(1);
		expect(filterByCategorySlug(items, 'licenses')).toHaveLength(1);
	});
});

describe('shopViewModel factory', () => {
	it('initializes with defaults', () => {
		const vm = createShopViewModel(items);
		expect(vm.items).toHaveLength(3);
		expect(vm.popularItems).toHaveLength(2);
		expect(get(vm.selectedCategory)).toBe('all');
		expect(get(vm.selectedItem)).toBeNull();
		expect(get(vm.filteredItems)).toHaveLength(3);
	});
	it('selectCategory updates filteredItems', () => {
		const vm = createShopViewModel(items);
		vm.selectCategory('services');
		expect(get(vm.filteredItems)).toHaveLength(1);
	});
	it('selectItem sets selectedItem', () => {
		const vm = createShopViewModel(items);
		vm.selectItem(items[0]);
		expect(get(vm.selectedItem)).toEqual(items[0]);
		expect(getSelectedItemSnapshot(vm)).toEqual(items[0]);
	});
	it('addToCart calls callback except for coming-soon', () => {
		const cb = vi.fn();
		const vm = createShopViewModel(items, cb);
		vm.addToCart(items[0]);
		vm.addToCart(items[2]);
		expect(cb).toHaveBeenCalledTimes(1);
		expect(cb).toHaveBeenCalledWith(items[0]);
	});
	it('addToCart is a noop without callback', () => {
		const vm = createShopViewModel(items);
		expect(() => vm.addToCart(items[0])).not.toThrow();
	});
	it('reset restores initial state', () => {
		const vm = createShopViewModel(items);
		vm.selectCategory('services');
		vm.selectItem(items[0]);
		vm.reset();
		expect(get(vm.selectedCategory)).toBe('all');
		expect(get(vm.selectedItem)).toBeNull();
	});
	it('defaults to built-in marketplace items', () => {
		const vm = createShopViewModel();
		expect(vm.items.length).toBeGreaterThan(0);
		expect(vm.categories.length).toBeGreaterThan(0);
	});
});
