<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { web3AuthService, type Web3AuthUser } from '../web3/web3AuthService';
	import { appKitService } from '../web3/appKitService';
	import { walletInfo, isWalletConnected, formatAddress, formatBalance, getNetworkName } from '../stores/appKitStore';
	import { completeWalletDisconnect } from '../utils/walletDisconnect';
	
	let walletConnected = false;
	let isLoading = false;
	let errorMessage = '';
	let currentUser: Web3AuthUser | null = null;
	let connectionType: 'web3auth' | 'walletconnect' | null = null;

	let showDetails = false;
	let showConnectionModal = false;

	// Subscribe to WalletConnect state
	let walletConnectConnected = false;
	let walletConnectInfo: any = null;

	const unsubscribe = walletInfo.subscribe(info => {
		walletConnectConnected = info.isConnected;
		walletConnectInfo = info;
		
		// Update overall connection status
		if (info.isConnected && connectionType !== 'web3auth') {
			walletConnected = true;
			connectionType = 'walletconnect';
		} else if (!info.isConnected && connectionType === 'walletconnect') {
			walletConnected = currentUser !== null; // Keep Web3Auth connection if present
			if (!currentUser) connectionType = null;
		}
	});

	function toggleDetails() {
		showDetails = !showDetails;
	}

	function openConnectionModal() {
		showConnectionModal = true;
	}

	function closeConnectionModal() {
		showConnectionModal = false;
	}

	async function handleWalletConnect() {
		console.log('WalletConnect clicked - initializing AppKit...');
		isLoading = true;
		closeConnectionModal();
		
		try {
			// Initialize AppKit if not already done
			const initialized = await appKitService.initialize();
			if (!initialized) {
				throw new Error('Failed to initialize AppKit');
			}
			
			// Open the connection modal
			await appKitService.openModal();
			
			console.log('AppKit modal opened successfully');
			errorMessage = ''; // Clear any previous errors
		} catch (error) {
			console.error('WalletConnect failed:', error);
			const errorMsg = (error as any)?.message || String(error) || 'Unknown error';
			errorMessage = `WalletConnect failed: ${errorMsg}`;
		} finally {
			isLoading = false;
		}
	}

	async function handleWeb3AuthConnect() {
		console.log('Web3Auth Google authentication starting...');
		isLoading = true;
		closeConnectionModal();
		
		try {
			// Ensure polyfills are ready before attempting login
			const { polyfillsReady } = await import('$lib/polyfills');
			await polyfillsReady;
			console.log('Polyfills confirmed ready for login');
			
			const user = await web3AuthService.loginWithGoogle();
			if (user) {
				currentUser = user;
				walletConnected = true;
				connectionType = 'web3auth';
				console.log('Web3Auth login successful:', user);
				errorMessage = ''; // Clear any previous errors
			}
		} catch (error) {
			console.error('Web3Auth login failed:', error);
			const errorMsg = (error as any)?.message || String(error) || 'Unknown error';
			errorMessage = `Login failed: ${errorMsg}`;
			
			// Reset state on error
			walletConnected = false;
			currentUser = null;
			connectionType = null;
		} finally {
			isLoading = false;
		}
	}

	async function handleDisconnect() {
		console.log('🔌 Complete wallet disconnect initiated from UI');
		isLoading = true;
		
		try {
			// Use the centralized disconnect utility
			const result = await completeWalletDisconnect();
			
			// Reset all local component state
			walletConnected = false;
			connectionType = null;
			currentUser = null;
			showDetails = false;
			walletConnectConnected = false;
			walletConnectInfo = null;
			
			if (result.success) {
				errorMessage = '';
				console.log('✅ Complete wallet disconnect successful');
				
				// Show warnings if any
				if (result.warnings.length > 0) {
					console.warn('⚠️ Disconnect warnings:', result.warnings);
					// Optionally show warnings to user but don't treat as error
				}
			} else {
				console.error('❌ Disconnect completed with errors:', result.errors);
				errorMessage = `Disconnect completed with issues: ${result.errors.join(', ')}`;
			}
			
		} catch (error) {
			console.error('💥 Unexpected error during disconnect:', error);
			
			// Even if centralized disconnect fails, reset local component state
			walletConnected = false;
			connectionType = null;
			currentUser = null;
			showDetails = false;
			walletConnectConnected = false;
			walletConnectInfo = null;
			
			errorMessage = `Unexpected disconnect error: ${(error as any)?.message || 'Unknown error'}`;
		} finally {
			isLoading = false;
		}
	}

	function clearError() {
		errorMessage = '';
	}

	async function checkAuthStatus() {
		console.log('🔍 Web3Wallet: Checking authentication status...');
		console.log('🔍 Web3Wallet: Current component state before check:', {
			walletConnected,
			connectionType,
			hasCurrentUser: !!currentUser
		});
		
		try {
			const user = await web3AuthService.checkAuthStatus();
			console.log('🔍 Web3Wallet: checkAuthStatus returned:', !!user);
			
			if (user) {
				// Update component state
				currentUser = user;
				walletConnected = true;
				connectionType = 'web3auth';
				
				console.log('✅ Web3Wallet: User session restored successfully:', {
					email: user.userInfo.email,
					address: user.address
				});
				console.log('✅ Web3Wallet: Component state updated:', {
					walletConnected,
					connectionType,
					hasCurrentUser: !!currentUser
				});
			} else {
				console.log('ℹ️ Web3Wallet: No existing authentication session found');
				console.log('ℹ️ Web3Wallet: Component state remains:', {
					walletConnected,
					connectionType,
					hasCurrentUser: !!currentUser
				});
			}
		} catch (error) {
			console.error('❌ Web3Wallet: Error checking auth status:', error);
			// Don't set error message for initial auth check failures - this is normal
		}
	}
	
	onMount(async () => {
		console.log('🚀 Web3Wallet component mounted, initializing wallet services...');
		
		try {
			// Wait for polyfills to be ready before initializing Web3Auth
			console.log('⏳ Loading polyfills...');
			const { polyfillsReady } = await import('$lib/polyfills');
			await polyfillsReady;
			console.log('✅ Polyfills ready');
			
			// Give a small additional delay for any async module initialization
			await new Promise(resolve => setTimeout(resolve, 100));
			
			console.log('🔄 Checking for existing authentication sessions...');
			await checkAuthStatus();
			
			// If no session was found initially, try again after a longer delay
			// Web3Auth might need more time to restore sessions after page refresh
			if (!walletConnected) {
				console.log('⏳ No session found initially, retrying after delay...');
				await new Promise(resolve => setTimeout(resolve, 1000));
				await checkAuthStatus();
				
				// If still not connected, try one more time with an even longer delay
				if (!walletConnected) {
					console.log('⏳ Still no session, final retry after longer delay...');
					await new Promise(resolve => setTimeout(resolve, 2000));
					await checkAuthStatus();
				}
			}
			
			// Initialize AppKit in the background (don't await to avoid blocking)
			console.log('🔄 Initializing AppKit in background...');
			appKitService.initialize().catch(error => {
				console.log('⚠️ AppKit initialization failed (will retry when needed):', error);
			});
			
			console.log('✅ Web3Wallet initialization complete');
		} catch (error) {
			console.error('❌ Error during Web3Wallet component initialization:', error);
			// Don't set error message for initialization failures, just log them
			console.warn('⚠️ Wallet initialization failed, but continuing...');
		}
	});

	onDestroy(() => {
		// Clean up subscription
		if (unsubscribe) {
			unsubscribe();
		}
	});
