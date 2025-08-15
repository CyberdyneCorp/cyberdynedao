<script lang="ts">
	interface ContactMethod {
		id: string;
		name: string;
		icon: string;
		description: string;
		action: string;
		link: string;
		bgColor: string;
		hoverColor: string;
		iconBg: string;
	}

	const contactMethods: ContactMethod[] = [
		{
			id: 'whatsapp',
			name: 'WhatsApp Bot',
			icon: '💬',
			description: 'AI support for your Web3 projects',
			action: 'Start Chatting',
			link: 'https://wa.me/1234567890?text=Hello%20Cyberdyne%20Team',
			bgColor: 'bg-gradient-to-br from-green-400 via-green-500 to-green-600',
			hoverColor: 'hover:from-green-500 hover:via-green-600 hover:to-green-700',
			iconBg: 'bg-green-100'
		},
		{
			id: 'discord',
			name: 'Discord Community',
			icon: '🎮',
			description: 'Join our vibrant developer community',
			action: 'Join Server',
			link: 'https://discord.gg/cyberdyne',
			bgColor: 'bg-gradient-to-br from-indigo-400 via-purple-500 to-pink-600',
			hoverColor: 'hover:from-indigo-500 hover:via-purple-600 hover:to-pink-700',
			iconBg: 'bg-purple-100'
		}
	];

	function openContact(method: ContactMethod) {
		window.open(method.link, '_blank');
	}
</script>

