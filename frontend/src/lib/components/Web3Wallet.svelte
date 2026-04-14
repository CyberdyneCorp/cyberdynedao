<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { web3AuthService } from '../web3/web3AuthService';
	import { appKitService } from '../web3/appKitService';
	import { walletInfo, getNetworkName } from '../stores/appKitStore';
	import { completeWalletDisconnect } from '../utils/walletDisconnect';
	import { userTraits, hasAnyAccess, isLoadingTraits, getActiveTraits } from '../stores/accessNFTStore';
	import { walletInfo as web3WalletInfo } from '../stores/web3Store';
	import { createWeb3WalletViewModel, type Web3AuthUserLike } from '$lib/viewmodels/web3WalletViewModel';
	import NFTTerminal from './NFTTerminal.svelte';

	const vm = createWeb3WalletViewModel({
		connectWalletConnect: async () => {
			const initialized = await appKitService.initialize();
			if (!initialized) throw new Error('Failed to initialize AppKit');
			await appKitService.openModal();
		},
		connectWeb3Auth: async () => {
			const { polyfillsReady } = await import('$lib/polyfills');
			await polyfillsReady;
			const user = await web3AuthService.loginWithGoogle();
			return user as Web3AuthUserLike | null;
		},
		disconnect: async () => {
			const result = await completeWalletDisconnect();
			return result;
		},
		checkAuthStatus: async () => {
			const user = await web3AuthService.checkAuthStatus();
			return user as Web3AuthUserLike | null;
		},
		setGlobalWeb3Info: (info) => web3WalletInfo.set(info)
	});

	const {
		walletConnected,
		errorMessage,
		isLoading,
		currentUser,
		connectionType,
		showDetails,
		showConnectionModal,
		showNFTTerminal
	} = vm;

	let showNFTTerminalBind = false;
	const unsubShowNFT = showNFTTerminal.subscribe(v => (showNFTTerminalBind = v));

	const unsubscribe = walletInfo.subscribe(info => {
		vm.updateFromWalletConnect({
			address: info.address,
			balance: info.balance,
			chainId: info.chainId,
			isConnected: info.isConnected
		});
	});

	onMount(async () => {
		try {
			const { polyfillsReady } = await import('$lib/polyfills');
			await polyfillsReady;
			await new Promise(resolve => setTimeout(resolve, 100));
			await vm.checkAuthStatus();
			appKitService.initialize().catch(() => {});
		} catch {
			// Initialization errors are non-fatal.
		}
	});

	onDestroy(() => {
		unsubscribe?.();
		unsubShowNFT?.();
	});

	$: walletConnectInfoSnap = vm.snapshot().walletConnectInfo;
</script>

