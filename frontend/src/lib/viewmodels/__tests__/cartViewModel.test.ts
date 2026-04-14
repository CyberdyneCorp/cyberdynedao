import { describe, it, expect } from 'vitest';
import { get } from 'svelte/store';
import { createCartViewModel, cart } from '../cartViewModel';
import type { CartItem } from '$lib/types/cart';

const item = (id: string, price = 10, quantity = 1): CartItem => ({ id, name: `n-${id}`, price, quantity });

describe('cartViewModel', () => {
	it('starts empty', () => {
		const vm = createCartViewModel();
		expect(get(vm.items)).toEqual([]);
		expect(get(vm.count)).toBe(0);
		expect(get(vm.total)).toBe(0);
	});

	it('addItem adds new items', () => {
		const vm = createCartViewModel();
		vm.addItem(item('a'));
		vm.addItem(item('b', 20));
		expect(get(vm.items)).toHaveLength(2);
		expect(get(vm.total)).toBe(30);
	});

	it('addItem merges quantity for existing items', () => {
		const vm = createCartViewModel();
		vm.addItem(item('a', 10, 2));
		vm.addItem(item('a', 10, 3));
		const items = get(vm.items);
		expect(items).toHaveLength(1);
		expect(items[0].quantity).toBe(5);
		expect(get(vm.count)).toBe(5);
	});

	it('addItem defaults quantity to 1 when missing', () => {
		const vm = createCartViewModel();
		vm.addItem({ id: 'x', name: 'x', price: 5, quantity: 0 });
		expect(get(vm.items)[0].quantity).toBe(1);
	});

	it('removeItem drops by id', () => {
		const vm = createCartViewModel([item('a'), item('b')]);
		vm.removeItem('a');
		expect(get(vm.items)).toHaveLength(1);
	});

	it('updateQuantity changes or removes', () => {
		const vm = createCartViewModel([item('a', 10, 1)]);
		vm.updateQuantity('a', 5);
		expect(get(vm.items)[0].quantity).toBe(5);
		vm.updateQuantity('a', 0);
		expect(get(vm.items)).toHaveLength(0);
	});

	it('clear empties', () => {
		const vm = createCartViewModel([item('a')]);
		vm.clear();
		expect(get(vm.items)).toHaveLength(0);
	});

	it('snapshot returns current items', () => {
		const vm = createCartViewModel([item('a')]);
		expect(vm.snapshot()).toHaveLength(1);
	});

	it('exports singleton cart', () => {
		expect(cart).toBeDefined();
		expect(typeof cart.addItem).toBe('function');
	});

	it('count and total handle items missing quantity', () => {
		const vm = createCartViewModel();
		// @ts-expect-error intentionally omitting quantity
		vm.items.set([{ id: 'x', name: 'x', price: 10 }]);
		expect(get(vm.count)).toBe(1);
		expect(get(vm.total)).toBe(10);
	});

	it('addItem merges with existing items missing quantity', () => {
		const vm = createCartViewModel();
		// @ts-expect-error intentionally omitting quantity
		vm.items.set([{ id: 'a', name: 'a', price: 5 }]);
		vm.addItem({ id: 'a', name: 'a', price: 5, quantity: 2 });
		expect(get(vm.items)[0].quantity).toBe(3);
	});

	it('updateQuantity does not modify non-matching ids', () => {
		const vm = createCartViewModel([item('a', 10, 1), item('b', 20, 1)]);
		vm.updateQuantity('a', 5);
		expect(get(vm.items).find(i => i.id === 'b')?.quantity).toBe(1);
	});
});