<div class="flex flex-col h-full bg-black text-retro-green font-mono overflow-y-auto" style="background-color: #000 !important; color: #00ff00 !important; -webkit-overflow-scrolling: touch; scroll-behavior: smooth;">
	<!-- Retro Header -->
	<div class="p-2 border-b-2" style="background: linear-gradient(to right, #00aa00, #00ff00); border-color: #00ff00;">
		<div class="text-center">
			<div class="text-2xl mb-1 animate-pulse" style="color: #88ff88;">◉ CONTACT CYBERDYNE ◉</div>
			<div class="text-xs tracking-wider" style="color: #ccffcc;">[ SECURE COMMUNICATION CHANNELS ACTIVE ]</div>
		</div>
	</div>

	<!-- Cyberpunk Grid Background -->
	<div class="flex-1 relative overflow-hidden">
		<div class="absolute inset-0 opacity-10">
			<div class="grid grid-cols-8 h-full">
				{#each Array(32) as _, i}
					<div class="border-r animate-pulse" style="border-color: #00ff00; animation-delay: {i * 0.1}s"></div>
				{/each}
			</div>
		</div>

		<!-- Main Content -->
		<div class="relative z-10 flex items-center justify-center min-h-full p-2">
			<div class="w-full max-w-4xl">
				<!-- Terminal-style intro -->
				<div class="text-center mb-3">
					<div class="mb-1" style="color: #88ff88;">
						<span class="text-sm">></span> INITIALIZING CONTACT PROTOCOLS...
					</div>
					<div class="text-xs mb-1" style="color: #00ff00;">SELECT YOUR PREFERRED COMMUNICATION METHOD</div>
					<div class="text-xs" style="color: #66dd66;">[ ALL CHANNELS ENCRYPTED AND MONITORED ]</div>
				</div>

				<!-- Contact Cards Grid -->
				<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
					{#each contactMethods as method}
						<div class="group">
							<!-- Outer glow container -->
							<div class="relative p-1 rounded-lg transition-all duration-500" style="background: linear-gradient(to right, #00ff00, #88ff88, #00ff00); box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);">
								<!-- Inner card -->
								<div class="rounded-lg p-4 h-full border transition-all duration-300" style="background-color: #000; border-color: rgba(0, 255, 0, 0.3);">
									<!-- Status indicator -->
									<div class="flex justify-between items-start mb-3">
										<div class="flex items-center space-x-2">
											<div class="w-2 h-2 rounded-full animate-pulse" style="background-color: #00ff00;"></div>
											<span class="text-xs tracking-wider" style="color: #00ff00;">ONLINE</span>
										</div>
										<div class="text-xs" style="color: #66dd66;">ID: {method.id.toUpperCase()}</div>
									</div>

									<!-- Icon -->
									<div class="text-center mb-3">
										<div class="inline-block p-2.5 rounded-full border-2 transition-all duration-300" style="border-color: rgba(0, 255, 0, 0.5); box-shadow: 0 0 8px rgba(0, 255, 0, 0.2);">
											<span class="text-2xl">{method.icon}</span>
										</div>
									</div>

									<!-- Content -->
									<div class="text-center space-y-2">
										<h3 class="text-base font-bold tracking-wide" style="color: #88ff88;">
											{method.name.toUpperCase()}
										</h3>
										<p class="text-xs leading-relaxed" style="color: #00ff00;">
											{method.description}
										</p>

										<!-- Features -->
										<div class="flex justify-center space-x-3 text-xs" style="color: #66dd66;">
											{#if method.id === 'whatsapp'}
												<div class="flex items-center space-x-1">
													<span style="color: #00ff00;">■</span>
													<span>24/7 AI</span>
												</div>
												<div class="flex items-center space-x-1">
													<span style="color: #00ff00;">■</span>
													<span>INSTANT</span>
												</div>
											{:else}
												<div class="flex items-center space-x-1">
													<span style="color: #00ff00;">■</span>
													<span>COMMUNITY</span>
												</div>
												<div class="flex items-center space-x-1">
													<span style="color: #00ff00;">■</span>
													<span>EXPERTS</span>
												</div>
											{/if}
										</div>

										<!-- Action Button -->
										<button 
											class="w-full mt-3 font-bold py-2 px-3 text-xs tracking-wider transition-all duration-300 transform hover:scale-105"
											style="background: {method.id === 'whatsapp' ? '#25d366' : '#5865f2'}; border: 2px solid {method.id === 'whatsapp' ? '#25d366' : '#5865f2'}; color: #fff; border-radius: 4px; box-shadow: 0 0 8px rgba({method.id === 'whatsapp' ? '37, 211, 102' : '88, 101, 242'}, 0.4);"
											on:click={() => openContact(method)}
											on:mouseenter={(e) => {
												if (method.id === 'whatsapp') {
													e.target.style.backgroundColor = '#128c7e';
													e.target.style.borderColor = '#128c7e';
													e.target.style.boxShadow = '0 0 12px rgba(18, 140, 126, 0.6)';
												} else {
													e.target.style.backgroundColor = '#4752c4';
													e.target.style.borderColor = '#4752c4';
													e.target.style.boxShadow = '0 0 12px rgba(71, 82, 196, 0.6)';
												}
											}}
											on:mouseleave={(e) => {
												if (method.id === 'whatsapp') {
													e.target.style.backgroundColor = '#25d366';
													e.target.style.borderColor = '#25d366';
													e.target.style.boxShadow = '0 0 8px rgba(37, 211, 102, 0.4)';
												} else {
													e.target.style.backgroundColor = '#5865f2';
													e.target.style.borderColor = '#5865f2';
													e.target.style.boxShadow = '0 0 8px rgba(88, 101, 242, 0.4)';
												}
											}}
										>
											[ {method.action.toUpperCase()} ]
										</button>
									</div>

									<!-- Connection status -->
									<div class="mt-3 pt-2 text-center" style="border-top: 1px solid rgba(0, 255, 0, 0.3);">
										<div class="text-xs tracking-wider" style="color: #66dd66;">
											CONNECTION: <span style="color: #00ff00;">SECURE</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					{/each}
				</div>

				<!-- System Info -->
				<div class="text-center pb-4">
					<div class="inline-block rounded-lg p-3" style="background: linear-gradient(to right, rgba(0, 255, 0, 0.1), rgba(136, 255, 136, 0.1)); border: 1px solid rgba(0, 255, 0, 0.3); box-shadow: 0 0 8px rgba(0, 255, 0, 0.2);">
						<div class="font-bold mb-2 tracking-wider text-xs" style="color: #88ff88;">
							[ CYBERDYNE SYSTEMS ACTIVE ]
						</div>
						<div class="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-4 text-xs">
							<div class="text-center">
								<div class="mb-1" style="color: #00ff00;">◈</div>
								<div style="color: #66dd66;">WEB3 EXPERTS</div>
							</div>
							<div class="text-center">
								<div class="mb-1" style="color: #00ff00;">◈</div>
								<div style="color: #66dd66;">24/7 SUPPORT</div>
							</div>
							<div class="text-center">
								<div class="mb-1" style="color: #00ff00;">◈</div>
								<div style="color: #66dd66;">SECURE COMM</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>