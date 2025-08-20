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

// CyberdyneAccessNFT ABI
export const CYBERDYNE_ACCESS_NFT_ABI = [
	'function balanceOf(address owner) view returns (uint256)',
	'function tokenOfOwnerByIndex(address owner, uint256 index) view returns (uint256)',
	'function getUserTokens(address user) view returns (uint256[])',
	'function getUserPermissions(address user) view returns (uint256[] tokenIds, tuple(bool learningMaterials, bool frontendServers, bool backendServers, bool blogCreator, bool admin, bool canSellMarketplace, uint256 issuedAt, uint256 lastUpdated, string metadataURI)[] permissions)',
	'function getTokenPermissions(uint256 tokenId) view returns (tuple(bool learningMaterials, bool frontendServers, bool backendServers, bool blogCreator, bool admin, bool canSellMarketplace, uint256 issuedAt, uint256 lastUpdated, string metadataURI))',
	'function tokenURI(uint256 tokenId) view returns (string)',
	'function addressHasLearningAccess(address user) view returns (bool)',
	'function addressHasFrontendAccess(address user) view returns (bool)',
	'function addressHasBackendAccess(address user) view returns (bool)',
	'function addressHasBlogCreatorAccess(address user) view returns (bool)',
	'function addressHasAdminAccess(address user) view returns (bool)',
	'function addressHasMarketplaceSellAccess(address user) view returns (bool)'
];

// Access NFT Types
export interface AccessPermissions {
	learningMaterials: boolean;
	frontendServers: boolean;
	backendServers: boolean;
	blogCreator: boolean;
	admin: boolean;
	canSellMarketplace: boolean;
	issuedAt: bigint;
	lastUpdated: bigint;
	metadataURI: string;
}

export interface UserNFTData {
	tokenIds: bigint[];
	permissions: AccessPermissions[];
}

export interface NFTTraits {
	Learning: boolean;
	Frontend: boolean;
	Backend: boolean;
	'Blog Creator': boolean;
	Admin: boolean;
	Marketplace: boolean;
}

export class CyberdyneAccessNFTManager {
	private contractAddress: string;

	constructor(contractAddress: string) {
		this.contractAddress = contractAddress;
	}

	private getContract(withSigner = false) {
		const signerOrProvider = withSigner ? walletManager.getSigner() : provider;
		return new ethers.Contract(this.contractAddress, CYBERDYNE_ACCESS_NFT_ABI, signerOrProvider);
	}

	async getUserTokens(userAddress: string): Promise<bigint[]> {
		try {
			const contract = this.getContract();
			return await contract.getUserTokens(userAddress);
		} catch (error) {
			console.error('Error fetching user tokens:', error);
			return [];
		}
	}

	async getUserPermissions(userAddress: string): Promise<UserNFTData | null> {
		try {
			const contract = this.getContract();
			const [tokenIds, permissions] = await contract.getUserPermissions(userAddress);
			return { tokenIds, permissions };
		} catch (error) {
			console.error('Error fetching user permissions:', error);
			return null;
		}
	}

	async getTokenURI(tokenId: bigint): Promise<string> {
		try {
			const contract = this.getContract();
			return await contract.tokenURI(tokenId);
		} catch (error) {
			console.error('Error fetching token URI:', error);
			return '';
		}
	}

	async parseTokenMetadata(tokenURI: string): Promise<NFTTraits | null> {
		try {
			let metadataJSON: any;

			if (tokenURI.startsWith('data:application/json;base64,')) {
				const base64Data = tokenURI.replace('data:application/json;base64,', '');
				const decodedData = atob(base64Data);
				metadataJSON = JSON.parse(decodedData);
			} else if (tokenURI.startsWith('http')) {
				const response = await fetch(tokenURI);
				metadataJSON = await response.json();
			} else {
				console.error('Unsupported token URI format:', tokenURI);
				return null;
			}

			if (!metadataJSON.attributes) {
				return null;
			}

			const traits: NFTTraits = {
				Learning: false,
				Frontend: false,
				Backend: false,
				'Blog Creator': false,
				Admin: false,
				Marketplace: false
			};

			metadataJSON.attributes.forEach((attr: any) => {
				const traitType = attr.trait_type;
				const value = attr.value === true || attr.value === 'true';
				
				if (traitType in traits) {
					(traits as any)[traitType] = value;
				}
			});

			return traits;
		} catch (error) {
			console.error('Error parsing token metadata:', error);
			return null;
		}
	}

	async getUserTraits(userAddress: string): Promise<NFTTraits | null> {
		try {
			const userData = await this.getUserPermissions(userAddress);
			if (!userData || userData.tokenIds.length === 0) {
				return null;
			}

			const combinedTraits: NFTTraits = {
				Learning: false,
				Frontend: false,
				Backend: false,
				'Blog Creator': false,
				Admin: false,
				Marketplace: false
			};

			for (let i = 0; i < userData.tokenIds.length; i++) {
				const permissions = userData.permissions[i];
				combinedTraits.Learning = combinedTraits.Learning || permissions.learningMaterials;
				combinedTraits.Frontend = combinedTraits.Frontend || permissions.frontendServers;
				combinedTraits.Backend = combinedTraits.Backend || permissions.backendServers;
				combinedTraits['Blog Creator'] = combinedTraits['Blog Creator'] || permissions.blogCreator;
				combinedTraits.Admin = combinedTraits.Admin || permissions.admin;
				combinedTraits.Marketplace = combinedTraits.Marketplace || permissions.canSellMarketplace;
			}

			return combinedTraits;
		} catch (error) {
			console.error('Error fetching user traits:', error);
			return null;
		}
	}

	async hasAnyAccess(userAddress: string): Promise<boolean> {
		try {
			const contract = this.getContract();
			const balance = await contract.balanceOf(userAddress);
			return balance > 0n;
		} catch (error) {
			console.error('Error checking access:', error);
			return false;
		}
	}
}