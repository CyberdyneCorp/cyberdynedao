import { ethers, type Eip1193Provider } from 'ethers';
import { BASE_NETWORK, SUPPORTED_NETWORKS, formatAddress, formatBalance } from './config';

export interface WalletInfo {
	address: string;
	balance: string;
	chainId: number;
	isConnected: boolean;
}

export class WalletManager {
	private provider: ethers.BrowserProvider | null = null;
	private signer: ethers.JsonRpcSigner | null = null;

	constructor() {
		// Listen for account/network changes
		if (typeof window !== 'undefined' && window.ethereum) {
			window.ethereum.on('accountsChanged', this.handleAccountsChanged.bind(this));
			window.ethereum.on('chainChanged', this.handleChainChanged.bind(this));
			window.ethereum.on('disconnect', this.handleDisconnect.bind(this));
		}
	}

	// Check if wallet extension is available
	isWalletAvailable(): boolean {
		return typeof window !== 'undefined' && !!window.ethereum;
	}

	// Connect wallet
	async connectWallet(): Promise<WalletInfo | null> {
		if (!this.isWalletAvailable()) {
			throw new Error('No wallet extension found. Please install MetaMask or another Web3 wallet.');
		}

		try {
			this.provider = new ethers.BrowserProvider(window.ethereum as Eip1193Provider);
			
			// Request account access
			await this.provider.send('eth_requestAccounts', []);
			
			// Get signer
			this.signer = await this.provider.getSigner();
			
			// Get wallet info
			const address = await this.signer.getAddress();
			const balance = await this.provider.getBalance(address);
			const network = await this.provider.getNetwork();
			
			// Check if we're on the correct network
			if (Number(network.chainId) !== BASE_NETWORK.chainId) {
				await this.switchToBaseNetwork();
			}

			const walletInfo: WalletInfo = {
				address,
				balance: formatBalance(balance.toString()),
				chainId: Number(network.chainId),
				isConnected: true
			};

			return walletInfo;
		} catch (error) {
			console.error('Error connecting wallet:', error);
			throw error;
		}
	}

	// Disconnect wallet
	async disconnectWallet(): Promise<void> {
		this.provider = null;
		this.signer = null;
	}

	// Get current wallet info
	async getWalletInfo(): Promise<WalletInfo | null> {
		if (!this.provider || !this.signer) {
			return null;
		}

		try {
			const address = await this.signer.getAddress();
			const balance = await this.provider.getBalance(address);
			const network = await this.provider.getNetwork();

			return {
				address,
				balance: formatBalance(balance.toString()),
				chainId: Number(network.chainId),
				isConnected: true
			};
		} catch (error) {
			console.error('Error getting wallet info:', error);
			return null;
		}
	}

	// Switch to Base network
	async switchToBaseNetwork(): Promise<void> {
		if (!this.provider) {
			throw new Error('No wallet connected');
		}

		try {
			await this.provider.send('wallet_switchEthereumChain', [
				{ chainId: `0x${BASE_NETWORK.chainId.toString(16)}` }
			]);
		} catch (error: any) {
			// If the network is not added, add it
			if (error.code === 4902) {
				await this.addBaseNetwork();
			} else {
				throw error;
			}
		}
	}

	// Add Base network to wallet
	private async addBaseNetwork(): Promise<void> {
		if (!this.provider) {
			throw new Error('No wallet connected');
		}

		await this.provider.send('wallet_addEthereumChain', [
			{
				chainId: `0x${BASE_NETWORK.chainId.toString(16)}`,
				chainName: BASE_NETWORK.name,
				nativeCurrency: BASE_NETWORK.nativeCurrency,
				rpcUrls: [BASE_NETWORK.rpcUrl],
				blockExplorerUrls: [BASE_NETWORK.blockExplorer]
			}
		]);
	}

	// Send transaction
	async sendTransaction(to: string, value: string, data?: string): Promise<string> {
		if (!this.signer) {
			throw new Error('No wallet connected');
		}

		const tx = {
			to,
			value: ethers.parseEther(value),
			data: data || '0x'
		};

		const transaction = await this.signer.sendTransaction(tx);
		return transaction.hash;
	}

	// Get signer for contract interactions
	getSigner(): ethers.JsonRpcSigner | null {
		return this.signer;
	}

	// Get provider
	getProvider(): ethers.BrowserProvider | null {
		return this.provider;
	}

	// Event handlers
	private handleAccountsChanged(accounts: string[]): void {
		if (accounts.length === 0) {
			// User disconnected wallet
			this.disconnectWallet();
		}
		// You can emit events or update stores here
		window.dispatchEvent(new CustomEvent('wallet:accountsChanged', { detail: accounts }));
	}

	private handleChainChanged(chainId: string): void {
		// Network changed
		window.dispatchEvent(new CustomEvent('wallet:chainChanged', { detail: parseInt(chainId, 16) }));
	}

	private handleDisconnect(): void {
		this.disconnectWallet();
		window.dispatchEvent(new CustomEvent('wallet:disconnected'));
	}
}

// Export singleton instance
export const walletManager = new WalletManager();

// Utility functions
export { formatAddress, formatBalance };

// Types
export type { WalletInfo };