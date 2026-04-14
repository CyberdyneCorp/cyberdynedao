export interface ServiceBullet {
	title: string;
	description: string;
}

export interface ServiceSection {
	id: string;
	icon: string;
	title: string;
	intro: string;
	bullets: ServiceBullet[];
	gradientFrom: string;
	gradientTo: string;
	borderColor: string;
	bulletColor: string;
}

export const serviceSections: ServiceSection[] = [
	{
		id: 'strategy',
		icon: '🎯',
		title: 'Strategy & Discovery',
		intro: 'Turn ideas into a buildable plan—with token-aware economics.',
		bullets: [
			{ title: 'Product Strategy & PRD', description: 'for full-stack builds (frontend, backend, automation, LLMs).' },
			{ title: 'Tokenomics & DAO Design', description: 'aligned to a yield-powered model (ops funded by DeFi; dividends optional).' },
			{ title: 'Roadmap fit', description: 'with phased governance (incl. a Cosmos-SDK chain w/ IBC for scale in Phase 3).' }
		],
		gradientFrom: 'from-purple-50',
		gradientTo: 'to-blue-50',
		borderColor: 'border-purple-200',
		bulletColor: 'text-purple-600'
	},
	{
		id: 'frontend',
		icon: '🎨',
		title: 'Frontend Engineering',
		intro: 'Fast, portable frontends you can host anywhere.',
		bullets: [
			{ title: 'Web Apps', description: 'in Svelte + TypeScript + Tailwind with clean component systems.' },
			{ title: 'Mobile', description: 'in SwiftUI (iOS) and Kotlin/Jetpack (Android).' },
			{ title: 'Launch & Hosting:', description: 'Supabase-style backends and Coolify-like app deploys for frictionless DX.' }
		],
		gradientFrom: 'from-green-50',
		gradientTo: 'to-emerald-50',
		borderColor: 'border-green-200',
		bulletColor: 'text-green-600'
	},
	{
		id: 'backend',
		icon: '⚡',
		title: 'Backend, Data & DevOps',
		intro: 'Cloud-simple, production-sharp.',
		bullets: [
			{ title: 'APIs & Services', description: 'on Supabase (Auth, DB, Edge Functions) and Python/Go/Rust stacks.' },
			{ title: 'Automation', description: 'with n8n for ingest, enrichment, and ops runbooks.' },
			{ title: 'Containers & Orchestration', description: 'using Docker and Kubernetes, with CI/CD pipelines and observability.' }
		],
		gradientFrom: 'from-blue-50',
		gradientTo: 'to-indigo-50',
		borderColor: 'border-blue-200',
		bulletColor: 'text-blue-600'
	},
	{
		id: 'ai',
		icon: '🧠',
		title: 'AI & Knowledge Systems',
		intro: 'From RAG to agents—shipped responsibly.',
		bullets: [
			{ title: 'Integrated LLMs', description: '(OpenRouter) when you want hosted intelligence without gatekeeping.' },
			{ title: 'Self-hosted inference', description: 'using Ollama and vLLM; plug in open-source models like DeepSeek or Gemma.' },
			{ title: 'Data pipelines', description: 'and doc parsing ready for knowledge graphs and retrieval workflows.' }
		],
		gradientFrom: 'from-orange-50',
		gradientTo: 'to-yellow-50',
		borderColor: 'border-orange-200',
		bulletColor: 'text-orange-600'
	},
	{
		id: 'blockchain',
		icon: '⛓️',
		title: 'Blockchain, DeFi & On-Chain Apps',
		intro: 'Credible Web3 that survives mainnet.',
		bullets: [
			{ title: 'EVM smart contracts', description: '(Solidity) with oracles (Chainlink) and tested release flows.' },
			{ title: 'Wallet & Auth', description: 'via Web3Auth/OpenWallet; fiat on-ramp with Coinbase SDK.' },
			{ title: 'Target chains', description: 'include Arbitrum and Base for cost/perf balance.' },
			{ title: 'DeFi-native operations:', description: 'leverage AAVE/Uniswap to structure covered loans and reduce liquidity costs.' },
			{ title: 'DAO at scale:', description: 'Cosmos-SDK + IBC path for governance throughput when you need it.' },
			{ title: 'Treasury & Finance:', description: 'ops funded by 4–6%/mo DeFi yield; optional dividend distribution to holders.' }
		],
		gradientFrom: 'from-purple-50',
		gradientTo: 'to-pink-50',
		borderColor: 'border-purple-200',
		bulletColor: 'text-purple-600'
	},
	{
		id: 'storage',
		icon: '💾',
		title: 'Decentralized Storage & Compute',
		intro: "Put your app where it can't be \"turned off.\"",
		bullets: [
			{ title: 'Storage', description: 'on Arweave and IPFS for assets, docs, and audit trails.' },
			{ title: 'Portable compute', description: 'across your infra or decentralized providers, with caching/rate-limit strategies.' }
		],
		gradientFrom: 'from-teal-50',
		gradientTo: 'to-cyan-50',
		borderColor: 'border-teal-200',
		bulletColor: 'text-teal-600'
	},
	{
		id: 'security',
		icon: '🔒',
		title: 'Security, Reliability & Support',
		intro: 'Trust is a feature.',
		bullets: [
			{ title: 'Security basics:', description: 'secrets, key handling, principle of least privilege.' },
			{ title: 'Audits & Testing', description: 'for contracts and apps; threat modeling and fuzzing.' },
			{ title: 'SLA-style support:', description: 'incident response, patch windows, and monthly ops reviews.' }
		],
		gradientFrom: 'from-red-50',
		gradientTo: 'to-pink-50',
		borderColor: 'border-red-200',
		bulletColor: 'text-red-600'
	}
];

export const workflowSteps: string[] = [
	'Discover the smallest valuable slice.',
	'Design the system and the experience, together.',
	'Build with tests, telemetry, and CI from day zero.',
	'Ship to users, not staging.',
	"Measure what moved (or didn't) and why.",
	'Grow & Govern with DAO rituals and clear economics.'
];

export const whyCyberdynePoints: ServiceBullet[] = [
	{ title: 'Yield-powered:', description: '"Usage ⇒ Yield ⇒ Self-Sustaining Infrastructure."' },
	{ title: 'All-in-one:', description: 'Firebase + OpenAI + Heroku—but decentralized, community-owned, and yield-paying.' },
	{ title: 'Open & composable:', description: 'choose hosted LLMs (OpenRouter) or your own (Ollama/vLLM).' },
	{ title: 'DAO-native:', description: 'EVM compatible and governance-ready; CBY max supply fixed at 25,000,000.' }
];
