<script lang="ts">
	import { onMount } from 'svelte';
	import { Badge, PixelButton, PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import type { BlogPost } from '$lib/types/components';
	import { formatDate } from '$lib/utils/formatters';
	import {
		createNewsViewModel,
		truncateTitle
	} from '$lib/viewmodels/newsViewModel';
	import { fetchBlogPosts, fetchBlogPost, type BlogPostSummary } from '$lib/api/contentApi';

	let { isMobile = false }: { isMobile?: boolean } = $props();
	// Layout adapts via CSS media queries — keep the prop for caller
	// compatibility but it's not read directly.
	void isMobile;

	const vm = createNewsViewModel();
	const { selectedCategory, selectedPost, filteredPosts } = vm;
	const { categories, featuredPosts } = vm;

	let blogPosts = $state<BlogPost[]>(vm.posts);

	// Full body of the selected post (markdown), lazy-loaded on select.
	let bodyBlocks = $state<MdBlock[]>([]);
	let bodyLoading = $state(false);
	let bodyError = $state(false);

	onMount(async () => {
		const list = await fetchBlogPosts({ pageSize: 50 });
		if (list.items.length === 0) return;
		blogPosts = list.items.map(apiPostToFrontend);
	});

	function apiPostToFrontend(p: BlogPostSummary): BlogPost {
		const wordCount = (p.excerpt || '').split(/\s+/).length;
		const readTimeMin = Math.max(1, Math.round(wordCount / 200));
		return {
			id: p.slug,
			title: p.title,
			category: p.categorySlug ?? 'general',
			excerpt: p.excerpt,
			author: 'Cyberdyne',
			date: (p.publishedAt ?? p.createdAt).slice(0, 10),
			readTime: `${readTimeMin} min read`,
			tags: p.tags,
			featured: false
		};
	}

	async function selectPost(post: BlogPost) {
		vm.selectPost(post);
		// Pull the full body. `post.id` is the slug (set in apiPostToFrontend).
		bodyBlocks = [];
		bodyError = false;
		bodyLoading = true;
		try {
			const detail = await fetchBlogPost(post.id);
			if (detail && detail.bodyMd) {
				bodyBlocks = parseMarkdown(detail.bodyMd);
			} else {
				bodyError = !detail;
			}
		} finally {
			bodyLoading = false;
		}
	}

	// ── Minimal, XSS-safe markdown → block list ───────────────────────
	// We render the returned blocks with Svelte markup (no {@html}), so
	// nothing in the post body can inject script. Supports headings,
	// unordered lists, fenced code, and paragraphs — enough for our posts.
	type MdBlock =
		| { kind: 'h'; level: number; text: string }
		| { kind: 'p'; text: string }
		| { kind: 'ul'; items: string[] }
		| { kind: 'code'; text: string };

	function parseMarkdown(md: string): MdBlock[] {
		const blocks: MdBlock[] = [];
		const lines = md.replace(/\r\n/g, '\n').split('\n');
		let para: string[] = [];
		let list: string[] = [];
		let code: string[] | null = null;

		const flushPara = () => {
			if (para.length) {
				blocks.push({ kind: 'p', text: para.join(' ').trim() });
				para = [];
			}
		};
		const flushList = () => {
			if (list.length) {
				blocks.push({ kind: 'ul', items: list.slice() });
				list = [];
			}
		};

		for (const raw of lines) {
			const line = raw;
			if (line.trim().startsWith('```')) {
				if (code === null) {
					flushPara();
					flushList();
					code = [];
				} else {
					blocks.push({ kind: 'code', text: code.join('\n') });
					code = null;
				}
				continue;
			}
			if (code !== null) {
				code.push(line);
				continue;
			}
			const heading = /^(#{1,4})\s+(.*)$/.exec(line.trim());
			if (heading) {
				flushPara();
				flushList();
				blocks.push({ kind: 'h', level: heading[1].length, text: heading[2].trim() });
				continue;
			}
			const item = /^[-*]\s+(.*)$/.exec(line.trim());
			if (item) {
				flushPara();
				list.push(item[1].trim());
				continue;
			}
			if (line.trim() === '') {
				flushPara();
				flushList();
				continue;
			}
			flushList();
			para.push(line.trim());
		}
		if (code !== null) blocks.push({ kind: 'code', text: code.join('\n') });
		flushPara();
		flushList();
		return blocks;
	}

	// ── Palette + per-category accent mapping (mirrors CyberddyneView) ─
	type Palette = 'blue' | 'green' | 'purple' | 'orange' | 'red';

	const paletteVars: Record<Palette, { accent: string; accentDark: string }> = {
		blue:   { accent: '#3b82f6', accentDark: '#1d4ed8' },
		green:  { accent: '#22c55e', accentDark: '#15803d' },
		purple: { accent: '#a855f7', accentDark: '#7e22ce' },
		orange: { accent: '#f97316', accentDark: '#c2410c' },
		red:    { accent: '#ef4444', accentDark: '#b91c1c' }
	};

	const categoryPalette: Record<string, Palette> = {
		Governance:     'purple',
		DeFi:           'green',
		Development:    'blue',
		Security:       'red',
		Economics:      'orange',
		Infrastructure: 'blue',
		NFTs:           'red',
		'UX/UI':        'purple'
	};

	const categoryBadgeVariant: Record<
		Palette,
		'info' | 'success' | 'warning' | 'danger' | 'neutral'
	> = {
		blue:   'info',
		green:  'success',
		purple: 'neutral',
		orange: 'warning',
		red:    'danger'
	};

	function catPal(category: string): Palette {
		return categoryPalette[category] ?? 'blue';
	}

	function palStyle(p: Palette): string {
		const v = paletteVars[p];
		return `--accent: ${v.accent}; --accent-dark: ${v.accentDark};`;
	}
</script>

<PixelScrollArea maxHeight="100%" ariaLabel="Cyberdyne Blog">
<div class="blog-view">
	<!-- Hero -->
	<header class="hero" style={palStyle('blue')}>
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">📰</span>
			<h1 class="hero__title">CYBERDYNE BLOG</h1>
		</div>
		<p class="hero__tagline">Latest insights on Web3, DeFi, DAOs &amp; blockchain technology.</p>
	</header>

	<div class="content">
		<!-- Sidebar column -->
		<aside class="sidebar">
			<!-- Categories card -->
			<section class="card" style={palStyle('blue')}>
				<h2 class="card__title">Categories</h2>
				<div class="cat-list">
					{#each categories as category}
						{@const pal = category.id === 'all' ? 'blue' : catPal(category.name)}
						<button
							type="button"
							class="cat-btn"
							class:cat-btn--active={$selectedCategory === category.id}
							style={palStyle(pal)}
							onclick={() => vm.selectCategory(category.id)}
						>
							<span class="cat-btn__icon" aria-hidden="true">{category.icon}</span>
							<span class="cat-btn__name">{category.name}</span>
							<Badge variant="neutral" size="sm">{category.count}</Badge>
						</button>
					{/each}
				</div>
			</section>

			<!-- Featured card -->
			{#if $selectedCategory === 'all' && featuredPosts.length > 0}
				<section class="card" style={palStyle('orange')}>
					<h2 class="card__title">⭐ Featured</h2>
					<div class="post-list">
						{#each featuredPosts as post}
							{@const pal = catPal(post.category)}
							<button
								type="button"
								class="post"
								class:post--active={$selectedPost?.id === post.id}
								style={palStyle(pal)}
								onclick={() => selectPost(post)}
							>
								<h4 class="post__title">{truncateTitle(post.title, 64)}</h4>
								<div class="post__meta">
									<span class="post__author">{post.author}</span>
									<Badge variant={categoryBadgeVariant[pal]} size="sm">
										{post.category}
									</Badge>
								</div>
							</button>
						{/each}
					</div>
				</section>
			{/if}

			<!-- Recent card -->
			<section class="card" style={palStyle('green')}>
				<h2 class="card__title">Recent Posts</h2>
				<div class="post-list">
					{#each $filteredPosts.slice(0, 8) as post}
						{@const pal = catPal(post.category)}
						<button
							type="button"
							class="post"
							class:post--active={$selectedPost?.id === post.id}
							style={palStyle(pal)}
							onclick={() => selectPost(post)}
						>
							<h4 class="post__title">{truncateTitle(post.title, 56)}</h4>
							<div class="post__meta">
								<span class="post__date">{formatDate(post.date)}</span>
								<span class="post__readtime">{post.readTime}</span>
							</div>
						</button>
					{/each}
					{#if $filteredPosts.length === 0}
						<p class="post-list__empty">No posts in this category yet.</p>
					{/if}
				</div>
			</section>
		</aside>

		<!-- Main column -->
		<main class="main">
			{#if $selectedPost}
				{@const pal = catPal($selectedPost.category)}
				<article class="card article" style={palStyle(pal)}>
					<header class="article__header">
						<div class="article__meta">
							<Badge variant={categoryBadgeVariant[pal]} size="sm">
								{$selectedPost.category}
							</Badge>
							<span class="article__date">{formatDate($selectedPost.date)}</span>
							<span class="article__sep">•</span>
							<span class="article__readtime">{$selectedPost.readTime}</span>
						</div>
						<h2 class="article__title">{$selectedPost.title}</h2>
						<p class="article__byline">By {$selectedPost.author}</p>
					</header>

					{#if $selectedPost.image}
						<img class="article__image" src={$selectedPost.image} alt={$selectedPost.title} />
					{/if}

					<p class="article__excerpt">{$selectedPost.excerpt}</p>

					{#if bodyLoading}
						<p class="article__loading">Loading article…</p>
					{:else if bodyBlocks.length > 0}
						<div class="article__body">
							{#each bodyBlocks as block}
								{#if block.kind === 'h'}
									{#if block.level <= 2}
										<h3 class="body-h">{block.text}</h3>
									{:else}
										<h4 class="body-h body-h--sm">{block.text}</h4>
									{/if}
								{:else if block.kind === 'ul'}
									<ul class="body-ul">
										{#each block.items as it}
											<li>{it}</li>
										{/each}
									</ul>
								{:else if block.kind === 'code'}
									<pre class="body-code">{block.text}</pre>
								{:else}
									<p class="body-p">{block.text}</p>
								{/if}
							{/each}
						</div>
					{:else if bodyError}
						<p class="article__loading">Full article unavailable right now.</p>
					{/if}

					{#if $selectedPost.tags && $selectedPost.tags.length > 0}
						<div class="tags">
							<h3 class="subsection-title">Tags</h3>
							<div class="tags__list">
								{#each $selectedPost.tags as tag}
									<span class="tag">{tag}</span>
								{/each}
							</div>
						</div>
					{/if}

					<div class="article__cta">
						<PixelButton variant="outline" size="md">👍 Like</PixelButton>
						<PixelButton variant="outline" size="md">🔗 Share</PixelButton>
					</div>
				</article>
			{:else}
				<section class="card welcome" style={palStyle('blue')}>
					<div class="welcome__intro">
						<span class="welcome__mark" aria-hidden="true">📰</span>
						<h2 class="card__title">Welcome to Cyberdyne Blog</h2>
						<p class="card__lead">
							Explore our latest insights on Web3 technology, DeFi protocols, and blockchain development.
						</p>
					</div>

					<div class="stat-grid">
						<div class="stat" style={palStyle('green')}>
							<div class="stat__icon" aria-hidden="true">📝</div>
							<div class="stat__value">{blogPosts.length}</div>
							<div class="stat__label">Articles</div>
							<div class="stat__sublabel">In-depth analysis</div>
						</div>
						<div class="stat" style={palStyle('blue')}>
							<div class="stat__icon" aria-hidden="true">👥</div>
							<div class="stat__value">Expert</div>
							<div class="stat__label">Authors</div>
							<div class="stat__sublabel">Industry leaders</div>
						</div>
						<div class="stat" style={palStyle('purple')}>
							<div class="stat__icon" aria-hidden="true">🔄</div>
							<div class="stat__value">Weekly</div>
							<div class="stat__label">Updates</div>
							<div class="stat__sublabel">Fresh content</div>
						</div>
					</div>
				</section>
			{/if}
		</main>
	</div>
</div>
</PixelScrollArea>

<style>
	.blog-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #ffffff;
		color: #111827;
		min-height: 100%;
	}

	/* ---------- Hero ---------- */
	.hero {
		padding: 22px 26px;
		background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
	}
	.hero__brand {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 8px;
	}
	.hero__mark { font-size: 1.6rem; }
	.hero__title {
		font-size: 1.625rem;
		font-weight: 800;
		margin: 0;
		letter-spacing: 0.12em;
		color: #ffffff;
	}
	.hero__tagline {
		margin: 0;
		font-size: 0.875rem;
		line-height: 1.55;
		color: #e0e7ff;
		max-width: 820px;
	}

	/* ---------- Content layout ---------- */
	.content {
		padding: 20px;
		display: grid;
		grid-template-columns: minmax(280px, 360px) minmax(0, 1fr);
		gap: 18px;
		max-width: 1200px;
		margin: 0 auto;
		align-items: start;
	}
	@media (max-width: 820px) {
		.content { grid-template-columns: minmax(0, 1fr); }
	}

	.sidebar, .main {
		display: flex;
		flex-direction: column;
		gap: 18px;
		min-width: 0;
	}

	/* ---------- Card primitive (mirrors CyberddyneView .card) ---------- */
	.card {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
		padding: 18px 18px 18px 26px;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	.card::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.card__title {
		font-size: 1.05rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--accent-dark);
		margin: 0;
	}
	.card__lead {
		font-size: 0.9rem;
		line-height: 1.6;
		color: #1f2937;
		margin: 0;
	}
	.subsection-title {
		font-size: 0.7rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: var(--accent-dark);
		font-weight: 700;
		margin: 0;
	}

	/* ---------- Categories ---------- */
	.cat-list {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.cat-btn {
		position: relative;
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 10px 8px 16px;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.35);
		font-family: inherit;
		font-size: 0.8125rem;
		font-weight: 600;
		color: #1f2937;
		cursor: pointer;
		text-align: left;
		transition: transform 0.1s ease, box-shadow 0.1s ease;
	}
	.cat-btn::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.cat-btn:hover {
		transform: translate(-1px, -1px);
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.45);
	}
	.cat-btn--active {
		background: color-mix(in srgb, var(--accent) 12%, #ffffff);
		color: var(--accent-dark);
	}
	.cat-btn__icon {
		flex: 0 0 auto;
		font-size: 0.95rem;
		line-height: 1;
	}
	.cat-btn__name {
		flex: 1 1 auto;
		min-width: 0;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	/* ---------- Post tiles ---------- */
	.post-list {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.post-list__empty {
		font-size: 0.8125rem;
		color: #6b7280;
		font-style: italic;
		margin: 0;
	}
	.post {
		position: relative;
		text-align: left;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 10px 12px 10px 18px;
		display: flex;
		flex-direction: column;
		gap: 6px;
		font-family: inherit;
		cursor: pointer;
		color: inherit;
		transition: transform 0.1s ease, box-shadow 0.1s ease;
	}
	.post::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.post:hover {
		transform: translate(-2px, -2px);
		box-shadow: 5px 5px 0 rgba(0, 0, 0, 0.5);
	}
	.post--active {
		background: color-mix(in srgb, var(--accent) 10%, #ffffff);
	}
	.post__title {
		font-size: 0.875rem;
		font-weight: 700;
		color: #000;
		margin: 0;
		line-height: 1.35;
		word-break: break-word;
	}
	.post__meta {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 6px;
		font-size: 0.6875rem;
		color: #4b5563;
	}
	.post__author { font-weight: 600; }
	.post__readtime { color: #6b7280; }

	/* ---------- Article view ---------- */
	.article { gap: 16px; }
	.article__header {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.article__meta {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		font-size: 0.75rem;
		color: #4b5563;
	}
	.article__sep { color: #9ca3af; }
	.article__title {
		font-size: 1.375rem;
		font-weight: 800;
		color: #000;
		margin: 0;
		line-height: 1.25;
	}
	.article__byline {
		margin: 0;
		font-size: 0.8125rem;
		color: #374151;
	}
	.article__image {
		width: 100%;
		max-height: 280px;
		object-fit: cover;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
	}
	.article__excerpt {
		font-size: 0.9375rem;
		line-height: 1.65;
		color: #1f2937;
		margin: 0;
		font-weight: 600;
	}
	.article__loading {
		font-size: 0.875rem;
		color: #6b7280;
		font-style: italic;
		margin: 0;
	}
	.article__body {
		display: flex;
		flex-direction: column;
		gap: 10px;
		border-top: 2px solid #000;
		padding-top: 14px;
	}
	.body-h {
		font-size: 1.05rem;
		font-weight: 800;
		color: #000;
		margin: 6px 0 0;
		line-height: 1.3;
	}
	.body-h--sm {
		font-size: 0.9rem;
		color: var(--accent-dark);
		text-transform: uppercase;
		letter-spacing: 0.04em;
	}
	.body-p {
		font-size: 0.9375rem;
		line-height: 1.65;
		color: #1f2937;
		margin: 0;
	}
	.body-ul {
		margin: 0;
		padding-left: 20px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.body-ul li {
		font-size: 0.9375rem;
		line-height: 1.5;
		color: #1f2937;
		list-style: square;
	}
	.body-code {
		margin: 0;
		padding: 10px 12px;
		background: #0b1120;
		color: #c9ffd9;
		border: 2px solid #000;
		font-size: 0.8125rem;
		overflow-x: auto;
		white-space: pre;
	}
	.tags {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.tags__list {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}
	.tag {
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 3px 8px;
		background: var(--accent);
		color: #ffffff;
		border: 1.5px solid #000;
		letter-spacing: 0.04em;
		text-transform: lowercase;
	}
	.article__cta {
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
		padding-top: 4px;
	}

	/* ---------- Welcome state ---------- */
	.welcome { gap: 18px; }
	.welcome__intro {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
		text-align: center;
		padding: 6px 0;
	}
	.welcome__mark { font-size: 2.25rem; }

	.stat-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 12px;
	}
	@media (max-width: 720px) {
		.stat-grid { grid-template-columns: minmax(0, 1fr); }
	}
	.stat {
		position: relative;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
		padding: 12px 12px 14px 18px;
		display: flex;
		flex-direction: column;
		gap: 2px;
	}
	.stat::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: var(--accent);
		border-right: 2px solid #000;
	}
	.stat__icon { font-size: 1.4rem; line-height: 1; margin-bottom: 4px; }
	.stat__value {
		font-size: 1.25rem;
		font-weight: 800;
		color: var(--accent-dark);
		line-height: 1.1;
	}
	.stat__label {
		font-size: 0.85rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: #000;
	}
	.stat__sublabel {
		font-size: 0.7rem;
		color: #6b7280;
		margin-top: 2px;
	}
</style>
