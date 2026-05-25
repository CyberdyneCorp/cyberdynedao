import type { LearningModule, LearningPath } from '$lib/types/components';

export const learnHeroSubtitle =
	'Learn the Cyberdyne stack — from blockchain fundamentals to hexagonal cores, MCP backends, and production-grade Web3.';

export const learnWelcomeHeadline = 'Welcome to Cyberdyne Academy';
export const learnWelcomeBody =
	'Pick a module to dive into one topic, or follow a learning path to assemble a complete skill set. Every module is grounded in software actually running in production.';

export const learningModules: LearningModule[] = [
	{
		id: 'blockchain-basics',
		title: 'Blockchain Fundamentals',
		category: 'Blockchain',
		description:
			'Distributed ledgers, consensus, cryptographic hashing — the substrate every Web3 system stands on.',
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
		description:
			'Solidity, security patterns, gas optimization, and the test discipline that keeps mainnet deploys boring.',
		level: 'Intermediate',
		duration: '1h 30min',
		icon: '📜',
		topics: ['Solidity Basics', 'Contract Security', 'Gas Optimization', 'Foundry & Hardhat'],
		completed: false
	},
	{
		id: 'hexagonal-architecture',
		title: 'Hexagonal Architecture in Production',
		category: 'Architecture',
		description:
			'Ports & adapters, dependency inversion, and how to enforce them with import-linter so the boundaries actually hold over time.',
		level: 'Intermediate',
		duration: '1h 30min',
		icon: '⬡',
		topics: ['Ports & Adapters', 'Dependency Inversion', 'Import-Linter Contracts', 'Use Cases & UoW'],
		completed: false
	},
	{
		id: 'mcp-servers',
		title: 'MCP Servers & Agent Backends',
		category: 'Development',
		description:
			'Model Context Protocol — give an LLM agent first-class access to the same use cases your REST API serves.',
		level: 'Intermediate',
		duration: '1h 15min',
		icon: '🔌',
		topics: ['MCP Protocol', 'FastMCP & FastAPI', 'Dual REST + MCP Surfaces', 'Tool Design'],
		completed: false
	},
	{
		id: 'rag-knowledge-graphs',
		title: 'Knowledge Graphs & RAG',
		category: 'AI',
		description:
			'Beyond flat-chunk RAG — entity-relation graphs on pgvector + Apache AGE, multi-hop queries, multi-tenant workspaces.',
		level: 'Advanced',
		duration: '2h',
		icon: '🧠',
		topics: ['LightRAG Engine', 'pgvector + AGE', 'Multi-hop Queries', 'Multi-tenant Workspaces'],
		completed: false
	},
	{
		id: 'geospatial-ai',
		title: 'Geospatial AI Foundations',
		category: 'Geospatial',
		description:
			'STAC catalogs, lazy xarray + Dask loading, spectral indices, parametric payouts, and EUDR compliance pipelines.',
		level: 'Advanced',
		duration: '2h 30min',
		icon: '🌍',
		topics: ['STAC + pgstac', 'xarray + Dask', 'Spectral Indices', 'Parametric Insurance'],
		completed: false
	},
	{
		id: 'dao-governance',
		title: 'DAO Governance & Structure',
		category: 'Governance',
		description:
			'Token-based voting, proposal systems, treasury management — and when to graduate from Snapshot to a sovereign chain.',
		level: 'Intermediate',
		duration: '1h 15min',
		icon: '🏛️',
		topics: ['Token-based Voting', 'Proposal Systems', 'Treasury Management', 'Community Rituals'],
		completed: false
	},
	{
		id: 'defi-protocols',
		title: 'DeFi Protocols & Yield Farming',
		category: 'DeFi',
		description:
			'AMM design, liquidity provision, yield strategies, and the risk model behind a yield-powered treasury.',
		level: 'Advanced',
		duration: '2h',
		icon: '💰',
		topics: ['AMM Design', 'Liquidity Mining', 'Yield Strategies', 'Risk & Covered Loans'],
		completed: false
	},
	{
		id: 'web3-development',
		title: 'Web3 Frontend Development',
		category: 'Development',
		description:
			'Modern Web3 apps with SvelteKit + TypeScript, Web3Auth social login, WalletConnect, and the Cyberdyne component library.',
		level: 'Intermediate',
		duration: '2h 30min',
		icon: '🌐',
		topics: ['SvelteKit + TypeScript', 'Web3Auth / WalletConnect', 'IPFS + Provenance', '@cyberdynecorp/svelte-ui-core'],
		completed: false
	},
	{
		id: 'tokenomics',
		title: 'Tokenomics & Economic Models',
		category: 'Economics',
		description:
			'Distribution, incentive design, and how to keep a token tied to real product value instead of speculation.',
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
		description:
			'Build sovereign chains with the Cosmos SDK, integrate IBC, and design governance modules built for throughput.',
		level: 'Advanced',
		duration: '3h',
		icon: '🌌',
		topics: ['Tendermint Consensus', 'Module Development', 'IBC Protocol', 'Chain Governance'],
		completed: false
	},
	{
		id: 'cybersecurity-web3',
		title: 'Web3 Security & Sandboxing',
		category: 'Security',
		description:
			'Smart-contract audits, wallet security, and sandboxing user code with real OS isolation — subprocess + netns + egress allowlist.',
		level: 'Intermediate',
		duration: '1h 30min',
		icon: '🛡️',
		topics: ['Contract Audits', 'Wallet Security', 'OS Sandboxing', 'Bridge Vulnerabilities'],
		completed: false
	}
];

