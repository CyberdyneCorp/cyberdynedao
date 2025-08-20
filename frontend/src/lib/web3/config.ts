import { ethers } from 'ethers';

// Get environment variables using import.meta.env
const VITE_INFURA_ENDPOINT = import.meta.env.VITE_INFURA_ENDPOINT;
const VITE_CHAIN_ID = import.meta.env.VITE_CHAIN_ID;
const VITE_NETWORK_NAME = import.meta.env.VITE_NETWORK_NAME;
const VITE_NATIVE_CURRENCY = import.meta.env.VITE_NATIVE_CURRENCY;

export interface NetworkConfig {
	chainId: number;
	name: string;
	rpcUrl: string;
	nativeCurrency: {
		name: string;
		symbol: string;
		decimals: number;
	};
	blockExplorer: string;
}

export const BASE_NETWORK: NetworkConfig = {
	chainId: parseInt(VITE_CHAIN_ID),
	name: VITE_NETWORK_NAME,
	rpcUrl: VITE_INFURA_ENDPOINT,
	nativeCurrency: {
		name: 'Ethereum',
		symbol: VITE_NATIVE_CURRENCY,
		decimals: 18
	},
	blockExplorer: 'https://basescan.org'
};

export const SUPPORTED_NETWORKS: Record<number, NetworkConfig> = {
	[BASE_NETWORK.chainId]: BASE_NETWORK
};

// Create provider instance
export const createProvider = (): ethers.JsonRpcProvider => {
	return new ethers.JsonRpcProvider(BASE_NETWORK.rpcUrl);
};

// Provider instance
export const provider = createProvider();

// Common contract addresses on Base (you can expand this)
export const CONTRACT_ADDRESSES = {
	// Add your contract addresses here
	// Example: USDC: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
	// Example: WETH: '0x4200000000000000000000000000000000000006'
	CYBERDYNE_ACCESS_NFT: import.meta.env.VITE_CYBERDYNE_ACCESS_NFT_ADDRESS || ''
};

// Gas estimation helpers
export const GAS_LIMITS = {
	SIMPLE_TRANSFER: 21000,
	TOKEN_TRANSFER: 60000,
	CONTRACT_INTERACTION: 200000,
	SWAP: 300000
} as const;

export const formatAddress = (address: string): string => {
	if (!address) return '';
	return `${address.slice(0, 6)}...${address.slice(-4)}`;
};

export const formatBalance = (balance: string, decimals: number = 18): string => {
	const formatted = ethers.formatUnits(balance, decimals);
	const num = parseFloat(formatted);
	
	if (num === 0) return '0';
	if (num < 0.0001) return '< 0.0001';
	if (num < 1) return num.toFixed(4);
	if (num < 1000) return num.toFixed(2);
	
	return `${(num / 1000).toFixed(2)}k`;
};

export const validateAddress = (address: string): boolean => {
	try {
		return ethers.isAddress(address);
	} catch {
		return false;
	}
};