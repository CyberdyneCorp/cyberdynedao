import { describe, it, expect } from 'vitest';
import { get } from 'svelte/store';
import {
	createNewsViewModel,
	getBlogCategoryColor,
	filterPostsByCategory,
	truncateTitle
} from '../newsViewModel';
import type { BlogPost } from '$lib/types/components';

const posts: BlogPost[] = [
	{ id: '1', title: 'A long title for testing purposes that exceeds limits', excerpt: 'e', category: 'Governance', author: 'x', date: '2024-01-01', readTime: '5m', tags: [], featured: true },
	{ id: '2', title: 'Short', excerpt: 'e', category: 'DeFi', author: 'x', date: '2024-01-02', readTime: '5m', tags: [] }
];

describe('newsViewModel helpers', () => {
	it('getBlogCategoryColor covers all branches', () => {
		for (const c of ['Governance', 'DeFi', 'Development', 'Security', 'Economics', 'Infrastructure', 'NFTs', 'UX/UI', 'Other']) {
			expect(getBlogCategoryColor(c)).toContain('bg-');
		}
	});
	it('filterPostsByCategory', () => {
		expect(filterPostsByCategory(posts, 'all')).toHaveLength(2);
		expect(filterPostsByCategory(posts, 'defi')).toHaveLength(1);
	});
	it('truncateTitle', () => {
		expect(truncateTitle('hello', 10)).toBe('hello');
		expect(truncateTitle('helloworld', 5)).toBe('hello...');
	});
});

describe('newsViewModel factory', () => {
	it('initial state', () => {
		const vm = createNewsViewModel(posts);
		expect(vm.posts).toHaveLength(2);
		expect(vm.featuredPosts).toHaveLength(1);
		expect(vm.categories[0].id).toBe('all');
	});
	it('selectCategory changes filteredPosts', () => {
		const vm = createNewsViewModel(posts);
		vm.selectCategory('defi');
		expect(get(vm.filteredPosts)).toHaveLength(1);
	});
	it('selectPost sets store', () => {
		const vm = createNewsViewModel(posts);
		vm.selectPost(posts[0]);
		expect(get(vm.selectedPost)).toEqual(posts[0]);
	});
	it('reset', () => {
		const vm = createNewsViewModel(posts);
		vm.selectCategory('defi');
		vm.selectPost(posts[0]);
		vm.reset();
		expect(get(vm.selectedCategory)).toBe('all');
		expect(get(vm.selectedPost)).toBeNull();
	});
	it('defaults to built-in posts', () => {
		const vm = createNewsViewModel();
		expect(vm.posts.length).toBeGreaterThan(0);
	});
});
