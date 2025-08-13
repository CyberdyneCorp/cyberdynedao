<script lang="ts">
	export let onAddToCart: ((item: any) => void) | undefined = undefined;

	interface MarketplaceItem {
		id: string;
		title: string;
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

	interface MarketplaceCategory {
		id: string;
		name: string;
		icon: string;
		count: number;
		description: string;
	}

	const marketplaceItems: MarketplaceItem[] = [
		// Services - Frontend
		{
			id: 'frontend-webapp',
			title: 'Custom Web Application',
			description: 'Full-stack web application development with modern React/Svelte frontend, responsive design, and seamless user experience.',
			category: 'Services',
			subcategory: 'Frontend',
			price: 5000,
			duration: '4-8 weeks',
			features: ['React/Svelte/Vue', 'Responsive Design', 'TypeScript', 'Tailwind CSS', 'Component Library'],
			popular: true,
			image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'frontend-dapp',
			title: 'Web3 dApp Frontend',
			description: 'Modern decentralized application frontend with wallet integration, smart contract interaction, and Web3 UX patterns.',
			category: 'Services',
			subcategory: 'Frontend',
			price: 7500,
			duration: '6-10 weeks',
			features: ['Wallet Integration', 'Smart Contract UI', 'Web3 Libraries', 'IPFS Storage', 'MetaMask Support'],
			popular: true,
			image: 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'frontend-dashboard',
			title: 'Analytics Dashboard',
			description: 'Custom analytics dashboard with real-time data visualization, charts, and comprehensive reporting features.',
			category: 'Services',
			subcategory: 'Frontend',
			price: 4000,
			duration: '3-6 weeks',
			features: ['Chart.js/D3.js', 'Real-time Updates', 'Data Export', 'Custom Widgets', 'Mobile Responsive'],
			image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=150&h=150&fit=crop',
			status: 'available'
		},
		// Services - Backend
		{
			id: 'backend-api',
			title: 'REST API Development',
			description: 'Scalable REST API with authentication, database integration, and comprehensive documentation.',
			category: 'Services',
			subcategory: 'Backend',
			price: 6000,
			duration: '4-8 weeks',
			features: ['Node.js/Python', 'Database Design', 'Authentication', 'API Documentation', 'Testing Suite'],
			popular: true,
			image: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'backend-blockchain',
			title: 'Blockchain Backend',
			description: 'Custom blockchain integration with smart contract deployment, indexing, and Web3 infrastructure.',
			category: 'Services',
			subcategory: 'Backend',
			price: 8500,
			duration: '6-12 weeks',
			features: ['Smart Contracts', 'Web3 Integration', 'Blockchain Indexing', 'IPFS Backend', 'Event Listeners'],
			popular: true,
			image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'backend-microservices',
			title: 'Microservices Architecture',
			description: 'Scalable microservices architecture with containerization, load balancing, and monitoring.',
			category: 'Services',
			subcategory: 'Backend',
			price: 12000,
			duration: '8-16 weeks',
			features: ['Docker/Kubernetes', 'Service Mesh', 'Load Balancing', 'Monitoring', 'CI/CD Pipeline'],
			image: 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=150&h=150&fit=crop',
			status: 'available'
		},
		// Training Materials
		{
			id: 'training-web3-basics',
			title: 'Web3 Development Fundamentals',
			description: 'Comprehensive course covering blockchain basics, smart contracts, and dApp development from scratch.',
			category: 'Training Material',
			price: 299,
			duration: '40 hours',
			features: ['Video Lectures', 'Hands-on Projects', 'Code Examples', 'Certificate', 'Community Access'],
			popular: true,
			image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'training-solidity-advanced',
			title: 'Advanced Solidity Programming',
			description: 'Deep dive into Solidity optimization, security patterns, and complex smart contract architecture.',
			category: 'Training Material',
			price: 399,
			duration: '60 hours',
			features: ['Advanced Patterns', 'Security Auditing', 'Gas Optimization', 'Testing Frameworks', 'Real Projects'],
			popular: true,
			image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'training-defi-protocols',
			title: 'DeFi Protocol Development',
			description: 'Learn to build DeFi protocols including AMMs, lending platforms, and yield farming contracts.',
			category: 'Training Material',
			price: 499,
			duration: '80 hours',
			features: ['AMM Development', 'Lending Protocols', 'Yield Strategies', 'Tokenomics', 'Live Deployment'],
			image: 'https://images.unsplash.com/photo-1641580318252-8c4e5c3aaf8f?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'training-dao-governance',
			title: 'DAO Governance & Operations',
			description: 'Complete guide to DAO creation, governance mechanisms, and community management strategies.',
			category: 'Training Material',
			price: 349,
			duration: '50 hours',
			features: ['Governance Design', 'Token Models', 'Voting Systems', 'Treasury Management', 'Case Studies'],
			image: 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=150&h=150&fit=crop',
			status: 'available'
		},
		// Licenses
		{
			id: 'license-trade4me',
			title: 'Trade4Me License',
			description: 'Advanced algorithmic trading platform with AI-powered market analysis and automated execution strategies.',
			category: 'Licenses',
			price: 2499,
			duration: '1 year',
			features: ['AI Trading Algorithms', 'Market Analysis', 'Risk Management', 'Portfolio Optimization', 'API Access'],
			popular: true,
			image: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'license-liquidity4me',
			title: 'Liquidity4Me License',
			description: 'DeFi liquidity management platform with yield optimization, impermanent loss protection, and automated rebalancing.',
			category: 'Licenses',
			price: 1999,
			duration: '1 year',
			features: ['Yield Optimization', 'LP Management', 'Risk Analysis', 'Auto-rebalancing', 'Multi-chain Support'],
			popular: true,
			image: 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=150&h=150&fit=crop',
			status: 'available'
		},
		{
			id: 'license-study4me',
			title: 'Study4Me License',
			description: 'AI-powered learning platform with personalized curricula, progress tracking, and skill assessment for Web3 education.',
			category: 'Licenses',
			price: 799,
			duration: '1 year',
			features: ['Personalized Learning', 'Progress Tracking', 'Skill Assessment', 'Certification', 'Mentor Access'],
			image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=150&h=150&fit=crop',
			status: 'beta'
		},
		{
			id: 'license-surf4me',
			title: 'Surf4Me License',
			description: 'Intelligent Web3 navigation and discovery platform with curated content, trend analysis, and research tools.',
			category: 'Licenses',
			price: 599,
			duration: '1 year',
			features: ['Content Curation', 'Trend Analysis', 'Research Tools', 'Bookmark Management', 'Team Collaboration'],
			image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=150&h=150&fit=crop',
			status: 'coming-soon'
		}
	];

	const categories: MarketplaceCategory[] = [
		{ 
			id: 'all', 
			name: 'All Products', 
			icon: '🛍️', 
			count: marketplaceItems.length,
			description: 'Browse all available products and services'
		},
		{ 
			id: 'services', 
			name: 'Services', 
			icon: '⚙️', 
			count: marketplaceItems.filter(item => item.category === 'Services').length,
			description: 'Custom development services'
		},
		{ 
			id: 'training', 
			name: 'Training Material', 
			icon: '📚', 
			count: marketplaceItems.filter(item => item.category === 'Training Material').length,
			description: 'Educational courses and materials'
		},
		{ 
			id: 'licenses', 
			name: 'Licenses', 
			icon: '🔑', 
			count: marketplaceItems.filter(item => item.category === 'Licenses').length,
			description: 'Software licenses and subscriptions'
		}
	];

	let selectedCategory = 'all';
	let selectedItem: MarketplaceItem | null = null;

	$: filteredItems = selectedCategory === 'all' 
		? marketplaceItems 
		: marketplaceItems.filter(item => item.category.toLowerCase().replace(' ', '') === selectedCategory);

	$: popularItems = marketplaceItems.filter(item => item.popular);

	function selectItem(item: MarketplaceItem) {
		selectedItem = item;
	}

	function addToCart(item: MarketplaceItem) {
		if (onAddToCart) {
			onAddToCart(item);
		}
	}

	function getCategoryColor(category: string) {
		switch(category) {
			case 'Services': return 'text-blue-600 bg-blue-100';
			case 'Training Material': return 'text-green-600 bg-green-100';
			case 'Licenses': return 'text-purple-600 bg-purple-100';
			default: return 'text-gray-600 bg-gray-100';
		}
	}

	function getStatusColor(status: string) {
		switch(status) {
			case 'available': return 'text-green-600 bg-green-100';
			case 'beta': return 'text-yellow-600 bg-yellow-100';
			case 'coming-soon': return 'text-orange-600 bg-orange-100';
			default: return 'text-gray-600 bg-gray-100';
		}
	}

	function getStatusText(status: string) {
		switch(status) {
			case 'available': return 'Available';
			case 'beta': return 'Beta';
			case 'coming-soon': return 'Coming Soon';
			default: return 'Unknown';
		}
	}

	function formatPrice(price: number) {
		return price >= 1000 ? `$${(price / 1000).toFixed(1)}k` : `$${price}`;
	}
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<!-- Header -->
	<div class="bg-gradient-to-r from-orange-600 to-red-600 p-2 border-b-2 border-black">
		<h1 class="text-lg font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-xl">🛍️</span>
			CYBERDYNE MARKETPLACE
		</h1>
		<p class="font-mono text-xs text-black">Professional services • Training materials • Software licenses</p>
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
							class:bg-orange-100={selectedCategory === category.id}
							class:text-orange-700={selectedCategory === category.id}
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

			<!-- Popular Items -->
			{#if selectedCategory === 'all'}
				<div class="p-2 border-t border-gray-200">
					<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">⭐ Popular</h3>
					<div class="space-y-1.5">
						{#each popularItems.slice(0, 4) as item}
							<div 
								class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
								class:ring-2={selectedItem?.id === item.id}
								class:ring-orange-400={selectedItem?.id === item.id}
								on:click={() => selectItem(item)}
								role="button"
								tabindex="0"
							>
								<h4 class="font-mono font-bold text-xs leading-tight mb-1">{item.title}</h4>
								<div class="flex items-center justify-between text-xs">
									<span class="px-1.5 py-0.5 rounded font-mono {getCategoryColor(item.category)}">
										{item.category}
									</span>
									<span class="text-gray-600 font-mono font-bold">{formatPrice(item.price)}</span>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Items List -->
			<div class="p-2 border-t border-gray-200">
				<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">
					{selectedCategory === 'all' ? 'All Products' : categories.find(c => c.id === selectedCategory)?.name}
				</h3>
				<div class="space-y-1.5">
					{#each filteredItems.slice(0, 8) as item}
						<div 
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={selectedItem?.id === item.id}
							class:ring-orange-400={selectedItem?.id === item.id}
							on:click={() => selectItem(item)}
							role="button"
							tabindex="0"
						>
							<div class="flex items-center gap-1 mb-1">
								<h4 class="font-mono font-bold text-xs leading-tight flex-1">{item.title}</h4>
								{#if item.popular}
									<span class="text-xs">⭐</span>
								{/if}
							</div>
							<div class="flex items-center justify-between text-xs mb-0.5">
								<span class="px-1.5 py-0.5 rounded font-mono {getCategoryColor(item.category)}">
									{item.subcategory || item.category}
								</span>
								<span class="px-1.5 py-0.5 rounded font-mono {getStatusColor(item.status)}">
									{getStatusText(item.status)}
								</span>
							</div>
							<div class="flex items-center justify-between text-xs">
								<span class="text-gray-600 font-mono">{item.duration || 'Custom'}</span>
								<span class="text-gray-800 font-mono font-bold">{formatPrice(item.price)}</span>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<!-- Main Content -->
		<div class="flex-1 overflow-y-auto">
			{#if selectedItem}
				<div class="p-3">
					<div class="flex items-start gap-2 mb-3">
						<img 
							src={selectedItem.image} 
							alt={selectedItem.title}
							class="w-16 h-16 object-cover rounded border border-gray-200"
						/>
						<div class="flex-1">
							<div class="flex items-center gap-2 mb-1">
								<h2 class="text-lg font-bold font-mono text-gray-800">{selectedItem.title}</h2>
								{#if selectedItem.popular}
									<span class="text-lg">⭐</span>
								{/if}
							</div>
							<div class="flex items-center gap-2 mb-2">
								<span class="text-xs px-2 py-0.5 rounded font-mono {getCategoryColor(selectedItem.category)}">
									{selectedItem.subcategory || selectedItem.category}
								</span>
								<span class="text-xs px-2 py-0.5 rounded font-mono {getStatusColor(selectedItem.status)}">
									{getStatusText(selectedItem.status)}
								</span>
								{#if selectedItem.duration}
									<span class="text-xs text-gray-600 font-mono">⏱️ {selectedItem.duration}</span>
								{/if}
							</div>
							<p class="text-sm text-gray-700 leading-relaxed">{selectedItem.description}</p>
						</div>
					</div>

					<div class="bg-gray-50 rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">✨ Features Included</h3>
						<div class="grid grid-cols-2 gap-1">
							{#each selectedItem.features as feature}
								<div class="flex items-center gap-1 text-xs">
									<span class="text-green-500">✓</span>
									<span class="font-mono">{feature}</span>
								</div>
							{/each}
						</div>
					</div>

					<div class="bg-orange-50 rounded border border-orange-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">💰 Pricing</h3>
						<div class="flex items-center gap-4">
							<div>
								<span class="text-2xl font-bold font-mono text-orange-600">${selectedItem.price.toLocaleString()}</span>
								{#if selectedItem.duration}
									<span class="text-xs text-gray-600 font-mono">/ {selectedItem.duration}</span>
								{/if}
							</div>
							{#if selectedItem.category === 'Services'}
								<div class="text-xs text-gray-600 font-mono">
									<p>• Custom quote based on requirements</p>
									<p>• 50% upfront, 50% on completion</p>
								</div>
							{:else if selectedItem.category === 'Licenses'}
								<div class="text-xs text-gray-600 font-mono">
									<p>• Annual subscription</p>
									<p>• Full access and updates included</p>
								</div>
							{:else}
								<div class="text-xs text-gray-600 font-mono">
									<p>• Lifetime access</p>
									<p>• All future updates included</p>
								</div>
							{/if}
						</div>
					</div>

					<div class="flex gap-2">
						<button 
							class="bg-orange-600 text-white px-4 py-1.5 rounded font-mono text-xs font-bold hover:bg-orange-700 transition-colors"
							class:opacity-50={selectedItem.status === 'coming-soon'}
							class:cursor-not-allowed={selectedItem.status === 'coming-soon'}
							disabled={selectedItem.status === 'coming-soon'}
							on:click={() => addToCart(selectedItem)}
						>
							{selectedItem.status === 'coming-soon' ? 'Coming Soon' : 'Add to Cart'}
						</button>
						<button class="border border-gray-300 text-gray-700 px-4 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							💬 Contact Sales
						</button>
						<button class="border border-gray-300 text-gray-700 px-4 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							❤️ Wishlist
						</button>
					</div>
				</div>
			{:else}
				<div class="p-3 text-center">
					<div class="text-3xl mb-2">🛍️</div>
					<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">Cyberdyne Marketplace</h2>
					<p class="text-sm text-gray-600 font-mono mb-4">Discover professional services, training materials, and software licenses for Web3 development.</p>
					
					<div class="grid grid-cols-3 gap-2">
						<div class="bg-blue-50 rounded border border-blue-200 p-2">
							<div class="text-lg mb-1">⚙️</div>
							<h3 class="font-mono font-bold text-xs">Services</h3>
							<p class="text-xs text-gray-600">Custom development</p>
						</div>
						<div class="bg-green-50 rounded border border-green-200 p-2">
							<div class="text-lg mb-1">📚</div>
							<h3 class="font-mono font-bold text-xs">Training</h3>
							<p class="text-xs text-gray-600">Learn & grow</p>
						</div>
						<div class="bg-purple-50 rounded border border-purple-200 p-2">
							<div class="text-lg mb-1">🔑</div>
							<h3 class="font-mono font-bold text-xs">Licenses</h3>
							<p class="text-xs text-gray-600">Software access</p>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>

