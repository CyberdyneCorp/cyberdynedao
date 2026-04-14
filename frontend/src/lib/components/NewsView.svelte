<script lang="ts">
	import type { BlogPost } from '$lib/types/components';
	import { formatDate } from '$lib/utils/formatters';
	import {
		createNewsViewModel,
		getBlogCategoryColor as getCategoryColor,
		truncateTitle
	} from '$lib/viewmodels/newsViewModel';

	export const isMobile: boolean = false;

	const vm = createNewsViewModel();
	const { selectedCategory, selectedPost, filteredPosts } = vm;
	const { posts: blogPosts, categories, featuredPosts } = vm;

	function selectPost(post: BlogPost) {
		vm.selectPost(post);
	}
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<!-- Header -->
	<div class="bg-gradient-to-r from-green-600 to-blue-600 p-2 border-b-2 border-black">
		<h1 class="text-lg font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-xl">📰</span>
			CYBERDYNE BLOG
		</h1>
		<p class="font-mono text-xs text-black">Latest insights on Web3, DeFi, DAOs & Blockchain Technology</p>
	</div>

	<div class="flex-1 flex">
		<!-- Sidebar -->
		<div class="w-1/3 border-r border-gray-200 bg-gray-50 overflow-y-auto">
			<!-- Categories -->
			<div class="p-2">
				<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">Categories</h3>
				<div class="space-y-1">
					{#each categories as category}
						<button
							class="w-full text-left px-2 py-1 text-xs font-mono rounded transition-colors flex items-center gap-1.5"
							class:bg-blue-100={$selectedCategory === category.id}
							class:text-blue-700={$selectedCategory === category.id}
							class:font-bold={$selectedCategory === category.id}
							on:click={() => vm.selectCategory(category.id)}
						>
							<span>{category.icon}</span>
							<span class="flex-1">{category.name}</span>
							<span class="text-gray-500">({category.count})</span>
						</button>
					{/each}
				</div>
			</div>

			<!-- Featured Posts -->
			{#if $selectedCategory === 'all'}
				<div class="p-2 border-t border-gray-200">
					<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">⭐ Featured</h3>
					<div class="space-y-2">
						{#each featuredPosts as post}
							<div
								class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
								class:ring-2={$selectedPost?.id === post.id}
								class:ring-blue-400={$selectedPost?.id === post.id}
								on:click={() => selectPost(post)}
								on:keydown={(e) => e.key === 'Enter' && selectPost(post)}
								role="button"
								tabindex="0"
							>
								<h4 class="font-mono font-bold text-xs leading-tight mb-1">{truncateTitle(post.title, 60)}</h4>
								<div class="flex items-center justify-between text-xs">
									<span class="text-gray-600 font-mono">{post.author}</span>
									<span class="px-1.5 py-0.5 rounded font-mono {getCategoryColor(post.category)}">
										{post.category}
									</span>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Recent Posts List -->
			<div class="p-2 border-t border-gray-200">
				<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">Recent Posts</h3>
				<div class="space-y-1.5">
					{#each $filteredPosts.slice(0, 8) as post}
						<div
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={$selectedPost?.id === post.id}
							class:ring-blue-400={$selectedPost?.id === post.id}
							on:click={() => selectPost(post)}
							on:keydown={(e) => e.key === 'Enter' && selectPost(post)}
							role="button"
							tabindex="0"
						>
							<h4 class="font-mono font-bold text-xs leading-tight mb-1">{truncateTitle(post.title, 50)}</h4>
							<div class="flex items-center justify-between text-xs">
								<span class="text-gray-600 font-mono">{formatDate(post.date)}</span>
								<span class="text-gray-500 font-mono">{post.readTime}</span>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<!-- Main Content -->
		<div class="flex-1 overflow-y-auto">
			{#if $selectedPost}
				<div class="p-3">
					<div class="mb-3">
						<div class="flex items-center gap-2 mb-2">
							<span class="text-xs px-2 py-0.5 rounded font-mono {getCategoryColor($selectedPost.category)}">
								{$selectedPost.category}
							</span>
							<span class="text-xs text-gray-600 font-mono">{formatDate($selectedPost.date)}</span>
							<span class="text-xs text-gray-500 font-mono">• {$selectedPost.readTime}</span>
						</div>
						<h2 class="text-lg font-bold font-mono text-gray-800 mb-2 leading-tight">{$selectedPost.title}</h2>
						<div class="flex items-center gap-2 mb-2">
							<span class="text-xs text-gray-600 font-mono">By {$selectedPost.author}</span>
						</div>
					</div>

					{#if $selectedPost.image}
						<div class="mb-3">
							<img
								src={$selectedPost.image}
								alt={$selectedPost.title}
								class="w-full h-32 object-cover rounded border border-gray-200"
							/>
						</div>
					{/if}

					<div class="mb-3">
						<p class="text-sm text-gray-700 leading-relaxed font-mono">{$selectedPost.excerpt}</p>
					</div>

					<div class="mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">🏷️ Tags</h3>
						<div class="flex flex-wrap gap-1">
							{#each $selectedPost.tags as tag}
								<span class="text-xs px-2 py-0.5 bg-gray-100 text-gray-700 rounded font-mono border">
									{tag}
								</span>
							{/each}
						</div>
					</div>

					<div class="bg-gray-50 rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">📖 Full Article</h3>
						<p class="text-xs text-gray-600 font-mono mb-2">This is a preview of the blog post. The full article contains detailed technical explanations, code examples, and comprehensive analysis.</p>
						<button class="bg-blue-600 text-white px-3 py-1.5 rounded font-mono text-xs font-bold hover:bg-blue-700 transition-colors">
							Read Full Article
						</button>
					</div>

					<div class="flex gap-2">
						<button class="border border-gray-300 text-gray-700 px-3 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							👍 Like
						</button>
						<button class="border border-gray-300 text-gray-700 px-3 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							💬 Comment
						</button>
						<button class="border border-gray-300 text-gray-700 px-3 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							🔗 Share
						</button>
					</div>
				</div>
			{:else}
				<div class="p-3 text-center">
					<div class="text-3xl mb-2">📰</div>
					<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">Welcome to Cyberdyne Blog</h2>
					<p class="text-sm text-gray-600 font-mono mb-4">Explore our latest insights on Web3 technology, DeFi protocols, and blockchain development.</p>

					<div class="grid grid-cols-3 gap-2">
						<div class="bg-green-50 rounded border border-green-200 p-2">
							<div class="text-lg mb-1">📝</div>
							<h3 class="font-mono font-bold text-xs">{blogPosts.length} Articles</h3>
							<p class="text-xs text-gray-600">In-depth analysis</p>
						</div>
						<div class="bg-blue-50 rounded border border-blue-200 p-2">
							<div class="text-lg mb-1">👥</div>
							<h3 class="font-mono font-bold text-xs">Expert Authors</h3>
							<p class="text-xs text-gray-600">Industry leaders</p>
						</div>
						<div class="bg-purple-50 rounded border border-purple-200 p-2">
							<div class="text-lg mb-1">🔄</div>
							<h3 class="font-mono font-bold text-xs">Weekly Updates</h3>
							<p class="text-xs text-gray-600">Fresh content</p>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>

