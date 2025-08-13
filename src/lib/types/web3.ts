import type { ethers } from 'ethers';

export interface TokenInfo {
	address: string;
	symbol: string;
	name: string;
	decimals: number;
	logoURI?: string;
}

export interface TransactionRequest {
	to: string;
	value?: string;
	data?: string;
	gasLimit?: number;
	gasPrice?: string;
}

export interface TransactionResponse {
	hash: string;
	from: string;
	to: string;
	value: string;
	gasLimit: string;
	gasPrice: string;
	nonce: number;
	blockNumber?: number;
	blockHash?: string;
	timestamp?: number;
	status?: number;
}

export interface ContractCallResult<T = any> {
	success: boolean;
	data?: T;
	error?: string;
	transactionHash?: string;
}

export interface WalletState {
	address: string | null;
	balance: string;
	chainId: number;
	isConnected: boolean;
	isConnecting: boolean;
	error: string | null;
}

export interface NetworkInfo {
	chainId: number;
	name: string;
	currency: string;
	rpcUrl: string;
	explorerUrl: string;
}

// Extend Window interface for ethereum provider
declare global {
	interface Window {
		ethereum?: {
			request: (args: { method: string; params?: any[] }) => Promise<any>;
			on: (event: string, handler: (...args: any[]) => void) => void;
			removeListener: (event: string, handler: (...args: any[]) => void) => void;
			isMetaMask?: boolean;
			chainId?: string;
			selectedAddress?: string;
		};
	}
}

export type EthereumProvider = Window['ethereum'];