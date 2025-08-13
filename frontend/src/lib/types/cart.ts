/**
 * Cart item interface for type safety
 */
export interface CartItem {
	id: string;
	name: string;
	price: number;
	quantity: number;
	icon?: string;
}

/**
 * Cart state interface
 */
export interface CartState {
	items: CartItem[];
	totalCount: number;
	totalPrice: number;
}