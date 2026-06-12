import { describe, it, expect, beforeEach, vi } from 'vitest';
import { get } from 'svelte/store';
import { windows } from '$lib/stores/windowStore';
import {
	createShellViewModel,
	NON_SLIDE_CLICK_TARGETS,
	localizeSections,
	_internals
} from '../shellViewModel';
import { cart } from '../cartViewModel';
import { translate } from '$lib/i18n';

describe('shellViewModel', () => {
	beforeEach(() => {
		windows.set([]);
		cart.clear();
	});

	it('exposes a full app launcher with utility actions', () => {
		const shell = createShellViewModel();
		const ids = shell.startMenuItems.map((i) => i.id);
		// All the apps plus the system utilities.
		expect(ids).toContain('Cyberdyne');
		expect(ids).toContain('MATLAB');
		expect(ids).toContain('Agent');
		expect(ids).toContain('terminal');
		expect(ids).toContain('cart');
		expect(ids).toContain('disconnect');
		expect(ids).toContain('close-all');
		expect(shell.startMenuItems.length).toBeGreaterThan(12);
	});

	it('exposes sectioned start menu data', () => {
		const shell = createShellViewModel();
		const sectionIds = shell.startMenuSections.map((s) => s.id);
		expect(sectionIds).toEqual(['core', 'ecosystem', 'learn', 'system']);
		const ecosystem = shell.startMenuSections.find((s) => s.id === 'ecosystem')!;
		const products = ecosystem.items.find((i) => i.id === 'Products')!;
		// Products has a hover submenu with title + subtitle items.
		expect(products.children?.length).toBeGreaterThan(3);
		expect(products.children?.[0].subtitle).toBeTruthy();
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
		cart.addItem({ id: 'a', name: 'A', price: 1, quantity: 2 });
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

	it('handleStartSelect("Team") opens the team window', () => {
		const shell = createShellViewModel();
		shell.handleStartSelect('Team');
		expect(get(windows)[0].content).toBe('team');
	});

	it('handleStartSelect routes an app id through viewMap', () => {
		const shell = createShellViewModel();
		shell.handleStartSelect('MATLAB');
		expect(get(windows)[0].content).toBe('matlab');
	});

	it('handleStartSelect("cart") opens the cart window', () => {
		const shell = createShellViewModel();
		shell.handleStartSelect('cart');
		expect(get(windows)[0].content).toBe('cart');
	});

	it('handleStartSelect("settings") opens the settings window', () => {
		const shell = createShellViewModel();
		shell.handleStartSelect('settings');
		const open = get(windows);
		expect(open).toHaveLength(1);
		expect(open[0].content).toBe('settings');
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

	describe('localizeSections', () => {
		const fr = (key: string) => translate('fr', key);

		it('localizes section + item labels while keeping ids stable', () => {
			const sections = localizeSections(_internals.DEFAULT_START_SECTIONS, fr);
			const system = sections.find((s) => s.id === 'system')!;
			expect(system.label).toBe(translate('fr', 'startMenu.section.system'));
			const settings = system.items.find((i) => i.id === 'settings')!;
			expect(settings.id).toBe('settings'); // routing id unchanged
			expect(settings.label).toBe(translate('fr', 'startMenu.item.settings.label'));
		});

		it('only sets a subtitle when the source item has one', () => {
			const sections = localizeSections(_internals.DEFAULT_START_SECTIONS, fr);
			const core = sections.find((s) => s.id === 'core')!;
			const cyberdyne = core.items.find((i) => i.id === 'Cyberdyne')!;
			const python = core.items.find((i) => i.id === 'Python')!;
			expect(cyberdyne.subtitle).toBeUndefined();
			expect(python.subtitle).toBe(translate('fr', 'startMenu.item.Python.subtitle'));
		});

		it('localizes nested children under their parent id', () => {
			const sections = localizeSections(_internals.DEFAULT_START_SECTIONS, fr);
			const products = sections
				.flatMap((s) => s.items)
				.find((i) => i.id === 'Products' && i.children)!;
			const child = products.children!.find((c) => c.id === 'Agent')!;
			expect(child.label).toBe(translate('fr', 'startMenu.item.Products.child.Agent.label'));
		});
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
