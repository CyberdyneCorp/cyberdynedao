<script lang="ts">
	import {
		problemPoints,
		solutionOfferings,
		targetUsers,
		tokenomicsRows,
		tokenUtilityPoints,
		strategicAdvantages,
		flagshipProducts,
		exampleEconomics,
		roadmapPhases
	} from '$lib/data/cyberdyne';

	const phaseBorderColor: Record<string, string> = {
		green: 'border-green-500',
		blue: 'border-blue-500',
		purple: 'border-purple-500',
		orange: 'border-orange-500',
		red: 'border-red-500'
	};
	const phaseTextColor: Record<string, string> = {
		green: 'text-green-700',
		blue: 'text-blue-700',
		purple: 'text-purple-700',
		orange: 'text-orange-700',
		red: 'text-red-700'
	};
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<div class="bg-gradient-to-r from-cyan-600 to-blue-600 p-3 border-b-2 border-black">
		<h1 class="text-xl font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-2xl">🧠</span>
			CYBERDYNE DAO
		</h1>
		<p class="font-mono text-sm text-black">The Future of Self-Sustaining Developer Infrastructure</p>
	</div>

	<div class="flex-1 p-4 space-y-6">
		<!-- What is Cyberdyne -->
		<section class="bg-gradient-to-r from-blue-50 to-cyan-50 rounded border border-blue-200 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">🚀</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">What is Cyberdyne?</h2>
			</div>
			<p class="text-gray-700 mb-3 font-medium">
				Cyberdyne DAO is the first self-funding, community-governed developer platform — a complete, modular development stack that pays for itself.
			</p>
			<p class="text-gray-700 mb-3">It's Firebase + OpenAI + Heroku, but:</p>
			<ul class="space-y-2 text-sm ml-4">
				<li class="flex items-start gap-2"><span class="text-blue-600">•</span><span><strong>Powered by DeFi yields</strong></span></li>
				<li class="flex items-start gap-2"><span class="text-blue-600">•</span><span><strong>Governed by developers</strong></span></li>
				<li class="flex items-start gap-2"><span class="text-blue-600">•</span><span><strong>Owned by the community</strong></span></li>
			</ul>
			<p class="text-gray-700 mt-3 text-sm">
				With Cyberdyne, developers deploy frontend, backend, and automation workflows, and tap into integrated LLMs — all without monthly bills. Infrastructure costs are covered by the DAO treasury's DeFi yield, and surplus is distributed as dividends to token holders.
			</p>
		</section>

		<!-- The Problem -->
		<section class="bg-gradient-to-r from-red-50 to-pink-50 rounded border border-red-200 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">❌</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">The Problem</h2>
			</div>
			<ul class="space-y-2 text-sm">
				{#each problemPoints as p}
					<li class="flex items-start gap-2"><span class="text-red-600">•</span><span>{p}</span></li>
				{/each}
			</ul>
		</section>

		<!-- The Solution -->
		<section class="bg-gradient-to-r from-green-50 to-emerald-50 rounded border border-green-200 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">✅</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">The Solution</h2>
			</div>
			<p class="text-gray-700 mb-3 font-medium">A modular, open-source platform offering:</p>
			<ul class="space-y-2 text-sm mb-4">
				{#each solutionOfferings as s}
					<li class="flex items-start gap-2"><span class="text-green-600">{s.icon}</span><span><strong>{s.title}</strong> {s.description}</span></li>
				{/each}
			</ul>
			<div class="bg-gray-100 rounded p-3">
				<h3 class="font-bold text-sm mb-2">Funding model:</h3>
				<p class="text-sm text-gray-700">
					DAO treasury is staked into diversified DeFi protocols (AAVE, Uniswap LPs, covered loans).
					Yield covers infra, AI, and ops; surplus is paid out in stablecoins to CBY stakers.
				</p>
			</div>
		</section>

		<!-- Target Users -->
		<section class="bg-gradient-to-r from-purple-50 to-indigo-50 rounded border border-purple-200 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">🎯</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">Target Users</h2>
			</div>
			<ul class="space-y-2 text-sm">
				{#each targetUsers as u}
					<li class="flex items-start gap-2"><span class="text-purple-600">•</span><span><strong>{u.name}</strong> → {u.description}</span></li>
				{/each}
			</ul>
		</section>

		<!-- Tokenomics -->
		<section class="bg-gradient-to-r from-yellow-50 to-orange-50 rounded border border-yellow-200 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">🪙</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">Tokenomics (CBY)</h2>
			</div>
			<p class="text-gray-700 mb-3 font-medium">Fixed Supply: 25,000,000 CBY | EVM-compatible</p>

			<div class="overflow-x-auto mb-4">
				<table class="w-full text-xs border-collapse">
					<thead>
						<tr class="bg-gray-100">
							<th class="border p-2 text-left font-mono">Allocation</th>
							<th class="border p-2 text-left font-mono">%</th>
							<th class="border p-2 text-left font-mono">Vesting</th>
						</tr>
					</thead>
					<tbody class="font-mono">
						{#each tokenomicsRows as row}
							<tr>
								<td class="border p-2">{row.allocation}</td>
								<td class="border p-2">{row.percentage}</td>
								<td class="border p-2">{row.vesting}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<h3 class="font-bold text-sm mb-2">Utility:</h3>
			<ul class="space-y-1 text-sm">
				{#each tokenUtilityPoints as u}
					<li class="flex items-start gap-2"><span class="text-orange-600">•</span><span>{u}</span></li>
				{/each}
			</ul>
		</section>

		<!-- Strategic Advantages -->
		<section class="bg-gradient-to-r from-teal-50 to-green-50 rounded border border-teal-200 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">🔥</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">Strategic Advantages</h2>
			</div>
			<ul class="space-y-2 text-sm">
				{#each strategicAdvantages as a}
					<li class="flex items-start gap-2"><span class="text-teal-600">•</span><span><strong>{a.title}</strong> {a.description}</span></li>
				{/each}
			</ul>
		</section>

		<!-- Flagship Products -->
		<section class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded border border-indigo-200 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">🧠</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">Flagship Products</h2>
			</div>
			<ul class="space-y-2 text-sm">
				{#each flagshipProducts as f}
					<li class="flex items-start gap-2"><span class="text-indigo-600">•</span><span><strong>{f.name}</strong> – {f.description}</span></li>
				{/each}
			</ul>
		</section>

		<!-- Example Economics -->
		<section class="bg-gradient-to-r from-green-100 to-emerald-100 rounded border border-green-300 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">💸</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">Example Economics</h2>
			</div>
			<div class="grid grid-cols-2 gap-4 text-sm font-mono">
				{#each exampleEconomics as e}
					<div class="bg-white rounded p-2">
						<div class="text-gray-600">{e.label}</div>
						<div class="font-bold">{e.value}</div>
					</div>
				{/each}
			</div>
			<p class="text-sm text-gray-700 mt-3 font-medium">
				<strong>Result:</strong> Infra is free for users, DAO grows, stakers earn yield.
			</p>
		</section>

		<!-- Roadmap -->
		<section class="bg-gradient-to-r from-gray-50 to-slate-50 rounded border border-gray-300 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">📍</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">Roadmap</h2>
			</div>

			<div class="space-y-4">
				{#each roadmapPhases as phase}
					<div class="border-l-4 {phaseBorderColor[phase.color]} pl-4">
						<h3 class="font-bold text-sm {phaseTextColor[phase.color]}">{phase.title}</h3>
						<ul class="text-xs space-y-1 mt-1">
							{#each phase.items as item}
								<li class="flex items-start gap-2">
									<span class={phaseTextColor[phase.color]}>{item.icon}</span>
									<span>{item.text}</span>
								</li>
							{/each}
						</ul>
					</div>
				{/each}
			</div>
		</section>

		<!-- Closing Statement -->
		<section class="bg-gradient-to-r from-cyan-900 to-blue-900 rounded border border-cyan-700 p-4 text-center">
			<div class="flex items-center justify-center gap-2 mb-3">
				<span class="text-xl">🧠</span>
				<h2 class="text-lg font-bold font-mono text-black">Closing Statement</h2>
			</div>
			<p class="text-sm mb-3 text-black">
				<strong>Cyberdyne is where infrastructure doesn't cost — it yields.</strong>
			</p>
			<p class="text-sm mb-3 text-black">
				Build apps, earn dividends, and govern a self-sustaining ecosystem powered by DeFi.
			</p>
			<div class="bg-white text-black rounded p-3 font-mono text-sm font-bold">
				Cyberdyne = Decentralized Firebase + OpenAI + Heroku → Paid by Yield, Owned by Builders.
			</div>
		</section>
	</div>
</div>
