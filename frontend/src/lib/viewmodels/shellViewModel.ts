/**
 * Shell view-model for the root desktop page.
 *
 * Wraps windowStore + cart bridge + start-menu config so the view
 * (+page.svelte) contains no business logic — only rendering.
 */
import { derived, type Readable } from 'svelte/store';
import {
	windows,
	createWindow as storeCreateWindow,
	closeAllWindows,
	toggleWindowSlide,
	type WindowState
} from '$lib/stores/windowStore';
import { viewMap, type NavItem } from '$lib/constants/navigation';
import { cart, marketplaceItemToCartItem } from '$lib/viewmodels/cartViewModel';
import type { MarketplaceItem } from '$lib/types/components';

export interface StartMenuItemConfig {
	id: string;
	label: string;
	icon: string;
}

/**
 * DOM classes whose click events should NOT trigger a desktop slide.
 * Exported so the view can stay declarative.
 */
export const NON_SLIDE_CLICK_TARGETS = [
	'.cy-rwin',
	'.cy-dicon',
	'.cy-start',
	'.cy-taskbar',
	'button'
] as const;

export interface ShellViewModel {
	windows: typeof windows;
	cartCount: Readable<number>;
	startMenuItems: StartMenuItemConfig[];
	openWindowFor(name: string): void;
	openWindowByNavItem(item: NavItem): void;
	openCart(): void;
	addToCart(item: MarketplaceItem): void;
	handleStartSelect(id: string): void;
	shouldSlideOnClick(target: EventTarget | null): boolean;
	handleDesktopBgClick(e: Event): void;
}

const DEFAULT_START_MENU: StartMenuItemConfig[] = [
	{ id: 'team', label: 'Our Team', icon: '👥' },
	{ id: 'terminal', label: 'Terminal', icon: '💻' },
	{ id: 'close-all', label: 'Close All Windows', icon: '❌' }
];

export function createShellViewModel(
	startMenuItems: StartMenuItemConfig[] = DEFAULT_START_MENU
): ShellViewModel {
	const cartCount = cart.count;

	function openWindowFor(name: string) {
		const content = (viewMap[name] || name.toLowerCase()) as WindowState['content'];
		storeCreateWindow(content, name);
	}

	function openWindowByNavItem(item: NavItem) {
		openWindowFor(item.name);
	}

	function openCart() {
		const count = getCount(cartCount);
		storeCreateWindow('cart', `Your Bag (${count})`);
	}

	function addToCart(item: MarketplaceItem) {
		cart.addItem(marketplaceItemToCartItem(item));
	}

	function handleStartSelect(id: string) {
		if (id === 'terminal') storeCreateWindow('terminal', 'Terminal');
		else if (id === 'team') openWindowFor('Team');
		else if (id === 'close-all') closeAllWindows();
	}

	function shouldSlideOnClick(target: EventTarget | null): boolean {
		if (!(target instanceof HTMLElement)) return false;
		return !NON_SLIDE_CLICK_TARGETS.some((sel) => target.closest(sel));
	}

	function handleDesktopBgClick(e: Event) {
		if (!shouldSlideOnClick(e.target)) return;
		if (getWindowCount() > 0) toggleWindowSlide();
	}

	return {
		windows,
		cartCount,
		startMenuItems,
		openWindowFor,
		openWindowByNavItem,
		openCart,
		addToCart,
		handleStartSelect,
		shouldSlideOnClick,
		handleDesktopBgClick
	};
}

// --- helpers (kept local so the VM stays a pure module) ---

function getCount(store: Readable<number>): number {
	let value = 0;
	const unsub = store.subscribe((v) => (value = v));
	unsub();
	return value;
}

function getWindowCount(): number {
	let count = 0;
	const unsub = windows.subscribe((w) => (count = w.length));
	unsub();
	return count;
}

// Exported for tests
export const _internals = { DEFAULT_START_MENU };
