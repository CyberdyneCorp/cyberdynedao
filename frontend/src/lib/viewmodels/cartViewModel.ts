import { writable, derived, get, type Readable, type Writable } from 'svelte/store';
import type { CartItem } from '$lib/types/cart';
import type { MarketplaceItem } from '$lib/types/components';

export function marketplaceItemToCartItem(item: MarketplaceItem): CartItem {
	return {
		id: item.id,
		name: item.title,
		price: item.price,
		quantity: 1,
		icon: item.image
	};
}

export interface CartViewModel {
	items: Writable<CartItem[]>;
	count: Readable<number>;
	total: Readable<number>;
	addItem: (item: CartItem) => void;
	removeItem: (id: string) => void;
	updateQuantity: (id: string, quantity: number) => void;
	clear: () => void;
	snapshot: () => CartItem[];
}

export function createCartViewModel(initial: CartItem[] = []): CartViewModel {
	const items = writable<CartItem[]>([...initial]);
	const count = derived(items, ($items) => $items.reduce((sum, i) => sum + (i.quantity || 1), 0));
	const total = derived(items, ($items) =>
		$items.reduce((sum, i) => sum + i.price * (i.quantity || 1), 0)
	);

	return {
		items,
		count,
		total,
		addItem: (item) => {
			items.update(current => {
				const existing = current.find(c => c.id === item.id);
				if (existing) {
					return current.map(c =>
						c.id === item.id ? { ...c, quantity: (c.quantity || 1) + (item.quantity || 1) } : c
					);
				}
				return [...current, { ...item, quantity: item.quantity || 1 }];
			});
		},
		removeItem: (id) => {
			items.update(current => current.filter(c => c.id !== id));
		},
		updateQuantity: (id, quantity) => {
			if (quantity <= 0) {
				items.update(current => current.filter(c => c.id !== id));
				return;
			}
			items.update(current => current.map(c => (c.id === id ? { ...c, quantity } : c)));
		},
		clear: () => items.set([]),
		snapshot: () => get(items)
	};
}

export const cart = createCartViewModel();
