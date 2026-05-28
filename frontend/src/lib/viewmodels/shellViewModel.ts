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
import { authVM } from '$lib/auth/authViewModel.svelte';
import type { MarketplaceItem } from '$lib/types/components';
import type { LauncherMenuSection } from '@cyberdynecorp/svelte-ui-core';
type StartMenuSection = LauncherMenuSection;

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
	/** Sectioned items for the redesigned StartMenu (MAIN/BUSINESS/CONTENT/SYSTEM). */
	startMenuSections: StartMenuSection[];
	openWindowFor(name: string): void;
	openWindowByNavItem(item: NavItem): void;
	openCart(): void;
	addToCart(item: MarketplaceItem): void;
	handleStartSelect(id: string): void;
	shouldSlideOnClick(target: EventTarget | null): boolean;
	handleDesktopBgClick(e: Event): void;
}

// Sectioned launcher data backing the redesigned StartMenu.
// Item ids match navigation names so ``openWindowFor`` routes through
// ``viewMap``; special ids are handled in ``handleStartSelect``
// (cart / terminal / close-all / settings / disconnect).
const DEFAULT_START_SECTIONS: StartMenuSection[] = [
	{
		id: 'core',
		label: 'CORE',
		items: [
			{ id: 'Cyberdyne', label: 'About Cyberdyne', icon: '🏢' },
			{ id: 'Agent', label: 'AI Agent', icon: '🤖' },
			{ id: 'MATLAB', label: 'MATLAB REPL', icon: '🔢' }
		]
	},
	{
		id: 'ecosystem',
		label: 'ECOSYSTEM',
		items: [
			{
				id: 'Products',
				label: 'Products',
				icon: '📦',
				children: [
					{
						id: 'Agent',
						label: 'AI Knowledge Systems',
						icon: '🤖',
						subtitle: 'RAG, Agents, MCP'
					},
					{
						id: 'Cyberdyne',
						label: 'Geospatial Platform',
						icon: '🛰',
						subtitle: 'Satellite, Risk, Analytics'
					},
					{
						id: 'MATLAB',
						label: 'MATLAB LLVM Compiler',
						icon: '🔢',
						subtitle: 'High performance infra'
					},
					{
						id: 'DAO',
						label: 'DAO / DeFi Tools',
						icon: '🏦',
						subtitle: 'Yield, Treasury, Governance'
					},
					{
						id: 'Services',
						label: 'Developer Services',
						icon: '🛠️',
						subtitle: 'APIs, SDKs, Infrastructure'
					},
					{ id: 'Products', label: 'View all products', icon: '↗' }
				]
			},
			{ id: 'Marketplace', label: 'Marketplace', icon: '🛒' },
			{ id: 'Investments', label: 'Investments', icon: '📈' },
			{ id: 'DAO', label: 'DAO Treasury', icon: '🏦' }
		]
	},
	{
		id: 'learn',
		label: 'LEARN',
		items: [
			{ id: 'Blog', label: 'Blog', icon: '📰' },
			{ id: 'Learn', label: 'Academy', icon: '🎓' }
		]
	},
	{
		id: 'system',
		label: 'SYSTEM',
		items: [
			{ id: 'cart', label: 'Your Bag', icon: '🛍️' },
			{ id: 'terminal', label: 'Terminal', icon: '💻', subtitle: 'Linux sandbox shell' },
			{ id: 'settings', label: 'Settings', icon: '⚙️' },
			{
				id: 'disconnect',
				label: 'Disconnect',
				icon: '⎋',
				subtitle: 'Log out of Cyberdyne'
			},
			{ id: 'close-all', label: 'Close All Windows', icon: '❌' }
		]
	}
];

// Flattened legacy view for back-compat — the old flat StartMenu API
// is still consumed by tests and any caller that doesn't know about
// sections.
function flatten(sections: StartMenuSection[]): StartMenuItemConfig[] {
	return sections.flatMap((s) => s.items.map((i) => ({ id: i.id, label: i.label, icon: i.icon })));
}

const DEFAULT_START_MENU: StartMenuItemConfig[] = flatten(DEFAULT_START_SECTIONS);

export function createShellViewModel(
	startMenuItems: StartMenuItemConfig[] = DEFAULT_START_MENU,
	startMenuSections: StartMenuSection[] = DEFAULT_START_SECTIONS
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
		else if (id === 'close-all') closeAllWindows();
		else if (id === 'cart') openCart();
		else if (id === 'disconnect') void authVM.logout();
		else if (id === 'settings') {
			/* settings window not built yet — no-op until then */
		} else if (id in viewMap) openWindowFor(id);
		// Unknown id → no-op.
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
		startMenuSections,
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
export const _internals = { DEFAULT_START_MENU, DEFAULT_START_SECTIONS };
