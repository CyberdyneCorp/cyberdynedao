<script lang="ts">
	import type { LearningModule, LearningPath } from '$lib/types/components';
	import {
		createLearnViewModel,
		getLevelColor,
		getLearnCategoryColor as getCategoryColor
	} from '$lib/viewmodels/learnViewModel';

	const vm = createLearnViewModel();
	const { selectedModule, selectedPath, activeTab } = vm;
	const { modules: learningModules, paths: learningPaths } = vm;

	function selectModule(module: LearningModule) {
		vm.selectModule(module);
	}

	function selectPath(path: LearningPath) {
		vm.selectPath(path);
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
				class:bg-white={$activeTab === 'modules'}
				class:text-blue-600={$activeTab === 'modules'}
				class:font-bold={$activeTab === 'modules'}
				on:click={() => vm.setTab('modules')}
			>
				📚 Learning Modules
			</button>
			<button
				class="px-3 py-1.5 border-r border-gray-200 transition-colors"
				class:bg-white={$activeTab === 'paths'}
				class:text-blue-600={$activeTab === 'paths'}
				class:font-bold={$activeTab === 'paths'}
				on:click={() => vm.setTab('paths')}
			>
				🗺️ Learning Paths
			</button>
			<button
				class="px-3 py-1.5 transition-colors"
				class:bg-white={$activeTab === 'resources'}
				class:text-blue-600={$activeTab === 'resources'}
				class:font-bold={$activeTab === 'resources'}
				on:click={() => vm.setTab('resources')}
			>
				📖 Resources
			</button>
		</nav>
	</div>

	<div class="flex-1 flex">
		<!-- Sidebar -->
		<div class="w-1/3 border-r border-gray-200 bg-gray-50 overflow-y-auto">
			{#if $activeTab === 'modules'}
				<div class="p-2 space-y-2">
					{#each learningModules as module}
						<div
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={$selectedModule?.id === module.id}
							class:ring-blue-400={$selectedModule?.id === module.id}
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
			{:else if $activeTab === 'paths'}
				<div class="p-2 space-y-2">
					{#each learningPaths as path}
						<div
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={$selectedPath?.id === path.id}
							class:ring-blue-400={$selectedPath?.id === path.id}
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
			{#if $selectedModule}
				<div class="p-3">
					<div class="flex items-start gap-2 mb-3">
						<span class="text-2xl">{$selectedModule.icon}</span>
						<div class="flex-1">
							<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">{$selectedModule.title}</h2>
							<div class="flex items-center gap-2 mb-2">
								<span class="text-xs px-2 py-0.5 rounded font-mono {getCategoryColor($selectedModule.category)}">
									{$selectedModule.category}
								</span>
								<span class="text-xs px-2 py-0.5 rounded font-mono {getLevelColor($selectedModule.level)}">
									{$selectedModule.level}
								</span>
								<span class="text-xs text-gray-600 font-mono">⏱️ {$selectedModule.duration}</span>
							</div>
							<p class="text-sm text-gray-700 leading-relaxed">{$selectedModule.description}</p>
						</div>
					</div>

					<div class="bg-gray-50 rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">📋 Learning Topics</h3>
						<div class="grid grid-cols-2 gap-1">
							{#each $selectedModule.topics as topic}
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
			{:else if $selectedPath}
				<div class="p-3">
					<div class="flex items-start gap-2 mb-3">
						<span class="text-2xl">{$selectedPath.icon}</span>
						<div class="flex-1">
							<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">{$selectedPath.title}</h2>
							<p class="text-sm text-gray-700 leading-relaxed mb-2">{$selectedPath.description}</p>
							<p class="text-xs text-blue-600 font-mono">📅 Estimated completion: {$selectedPath.estimatedTime}</p>
						</div>
					</div>

					<div class="bg-gray-50 rounded border border-gray-200 p-2 mb-3">
						<h3 class="font-mono font-bold text-sm mb-2">📚 Learning Modules</h3>
						<div class="space-y-1.5">
							{#each $selectedPath.modules as moduleId, index}
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
							<h3 class="font-mono font-bold text-xs">{learningModules.length} Modules</h3>
							<p class="text-xs text-gray-600">Comprehensive topics</p>
						</div>
						<div class="bg-purple-50 rounded border border-purple-200 p-2">
							<div class="text-lg mb-1">🗺️</div>
							<h3 class="font-mono font-bold text-xs">{learningPaths.length} Paths</h3>
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
