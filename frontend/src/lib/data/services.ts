export type ServicePalette = 'blue' | 'green' | 'purple' | 'orange' | 'red';

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
	palette: ServicePalette;
	fullWidth?: boolean;
}

export const heroSubtitle =
	'Production-grade software end-to-end — strategy, full-stack engineering, AI, blockchain, and the open infrastructure to run it.';

export const serviceSections: ServiceSection[] = [
	{
		id: 'strategy',
		icon: '🎯',
		title: 'Strategy & Discovery',
		intro: 'Turn an idea into a buildable plan — architecture decided before the first commit.',
		bullets: [
			{ title: 'Product strategy & PRDs', description: 'scoped for full-stack delivery, not slideware.' },
			{ title: 'Architecture review', description: 'hexagonal cores, ports & adapters, tested at the seams.' },
			{ title: 'Tokenomics & DAO design', description: 'yield-powered models where DeFi pays the ops bill.' },
			{ title: 'Roadmap fit', description: 'phased, governance-aware, Cosmos-SDK + IBC when scale demands it.' }
		],
		palette: 'purple'
	},
	{
		id: 'frontend',
		icon: '🎨',
		title: 'Frontend Engineering',
		intro: 'Fast, portable frontends on the same component library already shipping in production.',
		bullets: [
			{ title: 'Web apps', description: 'Svelte + TypeScript + Tailwind, MVVM end-to-end.' },
			{ title: 'Mobile', description: 'SwiftUI (iOS) + Kotlin / Jetpack Compose (Android).' },
			{ title: 'Design system', description: '@cyberdynecorp/svelte-ui-core — retro chrome and crypto primitives included.' },
			{ title: 'Accessibility & type-safety', description: 'svelte-check clean, a11y-tested on every PR.' }
		],
		palette: 'blue'
	},
	{
		id: 'backend',
		icon: '⚡',
		title: 'Backend, Data & DevOps',
		intro: 'Hexagonal cores, real coverage gates, predictable releases.',
		bullets: [
			{ title: 'APIs', description: 'FastAPI, Go, Rust — import-linter contracts enforce architecture on every PR.' },
			{ title: 'REST + MCP dual surfaces', description: 'the same use cases serve agents and apps.' },
			{ title: 'PostgreSQL stack', description: 'pgvector + Apache AGE for knowledge graphs.' },
			{ title: 'Ops', description: 'Coolify-first deploys, containers, structlog + Prometheus + Sentry.' }
		],
		palette: 'orange'
	},
	{
		id: 'ai',
		icon: '🧠',
		title: 'AI & Knowledge Systems',
		intro: 'From RAG to agents — production, not demos.',
		bullets: [
			{ title: 'Knowledge graphs', description: 'LightRAG-backed, multi-tenant from day one.' },
			{ title: 'Agent orchestration', description: 'multi-step agents with tool use, streaming, and human-in-the-loop handoff.' },
			{ title: 'LLM ops', description: 'hosted (OpenRouter, Anthropic, OpenAI) or self-hosted (Ollama, vLLM).' },
			{ title: 'MCP servers', description: 'first-class agent access to your data — same use cases over HTTP.' }
		],
		palette: 'red'
	},
	{
		id: 'blockchain',
		icon: '⛓️',
		title: 'Blockchain & On-Chain Apps',
		intro: 'Credible Web3 that survives mainnet.',
		bullets: [
			{ title: 'EVM smart contracts', description: 'Solidity with oracles, tested release flows, audited.' },
			{ title: 'Wallet auth', description: 'EIP-4361, Web3Auth social login, WalletConnect (50+ wallets).' },
			{ title: 'Chain focus', description: 'Base + Arbitrum for cost/perf, USDC-native economies.' },
			{ title: 'NFT-tier IAM', description: 'on-chain Identity / Policy / Group contracts, dynamic permissions.' },
			{ title: 'DeFi treasury', description: 'AAVE supply, Uniswap LPs, covered loans — proven, not theorized.' },
			{ title: 'DAO at scale', description: 'Cosmos-SDK + IBC when governance throughput needs to scale.' }
		],
		palette: 'blue'
	},
	{
		id: 'security',
		icon: '🔒',
		title: 'Security & Reliability',
		intro: 'Trust is a feature — and we test it like one.',
		bullets: [
			{ title: 'Sandboxed user code', description: 'real subprocess + Linux netns + egress allowlist for untrusted user hooks.' },
			{ title: 'Hardened parsers', description: 'XXE defenses, size caps, sanitization, fuzzing on untrusted input.' },
			{ title: 'SLA-style support', description: 'incident response, patch windows, monthly ops reviews.' },
			{ title: 'Least-privilege everywhere', description: 'secrets hygiene, threat modeling, audit trails.' }
		],
		palette: 'purple'
	}
];

export const workflowSteps: { title: string; description: string }[] = [
	{ title: 'Discover', description: 'Find the smallest valuable slice.' },
	{ title: 'Architect', description: 'Pick ports & adapters before the first PR.' },
	{ title: 'Build', description: 'Tests, telemetry, and CI from day zero.' },
	{ title: 'Ship', description: 'To users, not staging.' },
	{ title: 'Measure', description: "What moved (or didn't) and why." },
	{ title: 'Govern', description: 'DAO rituals and clear economics, when it’s time.' }
];

export const whyCyberdynePoints: ServiceBullet[] = [
	{
		title: 'Production proof',
		description: 'Eleven projects shipping. Coverage gates at 83–97%. Tests in the thousands.'
	},
	{
		title: 'Open by default',
		description: 'Every project hexagonal, open-source, swappable at the seams — no vendor lock-in.'
	},
	{
		title: 'Full stack, one collective',
		description: 'Strategy, mobile, backend, AI, and Web3 — one team, one taste.'
	},
	{
		title: 'Yield-powered economics',
		description: 'For clients who want ops funded by DeFi yield, not per-seat SaaS taxes.'
	}
];

export const ctaHeadline = 'Ready to Build?';
export const ctaBody =
	'Whether it’s an AI-native operating system, a DeFi-funded platform, or developer tooling — let’s scope the first valuable slice.';
export const ctaPills: string[] = ['Strategy', 'Engineering', 'AI', 'Web3'];
