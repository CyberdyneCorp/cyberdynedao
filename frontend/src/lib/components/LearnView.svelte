<script lang="ts">
	interface LearningModule {
		id: string;
		title: string;
		category: string;
		description: string;
		level: 'Beginner' | 'Intermediate' | 'Advanced';
		duration: string;
		icon: string;
		topics: string[];
		completed?: boolean;
	}

	interface LearningPath {
		id: string;
		title: string;
		description: string;
		modules: string[];
		icon: string;
		estimatedTime: string;
	}

	const learningModules: LearningModule[] = [
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

	const learningPaths: LearningPath[] = [
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

	let selectedModule: LearningModule | null = null;
	let selectedPath: LearningPath | null = null;
	let activeTab: 'modules' | 'paths' | 'resources' = 'modules';

	function selectModule(module: LearningModule) {
		selectedModule = module;
		selectedPath = null;
	}

	function selectPath(path: LearningPath) {
		selectedPath = path;
		selectedModule = null;
	}

	function getLevelColor(level: string) {
		switch(level) {
			case 'Beginner': return 'text-green-600 bg-green-100';
			case 'Intermediate': return 'text-yellow-600 bg-yellow-100';
			case 'Advanced': return 'text-red-600 bg-red-100';
			default: return 'text-gray-600 bg-gray-100';
		}
	}

	function getCategoryColor(category: string) {
		switch(category) {
			case 'Blockchain': return 'text-blue-600 bg-blue-100';
			case 'Development': return 'text-purple-600 bg-purple-100';
			case 'Governance': return 'text-indigo-600 bg-indigo-100';
			case 'DeFi': return 'text-green-600 bg-green-100';
			case 'Economics': return 'text-orange-600 bg-orange-100';
			case 'Infrastructure': return 'text-gray-600 bg-gray-100';
			case 'Security': return 'text-red-600 bg-red-100';
			default: return 'text-gray-600 bg-gray-100';
		}
	}
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<!-- Header -->
	<div class="bg-gradient-to-r from-purple-600 to-blue-600 p-2 border-b-2 border-black">
		<h1 class="text-lg font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-xl">🎓</span>
			CYBERDYNE ACADEMY
		</h1>
		<p class="font-mono text-xs text-black">Learn Blockchain • Web3 Development • DAO Operations • DeFi Protocols</p>
	</div>

	<!-- Navigation Tabs -->
	<div class="border-b border-gray-200 bg-gray-50">
		<nav class="flex font-mono text-xs">
			<button 
				class="px-3 py-1.5 border-r border-gray-200 transition-colors"
				class:bg-white={activeTab === 'modules'}
				class:text-blue-600={activeTab === 'modules'}
				class:font-bold={activeTab === 'modules'}
				on:click={() => activeTab = 'modules'}
			>
				📚 Learning Modules
			</button>
			<button 
				class="px-3 py-1.5 border-r border-gray-200 transition-colors"
				class:bg-white={activeTab === 'paths'}
				class:text-blue-600={activeTab === 'paths'}
				class:font-bold={activeTab === 'paths'}
				on:click={() => activeTab = 'paths'}
			>
				🗺️ Learning Paths
			</button>
			<button 
				class="px-3 py-1.5 transition-colors"
				class:bg-white={activeTab === 'resources'}
				class:text-blue-600={activeTab === 'resources'}
				class:font-bold={activeTab === 'resources'}
				on:click={() => activeTab = 'resources'}
			>
				📖 Resources
			</button>
		</nav>
	</div>

	<div class="flex-1 flex">
		<!-- Sidebar -->
		<div class="w-1/3 border-r border-gray-200 bg-gray-50 overflow-y-auto">
			{#if activeTab === 'modules'}
				<div class="p-2 space-y-2">
					{#each learningModules as module}
						<div 
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={selectedModule?.id === module.id}
							class:ring-blue-400={selectedModule?.id === module.id}
							on:click={() => selectModule(module)}
							on:keydown={(e) => e.key === 'Enter' && selectModule(module)}
							role="button"
							tabindex="0"
						>
							<div class="flex items-start gap-1.5 mb-1">
								<span class="text-sm">{module.icon}</span>
								<div class="flex-1 min-w-0">
									<h3 class="font-mono font-bold text-xs leading-tight">{module.title}</h3>
									<div class="flex items-center gap-1 mt-0.5">
										<span class="text-xs px-1.5 py-0.5 rounded font-mono {getCategoryColor(module.category)}">
											{module.category}
										</span>
										<span class="text-xs px-1.5 py-0.5 rounded font-mono {getLevelColor(module.level)}">
											{module.level}
										</span>
									</div>
									<p class="text-xs text-gray-600 mt-0.5 font-mono">⏱️ {module.duration}</p>
								</div>
							</div>
						</div>
					{/each}
				</div>
			{:else if activeTab === 'paths'}
				<div class="p-2 space-y-2">
					{#each learningPaths as path}
						<div 
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={selectedPath?.id === path.id}
							class:ring-blue-400={selectedPath?.id === path.id}
							on:click={() => selectPath(path)}
							on:keydown={(e) => e.key === 'Enter' && selectPath(path)}
							role="button"
							tabindex="0"
						>
							<div class="flex items-start gap-1.5 mb-1">
								<span class="text-sm">{path.icon}</span>
								<div class="flex-1 min-w-0">
									<h3 class="font-mono font-bold text-xs leading-tight">{path.title}</h3>
									<p class="text-xs text-gray-600 mt-0.5 font-mono leading-tight">{path.description}</p>
									<p class="text-xs text-blue-600 mt-0.5 font-mono">📅 {path.estimatedTime}</p>
								</div>
							</div>
						</div>
					{/each}
				</div>
			{:else}
				<div class="p-2 space-y-2">
					<div class="bg-white rounded border border-gray-200 p-2">
						<h3 class="font-mono font-bold text-xs mb-1">📚 Documentation</h3>
						<ul class="space-y-0.5 text-xs">
							<li><a href="https://docs.cosmos.network/" class="text-blue-600 hover:underline">Cosmos SDK Docs</a></li>
							<li><a href="https://docs.soliditylang.org/" class="text-blue-600 hover:underline">Solidity Documentation</a></li>
							<li><a href="https://web3js.readthedocs.io/" class="text-blue-600 hover:underline">Web3.js Guide</a></li>
						</ul>
					</div>
					<div class="bg-white rounded border border-gray-200 p-2">
						<h3 class="font-mono font-bold text-xs mb-1">🛠️ Tools</h3>
						<ul class="space-y-0.5 text-xs">
							<li><a href="https://remix.ethereum.org/" class="text-blue-600 hover:underline">Remix IDE</a></li>
							<li><a href="https://hardhat.org/" class="text-blue-600 hover:underline">Hardhat Framework</a></li>
							<li><a href="https://metamask.io/" class="text-blue-600 hover:underline">MetaMask</a></li>
						</ul>
					</div>
					<div class="bg-white rounded border border-gray-200 p-2">
						<h3 class="font-mono font-bold text-xs mb-1">🌐 Communities</h3>
						<ul class="space-y-0.5 text-xs">
							<li><button class="text-blue-600 hover:underline text-left" disabled>Cyberdyne Discord (Coming Soon)</button></li>
							<li><button class="text-blue-600 hover:underline text-left" disabled>Developer Forum (Coming Soon)</button></li>
							<li><button class="text-blue-600 hover:underline text-left" disabled>Weekly Dev Calls (Coming Soon)</button></li>
						</ul>
					</div>
				</div>
			{/if}
		</div>

		<!-- Main Content -->
		<div class="flex-1 overflow-y-auto">
			{#if selectedModule}
				<div class="p-3">
					<div class="flex items-start gap-2 mb-3">
						<span class="text-2xl">{selectedModule.icon}</span>
						<div class="flex-1">
							<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">{selectedModule.title}</h2>
							<div class="flex items-center gap-2 mb-2">
								<span class="text-xs px-2 py-0.5 rounded font-mono {getCategoryColor(selectedModule.category)}">
									{selectedModule.category}
								</span>
								<span class="text-xs px-2 py-0.5 rounded font-mono {getLevelColor(selectedModule.level)}">
									{selectedModule.level}
								</span>
								<span class="text-xs text-gray-600 font-mono">⏱️ {selectedModule.duration}</span>
							</div>
							<p class="text-sm text-gray-700 leading-relaxed">{selectedModule.description}</p>
						</div>
					</div>

					<div class="bg-gray-50 rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">📋 Learning Topics</h3>
						<div class="grid grid-cols-2 gap-1">
							{#each selectedModule.topics as topic}
								<div class="flex items-center gap-1 text-xs">
									<span class="text-green-500">✓</span>
									<span class="font-mono">{topic}</span>
								</div>
							{/each}
						</div>
					</div>

					<div class="flex gap-2">
						<button class="bg-blue-600 text-white px-4 py-1.5 rounded font-mono text-xs font-bold hover:bg-blue-700 transition-colors">
							Start Learning
						</button>
						<button class="border border-gray-300 text-gray-700 px-4 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							Add to Favorites
						</button>
					</div>
				</div>
			{:else if selectedPath}
				<div class="p-3">
					<div class="flex items-start gap-2 mb-3">
						<span class="text-2xl">{selectedPath.icon}</span>
						<div class="flex-1">
							<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">{selectedPath.title}</h2>
							<p class="text-sm text-gray-700 leading-relaxed mb-2">{selectedPath.description}</p>
							<p class="text-xs text-blue-600 font-mono">📅 Estimated completion: {selectedPath.estimatedTime}</p>
						</div>
					</div>

					<div class="bg-gray-50 rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">📚 Learning Modules</h3>
						<div class="space-y-1.5">
							{#each selectedPath.modules as moduleId, index}
								{@const module = learningModules.find(m => m.id === moduleId)}
								{#if module}
									<div class="flex items-center gap-2 p-2 bg-white rounded border border-gray-200">
										<span class="bg-blue-100 text-blue-600 text-xs font-bold font-mono w-5 h-5 rounded-full flex items-center justify-center">
											{index + 1}
										</span>
										<span class="text-sm">{module.icon}</span>
										<div class="flex-1">
											<h4 class="font-mono font-bold text-xs">{module.title}</h4>
											<p class="text-xs text-gray-600 font-mono">⏱️ {module.duration}</p>
										</div>
										<span class="text-xs px-1.5 py-0.5 rounded font-mono {getLevelColor(module.level)}">
											{module.level}
										</span>
									</div>
								{/if}
							{/each}
						</div>
					</div>

					<div class="flex gap-2">
						<button class="bg-purple-600 text-white px-4 py-1.5 rounded font-mono text-xs font-bold hover:bg-purple-700 transition-colors">
							Start Learning Path
						</button>
						<button class="border border-gray-300 text-gray-700 px-4 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
							Save for Later
						</button>
					</div>
				</div>
			{:else}
				<div class="p-3 text-center">
					<div class="text-3xl mb-2">🎓</div>
					<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">Welcome to Cyberdyne Academy</h2>
					<p class="text-sm text-gray-600 font-mono mb-4">Select a learning module or path to get started with your Web3 education journey.</p>
					
					<div class="grid grid-cols-3 gap-2">
						<div class="bg-blue-50 rounded border border-blue-200 p-2">
							<div class="text-lg mb-1">📚</div>
							<h3 class="font-mono font-bold text-xs">8 Modules</h3>
							<p class="text-xs text-gray-600">Comprehensive topics</p>
						</div>
						<div class="bg-purple-50 rounded border border-purple-200 p-2">
							<div class="text-lg mb-1">🗺️</div>
							<h3 class="font-mono font-bold text-xs">3 Paths</h3>
							<p class="text-xs text-gray-600">Structured learning</p>
						</div>
						<div class="bg-green-50 rounded border border-green-200 p-2">
							<div class="text-lg mb-1">🏆</div>
							<h3 class="font-mono font-bold text-xs">Certificates</h3>
							<p class="text-xs text-gray-600">Verifiable credentials</p>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>