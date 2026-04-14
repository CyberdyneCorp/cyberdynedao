import { writable, derived, get, type Readable, type Writable } from 'svelte/store';
import type { MarketplaceItem, MarketplaceCategory } from '$lib/types/components';
import { marketplaceItems as defaultItems, buildMarketplaceCategories } from '$lib/data/shop';

export function getCategoryColor(category: string): string {
	switch (category) {
		case 'Services': return 'text-blue-600 bg-blue-100';
		case 'Training Material': return 'text-green-600 bg-green-100';
		case 'Licenses': return 'text-purple-600 bg-purple-100';
		default: return 'text-gray-600 bg-gray-100';
	}
}

export function getStatusColor(status: string): string {
	switch (status) {
		case 'available': return 'text-green-600 bg-green-100';
		case 'beta': return 'text-yellow-600 bg-yellow-100';
		case 'coming-soon': return 'text-orange-600 bg-orange-100';
		default: return 'text-gray-600 bg-gray-100';
	}
}

export function getStatusText(status: string): string {
	switch (status) {
		case 'available': return 'Available';
		case 'beta': return 'Beta';
		case 'coming-soon': return 'Coming Soon';
		default: return 'Unknown';
	}
}

export function formatMarketplacePrice(price: number): string {
	return price >= 1000 ? `$${(price / 1000).toFixed(1)}k` : `$${price}`;
}

export function filterByCategorySlug(items: MarketplaceItem[], categoryId: string): MarketplaceItem[] {
	if (categoryId === 'all') return items;
	return items.filter(item => item.category.toLowerCase().replace(' ', '') === categoryId);
}

export interface ShopViewModel {
	items: MarketplaceItem[];
	categories: MarketplaceCategory[];
	popularItems: MarketplaceItem[];
	selectedCategory: Writable<string>;
	selectedItem: Writable<MarketplaceItem | null>;
	filteredItems: Readable<MarketplaceItem[]>;
	selectItem: (item: MarketplaceItem) => void;
	selectCategory: (categoryId: string) => void;
	addToCart: (item: MarketplaceItem) => void;
	reset: () => void;
}

export function createShopViewModel(
	items: MarketplaceItem[] = defaultItems,
	onAddToCart?: (item: MarketplaceItem) => void
): ShopViewModel {
	const selectedCategory = writable<string>('all');
	const selectedItem = writable<MarketplaceItem | null>(null);

	const filteredItems = derived(selectedCategory, ($cat) => filterByCategorySlug(items, $cat));

	return {
		items,
		categories: buildMarketplaceCategories(items),
		popularItems: items.filter(i => i.popular),
		selectedCategory,
		selectedItem,
		filteredItems,
		selectItem: (item) => selectedItem.set(item),
		selectCategory: (id) => selectedCategory.set(id),
		addToCart: (item) => {
			if (item.status === 'coming-soon') return;
			onAddToCart?.(item);
		},
		reset: () => {
			selectedCategory.set('all');
			selectedItem.set(null);
		}
	};
}

export function getSelectedItemSnapshot(vm: ShopViewModel): MarketplaceItem | null {
	return get(vm.selectedItem);
}
