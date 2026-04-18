<script lang="ts">
	import { PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import { serviceSections, workflowSteps, whyCyberdynePoints } from '$lib/data/services';
</script>

<div class="flex flex-col h-full bg-white">
	<div class="bg-gradient-to-r from-blue-600 to-cyan-600 p-3 border-b-2 border-black">
		<h1 class="text-xl font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-2xl">⚙️</span>
			CYBERDYNE SERVICES
		</h1>
		<p class="font-mono text-xs text-black">Full-Stack Development • Backend & Frontend Servers • Decentralized Infrastructure</p>
	</div>

	<PixelScrollArea maxHeight="100%" ariaLabel="Services">
	<div class="p-4 space-y-6">
		{#each serviceSections as section}
			<section class="bg-gradient-to-r {section.gradientFrom} {section.gradientTo} rounded border {section.borderColor} p-4">
				<div class="flex items-center gap-2 mb-3">
					<span class="text-xl">{section.icon}</span>
					<h2 class="text-lg font-bold font-mono text-gray-800">{section.title}</h2>
				</div>
				<p class="text-gray-700 mb-3 font-medium">{section.intro}</p>
				<ul class="space-y-2 text-sm">
					{#each section.bullets as bullet}
						<li class="flex items-start gap-2">
							<span class={section.bulletColor}>•</span>
							<span><strong>{bullet.title}</strong> {bullet.description}</span>
						</li>
					{/each}
				</ul>
			</section>
		{/each}

		<section class="bg-gradient-to-r from-gray-50 to-slate-50 rounded border border-gray-300 p-4">
			<div class="flex items-center gap-2 mb-3">
				<span class="text-xl">🚀</span>
				<h2 class="text-lg font-bold font-mono text-gray-800">How We Work (Short and Sweet)</h2>
			</div>
			<ol class="space-y-2 text-sm">
				{#each workflowSteps as step, idx}
					<li class="flex items-start gap-3">
						<span class="bg-gray-700 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold">{idx + 1}</span>
						<span>{step}</span>
					</li>
				{/each}
			</ol>
		</section>

		<section class="bg-gradient-to-r from-cyan-50 to-blue-50 rounded border border-cyan-200 p-4">
			<div class="flex items-center gap-2 mb-3">
				<svg class="w-5 h-5" fill="#eab308" viewBox="0 0 20 20">
					<path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
				</svg>
				<h2 class="text-lg font-bold font-mono text-gray-800">Why Cyberdyne</h2>
			</div>
			<ul class="space-y-2 text-sm">
				{#each whyCyberdynePoints as point}
					<li class="flex items-start gap-2">
						<span class="text-cyan-600">•</span>
						<span class="text-gray-700"><strong>{point.title}</strong> {point.description}</span>
					</li>
				{/each}
			</ul>
		</section>

		<section class="bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded border border-green-500 p-4 text-center">
			<h2 class="text-lg font-bold font-mono mb-2">Ready to Build?</h2>
			<p class="text-sm mb-3">Let's turn your vision into a self-sustaining, yield-powered platform.</p>
			<div class="flex justify-center gap-4 text-xs font-mono">
				<div class="bg-white text-green-600 px-3 py-1 rounded font-bold">Backend Development</div>
				<div class="bg-white text-green-600 px-3 py-1 rounded font-bold">Frontend Servers</div>
				<div class="bg-white text-green-600 px-3 py-1 rounded font-bold">Full-Stack Solutions</div>
			</div>
		</section>
	</div>
	</PixelScrollArea>
</div>
