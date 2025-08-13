<script lang="ts">
	// Products view component
</script>

<div class="products-container">
	<div class="header-section mb-8">
		<h1 class="text-3xl font-mono font-bold text-center mb-4">CyberdyneCorp Product Suite</h1>
		<p class="text-lg text-center text-gray-700 mb-6">
			Discover our comprehensive suite of cutting-edge financial and lifestyle products designed to transform your digital experience.
		</p>
	</div>

	<div class="products-grid grid grid-cols-1 md:grid-cols-2 gap-6">
		<!-- Trade4Me -->
		<div class="product-card bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg border-2 border-blue-200">
			<div class="flex items-center mb-4">
				<div class="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
					<span class="text-2xl">📈</span>
				</div>
				<h2 class="text-2xl font-mono font-bold text-blue-800">Trade4Me</h2>
			</div>
			<p class="text-gray-700 mb-4">
				Advanced algorithmic trading platform powered by AI. Execute trades with precision, 
				analyze market trends in real-time, and maximize your investment potential with our 
				intelligent trading algorithms.
			</p>
			<div class="features">
				<h3 class="font-semibold text-blue-700 mb-2">Key Features:</h3>
				<ul class="text-sm text-gray-600 space-y-1">
					<li>• AI-powered market analysis</li>
					<li>• Real-time portfolio optimization</li>
					<li>• Risk management algorithms</li>
					<li>• Multi-asset trading support</li>
				</ul>
			</div>
		</div>

		<!-- Liquidity4Me -->
		<div class="product-card bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border-2 border-green-200">
			<div class="flex items-center mb-4">
				<div class="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mr-4">
					<span class="text-2xl">💧</span>
				</div>
				<h2 class="text-2xl font-mono font-bold text-green-800">Liquidity4Me</h2>
			</div>
			<p class="text-gray-700 mb-4">
				Revolutionary liquidity mining and yield farming platform. Optimize your DeFi returns 
				through automated liquidity provision strategies across multiple protocols and chains.
			</p>
			<div class="features">
				<h3 class="font-semibold text-green-700 mb-2">Key Features:</h3>
				<ul class="text-sm text-gray-600 space-y-1">
					<li>• Cross-chain liquidity optimization</li>
					<li>• Automated yield farming</li>
					<li>• Impermanent loss protection</li>
					<li>• Smart contract audited</li>
				</ul>
			</div>
		</div>

		<!-- Surf4Me -->
		<div class="product-card bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-lg border-2 border-purple-200">
			<div class="flex items-center mb-4">
				<div class="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mr-4">
					<span class="text-2xl">🏄</span>
				</div>
				<h2 class="text-2xl font-mono font-bold text-purple-800">Surf4Me</h2>
			</div>
			<p class="text-gray-700 mb-4">
				Next-generation web3 browsing experience with built-in privacy protection, 
				decentralized content discovery, and seamless interaction with blockchain applications.
			</p>
			<div class="features">
				<h3 class="font-semibold text-purple-700 mb-2">Key Features:</h3>
				<ul class="text-sm text-gray-600 space-y-1">
					<li>• Privacy-first browsing</li>
					<li>• Integrated DApp discovery</li>
					<li>• Decentralized identity management</li>
					<li>• Built-in crypto wallet</li>
				</ul>
			</div>
		</div>

		<!-- Budget4Me -->
		<div class="product-card bg-gradient-to-br from-orange-50 to-orange-100 p-6 rounded-lg border-2 border-orange-200">
			<div class="flex items-center mb-4">
				<div class="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center mr-4">
					<span class="text-2xl">💰</span>
				</div>
				<h2 class="text-2xl font-mono font-bold text-orange-800">Budget4Me</h2>
			</div>
			<p class="text-gray-700 mb-4">
				Intelligent personal finance management system with AI-powered budgeting, 
				expense tracking, and financial goal optimization for the modern digital lifestyle.
			</p>
			<div class="features">
				<h3 class="font-semibold text-orange-700 mb-2">Key Features:</h3>
				<ul class="text-sm text-gray-600 space-y-1">
					<li>• AI budgeting recommendations</li>
					<li>• Automated expense categorization</li>
					<li>• Goal-based saving strategies</li>
					<li>• Multi-currency support</li>
				</ul>
			</div>
		</div>

		<!-- bHealthy -->
		<div class="product-card bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-lg border-2 border-red-200 md:col-span-2">
			<div class="flex items-center mb-4">
				<div class="w-12 h-12 bg-red-500 rounded-lg flex items-center justify-center mr-4">
					<span class="text-2xl">❤️</span>
				</div>
				<h2 class="text-2xl font-mono font-bold text-red-800">bHealthy</h2>
			</div>
			<p class="text-gray-700 mb-4">
				Comprehensive blockchain-based health management platform that puts you in control 
				of your health data while connecting you with healthcare providers and wellness programs.
			</p>
			<div class="features">
				<h3 class="font-semibold text-red-700 mb-2">Key Features:</h3>
				<div class="grid md:grid-cols-2 gap-4">
					<ul class="text-sm text-gray-600 space-y-1">
						<li>• Secure health data storage</li>
						<li>• AI health insights</li>
						<li>• Telemedicine integration</li>
						<li>• Fitness tracking & rewards</li>
					</ul>
					<ul class="text-sm text-gray-600 space-y-1">
						<li>• Medication reminders</li>
						<li>• Health NFT achievements</li>
						<li>• Provider network access</li>
						<li>• Anonymous health research</li>
					</ul>
				</div>
			</div>
		</div>
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
	.products-container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 20px;
	}
	
	.product-card {
		transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
	}
	
	.product-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
	}
</style>