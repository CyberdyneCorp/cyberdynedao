import { describe, it, expect, vi } from 'vitest';
import { createContactViewModel } from '../contactViewModel';
import { contactMethods } from '$lib/data/contact';

describe('contactViewModel', () => {
	it('defaults to built-in methods and calls opener with link', () => {
		const opener = vi.fn();
		const vm = createContactViewModel(undefined, opener);
		expect(vm.methods.length).toBeGreaterThan(0);
		vm.openContact(contactMethods[0]);
		expect(opener).toHaveBeenCalledWith(contactMethods[0].link);
	});

	it('accepts custom methods list', () => {
		const custom = [{ ...contactMethods[0], id: 'x' }];
		const vm = createContactViewModel(custom, () => {});
		expect(vm.methods).toHaveLength(1);
	});

	it('default opener safely no-ops without window (smoke)', () => {
		const vm = createContactViewModel();
		expect(() => vm.openContact(contactMethods[0])).not.toThrow();
	});
});
