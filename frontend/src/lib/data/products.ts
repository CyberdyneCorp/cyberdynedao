export interface ProductEntry {
	id: string;
	name: string;
	icon: string;
	description: string;
	features: string[];
	extraFeatures?: string[];
	palette: 'blue' | 'green' | 'purple' | 'orange' | 'red';
	fullWidth?: boolean;
}

export const productSuite: ProductEntry[] = [
	{
		id: 'trade4me',
		name: 'Trade4Me',
		icon: '📈',
		description:
			'Advanced algorithmic trading platform powered by AI. Execute trades with precision, analyze market trends in real-time, and maximize your investment potential with our intelligent trading algorithms.',
		features: [
			'AI-powered market analysis',
			'Real-time portfolio optimization',
			'Risk management algorithms',
			'Multi-asset trading support'
		],
		palette: 'blue'
	},
	{
		id: 'liquidity4me',
		name: 'Liquidity4Me',
		icon: '💧',
		description:
			'Revolutionary liquidity mining and yield farming platform. Optimize your DeFi returns through automated liquidity provision strategies across multiple protocols and chains.',
		features: [
			'Cross-chain liquidity optimization',
			'Automated yield farming',
			'Impermanent loss protection',
			'Smart contract audited'
		],
		palette: 'green'
	},
	{
		id: 'surf4me',
		name: 'Surf4Me',
		icon: '🏄',
		description:
			'Next-generation web3 browsing experience with built-in privacy protection, decentralized content discovery, and seamless interaction with blockchain applications.',
		features: [
			'Privacy-first browsing',
			'Integrated DApp discovery',
			'Decentralized identity management',
			'Built-in crypto wallet'
		],
		palette: 'purple'
	},
	{
		id: 'budget4me',
		name: 'Budget4Me',
		icon: '💰',
		description:
			'Intelligent personal finance management system with AI-powered budgeting, expense tracking, and financial goal optimization for the modern digital lifestyle.',
		features: [
			'AI budgeting recommendations',
			'Automated expense categorization',
			'Goal-based saving strategies',
			'Multi-currency support'
		],
		palette: 'orange'
	},
	{
		id: 'bhealthy',
		name: 'bHealthy',
		icon: '❤️',
		description:
			'Comprehensive blockchain-based health management platform that puts you in control of your health data while connecting you with healthcare providers and wellness programs.',
		features: [
			'Secure health data storage',
			'AI health insights',
			'Telemedicine integration',
			'Fitness tracking & rewards'
		],
		extraFeatures: [
			'Medication reminders',
			'Health NFT achievements',
			'Provider network access',
			'Anonymous health research'
		],
		palette: 'red',
		fullWidth: true
	}
];
