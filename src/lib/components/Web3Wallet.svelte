<script lang="ts">
	import { 
		walletInfo, 
		isConnected, 
		isConnecting, 
		connectionError, 
		shortAddress, 
		walletBalance,
		isCorrectNetwork,
		web3Actions 
	} from '$lib/stores/web3Store';
	import { BASE_NETWORK } from '$lib/web3/config';

	let showDetails = false;

	function toggleDetails() {
		showDetails = !showDetails;
	}

	async function handleConnect() {
		await web3Actions.connectWallet();
	}

	async function handleDisconnect() {
		await web3Actions.disconnectWallet();
		showDetails = false;
	}

	async function handleSwitchNetwork() {
		await web3Actions.switchToBaseNetwork();
	}

	function clearError() {
		web3Actions.clearError();
	}
</script>

<div class="web3-wallet">
	{#if $connectionError}
		<div class="error-banner bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded mb-2">
			<div class="flex items-center justify-between">
				<span class="text-xs font-mono">{$connectionError}</span>
				<button on:click={clearError} class="text-red-500 hover:text-red-700">
					<span class="text-xs">✕</span>
				</button>
			</div>
		</div>
	{/if}

	{#if !$isConnected}
		<button 
			on:click={handleConnect}
			disabled={$isConnecting}
			class="connect-btn w-full bg-blue-600 text-white py-2 px-4 rounded font-mono text-xs hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
		>
			{$isConnecting ? 'Connecting...' : '🔗 Connect Wallet'}
		</button>
	{:else}
		<div class="wallet-connected">
			{#if !$isCorrectNetwork}
				<div class="network-warning bg-orange-100 border border-orange-400 text-orange-700 px-3 py-2 rounded mb-2">
					<div class="flex items-center justify-between">
						<span class="text-xs font-mono">Wrong Network</span>
						<button 
							on:click={handleSwitchNetwork}
							class="bg-orange-600 text-white px-2 py-1 rounded text-xs hover:bg-orange-700"
						>
							Switch to {BASE_NETWORK.name}
						</button>
					</div>
				</div>
			{/if}

			<div class="wallet-info">
				<button 
					on:click={toggleDetails}
					class="wallet-summary w-full bg-green-100 border border-green-400 text-green-800 px-3 py-2 rounded font-mono text-xs hover:bg-green-200 transition-colors text-left"
				>
					<div class="flex items-center justify-between">
						<div>
							<div class="font-bold">🟢 Connected</div>
							<div class="text-xs opacity-75">{$shortAddress}</div>
						</div>
						<div class="text-right">
							<div class="font-bold">{$walletBalance} ETH</div>
							<div class="text-xs opacity-75">{showDetails ? '▲' : '▼'}</div>
						</div>
					</div>
				</button>

				{#if showDetails}
					<div class="wallet-details bg-white border border-gray-300 rounded-b px-3 py-2 -mt-1">
						<div class="space-y-2 text-xs font-mono">
							<div class="flex justify-between">
								<span class="text-gray-600">Network:</span>
								<span class="font-bold">{BASE_NETWORK.name}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Chain ID:</span>
								<span class="font-bold">{BASE_NETWORK.chainId}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Address:</span>
								<span class="font-mono text-xs break-all">{$walletInfo?.address}</span>
							</div>
							<div class="pt-2 border-t">
								<button 
									on:click={handleDisconnect}
									class="w-full bg-red-100 text-red-700 py-1 px-2 rounded text-xs hover:bg-red-200 transition-colors"
								>
									🔌 Disconnect
								</button>
							</div>
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.web3-wallet {
		font-family: 'Courier New', monospace;
	}

	.wallet-details {
		animation: slideDown 0.2s ease-out;
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
</style>