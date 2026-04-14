<script lang="ts">
	import { productSuite } from '$lib/data/products';

	const paletteClasses = {
		blue: { card: 'from-blue-50 to-blue-100 border-blue-200', icon: 'bg-blue-500', title: 'text-blue-800', feat: 'text-blue-700' },
		green: { card: 'from-green-50 to-green-100 border-green-200', icon: 'bg-green-500', title: 'text-green-800', feat: 'text-green-700' },
		purple: { card: 'from-purple-50 to-purple-100 border-purple-200', icon: 'bg-purple-500', title: 'text-purple-800', feat: 'text-purple-700' },
		orange: { card: 'from-orange-50 to-orange-100 border-orange-200', icon: 'bg-orange-500', title: 'text-orange-800', feat: 'text-orange-700' },
		red: { card: 'from-red-50 to-red-100 border-red-200', icon: 'bg-red-500', title: 'text-red-800', feat: 'text-red-700' }
	} as const;
</script>

<div class="products-container">
	<div class="header-section mb-8">
		<h1 class="text-3xl font-mono font-bold text-center mb-4">CyberdyneCorp Product Suite</h1>
		<p class="text-lg text-center text-gray-700 mb-6">
			Discover our comprehensive suite of cutting-edge financial and lifestyle products designed to transform your digital experience.
		</p>
	</div>

	<div class="products-grid grid grid-cols-1 md:grid-cols-2 gap-6">
		{#each productSuite as product}
			{@const p = paletteClasses[product.palette]}
			<div class="product-card bg-gradient-to-br {p.card} p-6 rounded-lg border-2" class:md:col-span-2={product.fullWidth}>
				<div class="flex items-center mb-4">
					<div class="w-12 h-12 {p.icon} rounded-lg flex items-center justify-center mr-4">
						<span class="text-2xl">{product.icon}</span>
					</div>
					<h2 class="text-2xl font-mono font-bold {p.title}">{product.name}</h2>
				</div>
				<p class="text-gray-700 mb-4">{product.description}</p>
				<div class="features">
					<h3 class="font-semibold {p.feat} mb-2">Key Features:</h3>
					{#if product.extraFeatures}
						<div class="grid md:grid-cols-2 gap-4">
							<ul class="text-sm text-gray-600 space-y-1">
								{#each product.features as f}<li>• {f}</li>{/each}
							</ul>
							<ul class="text-sm text-gray-600 space-y-1">
								{#each product.extraFeatures as f}<li>• {f}</li>{/each}
							</ul>
						</div>
					{:else}
						<ul class="text-sm text-gray-600 space-y-1">
							{#each product.features as f}<li>• {f}</li>{/each}
						</ul>
					{/if}
				</div>
			</div>
		{/each}
	</div>

	<div class="cta-section mt-8 text-center">
		<p class="text-lg text-gray-600 mb-4">
			Ready to experience the future of digital finance and lifestyle management?
		</p>
		<button class="px-6 py-3 bg-blue-600 text-white font-mono font-semibold rounded-lg hover:bg-blue-700 transition-colors">
			Explore Our Products
		</button>
	</div>
</div>

<style>
	.products-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
	.product-card { transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }
	.product-card:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); }
</style>
