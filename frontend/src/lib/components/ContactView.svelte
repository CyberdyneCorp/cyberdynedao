<script lang="ts">
	interface ContactMethod {
		id: string;
		name: string;
		icon: string;
		description: string;
		action: string;
		link: string;
		status: 'online' | 'away' | 'busy';
		responseTime: string;
		features: string[];
	}

	interface TeamMember {
		name: string;
		role: string;
		avatar: string;
		status: 'available' | 'busy' | 'offline';
		specialties: string[];
	}

	interface FAQ {
		question: string;
		answer: string;
		category: string;
	}

	const contactMethods: ContactMethod[] = [
		{
			id: 'whatsapp',
			name: 'WhatsApp Bot',
			icon: '💬',
			description: 'Get instant responses from our AI-powered WhatsApp bot for quick support and information.',
			action: 'Chat Now',
			link: 'https://wa.me/1234567890?text=Hello%20Cyberdyne%20Team',
			status: 'online',
			responseTime: 'Instant',
			features: ['24/7 Availability', 'Multi-language Support', 'Technical Q&A', 'Project Inquiries']
		},
		{
			id: 'discord',
			name: 'Discord Community',
			icon: '🎮',
			description: 'Join our Discord server to connect with developers, discuss projects, and get community support.',
			action: 'Join Discord',
			link: 'https://discord.gg/cyberdyne',
			status: 'online',
			responseTime: '< 1 hour',
			features: ['Community Support', 'Developer Chat', 'Announcements', 'Voice Channels']
		},
		{
			id: 'email',
			name: 'Email Support',
			icon: '📧',
			description: 'Send us detailed inquiries and get comprehensive responses from our technical team.',
			action: 'Send Email',
			link: 'mailto:hello@cyberdyne.xyz',
			status: 'online',
			responseTime: '24-48 hours',
			features: ['Detailed Support', 'Technical Documentation', 'Partnership Inquiries', 'Custom Solutions']
		}
	];

	const teamMembers: TeamMember[] = [
		{
			name: 'Alex Chen',
			role: 'Lead Developer',
			avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=50&h=50&fit=crop&crop=face',
			status: 'available',
			specialties: ['Smart Contracts', 'DeFi', 'Solidity']
		},
		{
			name: 'Sarah Rodriguez',
			role: 'Security Engineer',
			avatar: 'https://images.unsplash.com/photo-1494790108755-2616c1f3c85d?w=50&h=50&fit=crop&crop=face',
			status: 'available',
			specialties: ['Security Audits', 'Penetration Testing', 'Web3 Security']
		},
		{
			name: 'Marcus Thompson',
			role: 'Product Manager',
			avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=50&h=50&fit=crop&crop=face',
			status: 'busy',
			specialties: ['Product Strategy', 'Tokenomics', 'User Experience']
		},
		{
			name: 'Dr. Lisa Wang',
			role: 'Blockchain Architect',
			avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=50&h=50&fit=crop&crop=face',
			status: 'available',
			specialties: ['Cosmos SDK', 'IBC Protocol', 'Network Architecture']
		}
	];

	const faqs: FAQ[] = [
		{
			question: 'How can I get started with Cyberdyne services?',
			answer: 'You can start by joining our Discord community or WhatsApp bot for initial consultation. We offer free strategy sessions to understand your project requirements.',
			category: 'Getting Started'
		},
		{
			question: 'Do you provide smart contract auditing services?',
			answer: 'Yes, we offer comprehensive smart contract auditing with detailed security reports, vulnerability assessments, and optimization recommendations.',
			category: 'Services'
		},
		{
			question: 'What blockchain networks do you support?',
			answer: 'We specialize in Ethereum, Cosmos ecosystem, and various Layer 2 solutions. We can also work with other EVM-compatible networks.',
			category: 'Technical'
		},
		{
			question: 'How long does a typical project take?',
			answer: 'Project timelines vary based on complexity. Simple dApps: 4-8 weeks, Complex DeFi protocols: 12-24 weeks, Full DAO implementations: 16-32 weeks.',
			category: 'Timeline'
		},
		{
			question: 'Do you provide ongoing maintenance and support?',
			answer: 'Yes, we offer comprehensive maintenance packages including monitoring, updates, security patches, and feature enhancements.',
			category: 'Support'
		}
	];

	let selectedMethod: ContactMethod | null = null;
	let activeTab: 'contact' | 'team' | 'faq' = 'contact';
	let selectedFAQCategory = 'all';

	$: faqCategories = ['all', ...new Set(faqs.map(faq => faq.category))];
	$: filteredFAQs = selectedFAQCategory === 'all' 
		? faqs 
		: faqs.filter(faq => faq.category === selectedFAQCategory);

	function selectMethod(method: ContactMethod) {
		selectedMethod = method;
	}

	function openContact(method: ContactMethod) {
		if (method.id === 'whatsapp') {
			window.open(method.link, '_blank');
		} else if (method.id === 'discord') {
			window.open(method.link, '_blank');
		} else if (method.id === 'email') {
			window.location.href = method.link;
		}
	}

	function getStatusColor(status: string) {
		switch(status) {
			case 'online': case 'available': return 'text-green-600 bg-green-100';
			case 'away': case 'busy': return 'text-yellow-600 bg-yellow-100';
			case 'offline': return 'text-red-600 bg-red-100';
			default: return 'text-gray-600 bg-gray-100';
		}
	}

	function getStatusIndicator(status: string) {
		switch(status) {
			case 'online': case 'available': return '🟢';
			case 'away': case 'busy': return '🟡';
			case 'offline': return '🔴';
			default: return '⚫';
		}
	}
