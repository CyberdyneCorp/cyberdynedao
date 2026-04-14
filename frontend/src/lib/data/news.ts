import type { BlogPost, BlogCategory } from '$lib/types/components';

export const blogPosts: BlogPost[] = [
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

export function buildBlogCategories(posts: BlogPost[]): BlogCategory[] {
	return [
		{ id: 'all', name: 'All Posts', icon: '📰', count: posts.length },
		{ id: 'governance', name: 'Governance', icon: '🏛️', count: posts.filter(p => p.category === 'Governance').length },
		{ id: 'defi', name: 'DeFi', icon: '💰', count: posts.filter(p => p.category === 'DeFi').length },
		{ id: 'development', name: 'Development', icon: '💻', count: posts.filter(p => p.category === 'Development').length },
		{ id: 'security', name: 'Security', icon: '🛡️', count: posts.filter(p => p.category === 'Security').length },
		{ id: 'economics', name: 'Economics', icon: '📊', count: posts.filter(p => p.category === 'Economics').length },
		{ id: 'infrastructure', name: 'Infrastructure', icon: '🌐', count: posts.filter(p => p.category === 'Infrastructure').length }
	];
}

export const blogCategories = buildBlogCategories(blogPosts);
