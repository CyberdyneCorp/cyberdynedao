<script lang="ts">
	import { onMount } from 'svelte';
	import { web3AuthService, type Web3AuthUser } from '../web3/web3AuthService';
	
	let walletConnected = false;
	let isLoading = false;
	let errorMessage = '';
	let currentUser: Web3AuthUser | null = null;

	let showDetails = false;
	let showConnectionModal = false;

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
		console.log('WalletConnect clicked - feature coming soon');
		errorMessage = 'WalletConnect integration coming soon...';
		closeConnectionModal();
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
				console.log('Web3Auth login successful:', user);
				errorMessage = ''; // Clear any previous errors
			}
		} catch (error) {
			console.error('Web3Auth login failed:', error);
			const errorMsg = error?.message || error?.toString() || 'Unknown error';
			errorMessage = `Login failed: ${errorMsg}`;
			
			// Reset state on error
			walletConnected = false;
			currentUser = null;
		} finally {
			isLoading = false;
		}
	}

	async function handleDisconnect() {
		isLoading = true;
		try {
			await web3AuthService.logout();
			walletConnected = false;
			currentUser = null;
			showDetails = false;
			console.log('User disconnected successfully');
		} catch (error) {
			console.error('Disconnect failed:', error);
			errorMessage = `Disconnect failed: ${error?.message || 'Unknown error'}`;
		} finally {
			isLoading = false;
		}
	}

	function clearError() {
		errorMessage = '';
	}

	async function checkAuthStatus() {
		try {
			const user = await web3AuthService.checkAuthStatus();
			if (user) {
				currentUser = user;
				walletConnected = true;
				console.log('User already authenticated:', user);
			}
		} catch (error) {
			console.error('Error checking auth status:', error);
			// Don't set error message for initial auth check failures
		}
	}
	
	onMount(async () => {
		console.log('Web3Wallet component mounted, waiting for polyfills...');
		try {
			// Wait for polyfills to be ready before initializing Web3Auth
			const { polyfillsReady } = await import('$lib/polyfills');
			await polyfillsReady;
			
			// Give a small additional delay for any async module initialization
			await new Promise(resolve => setTimeout(resolve, 100));
			
			console.log('Polyfills loaded and settled, checking authentication status...');
			await checkAuthStatus();
		} catch (error) {
			console.error('Error during component initialization:', error);
			// Don't set error message for initialization failures, just log them
			console.warn('Wallet initialization failed, but continuing...');
		}
	});
</script>

<div class="web3-wallet">
	<!-- Connection Modal -->
	{#if showConnectionModal}
		<div class="connection-modal-overlay" on:click={closeConnectionModal}>
			<div class="connection-modal" on:click|stopPropagation>
				<div class="modal-header">
					<h2 class="modal-title">🖥️ CONNECT WALLET</h2>
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
							<div class="option-description">Scan QR code with mobile wallet</div>
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
							<div class="status-text">█ CONNECTED</div>
							<div class="wallet-type">{currentUser?.userInfo.typeOfLogin?.toUpperCase() || 'WEB3AUTH'}</div>
						</div>
						<div class="wallet-balance">
							<div class="balance-amount">{currentUser ? parseFloat(currentUser.balance).toFixed(4) : '0.0000'} ETH</div>
							<div class="expand-icon">{showDetails ? '▲' : '▼'}</div>
						</div>
					</div>
					<div class="wallet-address">{currentUser ? `${currentUser.address.slice(0, 6)}...${currentUser.address.slice(-4)}` : '0x0000...0000'}</div>
				</button>

				{#if showDetails}
					<div class="wallet-details">
						<div class="detail-grid">
							<div class="detail-row">
								<span class="detail-label">EMAIL:</span>
								<span class="detail-value">{currentUser?.userInfo.email || 'Not provided'}</span>
							</div>
							<div class="detail-row">
								<span class="detail-label">NAME:</span>
								<span class="detail-value">{currentUser?.userInfo.name || 'Not provided'}</span>
							</div>
							<div class="detail-row">
								<span class="detail-label">PROVIDER:</span>
								<span class="detail-value">{currentUser?.userInfo.typeOfLogin || 'Unknown'}</span>
							</div>
							<div class="detail-row">
								<span class="detail-label">ADDRESS:</span>
								<span class="detail-value address-full">{currentUser?.address || 'Not available'}</span>
							</div>
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

	.wallet-type {
		font-size: 9px;
		color: #e5e7eb;
	}

	.wallet-balance {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.balance-amount {
		font-weight: bold;
		color: #ffffff;
		font-size: 11px;
	}

	.expand-icon {
		font-size: 10px;
		color: #e5e7eb;
	}

	.wallet-address {
		font-size: 10px;
		color: #e5e7eb;
		font-family: monospace;
	}

	/* Wallet Details */
	.wallet-details {
		background: rgba(0, 255, 0, 0.05);
		border: 1px solid #00ff00;
		border-top: none;
		border-radius: 0 0 4px 4px;
		padding: 12px;
		animation: slideDown 0.2s ease-out;
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