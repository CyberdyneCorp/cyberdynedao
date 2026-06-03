export type ProductStatus = 'live' | 'active' | 'development' | 'planning' | 'design';

export interface ProductEntry {
	id: string;
	name: string;
	icon: string;
	description: string;
	features: string[];
	extraFeatures?: string[];
	palette: 'blue' | 'green' | 'purple' | 'orange' | 'red';
	status: ProductStatus;
	fullWidth?: boolean;
}

export const productSuite: ProductEntry[] = [
	{
		id: 'cyberdynedao',
		name: 'CyberdyneDAO',
		icon: '🖥️',
		description:
			'Retro-terminal Web3 platform for DAO operations. SvelteKit on Base with Web3Auth social login, WalletConnect, and NFT-gated access — wrapped in a green-phosphor cyberpunk shell.',
		features: [
			'Six-tier NFT-based access control',
			'IPFS + USDC training-materials contract',
			'Real-time on-chain balance & permissions',
			'Draggable retro window UI'
		],
		palette: 'blue',
		status: 'active'
	},
	{
		id: 'cybergeopy',
		name: 'CyberGeoPy',
		icon: '🗺️',
		description:
			'Geospatial processing engine of the Cyberdyne stack. Python library unifying ten satellite product managers, spectral indices, SAR primitives, anomaly detection, parametric payouts, and EUDR compliance.',
		features: [
			'Sentinel-1/2/3/5P + Landsat + VIIRS + SMAP + ERA5',
			'Pure-Python SAR (coherence, interferogram, unwrap)',
			'Climatology baseline + anomaly engine',
			'EUDR pipeline with TRACES-ready DDS payload'
		],
		palette: 'orange',
		status: 'development'
	},
	{
		id: 'orgpilot',
		name: 'OrgPilot',
		icon: '🧭',
		description:
			'AI-native company operating system. Connects people, projects, tasks, code, AI agents, and treasury under one governance layer — answers not just "what tasks exist?" but "who should do this, what is blocked, should capital move?"',
		features: [
			'270+ REST endpoints, 50+ MCP tools',
			'Company digital twin (skills, capacity, roles)',
			'PM intelligence & overload detection',
			'2000+ backend tests'
		],
		palette: 'blue',
		status: 'active'
	},
	{
		id: 'yieldpath',
		name: 'YieldPath',
		icon: '📊',
		description:
			'AI-powered DeFi life planner. Monitors LPs, lending, and staking positions, optimizes yields, and projects your path to financial independence — all in natural language.',
		features: [
			'DeFi LP / lending / staking monitoring',
			'Automated yield optimization',
			'FIRE-planning simulations',
			'Natural-language AI chat'
		],
		palette: 'green',
		status: 'planning'
	},
	{
		id: 'terraform-game',
		name: 'Terraform',
		icon: '🤖',
		description:
			'Mobile Action-RTS where you pilot a bipedal robot rebuilding a post-apocalyptic Earth, defending against insectoid swarms, and earning real DeFi yield via AAVE and Uniswap on Base.',
		features: [
			'Unity3D URP — iPad / iPhone first',
			'USDC economy (no proprietary token)',
			'AAVE V3 supply + Uniswap V3 LP fees',
			'Cute-anime low-poly art'
		],
		palette: 'purple',
		status: 'design'
	},
	{
		id: 'matlab-compiler',
		name: 'Matlab Compiler',
		icon: '⚙️',
		description:
			'Real LLVM + MLIR compiler stack for MATLAB. Treats MATLAB as a source language and lowers through progressive MLIR passes — emit portable C/C++/Python/TS, synthesizable SystemVerilog, Verilog-A, or JIT in-process.',
		features: [
			'322-program regression corpus',
			'Modular ~36k-LoC runtime, no BLAS/LAPACK shipped',
			'6 toolbox surfaces: Signal, Control, Comms, RF, Antenna, Propagation',
			'DAP debug server + .mflow flowchart I/O'
		],
		palette: 'orange',
		status: 'active'
	},
	{
		id: 'matforge-ide',
		name: 'MatForge IDE',
		icon: '💻',
		description:
			'SwiftUI macOS IDE for the matlab_llvm toolchain. Editor, REPL, full DAP debugger, visual .mflow flowchart editor, mflowLink signal-flow modeling, and mStateflow state-charts in one window.',
		features: [
			'Conditional / log / hit-count breakpoints',
			'Simulink-style signal-flow modeling',
			'State-chart authoring with TeX annotations',
			'≥97% test coverage on logic core'
		],
		palette: 'red',
		status: 'development'
	},
	{
		id: 'hdl-simulator',
		name: 'HDL Backend Simulator',
		icon: '🔌',
		description:
			'Cloud-ready HDL simulation platform + visual digital-circuit designer. REST API for compiling and simulating VHDL/Verilog (GHDL + Icarus + Yosys); SvelteKit frontend (DigiSim) for drag-and-drop circuit design.',
		features: [
			'VHDL / Verilog / SystemVerilog',
			'VCD + GHW waveforms, Yosys netlists',
			'18 component types, 50-level undo/redo',
			'Webhook callbacks on job completion'
		],
		palette: 'blue',
		status: 'active'
	},
	{
		id: 'vision-factory',
		name: 'Vision Factory',
		icon: '👁️',
		description:
			'Computer-vision pipeline validating that warehouse operators deposit items in the correct bin slot. Hybrid YOLOv8 + ByteTrack + SAM2 architecture, built for Mercado Livre.',
		features: [
			'~30 FPS real-time detection',
			'SAM2 precision masks at the critical ROI',
			'~40% less compute via hybrid scheduling',
			'Edge-deployable: Jetson + TensorRT'
		],
		palette: 'green',
		status: 'active'
	},
	{
		id: 'surf4me',
		name: 'Surf4Me',
		icon: '🏄',
		description:
			'Multi-platform marketplace connecting surfers with instructors, photographers, gear rentals, and accommodations. Five user types share one ecosystem.',
		features: [
			'SwiftUI (iOS) + Jetpack Compose (Android)',
			'Web3Auth wallet login',
			'Live surf + marine conditions',
			'Location-based discovery & bookings'
		],
		palette: 'purple',
		status: 'active'
	},
	{
		id: 'obsidian-mcp',
		name: 'Obsidian MCP Server',
		icon: '🧠',
		description:
			'Dual REST + MCP backend giving AI agents structured access to Obsidian vaults — semantic search via pgvector, knowledge graph via Apache AGE, and user-defined typed tables.',
		features: [
			'Vault ingestion from ZIP + wiki-link parsing',
			'pgvector + OpenAI embedding semantic search',
			'Graph queries: backlinks, shortest path, hubs, orphans',
			'CSV-importable structured tables'
		],
		palette: 'orange',
		status: 'active'
	},
	{
		id: 'claude-skills',
		name: 'Claude Skills',
		icon: '⚡',
		description:
			'Open collection of custom skills extending Claude Code — daily journaling, image / PDF / JSON tooling, NotebookLM automation, PostgreSQL exploration, Obsidian sync, and more.',
		features: [
			'Drop-in skills for Claude Code',
			'Workflow automation (journal, study, bookmarks)',
			'Data tooling (PG, JSON, CSV, PDF, image)',
			'Open source — leonardoaraujosantos/my_ai_skills'
		],
		palette: 'red',
		status: 'active'
	}
];