</script>

<div class="flex flex-col h-full bg-white overflow-y-auto">
	<!-- Header -->
	<div class="bg-gradient-to-r from-blue-600 to-purple-600 p-2 border-b-2 border-black">
		<h1 class="text-lg font-bold font-mono flex items-center gap-2 text-black">
			<span class="text-xl">📞</span>
			CONTACT CYBERDYNE
		</h1>
		<p class="font-mono text-xs text-black">Get in touch • Join our community • Expert support available 24/7</p>
	</div>

	<!-- Navigation Tabs -->
	<div class="border-b border-gray-200 bg-gray-50">
		<nav class="flex font-mono text-xs">
			<button 
				class="px-3 py-1.5 border-r border-gray-200 transition-colors"
				class:bg-white={activeTab === 'contact'}
				class:text-blue-600={activeTab === 'contact'}
				class:font-bold={activeTab === 'contact'}
				on:click={() => activeTab = 'contact'}
			>
				📞 Contact Methods
			</button>
			<button 
				class="px-3 py-1.5 border-r border-gray-200 transition-colors"
				class:bg-white={activeTab === 'team'}
				class:text-blue-600={activeTab === 'team'}
				class:font-bold={activeTab === 'team'}
				on:click={() => activeTab = 'team'}
			>
				👥 Our Team
			</button>
			<button 
				class="px-3 py-1.5 transition-colors"
				class:bg-white={activeTab === 'faq'}
				class:text-blue-600={activeTab === 'faq'}
				class:font-bold={activeTab === 'faq'}
				on:click={() => activeTab = 'faq'}
			>
				❓ FAQ
			</button>
		</nav>
	</div>

	<div class="flex-1 flex">
		<!-- Sidebar -->
		<div class="w-1/3 border-r border-gray-200 bg-gray-50 overflow-y-auto">
			{#if activeTab === 'contact'}
				<div class="p-2 space-y-2">
					<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">Choose Your Preferred Method</h3>
					{#each contactMethods as method}
						<div 
							class="bg-white rounded border border-gray-200 p-2 cursor-pointer transition-all hover:shadow-md"
							class:ring-2={selectedMethod?.id === method.id}
							class:ring-blue-400={selectedMethod?.id === method.id}
							on:click={() => selectMethod(method)}
							role="button"
							tabindex="0"
						>
							<div class="flex items-start gap-1.5 mb-1">
								<span class="text-lg">{method.icon}</span>
								<div class="flex-1 min-w-0">
									<div class="flex items-center gap-1 mb-0.5">
										<h3 class="font-mono font-bold text-xs leading-tight">{method.name}</h3>
										<span class="text-xs">{getStatusIndicator(method.status)}</span>
									</div>
									<div class="flex items-center gap-1 mb-1">
										<span class="text-xs px-1.5 py-0.5 rounded font-mono {getStatusColor(method.status)}">
											{method.status}
										</span>
										<span class="text-xs text-gray-600 font-mono">{method.responseTime}</span>
									</div>
									<p class="text-xs text-gray-600 leading-tight">{method.description.substring(0, 80)}...</p>
								</div>
							</div>
						</div>
					{/each}
				</div>
			{:else if activeTab === 'team'}
				<div class="p-2 space-y-2">
					<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">Meet Our Experts</h3>
					{#each teamMembers as member}
						<div class="bg-white rounded border border-gray-200 p-2">
							<div class="flex items-start gap-2">
								<img 
									src={member.avatar} 
									alt={member.name}
									class="w-8 h-8 rounded-full border border-gray-300"
								/>
								<div class="flex-1 min-w-0">
									<div class="flex items-center gap-1 mb-0.5">
										<h4 class="font-mono font-bold text-xs">{member.name}</h4>
										<span class="text-xs">{getStatusIndicator(member.status)}</span>
									</div>
									<p class="text-xs text-gray-600 font-mono mb-1">{member.role}</p>
									<div class="flex flex-wrap gap-0.5">
										{#each member.specialties.slice(0, 2) as specialty}
											<span class="text-xs px-1 py-0.5 bg-blue-100 text-blue-700 rounded font-mono">
												{specialty}
											</span>
										{/each}
									</div>
								</div>
							</div>
						</div>
					{/each}
				</div>
			{:else}
				<div class="p-2">
					<h3 class="font-mono font-bold text-xs mb-2 text-gray-700">FAQ Categories</h3>
					<div class="space-y-1">
						{#each faqCategories as category}
							<button 
								class="w-full text-left px-2 py-1 text-xs font-mono rounded transition-colors"
								class:bg-blue-100={selectedFAQCategory === category}
								class:text-blue-700={selectedFAQCategory === category}
								class:font-bold={selectedFAQCategory === category}
								on:click={() => selectedFAQCategory = category}
							>
								{category === 'all' ? '📋 All Questions' : `📌 ${category}`}
							</button>
						{/each}
					</div>
				</div>
			{/if}
		</div>

		<!-- Main Content -->
		<div class="flex-1 overflow-y-auto">
			{#if activeTab === 'contact'}
				{#if selectedMethod}
					<div class="p-3">
						<div class="flex items-start gap-2 mb-3">
							<span class="text-3xl">{selectedMethod.icon}</span>
							<div class="flex-1">
								<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">{selectedMethod.name}</h2>
								<div class="flex items-center gap-2 mb-2">
									<span class="text-xs px-2 py-0.5 rounded font-mono {getStatusColor(selectedMethod.status)}">
										{selectedMethod.status}
									</span>
									<span class="text-xs text-gray-600 font-mono">Response time: {selectedMethod.responseTime}</span>
								</div>
								<p class="text-sm text-gray-700 leading-relaxed">{selectedMethod.description}</p>
							</div>
						</div>

						<div class="bg-gray-50 rounded border border-gray-200 p-2 mb-3">
							<h3 class="font-mono font-bold text-sm mb-2">✨ Features</h3>
							<div class="grid grid-cols-2 gap-1">
								{#each selectedMethod.features as feature}
									<div class="flex items-center gap-1 text-xs">
										<span class="text-green-500">✓</span>
										<span class="font-mono">{feature}</span>
									</div>
								{/each}
							</div>
						</div>

						<div class="bg-blue-50 rounded border border-blue-200 p-2 mb-3">
							<h3 class="font-mono font-bold text-sm mb-2">🚀 Quick Start</h3>
							{#if selectedMethod.id === 'whatsapp'}
								<p class="text-xs text-gray-700 font-mono mb-2">Click the button below to start chatting with our AI bot. You can ask about:</p>
								<ul class="text-xs text-gray-600 font-mono space-y-0.5 mb-2">
									<li>• Project consultation</li>
									<li>• Technical questions</li>
									<li>• Service pricing</li>
									<li>• Scheduling meetings</li>
								</ul>
							{:else if selectedMethod.id === 'discord'}
								<p class="text-xs text-gray-700 font-mono mb-2">Join our Discord server to:</p>
								<ul class="text-xs text-gray-600 font-mono space-y-0.5 mb-2">
									<li>• Connect with developers</li>
									<li>• Get community support</li>
									<li>• Participate in discussions</li>
									<li>• Access exclusive channels</li>
								</ul>
							{:else if selectedMethod.id === 'email'}
								<p class="text-xs text-gray-700 font-mono mb-2">Send us an email for:</p>
								<ul class="text-xs text-gray-600 font-mono space-y-0.5 mb-2">
									<li>• Detailed project proposals</li>
									<li>• Partnership inquiries</li>
									<li>• Technical documentation</li>
									<li>• Custom solutions</li>
								</ul>
							{/if}
						</div>

						<div class="flex gap-2">
							<button 
								class="bg-blue-600 text-white px-4 py-1.5 rounded font-mono text-xs font-bold hover:bg-blue-700 transition-colors"
								on:click={() => openContact(selectedMethod)}
							>
								{selectedMethod.action}
							</button>
							<button class="border border-gray-300 text-gray-700 px-4 py-1.5 rounded font-mono text-xs hover:bg-gray-50 transition-colors">
								Save Contact
							</button>
						</div>
					</div>
				{:else}
					<div class="p-3 text-center">
						<div class="text-3xl mb-2">📞</div>
						<h2 class="text-lg font-bold font-mono text-gray-800 mb-1">Get in Touch</h2>
						<p class="text-sm text-gray-600 font-mono mb-4">Choose your preferred method to connect with our team and get expert support.</p>
						
						<div class="grid grid-cols-2 gap-2">
							<div class="bg-green-50 rounded border border-green-200 p-2">
								<div class="text-lg mb-1">💬</div>
								<h3 class="font-mono font-bold text-xs">WhatsApp Bot</h3>
								<p class="text-xs text-gray-600">Instant AI support</p>
							</div>
							<div class="bg-purple-50 rounded border border-purple-200 p-2">
								<div class="text-lg mb-1">🎮</div>
								<h3 class="font-mono font-bold text-xs">Discord</h3>
								<p class="text-xs text-gray-600">Join community</p>
							</div>
						</div>
					</div>
				{/if}
			{:else if activeTab === 'team'}
				<div class="p-3">
					<h2 class="text-lg font-bold font-mono text-gray-800 mb-2">Meet the Cyberdyne Team</h2>
					<p class="text-sm text-gray-600 font-mono mb-4">Our expert team is here to help you build the future of Web3.</p>
					
					<div class="grid grid-cols-1 gap-3">
						{#each teamMembers as member}
							<div class="bg-white rounded border border-gray-200 p-3">
								<div class="flex items-start gap-3">
									<img 
										src={member.avatar} 
										alt={member.name}
										class="w-12 h-12 rounded-full border-2 border-gray-300"
									/>
									<div class="flex-1">
										<div class="flex items-center gap-2 mb-1">
											<h3 class="font-mono font-bold text-sm">{member.name}</h3>
											<span class="text-sm">{getStatusIndicator(member.status)}</span>
											<span class="text-xs px-2 py-0.5 rounded font-mono {getStatusColor(member.status)}">
												{member.status}
											</span>
										</div>
										<p class="text-xs text-gray-600 font-mono mb-2">{member.role}</p>
										<div class="flex flex-wrap gap-1">
											{#each member.specialties as specialty}
												<span class="text-xs px-2 py-0.5 bg-blue-100 text-blue-700 rounded font-mono">
													{specialty}
												</span>
											{/each}
										</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{:else}
				<div class="p-3">
					<h2 class="text-lg font-bold font-mono text-gray-800 mb-2">Frequently Asked Questions</h2>
					<p class="text-sm text-gray-600 font-mono mb-4">Find answers to common questions about our services and processes.</p>
					
					<div class="space-y-3">
						{#each filteredFAQs as faq}
							<div class="bg-white rounded border border-gray-200 p-3">
								<h3 class="font-mono font-bold text-sm mb-2 text-gray-800">{faq.question}</h3>
								<p class="text-xs text-gray-700 leading-relaxed font-mono">{faq.answer}</p>
								<span class="inline-block mt-2 text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded font-mono">
									{faq.category}
								</span>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>