import type { MarketplaceItem, MarketplaceCategory } from '$lib/types/components';

export const marketplaceItems: MarketplaceItem[] = [
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

export function buildMarketplaceCategories(items: MarketplaceItem[]): MarketplaceCategory[] {
	return [
		{ id: 'all', name: 'All Products', icon: '🛍️', count: items.length, description: 'Browse all available products and services' },
		{ id: 'services', name: 'Services', icon: '⚙️', count: items.filter(i => i.category === 'Services').length, description: 'Custom development services' },
		{ id: 'training', name: 'Training Material', icon: '📚', count: items.filter(i => i.category === 'Training Material').length, description: 'Educational courses and materials' },
		{ id: 'licenses', name: 'Licenses', icon: '🔑', count: items.filter(i => i.category === 'Licenses').length, description: 'Software licenses and subscriptions' }
	];
}

export const marketplaceCategories = buildMarketplaceCategories(marketplaceItems);