<div class="web3-wallet">
	{#if $showConnectionModal}
		<div class="connection-modal-overlay" on:click={() => vm.closeConnectionModal()} on:keydown={(e) => e.key === 'Escape' && vm.closeConnectionModal()} role="button" tabindex="0">
			<div class="connection-modal" on:click|stopPropagation on:keydown={(e) => e.key === 'Escape' && vm.closeConnectionModal()} role="dialog" aria-labelledby="modal-title" tabindex="-1">
				<div class="modal-header">
					<h2 id="modal-title" class="modal-title">🖥️ CONNECT WALLET</h2>
					<button on:click={() => vm.closeConnectionModal()} class="close-btn">✕</button>
				</div>
				<div class="connection-options">
					<button on:click={() => vm.handleWalletConnect()} disabled={$isLoading} class="connection-option walletconnect-option">
						<div class="option-icon">📱</div>
						<div class="option-content">
							<div class="option-title">WalletConnect</div>
							<div class="option-description">Connect MetaMask, Trust Wallet & 50+ wallets</div>
						</div>
					</button>
					<button on:click={() => vm.handleWeb3AuthConnect()} disabled={$isLoading} class="connection-option web3auth-option">
						<div class="option-icon">G</div>
						<div class="option-content">
							<div class="option-title">Continue with Google</div>
							<div class="option-description">Secure authentication via Google</div>
						</div>
					</button>
				</div>
				{#if $isLoading}
					<div class="loading-indicator">
						<div class="loading-text">Connecting...</div>
						<div class="loading-dots">...</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}

	{#if $errorMessage}
		<div class="error-banner-absolute">
			<div class="error-content">
				<span class="error-text">{$errorMessage}</span>
				<button on:click={() => vm.clearError()} class="error-close">✕</button>
			</div>
		</div>
	{/if}

	{#if !$walletConnected}
		<button on:click={() => vm.openConnectionModal()} disabled={$isLoading} class="connect-btn">
			{$isLoading ? '> CONNECTING...' : '> CONNECT WALLET'}
		</button>
	{:else}
		<div class="wallet-connected">
			<div class="wallet-info">
				<button on:click={() => vm.toggleDetails()} class="wallet-summary">
					<div class="wallet-status">
						<div class="status-indicator">
							<div class="status-text">CONNECTED</div>
						</div>
						<div class="wallet-balance">
							<div class="expand-icon">{$showDetails ? '▲' : '▼'}</div>
						</div>
					</div>
				</button>

				{#if $showDetails}
					<div class="wallet-details">
						<div class="detail-grid">
							<div class="detail-row">
								<span class="detail-label">TYPE:</span>
								<span class="detail-value">{$connectionType === 'web3auth' ? 'Web3Auth (Google)' : $connectionType === 'walletconnect' ? 'WalletConnect' : 'Unknown'}</span>
							</div>
							<div class="detail-row">
								<span class="detail-label">ADDRESS:</span>
								<span class="detail-value address-full">
									{$connectionType === 'web3auth' ? $currentUser?.address || 'Not available' :
									 $connectionType === 'walletconnect' ? walletConnectInfoSnap?.address || 'Not available' : 'Not available'}
								</span>
							</div>
							{#if $connectionType === 'walletconnect'}
								<div class="detail-row">
									<span class="detail-label">NETWORK:</span>
									<span class="detail-value">{getNetworkName(walletConnectInfoSnap?.chainId)}</span>
								</div>
							{/if}
							{#if $connectionType === 'web3auth'}
								<div class="detail-row">
									<span class="detail-label">EMAIL:</span>
									<span class="detail-value">{$currentUser?.userInfo.email || 'Not provided'}</span>
								</div>
								<div class="detail-row">
									<span class="detail-label">NAME:</span>
									<span class="detail-value">{$currentUser?.userInfo.name || 'Not provided'}</span>
								</div>
							{/if}
							{#if $isLoadingTraits}
								<div class="detail-row">
									<span class="detail-label">ACCESS:</span>
									<span class="detail-value loading">Loading traits...</span>
								</div>
							{:else if $hasAnyAccess && $userTraits}
								<div class="detail-row traits-section">
									<span class="detail-label">ACCESS TRAITS NFT:</span>
									<div class="traits-container">
										{#each getActiveTraits($userTraits) as trait}
											<span class="trait-badge">{trait}</span>
										{/each}
										<button class="nft-view-btn" on:click={() => vm.openNFTTerminal()} title="View NFT Certificate">
											📜 VIEW NFT
										</button>
									</div>
								</div>
							{:else if $userTraits === null}
								<div class="detail-row">
									<span class="detail-label">ACCESS:</span>
									<span class="detail-value no-access">No Access NFT</span>
								</div>
							{/if}
						</div>
						<div class="wallet-actions">
							<button on:click={() => vm.handleDisconnect()} class="disconnect-btn">
								> DISCONNECT
							</button>
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}

	<NFTTerminal
		bind:isVisible={showNFTTerminalBind}
		userTraits={$userTraits}
		walletAddress={vm.resolveAddress()}
		on:close={() => vm.closeNFTTerminal()}
	/>
</div>

<style>
	.web3-wallet { font-family: 'JetBrains Mono', 'Courier New', monospace; color: #00ff00; background: transparent; position: relative; z-index: 5; min-height: fit-content; }
	.wallet-connected { position: relative; }
	.wallet-info { position: relative; z-index: 20; }
	.connection-modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; }
	.connection-modal { background: #000; border: 2px solid #00ff00; border-radius: 8px; padding: 24px; min-width: 400px; max-width: 90vw; box-shadow: 0 0 20px rgba(0,255,0,0.3); }
	.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #00ff00; padding-bottom: 12px; }
	.modal-title { color: #00ff00; font-size: 16px; font-weight: bold; margin: 0; }
	.close-btn { background: none; border: none; color: #00ff00; font-size: 18px; cursor: pointer; padding: 4px; border-radius: 4px; transition: all 0.2s ease; }
	.close-btn:hover { background: #00ff00; color: #000; }
	.connection-options { display: flex; flex-direction: column; gap: 16px; }
	.connection-option { display: flex; align-items: center; gap: 16px; padding: 16px; background: rgba(0,255,0,0.1); border: 1px solid #00ff00; border-radius: 6px; cursor: pointer; transition: all 0.2s ease; width: 100%; text-align: left; }
	.connection-option:hover:not(:disabled) { background: rgba(0,255,0,0.2); border-color: #40ff40; box-shadow: 0 0 10px rgba(0,255,0,0.2); }
	.connection-option:disabled { opacity: 0.5; cursor: not-allowed; }
	.option-icon { font-size: 24px; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: rgba(0,255,0,0.2); border: 1px solid #00ff00; }
	.web3auth-option .option-icon { background: #4285f4; color: white; font-weight: bold; border-color: #4285f4; }
	.option-content { flex: 1; }
	.option-title { font-weight: bold; color: #00ff00; margin-bottom: 4px; }
	.option-description { font-size: 12px; color: #80ff80; }
	.connect-btn { width: 100%; padding: 8px 12px; background: #22c55e; border: 2px solid #000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: bold; cursor: pointer; border-radius: 4px; transition: all 0.2s ease; text-align: center; box-shadow: 2px 2px 0 #000; }
	.connect-btn:hover:not(:disabled) { background: #16a34a; transform: translate(1px,1px); box-shadow: 1px 1px 0 #000; }
	.connect-btn:disabled { opacity: 0.6; cursor: not-allowed; }
	.error-banner-absolute { position: fixed; top: 70px; right: 20px; background: rgba(255,0,0,0.95); border: 2px solid #ff4444; border-radius: 8px; padding: 16px; z-index: 2147483647; box-shadow: 0 8px 24px rgba(0,0,0,0.4); min-width: 300px; max-width: 400px; }
	.error-content { display: flex; justify-content: space-between; align-items: center; }
	.error-text { color: #fff; font-size: 12px; font-weight: bold; }
	.error-close { background: rgba(255,255,255,0.2); border: 1px solid #fff; color: #fff; cursor: pointer; padding: 4px 8px; border-radius: 4px; transition: all 0.2s ease; font-weight: bold; }
	.error-close:hover { background: #fff; color: #ff4444; }
	.wallet-summary { width: 100%; padding: 8px 12px; background: #22c55e; border: 2px solid #000; color: #fff; font-family: 'JetBrains Mono', monospace; cursor: pointer; border-radius: 4px; transition: all 0.2s ease; text-align: left; box-shadow: 2px 2px 0 #000; }
	.wallet-summary:hover { background: #16a34a; transform: translate(1px,1px); box-shadow: 1px 1px 0 #000; }
	.wallet-status { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
	.status-text { font-weight: bold; font-size: 11px; color: #fff; }
	.wallet-details { background: rgba(0,0,0,0.8); border: 1px solid #00ff00; border-top: none; border-radius: 0 0 4px 4px; padding: 12px; animation: slideDown 0.2s ease-out; position: absolute; top: 100%; right: 0; z-index: 1000; margin-top: 0; box-shadow: 0 4px 12px rgba(0,0,0,0.3); width: 300px; max-height: 80vh; overflow-y: auto; }
	.detail-grid { display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; }
	.detail-row { display: flex; justify-content: space-between; align-items: center; }
	.detail-label { color: #80ff80; font-size: 10px; font-weight: bold; }
	.detail-value { color: #00ff00; font-size: 11px; font-family: monospace; }
	.address-full { max-width: 200px; overflow: hidden; text-overflow: ellipsis; }
	.traits-section { flex-direction: column; align-items: flex-start !important; gap: 8px; }
	.traits-container { display: flex; flex-wrap: wrap; gap: 6px; width: 100%; }
	.trait-badge { background: rgba(0,255,0,0.2); border: 1px solid #00ff00; color: #00ff00; padding: 4px 8px; border-radius: 12px; font-size: 9px; font-weight: bold; text-transform: uppercase; white-space: nowrap; }
	.loading { color: #80ff80; font-style: italic; }
	.no-access { color: #ff8080; font-style: italic; }
	.nft-view-btn { background: rgba(0,255,0,0.2); border: 1px solid #00ff00; color: #00ff00; padding: 6px 12px; border-radius: 12px; font-size: 9px; font-weight: bold; cursor: pointer; transition: all 0.2s ease; font-family: inherit; white-space: nowrap; margin-left: 8px; }
	.nft-view-btn:hover { background: rgba(0,255,0,0.3); box-shadow: 0 0 8px rgba(0,255,0,0.4); transform: translateY(-1px); }
	.disconnect-btn { width: 100%; padding: 8px; background: rgba(255,0,0,0.1); border: 1px solid #ff4444; color: #ff4444; font-family: inherit; font-size: 12px; font-weight: bold; cursor: pointer; border-radius: 4px; transition: all 0.2s ease; }
	.disconnect-btn:hover { background: rgba(255,0,0,0.2); box-shadow: 0 0 5px rgba(255,68,68,0.3); }
	.loading-indicator { margin-top: 16px; text-align: center; color: #80ff80; }
	.loading-text { font-size: 12px; margin-bottom: 8px; }
	.loading-dots { animation: pulse 1.5s infinite; font-size: 16px; color: #00ff00; }
	@keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
	@keyframes pulse { 0%,100% { opacity: 0.3; } 50% { opacity: 1; } }
</style>
