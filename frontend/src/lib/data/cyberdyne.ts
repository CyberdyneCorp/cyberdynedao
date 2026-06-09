export type Palette = 'green' | 'blue' | 'purple' | 'orange' | 'red';

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
	subtitle: string;
	status: 'shipped' | 'shipping' | 'active' | 'planned';
	color: Palette;
	items: RoadmapItem[];
}

export interface Domain {
	id: string;
	name: string;
	icon: string;
	palette: Palette;
	tagline: string;
	projects: string[];
	status: 'live' | 'shipping' | 'active' | 'planned';
}

export const heroTagline =
	'Open infrastructure for the next internet — built in the open, funded by yield, owned by the builders shipping it.';

export const introLead =
	'Cyberdyne is an independent builder collective shipping production-grade open infrastructure across AI knowledge systems, identity, developer tooling, DeFi, and games. Every project is open by default, hexagonal at its core, and designed to outlive any single vendor.';

export const introBullets: string[] = [
	'Eleven projects · one stack · zero vendor lock-in',
	'Hexagonal architecture, strict typing, real coverage gates',
	'A DAO underneath that turns DeFi yield into builder runway'
];

export const domains: Domain[] = [
	{
		id: 'ai-knowledge',
		name: 'AI Knowledge Systems',
		icon: '🧠',
		palette: 'purple',
		tagline:
			'AI-native company operating system, REST + MCP knowledge backends, and an open collection of Claude skills — built so agents can act, not just answer.',
		projects: ['OrgPilot', 'Obsidian MCP Server', 'Claude Skills'],
		status: 'active'
	},
	{
		id: 'defi-games',
		name: 'DeFi · Games · Apps',
		icon: '🎮',
		palette: 'blue',
		tagline:
			'From AI-powered DeFi life-planning to a mobile Action-RTS earning real on-chain yield, to surf-school bookings and warehouse computer vision — the apps the rest of the stack exists to support.',
		projects: ['CyberdyneDAO', 'YieldPath', 'Terraform', 'Surf4Me', 'Vision Factory'],
		status: 'active'
	},
	{
		id: 'dev-tools',
		name: 'Developer Tooling',
		icon: '⚙️',
		palette: 'orange',
		tagline:
			'A real LLVM + MLIR compiler for MATLAB that emits synthesizable SystemVerilog, a SwiftUI IDE that drives it, and a cloud HDL simulator with visual circuit design.',
		projects: ['Matlab Compiler', 'MatForge IDE', 'HDL Backend Simulator'],
		status: 'active'
	}
];

export const beliefs: { title: string; description: string }[] = [
	{
		title: 'Built in the open',
		description:
			'Every project ships open-source, with hexagonal boundaries enforced on every PR. No closed black boxes; no per-call SaaS taxes.'
	},
	{
		title: 'Production-grade by default',
		description:
			'Real coverage gates, not vibes. MatForge IDE ships at 97% coverage, OrgPilot at 2000+ backend tests, the Matlab Compiler against a 322-program regression corpus. The numbers are public.'
	},
	{
		title: 'No vendor lock-in',
		description:
			'Hexagonal cores mean any adapter can be swapped. Pick MongoDB or Postgres. Pick OpenAI or local models. Pick AAVE or Uniswap. The seams are stable; the implementations are yours.'
	},
	{
		title: 'Funded by yield, not speculation',
		description:
			'The DAO treasury sits in diversified DeFi. Yield covers infra and ops; surplus pays builder dividends. Software is the product; the token is the funding mechanism.'
	}
];

export const targetUsers: { name: string; description: string }[] = [
	{ name: 'Builders', description: 'Open infra and SDKs to ship on, with no monthly bill at the bottom' },
	{ name: 'Data & ML teams', description: 'Production knowledge graphs and data pipelines off the shelf' },
	{ name: 'Token holders', description: 'Governance + real yield tied to real software, not narratives' }
];

export const tokenomicsRows: TokenomicsRow[] = [
	{ allocation: 'Community & Airdrops', percentage: '35%', vesting: 'Linear 24 mo (1 mo cliff)' },
	{ allocation: 'DAO Treasury', percentage: '25%', vesting: 'Unlock via governance' },
	{ allocation: 'Strategic Investors', percentage: '15%', vesting: '12 mo cliff + 24 mo linear' },
	{ allocation: 'Team & Founders', percentage: '15%', vesting: '12 mo cliff + 24 mo linear' },
	{ allocation: 'Liquidity Reserve', percentage: '10%', vesting: 'DAO-governed provisioning' }
];

export const tokenUtilityPoints: string[] = [
	'Governance voting on treasury & roadmap',
	'Stake for monthly dividends in stablecoin',
	'Access to premium app tiers & priority builds',
	'Discounts on marketplace datasets & compute',
	'LP staking incentives'
];

export const exampleEconomics: { label: string; value: string }[] = [
	{ label: 'Treasury', value: '$40,000' },
	{ label: 'Yield', value: '4–6%/mo → $1.6k–$2.4k' },
	{ label: 'Infra & ops', value: '~$500/mo' },
	{ label: 'Builder dividends', value: '~$550/mo + $550 reinvested' }
];

export const roadmapPhases: RoadmapPhase[] = [
	{
		id: 'phase-3',
		title: 'Phase 1 · DAO + Dividends',
		subtitle: 'Yield meets shipping software',
		status: 'active',
		color: 'purple',
		items: [
			{ icon: '▸', text: 'CBY token mint + treasury deployment on Base' },
			{ icon: '▸', text: 'Diversified DeFi positions — AAVE, Uniswap, covered loans' },
			{ icon: '▸', text: 'First builder dividend round to stakers' }
		]
	},
	{
		id: 'phase-4',
		title: 'Phase 2 · Apps & Games',
		subtitle: 'Where the stack meets users',
		status: 'active',
		color: 'orange',
		items: [
			{ icon: '▸', text: 'Terraform Game closed beta on Base' },
			{ icon: '▸', text: 'YieldPath public launch — AI DeFi life planner' },
			{ icon: '▸', text: 'Surf4Me marketplace expansion (iOS + Android live)' }
		]
	}
];

export const closingHeadline = 'Infrastructure that doesn’t cost — it yields.';
export const closingBody =
	'Eleven projects. One open stack. Zero vendor lock-in. Build with us, earn with us, own with us.';
