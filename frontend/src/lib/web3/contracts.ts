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
		console.log('🔗 CyberdyneAccessNFTManager: Getting token URI for token ID:', tokenId.toString());
		
		try {
			const contract = this.getContract();
			console.log('📄 Contract instance created, calling tokenURI...');
			
			const uri = await contract.tokenURI(tokenId);
			console.log('✅ Token URI received:', uri.substring(0, 100) + (uri.length > 100 ? '...' : ''));
			
			return uri;
		} catch (error) {
			console.error('💥 Error fetching token URI:', error);
			console.error('Error details:', {
				name: error instanceof Error ? error.name : 'Unknown',
				message: error instanceof Error ? error.message : String(error)
			});
			return '';
		}
	}

	async parseTokenMetadata(tokenURI: string): Promise<NFTTraits | null> {
		console.log('🎨 CyberdyneAccessNFTManager: Parsing token metadata');
		console.log('🔗 Token URI:', tokenURI);
		
		try {
			let metadataJSON: any;

			if (tokenURI.startsWith('data:application/json;base64,')) {
				console.log('📋 Parsing Base64-encoded JSON metadata');
				const base64Data = tokenURI.replace('data:application/json;base64,', '');
				console.log('🔤 Base64 data length:', base64Data.length);
				
				const decodedData = atob(base64Data);
				console.log('📄 Decoded metadata JSON:', decodedData);
				
				metadataJSON = JSON.parse(decodedData);
				console.log('✅ Successfully parsed JSON metadata:', metadataJSON);
			} else if (tokenURI.startsWith('http')) {
				console.log('🌐 Fetching external metadata from HTTP URL');
				const response = await fetch(tokenURI);
				console.log('📡 HTTP response status:', response.status);
				
				metadataJSON = await response.json();
				console.log('✅ Successfully fetched JSON metadata:', metadataJSON);
			} else {
				console.error('❌ Unsupported token URI format:', tokenURI);
				return null;
			}

			if (!metadataJSON.attributes) {
				console.log('❌ No attributes found in metadata');
				return null;
			}

			console.log('📊 Found attributes:', metadataJSON.attributes);

			const traits: NFTTraits = {
				Learning: false,
				Frontend: false,
				Backend: false,
				'Blog Creator': false,
				Admin: false,
				Marketplace: false
			};

			console.log('🔄 Processing attributes...');
			metadataJSON.attributes.forEach((attr: any, index: number) => {
				console.log(`📝 Attribute ${index}:`, {
					trait_type: attr.trait_type,
					value: attr.value,
					value_type: typeof attr.value
				});
				
				const traitType = attr.trait_type;
				const value = attr.value === true || attr.value === 'true';
				
				console.log(`🎯 Processing trait "${traitType}" with value:`, value);
				
				if (traitType in traits) {
					(traits as any)[traitType] = value;
					console.log(`✅ Set trait "${traitType}" to:`, value);
				} else {
					console.log(`⚠️ Unknown trait type: "${traitType}"`);
				}
			});

			console.log('🎯 Final parsed traits:', traits);
			return traits;
		} catch (error) {
			console.error('Error parsing token metadata:', error);
			return null;
		}
	}

	async getUserTraits(userAddress: string): Promise<NFTTraits | null> {
		console.log('🎯 CyberdyneAccessNFTManager: Getting user traits');
		console.log('👤 User address:', userAddress);
		
		try {
			console.log('📊 Step 1: Getting user permissions from contract...');
			const userData = await this.getUserPermissions(userAddress);
			
			console.log('📋 User data received:', userData);
			
			if (!userData || userData.tokenIds.length === 0) {
				console.log('❌ No user data or no tokens found');
				return null;
			}

			console.log('🔢 Number of tokens found:', userData.tokenIds.length);
			console.log('🆔 Token IDs:', userData.tokenIds.map(id => id.toString()));

			const combinedTraits: NFTTraits = {
				Learning: false,
				Frontend: false,
				Backend: false,
				'Blog Creator': false,
				Admin: false,
				Marketplace: false
			};

			console.log('🔄 Processing permissions for each token...');
			for (let i = 0; i < userData.tokenIds.length; i++) {
				const tokenId = userData.tokenIds[i];
				const permissions = userData.permissions[i];
				
				console.log(`📝 Token #${tokenId.toString()} permissions:`, {
					learningMaterials: permissions.learningMaterials,
					frontendServers: permissions.frontendServers,
					backendServers: permissions.backendServers,
					blogCreator: permissions.blogCreator,
					admin: permissions.admin,
					canSellMarketplace: permissions.canSellMarketplace,
					metadataURI: permissions.metadataURI
				});

				// If there's a custom metadata URI, try to parse it for traits
				if (permissions.metadataURI && permissions.metadataURI.length > 0) {
					console.log(`🔗 Token #${tokenId.toString()} has custom metadata URI:`, permissions.metadataURI);
					
					try {
						const tokenURI = await this.getTokenURI(tokenId);
						console.log(`📄 Token #${tokenId.toString()} URI result:`, tokenURI);
						
						const traitsFromMetadata = await this.parseTokenMetadata(tokenURI);
						console.log(`🎨 Parsed traits from metadata for token #${tokenId.toString()}:`, traitsFromMetadata);
						
						if (traitsFromMetadata) {
							// Use metadata traits if available
							combinedTraits.Learning = combinedTraits.Learning || traitsFromMetadata.Learning;
							combinedTraits.Frontend = combinedTraits.Frontend || traitsFromMetadata.Frontend;
							combinedTraits.Backend = combinedTraits.Backend || traitsFromMetadata.Backend;
							combinedTraits['Blog Creator'] = combinedTraits['Blog Creator'] || traitsFromMetadata['Blog Creator'];
							combinedTraits.Admin = combinedTraits.Admin || traitsFromMetadata.Admin;
							combinedTraits.Marketplace = combinedTraits.Marketplace || traitsFromMetadata.Marketplace;
							continue;
						}
					} catch (metadataError) {
						console.warn(`⚠️ Error parsing metadata for token #${tokenId.toString()}:`, metadataError);
					}
				}

				// Fallback to using direct contract permissions
				console.log(`📊 Using direct contract permissions for token #${tokenId.toString()}`);
				combinedTraits.Learning = combinedTraits.Learning || permissions.learningMaterials;
				combinedTraits.Frontend = combinedTraits.Frontend || permissions.frontendServers;
				combinedTraits.Backend = combinedTraits.Backend || permissions.backendServers;
				combinedTraits['Blog Creator'] = combinedTraits['Blog Creator'] || permissions.blogCreator;
				combinedTraits.Admin = combinedTraits.Admin || permissions.admin;
				combinedTraits.Marketplace = combinedTraits.Marketplace || permissions.canSellMarketplace;
			}

			console.log('🎯 Final combined traits:', combinedTraits);
			return combinedTraits;
		} catch (error) {
			console.error('💥 Error fetching user traits:', error);
			console.error('Error details:', {
				name: error instanceof Error ? error.name : 'Unknown',
				message: error instanceof Error ? error.message : String(error),
				stack: error instanceof Error ? error.stack : undefined
			});
			return null;
		}
	}

	async hasAnyAccess(userAddress: string): Promise<boolean> {
		console.log('🔍 CyberdyneAccessNFTManager: Checking if user has any access NFTs');
		console.log('📍 Contract address:', this.contractAddress);
		console.log('👤 User address:', userAddress);
		
		try {
			const contract = this.getContract();
			console.log('📄 Contract instance created successfully');
			
			const balance = await contract.balanceOf(userAddress);
			console.log('💰 User NFT balance:', balance.toString());
			
			const hasAccess = balance > 0n;
			console.log('✅ User has access:', hasAccess);
			
			return hasAccess;
		} catch (error) {
			console.error('💥 Error checking access:', error);
			console.error('Error details:', {
				name: error instanceof Error ? error.name : 'Unknown',
				message: error instanceof Error ? error.message : String(error)
			});
			return false;
		}
	}
}