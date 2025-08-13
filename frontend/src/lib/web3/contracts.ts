import { ethers } from 'ethers';
import { provider } from './config';
import { walletManager } from './wallet';
import type { ContractCallResult, TokenInfo } from '$lib/types/web3';

// Standard ERC-20 ABI (minimal)
export const ERC20_ABI = [
	'function name() view returns (string)',
	'function symbol() view returns (string)',
	'function decimals() view returns (uint8)',
	'function totalSupply() view returns (uint256)',
	'function balanceOf(address owner) view returns (uint256)',
	'function allowance(address owner, address spender) view returns (uint256)',
	'function transfer(address to, uint256 amount) returns (bool)',
	'function approve(address spender, uint256 amount) returns (bool)',
	'function transferFrom(address from, address to, uint256 amount) returns (bool)',
	'event Transfer(address indexed from, address indexed to, uint256 value)',
	'event Approval(address indexed owner, address indexed spender, uint256 value)'
];

export class ContractManager {
	// Get ERC-20 token information
	async getTokenInfo(tokenAddress: string): Promise<TokenInfo | null> {
		try {
			const contract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
			
			const [name, symbol, decimals] = await Promise.all([
				contract.name(),
				contract.symbol(),
				contract.decimals()
			]);

			return {
				address: tokenAddress,
				name,
				symbol,
				decimals: Number(decimals)
			};
		} catch (error) {
			console.error('Error fetching token info:', error);
			return null;
		}
	}

	// Get token balance for an address
	async getTokenBalance(tokenAddress: string, userAddress: string): Promise<string> {
		try {
			const contract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
			const balance = await contract.balanceOf(userAddress);
			const decimals = await contract.decimals();
			
			return ethers.formatUnits(balance, decimals);
		} catch (error) {
			console.error('Error fetching token balance:', error);
			return '0';
		}
	}

	// Transfer tokens
	async transferToken(
		tokenAddress: string, 
		toAddress: string, 
		amount: string
	): Promise<ContractCallResult> {
		try {
			const signer = walletManager.getSigner();
			if (!signer) {
				throw new Error('Wallet not connected');
			}

			const contract = new ethers.Contract(tokenAddress, ERC20_ABI, signer);
			const decimals = await contract.decimals();
			const value = ethers.parseUnits(amount, decimals);

			const tx = await contract.transfer(toAddress, value);
			await tx.wait();

			return {
				success: true,
				transactionHash: tx.hash
			};
		} catch (error) {
			console.error('Error transferring token:', error);
			return {
				success: false,
				error: error instanceof Error ? error.message : 'Transfer failed'
			};
		}
	}

	// Approve token spending
	async approveToken(
		tokenAddress: string, 
		spenderAddress: string, 
		amount: string
	): Promise<ContractCallResult> {
		try {
			const signer = walletManager.getSigner();
			if (!signer) {
				throw new Error('Wallet not connected');
			}

			const contract = new ethers.Contract(tokenAddress, ERC20_ABI, signer);
			const decimals = await contract.decimals();
			const value = ethers.parseUnits(amount, decimals);

			const tx = await contract.approve(spenderAddress, value);
			await tx.wait();

			return {
				success: true,
				transactionHash: tx.hash
			};
		} catch (error) {
			console.error('Error approving token:', error);
			return {
				success: false,
				error: error instanceof Error ? error.message : 'Approval failed'
			};
		}
	}

	// Check token allowance
	async getTokenAllowance(
		tokenAddress: string, 
		ownerAddress: string, 
		spenderAddress: string
	): Promise<string> {
		try {
			const contract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
			const allowance = await contract.allowance(ownerAddress, spenderAddress);
			const decimals = await contract.decimals();
			
			return ethers.formatUnits(allowance, decimals);
		} catch (error) {
			console.error('Error fetching token allowance:', error);
			return '0';
		}
	}

	// Get transaction receipt
	async getTransactionReceipt(txHash: string) {
		try {
			return await provider.getTransactionReceipt(txHash);
		} catch (error) {
			console.error('Error fetching transaction receipt:', error);
			return null;
		}
	}

	// Wait for transaction confirmation
	async waitForTransaction(txHash: string, confirmations: number = 1) {
		try {
			return await provider.waitForTransaction(txHash, confirmations);
		} catch (error) {
			console.error('Error waiting for transaction:', error);
			return null;
		}
	}

	// Estimate gas for a transaction
	async estimateGas(
		contractAddress: string, 
		abi: string[], 
		methodName: string, 
		params: any[]
	): Promise<bigint | null> {
		try {
			const signer = walletManager.getSigner();
			if (!signer) {
				throw new Error('Wallet not connected');
			}

			const contract = new ethers.Contract(contractAddress, abi, signer);
			return await contract[methodName].estimateGas(...params);
		} catch (error) {
			console.error('Error estimating gas:', error);
			return null;
		}
	}
}

// Export singleton instance
export const contractManager = new ContractManager();

// Common Base network token addresses (update with actual addresses)
export const BASE_TOKENS = {
	WETH: '0x4200000000000000000000000000000000000006',
	USDC: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
	// Add more token addresses as needed
} as const;

export type BaseTokenSymbol = keyof typeof BASE_TOKENS;