</script>

<div class="web3-wallet">
	<!-- Connection Modal -->
	{#if showConnectionModal}
		<div class="connection-modal-overlay" on:click={closeConnectionModal} on:keydown={(e) => e.key === 'Escape' && closeConnectionModal()} role="button" tabindex="0">
			<div class="connection-modal" on:click|stopPropagation on:keydown={(e) => e.key === 'Escape' && closeConnectionModal()} role="dialog" aria-labelledby="modal-title" tabindex="-1">
				<div class="modal-header">
					<h2 id="modal-title" class="modal-title">🖥️ CONNECT WALLET</h2>
					<button on:click={closeConnectionModal} class="close-btn">✕</button>
				</div>
				
				<div class="connection-options">
					<!-- WalletConnect Option -->
					<button 
						on:click={handleWalletConnect}
						disabled={isLoading}
						class="connection-option walletconnect-option"
					>
						<div class="option-icon">📱</div>
						<div class="option-content">
							<div class="option-title">WalletConnect</div>
							<div class="option-description">Connect MetaMask, Trust Wallet & 50+ wallets</div>
						</div>
					</button>

					<!-- Web3Auth/Google Option -->
					<button 
						on:click={handleWeb3AuthConnect}
						disabled={isLoading}
						class="connection-option web3auth-option"
					>
						<div class="option-icon">G</div>
						<div class="option-content">
							<div class="option-title">Continue with Google</div>
							<div class="option-description">Secure authentication via Google</div>
						</div>
					</button>
				</div>

				<!-- Loading States -->
				{#if isLoading}
					<div class="loading-indicator">
						<div class="loading-text">Connecting...</div>
						<div class="loading-dots">...</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}

	<!-- Error Banner - positioned absolutely to avoid clipping -->
	{#if errorMessage}
		<div class="error-banner-absolute">
			<div class="error-content">
				<span class="error-text">{errorMessage}</span>
				<button on:click={clearError} class="error-close">✕</button>
			</div>
		</div>
	{/if}

	<!-- Main Wallet Interface -->
	{#if !walletConnected}
		<button 
			on:click={openConnectionModal}
			disabled={isLoading}
			class="connect-btn"
		>
			{isLoading ? '> CONNECTING...' : '> CONNECT WALLET'}
		</button>
	{:else}
		<div class="wallet-connected">
			<div class="wallet-info">
				<button 
					on:click={toggleDetails}
					class="wallet-summary"
				>
					<div class="wallet-status">
						<div class="status-indicator">
							<div class="status-text">CONNECTED</div>
						</div>
						<div class="wallet-balance">
							<div class="expand-icon">{showDetails ? '▲' : '▼'}</div>
						</div>
					</div>
				</button>

				{#if showDetails}
					<div class="wallet-details">
						<div class="detail-grid">
							<!-- Connection Type -->
							<div class="detail-row">
								<span class="detail-label">TYPE:</span>
								<span class="detail-value">{connectionType === 'web3auth' ? 'Web3Auth (Google)' : connectionType === 'walletconnect' ? 'WalletConnect' : 'Unknown'}</span>
							</div>
							
							<!-- Address -->
							<div class="detail-row">
								<span class="detail-label">ADDRESS:</span>
								<span class="detail-value address-full">
									{connectionType === 'web3auth' ? currentUser?.address || 'Not available' : 
									 connectionType === 'walletconnect' ? walletConnectInfo?.address || 'Not available' : 'Not available'}
								</span>
							</div>
							
							<!-- Network (for WalletConnect) -->
							{#if connectionType === 'walletconnect'}
								<div class="detail-row">
									<span class="detail-label">NETWORK:</span>
									<span class="detail-value">{getNetworkName(walletConnectInfo?.chainId)}</span>
								</div>
							{/if}
							
							<!-- Email and Name (only for Web3Auth) -->
							{#if connectionType === 'web3auth'}
								<div class="detail-row">
									<span class="detail-label">EMAIL:</span>
									<span class="detail-value">{currentUser?.userInfo.email || 'Not provided'}</span>
								</div>
								<div class="detail-row">
									<span class="detail-label">NAME:</span>
									<span class="detail-value">{currentUser?.userInfo.name || 'Not provided'}</span>
								</div>
							{/if}
						</div>
						<div class="wallet-actions">
							<button 
								on:click={handleDisconnect}
								class="disconnect-btn"
							>
								> DISCONNECT
							</button>
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.web3-wallet {
		font-family: 'JetBrains Mono', 'Courier New', monospace;
		color: #00ff00;
		background: transparent;
		position: relative;
		z-index: 5;
		min-height: fit-content;
	}
	
	.wallet-connected {
		position: relative;
	}
	
	.wallet-info {
		position: relative;
		z-index: 20;
	}

	/* Connection Modal */
	.connection-modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.6);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}

	.connection-modal {
		background: #000000;
		border: 2px solid #00ff00;
		border-radius: 8px;
		padding: 24px;
		min-width: 400px;
		max-width: 90vw;
		box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
	}

	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 24px;
		border-bottom: 1px solid #00ff00;
		padding-bottom: 12px;
	}

	.modal-title {
		color: #00ff00;
		font-size: 16px;
		font-weight: bold;
		margin: 0;
	}

	.close-btn {
		background: none;
		border: none;
		color: #00ff00;
		font-size: 18px;
		cursor: pointer;
		padding: 4px;
		border-radius: 4px;
		transition: all 0.2s ease;
	}

	.close-btn:hover {
		background: #00ff00;
		color: #000000;
	}

	.connection-options {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.connection-option {
		display: flex;
		align-items: center;
		gap: 16px;
		padding: 16px;
		background: rgba(0, 255, 0, 0.1);
		border: 1px solid #00ff00;
		border-radius: 6px;
		cursor: pointer;
		transition: all 0.2s ease;
		width: 100%;
		text-align: left;
	}

	.connection-option:hover:not(:disabled) {
		background: rgba(0, 255, 0, 0.2);
		border-color: #40ff40;
		box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
	}

	.connection-option:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.option-icon {
		font-size: 24px;
		width: 40px;
		height: 40px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(0, 255, 0, 0.2);
		border: 1px solid #00ff00;
	}

	.web3auth-option .option-icon {
		background: #4285f4;
		color: white;
		font-weight: bold;
		border-color: #4285f4;
	}

	.option-content {
		flex: 1;
	}

	.option-title {
		font-weight: bold;
		color: #00ff00;
		margin-bottom: 4px;
	}

	.option-description {
		font-size: 12px;
		color: #80ff80;
	}

	/* Main Interface */
	.connect-btn {
		width: 100%;
		padding: 8px 12px;
		background: #22c55e;
		border: 2px solid #000000;
		color: #ffffff;
		font-family: 'JetBrains Mono', monospace;
		font-size: 12px;
		font-weight: bold;
		cursor: pointer;
		border-radius: 4px;
		transition: all 0.2s ease;
		text-align: center;
		box-shadow: 2px 2px 0px #000000;
	}

	.connect-btn:hover:not(:disabled) {
		background: #16a34a;
		transform: translate(1px, 1px);
		box-shadow: 1px 1px 0px #000000;
	}

	.connect-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	/* Error Banner */

	.error-banner-absolute {
		position: fixed;
		top: 70px; /* Below the 60px TopBar */
		right: 20px;
		background: rgba(255, 0, 0, 0.95);
		border: 2px solid #ff4444;
		border-radius: 8px;
		padding: 16px;
		z-index: 2147483647; /* Higher than TopBar */
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
		min-width: 300px;
		max-width: 400px;
	}

	.error-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.error-text {
		color: #ffffff;
		font-size: 12px;
		font-weight: bold;
	}

	.error-close {
		background: rgba(255, 255, 255, 0.2);
		border: 1px solid #ffffff;
		color: #ffffff;
		cursor: pointer;
		padding: 4px 8px;
		border-radius: 4px;
		transition: all 0.2s ease;
		font-weight: bold;
	}

	.error-close:hover {
		background: #ffffff;
		color: #ff4444;
	}

	/* Network Warning - removed unused styles */

	/* Wallet Summary */
	.wallet-summary {
		width: 100%;
		padding: 8px 12px;
		background: #22c55e;
		border: 2px solid #000000;
		color: #ffffff;
		font-family: 'JetBrains Mono', monospace;
		cursor: pointer;
		border-radius: 4px;
		transition: all 0.2s ease;
		text-align: left;
		box-shadow: 2px 2px 0px #000000;
	}

	.wallet-summary:hover {
		background: #16a34a;
		transform: translate(1px, 1px);
		box-shadow: 1px 1px 0px #000000;
	}

	.wallet-status {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 4px;
	}

	.status-text {
		font-weight: bold;
		font-size: 11px;
		color: #ffffff;
	}


	/* Wallet Details */
	.wallet-details {
		background: rgba(0, 0, 0, 0.8);
		border: 1px solid #00ff00;
		border-top: none;
		border-radius: 0 0 4px 4px;
		padding: 12px;
		animation: slideDown 0.2s ease-out;
		position: absolute;
		top: 100%;
		right: 0;
		z-index: 1000;
		margin-top: 0;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
		width: 300px;
		max-height: 80vh;
		overflow-y: auto;
		margin-right: 0;
	}

	.detail-grid {
		display: flex;
		flex-direction: column;
		gap: 8px;
		margin-bottom: 12px;
	}

	.detail-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.detail-label {
		color: #80ff80;
		font-size: 10px;
		font-weight: bold;
	}

	.detail-value {
		color: #00ff00;
		font-size: 11px;
		font-family: monospace;
	}

	.address-full {
		max-width: 200px;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.disconnect-btn {
		width: 100%;
		padding: 8px;
		background: rgba(255, 0, 0, 0.1);
		border: 1px solid #ff4444;
		color: #ff4444;
		font-family: inherit;
		font-size: 12px;
		font-weight: bold;
		cursor: pointer;
		border-radius: 4px;
		transition: all 0.2s ease;
	}

	.disconnect-btn:hover {
		background: rgba(255, 0, 0, 0.2);
		box-shadow: 0 0 5px rgba(255, 68, 68, 0.3);
	}

	/* Modal Error - removed unused styles */

	/* Loading Indicator */
	.loading-indicator {
		margin-top: 16px;
		text-align: center;
		color: #80ff80;
	}

	.loading-text {
		font-size: 12px;
		margin-bottom: 8px;
	}

	.loading-dots {
		animation: pulse 1.5s infinite;
		font-size: 16px;
		color: #00ff00;
	}

	@keyframes slideDown {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes pulse {
		0%, 100% {
			opacity: 0.3;
		}
		50% {
			opacity: 1;
		}
	}
</style>