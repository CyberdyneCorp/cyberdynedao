// Consolidated TypeScript interfaces for components

// Base interface for items with common properties
export interface BaseItem {
	id: string;
	title: string;
	category: string;
}

// Blog and News related types
export interface BlogPost extends BaseItem {
	excerpt: string;
	author: string;
	date: string;
	readTime: string;
	tags: string[];
	featured?: boolean;
	image?: string;
}

export interface BlogCategory {
	id: string;
	name: string;
	icon: string;
	count: number;
}

// Shop and Marketplace types
export interface MarketplaceItem extends BaseItem {
	description: string;
	category: 'Services' | 'Training Material' | 'Licenses';
	subcategory?: string;
	price: number;
	duration?: string;
	features: string[];
	popular?: boolean;
	image: string;
	status: 'available' | 'coming-soon' | 'beta';
}

export interface MarketplaceCategory {
	id: string;
	name: string;
	icon: string;
	count: number;
	description: string;
}

// Learning related types
export interface LearningModule extends BaseItem {
	description: string;
	level: 'Beginner' | 'Intermediate' | 'Advanced';
	duration: string;
	icon: string;
	topics: string[];
	completed?: boolean;
}

export interface LearningPath {
	id: string;
	title: string;
	description: string;
	modules: string[];
	icon: string;
	estimatedTime: string;
}

// Cart related types
export interface CartItem {
	id: string;
	title: string;
	price: number;
	quantity: number;
	category: string;
	image: string;
}

// Investment related types
export interface LiquidityPosition {
	pool: string;
	token0: string;
	token1: string;
	liquidity: number;
	value: number;
	apy: number;
	rewards: number;
}

export interface PoolStats {
	name: string;
	tvl: number;
	volume24h: number;
	fees24h: number;
	apy: number;
}

// Contact related types
export interface ContactMethod {
	type: string;
	label: string;
	value: string;
	icon: string;
	primary?: boolean;
}