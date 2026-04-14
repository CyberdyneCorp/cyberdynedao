export interface TokenomicsRow {
	allocation: string;
	percentage: string;
	vesting: string;
}

export interface RoadmapItem {
	icon: string;
	text: string;
}

export interface RoadmapPhase {
	id: string;
	title: string;
	color: 'green' | 'blue' | 'purple' | 'orange' | 'red';
	items: RoadmapItem[];
}

export const problemPoints: string[] = [
	'Developers spend $50–$300/mo on infra tools like Vercel, Firebase, and OpenAI',
	'Toolchains are fragmented; vendor lock-in limits flexibility',
	'Users have no ownership or upside in the platforms they rely on',
	'Finding vetted developers for specific products is hard',
	'Crypto investors want real yield tied to real products'
];

export const solutionOfferings: { icon: string; title: string; description: string }[] = [
	{ icon: '⚡', title: 'Frontend hosting', description: '(Vercel-like)' },
	{ icon: '🔐', title: 'Backend as a Service', description: '(Supabase-based: DB, Auth, Storage)' },
	{ icon: '⚙️', title: 'Automation', description: '(n8n, Zapier-like)' },
	{ icon: '🤖', title: 'LLM integration', description: '(OpenRouter + local AI models)' },
	{ icon: '🧩', title: 'Marketplace', description: 'for datasets, training modules, compute, and storage' }
];

export const targetUsers: { name: string; description: string }[] = [
	{ name: 'Startups', description: 'Affordable, scalable infrastructure' },
	{ name: 'Developers', description: 'Free stack + earning potential' },
	{ name: 'Data Scientists', description: 'Buy/sell datasets & AI models' },
	{ name: 'Investors', description: 'Real yield + governance rights' },
	{ name: 'Communities & DAOs', description: 'Own and control the infra they use' }
];

export const tokenomicsRows: TokenomicsRow[] = [
	{ allocation: 'Community & Airdrops', percentage: '35%', vesting: 'Linear 24 mo (1 mo cliff)' },
	{ allocation: 'DAO Treasury', percentage: '25%', vesting: 'Unlock via governance' },
	{ allocation: 'Strategic Investors', percentage: '15%', vesting: '12 mo cliff + 24 mo linear' },
	{ allocation: 'Team & Founders', percentage: '15%', vesting: '12 mo cliff + 24 mo linear' },
	{ allocation: 'Liquidity Reserve', percentage: '10%', vesting: 'DAO-governed provisioning' }
];

export const tokenUtilityPoints: string[] = [
	'Governance voting',
	'Access to premium app features',
	'Stake for monthly dividends',
	'Discounts & exclusives in marketplace',
	'LP staking incentives'
];

export const strategicAdvantages: { title: string; description: string }[] = [
	{ title: 'Dividend flywheel:', description: 'Yield → Infra → Revenue → Dividends → Demand' },
	{ title: 'Modular stack:', description: 'Swap in/out tools without breaking core' },
	{ title: 'Global South-ready:', description: 'Low-cost infra for emerging markets' },
	{ title: 'First-mover:', description: 'No other DAO offers full dev stack + yield model' }
];

export const flagshipProducts: { name: string; description: string }[] = [
	{ name: 'Study4Me', description: 'AI-powered learning platform (videos, docs → knowledge graphs)' },
	{ name: 'Surf4Me', description: 'Local gig economy app for surf instructors and rentals' },
	{ name: 'Liquidity4Me', description: 'DeFi LP management, alerts, strategies' },
	{ name: 'Trade4Me', description: 'AI-assisted trading toolkit' },
	{ name: 'Terraform', description: 'NFT-driven mobile game' },
	{ name: 'Marketplace', description: 'Datasets, tutorials, compute/storage' }
];

export const exampleEconomics: { label: string; value: string }[] = [
	{ label: 'Treasury:', value: '$40,000' },
	{ label: 'Yield:', value: '4–6%/mo → $1,600–$2,400' },
	{ label: 'Costs:', value: '~$500/mo' },
	{ label: 'Dividends:', value: '~$550/mo + $550 reinvested' }
];

export const roadmapPhases: RoadmapPhase[] = [
	{
		id: 'phase-1',
		title: 'Phase 1 – MVP',
		color: 'green',
		items: [
			{ icon: '✅', text: 'Launch infra stack (frontend, backend, automation, LLM API)' },
			{ icon: '✅', text: 'Deploy first apps: Study4Me & Liquidity4Me' },
			{ icon: '✅', text: 'DAO governance & treasury setup' }
		]
	},
	{
		id: 'phase-2',
		title: 'Phase 2 – Decentralized Infra',
		color: 'blue',
		items: [
			{ icon: '🚀', text: 'Deploy to Akash Network (compute), Arweave & Filecoin (storage)' },
			{ icon: '🌐', text: 'Launch documentation hub, community onboarding' }
		]
	},
	{
		id: 'phase-3',
		title: 'Phase 3 – Ecosystem Growth',
		color: 'purple',
		items: [
			{ icon: '📈', text: 'Raise treasury to ~$35k–$50k for sustainable yield loop' },
			{ icon: '💸', text: 'Start dividend payouts to CBY stakers' },
			{ icon: '🎯', text: 'Launch bounties, partnerships, training programs' },
			{ icon: '📦', text: 'Expand marketplace (datasets, tutorials, AI models)' }
		]
	},
	{
		id: 'phase-4',
		title: 'Phase 4 – Blockchain Expansion',
		color: 'orange',
		items: [
			{ icon: '🛠', text: 'Build custom Cosmos SDK chain for DAO governance & service orchestration' },
			{ icon: '🔗', text: 'IBC connections for cross-chain operations' }
		]
	},
	{
		id: 'phase-5',
		title: 'Phase 5 – Global Scaling',
		color: 'red',
		items: [
			{ icon: '🌍', text: 'Target Global South dev & startup adoption' },
			{ icon: '📢', text: 'Marketing & growth campaigns' },
			{ icon: '🧠', text: 'Continuous product launches & community-driven features' }
		]
	}
];
