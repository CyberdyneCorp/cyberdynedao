import { writable, derived, type Readable, type Writable } from 'svelte/store';
import type { BlogPost, BlogCategory } from '$lib/types/components';
import { blogPosts as defaultPosts, buildBlogCategories } from '$lib/data/news';

export function getBlogCategoryColor(category: string): string {
	switch (category) {
		case 'Governance': return 'text-purple-600 bg-purple-100';
		case 'DeFi': return 'text-green-600 bg-green-100';
		case 'Development': return 'text-blue-600 bg-blue-100';
		case 'Security': return 'text-red-600 bg-red-100';
		case 'Economics': return 'text-orange-600 bg-orange-100';
		case 'Infrastructure': return 'text-gray-600 bg-gray-100';
		case 'NFTs': return 'text-pink-600 bg-pink-100';
		case 'UX/UI': return 'text-indigo-600 bg-indigo-100';
		default: return 'text-gray-600 bg-gray-100';
	}
}

export function filterPostsByCategory(posts: BlogPost[], categoryId: string): BlogPost[] {
	if (categoryId === 'all') return posts;
	return posts.filter(p => p.category.toLowerCase() === categoryId.toLowerCase());
}

export function truncateTitle(title: string, max: number): string {
	return title.length > max ? title.substring(0, max) + '...' : title;
}

export interface NewsViewModel {
	posts: BlogPost[];
	categories: BlogCategory[];
	featuredPosts: BlogPost[];
	selectedCategory: Writable<string>;
	selectedPost: Writable<BlogPost | null>;
	filteredPosts: Readable<BlogPost[]>;
	selectCategory: (id: string) => void;
	selectPost: (post: BlogPost) => void;
	reset: () => void;
}

export function createNewsViewModel(posts: BlogPost[] = defaultPosts): NewsViewModel {
	const selectedCategory = writable<string>('all');
	const selectedPost = writable<BlogPost | null>(null);
	const filteredPosts = derived(selectedCategory, ($cat) => filterPostsByCategory(posts, $cat));

	return {
		posts,
		categories: buildBlogCategories(posts),
		featuredPosts: posts.filter(p => p.featured),
		selectedCategory,
		selectedPost,
		filteredPosts,
		selectCategory: (id) => selectedCategory.set(id),
		selectPost: (post) => selectedPost.set(post),
		reset: () => {
			selectedCategory.set('all');
			selectedPost.set(null);
		}
	};
}
