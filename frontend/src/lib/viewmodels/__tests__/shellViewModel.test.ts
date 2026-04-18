import { describe, it, expect, beforeEach, vi } from 'vitest';
import { get } from 'svelte/store';
import { windows } from '$lib/stores/windowStore';
import { createShellViewModel, NON_SLIDE_CLICK_TARGETS } from '../shellViewModel';
import { cart } from '../cartViewModel';

describe('shellViewModel', () => {
	beforeEach(() => {
		windows.set([]);
		cart.clear();
	});

	it('exposes default start menu items', () => {
		const shell = createShellViewModel();
		expect(shell.startMenuItems).toHaveLength(3);
		expect(shell.startMenuItems.map((i) => i.id)).toEqual(['team', 'terminal', 'close-all']);
	});

	it('accepts custom start menu items', () => {
		const custom = [{ id: 'x', label: 'X', icon: '❌' }];
		const shell = createShellViewModel(custom);
		expect(shell.startMenuItems).toBe(custom);
	});

	it('openWindowFor maps via viewMap and creates a window', () => {
		const shell = createShellViewModel();
		shell.openWindowFor('Marketplace');
		expect(get(windows)).toHaveLength(1);
		expect(get(windows)[0].content).toBe('shop');
	});

	it('openCart creates a cart window with count in title', () => {
		cart.addItem({ id: 'a', name: 'A', price: 1, quantity: 2, category: 'c' });
		const shell = createShellViewModel();
		shell.openCart();
		const w = get(windows)[0];
		expect(w.content).toBe('cart');
		expect(w.title).toMatch(/Your Bag \(\d+\)/);
	});

	it('handleStartSelect("terminal") opens terminal window', () => {
		const shell = createShellViewModel();
		shell.handleStartSelect('terminal');
		expect(get(windows)[0].content).toBe('terminal');
	});

	it('handleStartSelect("team") opens team window', () => {
		const shell = createShellViewModel();
		shell.handleStartSelect('team');
		expect(get(windows)[0].content).toBe('team');
	});

	it('handleStartSelect("close-all") clears all windows', () => {
		const shell = createShellViewModel();
		shell.openWindowFor('Blog');
		shell.openWindowFor('Team');
		expect(get(windows)).toHaveLength(2);
		shell.handleStartSelect('close-all');
		expect(get(windows)).toHaveLength(0);
	});

	it('handleStartSelect with unknown id is a no-op', () => {
		const shell = createShellViewModel();
		shell.handleStartSelect('nonsense');
		expect(get(windows)).toHaveLength(0);
	});

	it('shouldSlideOnClick returns false for clicks inside protected targets', () => {
		const shell = createShellViewModel();
		for (const selector of NON_SLIDE_CLICK_TARGETS) {
			const el = selector.startsWith('.')
				? Object.assign(document.createElement('div'), { className: selector.slice(1) })
				: document.createElement(selector);
			document.body.appendChild(el);
			expect(shell.shouldSlideOnClick(el)).toBe(false);
			el.remove();
		}
	});

	it('shouldSlideOnClick returns true for plain desktop clicks', () => {
		const shell = createShellViewModel();
		const el = document.createElement('div');
		document.body.appendChild(el);
		expect(shell.shouldSlideOnClick(el)).toBe(true);
		el.remove();
	});

	it('shouldSlideOnClick returns false for null target', () => {
		const shell = createShellViewModel();
		expect(shell.shouldSlideOnClick(null)).toBe(false);
	});

	it('handleDesktopBgClick does nothing when no windows open', () => {
		const shell = createShellViewModel();
		const el = document.createElement('div');
		const ev = new MouseEvent('click');
		Object.defineProperty(ev, 'target', { value: el });
		shell.handleDesktopBgClick(ev);
		expect(get(windows)).toHaveLength(0);
	});

	it('handleDesktopBgClick toggles slide when windows are open', () => {
		const shell = createShellViewModel();
		shell.openWindowFor('Blog');
		const before = get(windows)[0].isSlideHidden;
		const el = document.createElement('div');
		const ev = new MouseEvent('click');
		Object.defineProperty(ev, 'target', { value: el });
		shell.handleDesktopBgClick(ev);
		expect(get(windows)[0].isSlideHidden).not.toBe(before);
	});

	it('addToCart adds the marketplace item to the cart', () => {
		const shell = createShellViewModel();
		const item = { id: 'x', name: 'X', price: 10, category: 'services' as const };
		shell.addToCart(item as never);
		const items = get(cart.items);
		expect(items).toHaveLength(1);
		expect(items[0].id).toBe('x');
	});
});
