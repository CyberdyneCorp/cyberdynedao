<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import type { NFTTraits } from '$lib/web3/contracts';
	
	export let isVisible = false;
	export let userTraits: NFTTraits | null = null;
	export let walletAddress = '';
	
	const dispatch = createEventDispatcher();
	let svgContent = '';
	let isLoadingSvg = false;
	
	function closeTerminal() {
		isVisible = false;
		dispatch('close');
	}
	
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			closeTerminal();
		}
	}
	
	function generateNFTUrl(): string {
		if (!userTraits || !walletAddress) {
			// Return base SVG URL for testing
			return '/assets/cyberdyne_nft_enhanced.svg';
		}
		
		// Format date as YYYY-MM-DD
		const today = new Date();
		const issued = today.toISOString().split('T')[0];
		
		// Map traits to URL parameters
		const params = new URLSearchParams({
			learning: userTraits.Learning ? '1' : '0',
			frontend: userTraits.Frontend ? '1' : '0',
			backend: userTraits.Backend ? '1' : '0',
			blog: userTraits['Blog Creator'] ? '1' : '0',
			admin: userTraits.Admin ? '1' : '0',
			market: userTraits.Marketplace ? '1' : '0',
			issued: issued,
			wallet: walletAddress
		});
		
		return `/assets/cyberdyne_nft_enhanced.svg?${params.toString()}`;
	}
	
	$: nftUrl = generateNFTUrl();
</script>

<!-- Terminal Window Modal -->
{#if isVisible}
	<div 
		class="terminal-overlay" 
		on:click={closeTerminal}
		on:keydown={handleKeydown}
		role="button" 
		tabindex="0"
	>
		<div 
			class="terminal-window" 
			on:click|stopPropagation
			on:keydown={handleKeydown}
			role="dialog" 
			aria-labelledby="terminal-title" 
			tabindex="-1"
		>
			<!-- Terminal Header -->
			<div class="terminal-header">
				<div class="terminal-controls">
					<button class="control-btn close-btn" on:click={closeTerminal} aria-label="Close">●</button>
					<button class="control-btn minimize-btn" aria-label="Minimize">●</button>
					<button class="control-btn maximize-btn" aria-label="Maximize">●</button>
				</div>
				<div class="terminal-title" id="terminal-title">CYBERDYNE ACCESS NFT - TERMINAL</div>
				<div class="terminal-spacer"></div>
			</div>
			
			<!-- Terminal Content -->
			<div class="terminal-content">
				<div class="terminal-output">
					<div class="terminal-line">
						<span class="prompt">cyberdyne@access:~$</span> 
						<span class="command">display-nft --user {walletAddress ? `${walletAddress.slice(0, 6)}...${walletAddress.slice(-4)}` : 'unknown'}</span>
					</div>
					<div class="terminal-line">
						<span class="output-text">Loading NFT data...</span>
					</div>
					<div class="terminal-line">
						<span class="output-success">✓ NFT certificate generated successfully</span>
					</div>
					<div class="terminal-line">
						<span class="output-info">→ Wallet: {walletAddress || 'unknown'}</span>
					</div>
					{#if userTraits}
						<div class="terminal-line">
							<span class="output-info">→ Active Permissions:</span>
						</div>
						{#each Object.entries(userTraits) as [key, value]}
							{#if value}
								<div class="terminal-line">
									<span class="output-success">  ✓ {key === 'Blog Creator' ? 'Blog Creator' : key.toUpperCase()}</span>
								</div>
							{/if}
						{/each}
					{/if}
					<div class="terminal-line">
						<span class="output-text">Rendering certificate...</span>
					</div>
					<div class="terminal-line">
						<span class="output-info">→ URL: {nftUrl}</span>
					</div>
				</div>
				
				<!-- NFT Display -->
				<div class="nft-display">
					{#if nftUrl}
						<object
							data={nftUrl}
							type="image/svg+xml"
							title="Cyberdyne Access NFT"
							class="nft-frame"
						>
							<img src={nftUrl} alt="Cyberdyne Access NFT" class="nft-frame" />
						</object>
					{/if}
				</div>
				
				<!-- Terminal Input -->
				<div class="terminal-input">
					<span class="prompt">cyberdyne@access:~$</span>
					<span class="cursor">_</span>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.terminal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.8);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 2000;
		backdrop-filter: blur(4px);
	}

	.terminal-window {
		background: #1e1e1e;
		border: 2px solid #00ff00;
		border-radius: 8px;
		width: 90vw;
		height: 90vh;
		max-width: 1200px;
		max-height: 800px;
		display: flex;
		flex-direction: column;
		box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
		font-family: 'JetBrains Mono', 'Courier New', monospace;
		overflow: hidden;
	}

	.terminal-header {
		background: #2d2d2d;
		border-bottom: 1px solid #444;
		padding: 8px 16px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		min-height: 40px;
	}

	.terminal-controls {
		display: flex;
		gap: 8px;
	}

	.control-btn {
		width: 16px;
		height: 16px;
		border-radius: 50%;
		border: none;
		cursor: pointer;
		font-size: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s ease;
	}

	.close-btn {
		background: #ff5f57;
		color: #8b0000;
	}

	.minimize-btn {
		background: #ffbd2e;
		color: #805600;
	}

	.maximize-btn {
		background: #28ca42;
		color: #004f0f;
	}

	.control-btn:hover {
		transform: scale(1.1);
	}

	.terminal-title {
		color: #00ff00;
		font-size: 14px;
		font-weight: bold;
		text-align: center;
		flex: 1;
	}

	.terminal-spacer {
		width: 80px; /* Balance the controls */
	}

	.terminal-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		background: #000;
	}

	.terminal-output {
		padding: 16px;
		color: #00ff00;
		font-size: 14px;
		line-height: 1.4;
		flex-shrink: 0;
	}

	.terminal-line {
		margin-bottom: 4px;
		word-wrap: break-word;
	}

	.prompt {
		color: #00d4aa;
		font-weight: bold;
	}

	.command {
		color: #ffffff;
	}

	.output-text {
		color: #cccccc;
	}

	.output-success {
		color: #00ff00;
	}

	.output-info {
		color: #00d4aa;
	}

	.nft-display {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 16px;
		background: #0a0a0a;
		border-top: 1px solid #333;
		overflow: hidden;
	}

	.nft-frame {
		width: 100%;
		height: 100%;
		max-width: 500px;
		max-height: 600px;
		border: 2px solid #00ff00;
		border-radius: 8px;
		background: #000;
		box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
	}

	.terminal-input {
		padding: 16px;
		border-top: 1px solid #333;
		display: flex;
		align-items: center;
		background: #000;
		flex-shrink: 0;
	}

	.cursor {
		color: #00ff00;
		animation: blink 1s infinite;
		margin-left: 4px;
	}

	@keyframes blink {
		0%, 50% { opacity: 1; }
		51%, 100% { opacity: 0; }
	}

	/* Mobile responsiveness */
	@media (max-width: 768px) {
		.terminal-window {
			width: 95vw;
			height: 95vh;
		}

		.terminal-title {
			font-size: 12px;
		}

		.terminal-output {
			font-size: 12px;
		}
	}
</style>