export const learningPaths: LearningPath[] = [
	{
		id: 'blockchain-developer',
		title: 'Blockchain Developer',
		description: 'From cryptography fundamentals to shipping audited smart contracts on mainnet.',
		modules: ['blockchain-basics', 'smart-contracts', 'web3-development', 'cybersecurity-web3'],
		icon: '👨‍💻',
		estimatedTime: '8–12 weeks'
	},
	{
		id: 'cyberdyne-stack',
		title: 'Build Like Cyberdyne',
		description: 'The exact architecture behind our production services — hexagonal cores, MCP backends, knowledge graphs.',
		modules: ['hexagonal-architecture', 'mcp-servers', 'rag-knowledge-graphs', 'cybersecurity-web3'],
		icon: '⚡',
		estimatedTime: '10–14 weeks'
	},
	{
		id: 'sovereign-ai',
		title: 'Sovereign Geospatial AI',
		description: 'For teams building regulated geospatial software — DFIs, parametric insurers, EUDR compliance.',
		modules: ['hexagonal-architecture', 'mcp-servers', 'geospatial-ai', 'cybersecurity-web3'],
		icon: '🛰️',
		estimatedTime: '12–16 weeks'
	},
	{
		id: 'dao-operator',
		title: 'DAO Operator',
		description: 'Design, deploy, and govern DAOs that pay their own bills via DeFi yield.',
		modules: ['blockchain-basics', 'dao-governance', 'tokenomics', 'defi-protocols'],
		icon: '🏛️',
		estimatedTime: '6–8 weeks'
	},
	{
		id: 'defi-specialist',
		title: 'DeFi Specialist',
		description: 'Master AMMs, liquidity strategies, and yield farming — including the risk side most courses skip.',
		modules: ['blockchain-basics', 'smart-contracts', 'defi-protocols', 'tokenomics'],
		icon: '💎',
		estimatedTime: '10–14 weeks'
	}
];

export interface ResourceLink {
	label: string;
	href: string;
	disabled?: boolean;
}

export interface ResourceGroup {
	id: string;
	icon: string;
	title: string;
	links: ResourceLink[];
}

export const resourceGroups: ResourceGroup[] = [
	{
		id: 'cyberdyne',
		icon: '🛠️',
		title: 'Cyberdyne',
		links: [
			{ label: 'CyberdyneCorp on GitHub', href: 'https://github.com/CyberdyneCorp' },
			{ label: 'Svelte UI Core (component library)', href: 'https://cyberdynecorp.github.io/' },
			{ label: 'CyberDocExtractor on PyPI', href: 'https://pypi.org/project/cyberdocextractor/' }
		]
	},
	{
		id: 'protocols',
		icon: '📚',
		title: 'Protocols & Specs',
		links: [
			{ label: 'Model Context Protocol (MCP)', href: 'https://modelcontextprotocol.io/' },
			{ label: 'STAC — SpatioTemporal Asset Catalog', href: 'https://stacspec.org/' },
			{ label: 'EIP-4361 (Sign-In With Ethereum)', href: 'https://eips.ethereum.org/EIPS/eip-4361' },
			{ label: 'Cosmos SDK Docs', href: 'https://docs.cosmos.network/' },
			{ label: 'Solidity Documentation', href: 'https://docs.soliditylang.org/' }
		]
	},
	{
		id: 'tools',
		icon: '⚙️',
		title: 'Tools',
		links: [
			{ label: 'FastMCP', href: 'https://github.com/jlowin/fastmcp' },
			{ label: 'LightRAG', href: 'https://github.com/HKUDS/LightRAG' },
			{ label: 'Foundry (smart-contract toolkit)', href: 'https://book.getfoundry.sh/' },
			{ label: 'Hardhat', href: 'https://hardhat.org/' },
			{ label: 'Web3Auth', href: 'https://web3auth.io/' }
		]
	},
	{
		id: 'communities',
		icon: '🌐',
		title: 'Communities',
		links: [
			{ label: 'Cyberdyne Discord (coming soon)', href: '#', disabled: true },
			{ label: 'Developer Forum (coming soon)', href: '#', disabled: true },
			{ label: 'Weekly Dev Calls (coming soon)', href: '#', disabled: true }
		]
	}
];
