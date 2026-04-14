import { describe, it, expect } from 'vitest';
import { marketplaceItems, marketplaceCategories, buildMarketplaceCategories } from '../shop';
import { blogPosts, blogCategories, buildBlogCategories } from '../news';
import { learningModules, learningPaths } from '../learn';

describe('data fixtures', () => {
	it('marketplace items have required fields', () => {
		expect(marketplaceItems.length).toBeGreaterThan(0);
		for (const item of marketplaceItems) {
			expect(item.id).toBeTruthy();
			expect(item.title).toBeTruthy();
			expect(['Services', 'Training Material', 'Licenses']).toContain(item.category);
		}
	});

	it('marketplaceCategories match counts', () => {
		expect(marketplaceCategories[0].count).toBe(marketplaceItems.length);
	});

	it('buildMarketplaceCategories with empty list', () => {
		const cats = buildMarketplaceCategories([]);
		expect(cats.every(c => c.count === 0)).toBe(true);
	});

	it('blog posts are well-formed', () => {
		expect(blogPosts.length).toBeGreaterThan(0);
		blogPosts.forEach(p => expect(p.tags.length).toBeGreaterThan(0));
	});

	it('blogCategories built from posts', () => {
		expect(blogCategories[0].id).toBe('all');
		expect(blogCategories[0].count).toBe(blogPosts.length);
		expect(buildBlogCategories([])[0].count).toBe(0);
	});

	it('learning modules and paths non-empty', () => {
		expect(learningModules.length).toBeGreaterThan(0);
		expect(learningPaths.length).toBeGreaterThan(0);
		learningPaths.forEach(p => expect(p.modules.length).toBeGreaterThan(0));
	});
});
