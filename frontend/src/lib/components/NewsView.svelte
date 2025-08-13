<script lang="ts">
	interface BlogPost {
		id: string;
		title: string;
		excerpt: string;
		category: string;
		author: string;
		date: string;
		readTime: string;
		tags: string[];
		featured?: boolean;
		image?: string;
	}

	interface BlogCategory {
		id: string;
		name: string;
		icon: string;
		count: number;
	}

	const blogPosts: BlogPost[] = [
		{
			id: 'dao-governance-evolution',
			title: 'The Evolution of DAO Governance: From Simple Voting to Complex Ecosystems',
			excerpt: 'Exploring how decentralized autonomous organizations have evolved from basic token voting to sophisticated governance mechanisms with delegation, quadratic voting, and multi-layered decision making.',
			category: 'Governance',
			author: 'Alex Chen',
			date: '2024-01-15',
			readTime: '8 min read',
			tags: ['DAO', 'Governance', 'DeFi', 'Blockchain'],
			featured: true,
			image: 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=150&h=150&fit=crop'
		},
		{
			id: 'web3-security-practices',
			title: 'Web3 Security Best Practices: Protecting Your dApps and Smart Contracts',
			excerpt: 'A comprehensive guide to securing Web3 applications, from smart contract audits to frontend security, wallet integrations, and common vulnerability prevention.',
			category: 'Security',
			author: 'Sarah Rodriguez',
			date: '2024-01-12',
			readTime: '12 min read',
			tags: ['Security', 'Smart Contracts', 'Web3', 'Audits'],
			featured: true,
			image: 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=150&h=150&fit=crop'
		},
		{
			id: 'defi-yield-strategies',
			title: 'Advanced DeFi Yield Strategies: Maximizing Returns in the New Economy',
			excerpt: 'Deep dive into sophisticated yield farming techniques, liquidity provision strategies, and risk management in decentralized finance protocols.',
			category: 'DeFi',
			author: 'Marcus Thompson',
			date: '2024-01-10',
			readTime: '10 min read',
			tags: ['DeFi', 'Yield Farming', 'Liquidity', 'Finance'],
			featured: false,
			image: 'https://images.unsplash.com/photo-1641580318252-8c4e5c3aaf8f?w=150&h=150&fit=crop'
		},
		{
			id: 'cosmos-ibc-guide',
			title: 'Building Cross-Chain Applications with Cosmos IBC Protocol',
			excerpt: 'Learn how to leverage the Inter-Blockchain Communication protocol to build applications that span multiple blockchain networks in the Cosmos ecosystem.',
			category: 'Development',
			author: 'Dr. Lisa Wang',
			date: '2024-01-08',
			readTime: '15 min read',
			tags: ['Cosmos', 'IBC', 'Cross-chain', 'Development'],
			featured: false,
			image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=150&h=150&fit=crop'
		},
		{
			id: 'tokenomics-design',
			title: 'Tokenomics Design: Creating Sustainable Economic Models for Web3',
			excerpt: 'Understanding the principles of tokenomics design, from incentive alignment to value accrual mechanisms and long-term sustainability.',
			category: 'Economics',
			author: 'Robert Kim',
			date: '2024-01-05',
			readTime: '9 min read',
			tags: ['Tokenomics', 'Economics', 'Token Design', 'Incentives'],
			featured: false,
			image: 'https://images.unsplash.com/photo-1559526323-cb2f2fe2591b?w=150&h=150&fit=crop'
		},
		{
			id: 'nft-marketplace-future',
			title: 'The Future of NFT Marketplaces: Beyond JPEGs to Utility and Governance',
			excerpt: 'Exploring the evolution of NFT marketplaces from simple art trading to complex utility tokens, governance rights, and membership systems.',
			category: 'NFTs',
			author: 'Emma Johnson',
			date: '2024-01-03',
			readTime: '7 min read',
			tags: ['NFTs', 'Marketplace', 'Utility', 'Digital Assets'],
			featured: false,
			image: 'https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?w=150&h=150&fit=crop'
		},
		{
			id: 'scaling-ethereum-l2',
			title: 'Scaling Ethereum: Layer 2 Solutions and the Multi-Chain Future',
			excerpt: 'Comprehensive analysis of Ethereum scaling solutions including Optimistic Rollups, ZK-Rollups, and the emerging multi-chain ecosystem.',
			category: 'Infrastructure',
			author: 'David Park',
			date: '2024-01-01',
			readTime: '11 min read',
			tags: ['Ethereum', 'Layer 2', 'Scaling', 'Infrastructure'],
			featured: false,
			image: 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=150&h=150&fit=crop'
		},
		{
			id: 'web3-user-experience',
			title: 'Improving Web3 User Experience: Bridging the Gap to Mass Adoption',
			excerpt: 'Examining the current state of Web3 UX and strategies for creating more intuitive, accessible decentralized applications.',
			category: 'UX/UI',
			author: 'Nina Patel',
			date: '2023-12-28',
			readTime: '6 min read',
			tags: ['UX/UI', 'Web3', 'User Experience', 'Adoption'],
			featured: false,
			image: 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=150&h=150&fit=crop'
		}
	];

	const categories: BlogCategory[] = [
		{ id: 'all', name: 'All Posts', icon: '📰', count: blogPosts.length },
		{ id: 'governance', name: 'Governance', icon: '🏛️', count: blogPosts.filter(p => p.category === 'Governance').length },
		{ id: 'defi', name: 'DeFi', icon: '💰', count: blogPosts.filter(p => p.category === 'DeFi').length },
		{ id: 'development', name: 'Development', icon: '💻', count: blogPosts.filter(p => p.category === 'Development').length },
		{ id: 'security', name: 'Security', icon: '🛡️', count: blogPosts.filter(p => p.category === 'Security').length },
		{ id: 'economics', name: 'Economics', icon: '📊', count: blogPosts.filter(p => p.category === 'Economics').length },
		{ id: 'infrastructure', name: 'Infrastructure', icon: '🌐', count: blogPosts.filter(p => p.category === 'Infrastructure').length }
	];

	let selectedCategory = 'all';
	let selectedPost: BlogPost | null = null;

	$: filteredPosts = selectedCategory === 'all' 
		? blogPosts 
		: blogPosts.filter(post => post.category.toLowerCase() === selectedCategory.toLowerCase());

	$: featuredPosts = blogPosts.filter(post => post.featured);

	function selectPost(post: BlogPost) {
		selectedPost = post;
	}

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString('en-US', { 
			year: 'numeric', 
			month: 'short', 
			day: 'numeric' 
		});
	}

	function getCategoryColor(category: string) {
		switch(category) {
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
							class:bg-blue-100={selectedCategory === category.id}
							class:text-blue-700={selectedCategory === category.id}
							class:font-bold={selectedCategory === category.id}
							on:click={() => selectedCategory = category.id}
						>
							<span>{category.icon}</span>
							<span class="flex-1">{category.name}</span>
							<span class="text-gray-500">({category.count})</span>
						</button>
					{/each}
				</div>
			</div>

			<!-- Featured Posts -->
			{#if selectedCategory === 'all'}
				<div class="p-2 border-t border-gray-200">
					<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">⭐ Featured</h3>
					<div class="space-y-2">
						{#each featuredPosts as post}
							<div 
								class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
								class:ring-2={selectedPost?.id === post.id}
								class:ring-blue-400={selectedPost?.id === post.id}
								on:click={() => selectPost(post)}
								role="button"
								tabindex="0"
							>
								<h4 class="font-mono font-bold text-xs leading-tight mb-1">{post.title.length > 60 ? post.title.substring(0, 60) + '...' : post.title}</h4>
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
					{#each filteredPosts.slice(0, 8) as post}
						<div 
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={selectedPost?.id === post.id}
							class:ring-blue-400={selectedPost?.id === post.id}
							on:click={() => selectPost(post)}
							role="button"
							tabindex="0"
						>
							<h4 class="font-mono font-bold text-xs leading-tight mb-1">{post.title.length > 50 ? post.title.substring(0, 50) + '...' : post.title}</h4>
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
			{#if selectedPost}
				<div class="p-3">
					<div class="mb-3">
						<div class="flex items-center gap-2 mb-2">
							<span class="text-xs px-2 py-0.5 rounded font-mono {getCategoryColor(selectedPost.category)}">
								{selectedPost.category}
							</span>
							<span class="text-xs text-gray-600 font-mono">{formatDate(selectedPost.date)}</span>
							<span class="text-xs text-gray-500 font-mono">• {selectedPost.readTime}</span>
						</div>
						<h2 class="text-lg font-bold font-mono text-gray-800 mb-2 leading-tight">{selectedPost.title}</h2>
						<div class="flex items-center gap-2 mb-2">
							<span class="text-xs text-gray-600 font-mono">By {selectedPost.author}</span>
						</div>
					</div>

					{#if selectedPost.image}
						<div class="mb-3">
							<img 
								src={selectedPost.image} 
								alt={selectedPost.title}
								class="w-full h-32 object-cover rounded border border-gray-200"
							/>
						</div>
					{/if}

					<div class="mb-3">
						<p class="text-sm text-gray-700 leading-relaxed font-mono">{selectedPost.excerpt}</p>
					</div>

					<div class="mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">🏷️ Tags</h3>
						<div class="flex flex-wrap gap-1">
							{#each selectedPost.tags as tag}
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

