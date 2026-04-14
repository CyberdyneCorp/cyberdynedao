import type { LearningModule, LearningPath } from '$lib/types/components';

export const learningModules: LearningModule[] = [
	{
		id: 'blockchain-basics',
		title: 'Blockchain Fundamentals',
		category: 'Blockchain',
		description: 'Learn the core concepts of blockchain technology, including distributed ledgers, consensus mechanisms, and cryptographic hashing.',
		level: 'Beginner',
		duration: '45 min',
		icon: '🔗',
		topics: ['Distributed Ledgers', 'Consensus Mechanisms', 'Cryptographic Hashing', 'Blocks & Transactions'],
		completed: false
	},
	{
		id: 'smart-contracts',
		title: 'Smart Contracts Deep Dive',
		category: 'Development',
		description: 'Understand how smart contracts work, their applications, and best practices for development.',
		level: 'Intermediate',
		duration: '1h 30min',
		icon: '📜',
		topics: ['Solidity Basics', 'Contract Security', 'Gas Optimization', 'Testing Frameworks'],
		completed: false
	},
	{
		id: 'dao-governance',
		title: 'DAO Governance & Structure',
		category: 'Governance',
		description: 'Explore decentralized autonomous organizations, governance tokens, and voting mechanisms.',
		level: 'Intermediate',
		duration: '1h 15min',
		icon: '🏛️',
		topics: ['Token-based Voting', 'Proposal Systems', 'Treasury Management', 'Community Building'],
		completed: false
	},
	{
		id: 'defi-protocols',
		title: 'DeFi Protocols & Yield Farming',
		category: 'DeFi',
		description: 'Learn about decentralized finance protocols, liquidity provision, and yield generation strategies.',
		level: 'Advanced',
		duration: '2h',
		icon: '💰',
		topics: ['AMM Design', 'Liquidity Mining', 'Yield Strategies', 'Risk Management'],
		completed: false
	},
	{
		id: 'web3-development',
		title: 'Web3 Frontend Development',
		category: 'Development',
		description: 'Build modern Web3 applications with React, Web3.js, and wallet integrations.',
		level: 'Intermediate',
		duration: '2h 30min',
		icon: '🌐',
		topics: ['Wallet Integration', 'Contract Interaction', 'IPFS Storage', 'Frontend Libraries'],
		completed: false
	},
	{
		id: 'tokenomics',
		title: 'Tokenomics & Economic Models',
		category: 'Economics',
		description: 'Design sustainable token economies with proper incentive mechanisms and distribution models.',
		level: 'Advanced',
		duration: '1h 45min',
		icon: '🎯',
		topics: ['Token Distribution', 'Incentive Design', 'Inflation Models', 'Value Accrual'],
		completed: false
	},
	{
		id: 'cosmos-sdk',
		title: 'Cosmos SDK & IBC',
		category: 'Infrastructure',
		description: 'Build sovereign blockchains using Cosmos SDK and enable cross-chain communication.',
		level: 'Advanced',
		duration: '3h',
		icon: '🌌',
		topics: ['Tendermint Consensus', 'Module Development', 'IBC Protocol', 'Chain Governance'],
		completed: false
	},
	{
		id: 'cybersecurity-web3',
		title: 'Web3 Security Best Practices',
		category: 'Security',
		description: 'Learn about common vulnerabilities and security practices in Web3 development.',
		level: 'Intermediate',
		duration: '1h 20min',
		icon: '🛡️',
		topics: ['Smart Contract Audits', 'Wallet Security', 'Bridge Vulnerabilities', 'Social Engineering'],
		completed: false
	}
];

export const learningPaths: LearningPath[] = [
	{
		id: 'blockchain-developer',
		title: 'Blockchain Developer Path',
		description: 'Complete learning path to become a proficient blockchain developer',
		modules: ['blockchain-basics', 'smart-contracts', 'web3-development', 'cybersecurity-web3'],
		icon: '👨‍💻',
		estimatedTime: '8-12 weeks'
	},
	{
		id: 'dao-operator',
		title: 'DAO Operator Path',
		description: 'Learn to create, manage, and operate decentralized autonomous organizations',
		modules: ['blockchain-basics', 'dao-governance', 'tokenomics', 'defi-protocols'],
		icon: '🏛️',
		estimatedTime: '6-8 weeks'
	},
	{
		id: 'defi-specialist',
		title: 'DeFi Specialist Path',
		description: 'Master decentralized finance protocols and yield generation strategies',
		modules: ['blockchain-basics', 'smart-contracts', 'defi-protocols', 'tokenomics'],
		icon: '💎',
		estimatedTime: '10-14 weeks'
	}
];
