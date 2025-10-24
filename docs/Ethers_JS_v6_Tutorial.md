# Ethers.js v6 Tutorial: Complete Guide with Examples

**Version:** 1.0
**Target:** Ethers.js v6.15.0
**Network:** Base (8453)
**Framework:** SvelteKit + TypeScript

---

## Table of Contents

1. [Introduction to Ethers.js v6](#1-introduction-to-ethersjs-v6)
2. [Installation & Setup](#2-installation--setup)
3. [Providers: Reading from Blockchain](#3-providers-reading-from-blockchain)
4. [Signers: Writing to Blockchain](#4-signers-writing-to-blockchain)
5. [Contract Interactions](#5-contract-interactions)
6. [Common Utilities](#6-common-utilities)
7. [Advanced Patterns](#7-advanced-patterns)
8. [Real-World Examples](#8-real-world-examples)
9. [Migration from v5](#9-migration-from-v5)
10. [Best Practices](#10-best-practices)

---

## 1) Introduction to Ethers.js v6

### What is Ethers.js?

Ethers.js is a complete Ethereum library for JavaScript/TypeScript that allows you to:
- **Read** blockchain data (balances, contract state, transactions)
- **Write** to the blockchain (send transactions, deploy contracts)
- **Interact** with smart contracts (call methods, listen to events)
- **Sign** messages and transactions securely

### Why v6?

**Key improvements over v5:**
- Native **BigInt** support (no more `BigNumber` class)
- Better **TypeScript** support
- Modern **ES6+** syntax
- Improved **tree-shaking** for smaller bundles
- Better **error handling**

### Core Concepts

```typescript
┌─────────────────────────────────────────────────┐
│                 Ethers.js v6                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  Provider          │  Signer                    │
│  (Read-Only)       │  (Can Sign & Send)         │
│  ─────────────────────────────────────────────  │
│  • Get balances    │  • Sign transactions       │
│  • Read contracts  │  • Send ETH/tokens         │
│  • Query events    │  • Call contract methods   │
│  • Get gas prices  │  • Deploy contracts        │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 2) Installation & Setup

### Install Dependencies

```bash
cd frontend
npm install ethers@6
```

### Import Ethers.js

```typescript
// Import specific utilities
import {
  ethers,
  BrowserProvider,
  JsonRpcProvider,
  Contract,
  parseEther,
  formatEther,
  parseUnits,
  formatUnits,
  isAddress,
  getAddress
} from 'ethers';

// Or import everything
import { ethers } from 'ethers';
```

### Basic Configuration

**`frontend/src/lib/web3/config.ts`:**

```typescript
import { ethers } from 'ethers';

export const BASE_NETWORK = {
  chainId: 8453,
  name: 'Base Mainnet',
  rpcUrl: import.meta.env.VITE_INFURA_ENDPOINT,
  nativeCurrency: {
    name: 'Ethereum',
    symbol: 'ETH',
    decimals: 18
  },
  blockExplorer: 'https://basescan.org'
};

// Create a read-only provider
export const provider = new ethers.JsonRpcProvider(BASE_NETWORK.rpcUrl);
```

---

## 3) Providers: Reading from Blockchain

Providers are **read-only** connections to the blockchain. Use them to query data without needing a wallet.

### Types of Providers

#### 1. JsonRpcProvider (Read-Only via RPC)

```typescript
import { JsonRpcProvider } from 'ethers';

// Connect to Base network
const provider = new JsonRpcProvider('https://mainnet.base.org');

// Check connection
const network = await provider.getNetwork();
console.log('Connected to:', network.name, network.chainId);
// Output: Connected to: base 8453n
```

#### 2. BrowserProvider (From Wallet like MetaMask)

```typescript
import { BrowserProvider } from 'ethers';

// Connect to user's wallet (MetaMask, etc.)
const provider = new BrowserProvider(window.ethereum);

// Request account access
await provider.send('eth_requestAccounts', []);

// Get the signer (can sign transactions)
const signer = await provider.getSigner();
const address = await signer.getAddress();
```

### Reading Blockchain Data

#### Get Account Balance

```typescript
// Get ETH balance
const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0';
const balance = await provider.getBalance(address);

console.log('Raw balance:', balance);
// Output: 1500000000000000000n (BigInt)

// Format to ETH (from wei)
const ethBalance = ethers.formatEther(balance);
console.log('Balance:', ethBalance, 'ETH');
// Output: Balance: 1.5 ETH
```

#### Get Current Block Number

```typescript
const blockNumber = await provider.getBlockNumber();
console.log('Current block:', blockNumber);
// Output: Current block: 7654321
```

#### Get Gas Price

```typescript
const feeData = await provider.getFeeData();

console.log('Max Fee:', ethers.formatUnits(feeData.maxFeePerGas, 'gwei'), 'gwei');
console.log('Priority Fee:', ethers.formatUnits(feeData.maxPriorityFeePerGas, 'gwei'), 'gwei');
```

#### Get Transaction

```typescript
const txHash = '0x...';
const tx = await provider.getTransaction(txHash);

console.log('From:', tx.from);
console.log('To:', tx.to);
console.log('Value:', ethers.formatEther(tx.value), 'ETH');
console.log('Gas Limit:', tx.gasLimit.toString());
```

#### Get Transaction Receipt

```typescript
const receipt = await provider.getTransactionReceipt(txHash);

if (receipt) {
  console.log('Block:', receipt.blockNumber);
  console.log('Status:', receipt.status === 1 ? 'Success' : 'Failed');
  console.log('Gas Used:', receipt.gasUsed.toString());
}
```

#### Wait for Transaction

```typescript
// Send a transaction (more on this later)
const tx = await signer.sendTransaction({
  to: '0x...',
  value: ethers.parseEther('0.1')
});

console.log('Transaction sent:', tx.hash);

// Wait for 1 confirmation
const receipt = await tx.wait();
console.log('Transaction mined in block:', receipt.blockNumber);

// Wait for 3 confirmations for extra security
const receipt3 = await tx.wait(3);
console.log('Transaction confirmed with 3 blocks');
```

---

## 4) Signers: Writing to Blockchain

Signers can **sign** messages and **send** transactions. They require a private key or wallet connection.

### Get Signer from Wallet

```typescript
import { BrowserProvider } from 'ethers';

// Connect to user's wallet
const provider = new BrowserProvider(window.ethereum);
const signer = await provider.getSigner();

const address = await signer.getAddress();
console.log('Signer address:', address);
```

### Send ETH Transaction

```typescript
// Simple ETH transfer
const tx = await signer.sendTransaction({
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0',
  value: ethers.parseEther('0.1') // 0.1 ETH
});

console.log('Transaction hash:', tx.hash);

// Wait for confirmation
const receipt = await tx.wait();
console.log('Transaction confirmed!');
```

### Send ETH with Custom Gas

```typescript
const tx = await signer.sendTransaction({
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0',
  value: ethers.parseEther('0.1'),
  gasLimit: 21000n,
  maxFeePerGas: ethers.parseUnits('50', 'gwei'),
  maxPriorityFeePerGas: ethers.parseUnits('2', 'gwei')
});
```

### Sign Message

```typescript
// Sign arbitrary message
const message = 'Hello Cyberdyne DAO!';
const signature = await signer.signMessage(message);

console.log('Signature:', signature);
// Output: 0x1234...abcd (130 characters)

// Verify signature
const recoveredAddress = ethers.verifyMessage(message, signature);
console.log('Signer address:', recoveredAddress);
```

### Sign Typed Data (EIP-712)

```typescript
const domain = {
  name: 'Cyberdyne DAO',
  version: '1',
  chainId: 8453,
  verifyingContract: '0x...'
};

const types = {
  Vote: [
    { name: 'proposalId', type: 'uint256' },
    { name: 'support', type: 'bool' },
    { name: 'voter', type: 'address' }
  ]
};

const value = {
  proposalId: 1n,
  support: true,
  voter: await signer.getAddress()
};

const signature = await signer.signTypedData(domain, types, value);
console.log('EIP-712 signature:', signature);
```

---

## 5) Contract Interactions

### Define Contract ABI

```typescript
// ERC-20 Token ABI (simplified)
const ERC20_ABI = [
  // Read-only functions
  'function name() view returns (string)',
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)',
  'function totalSupply() view returns (uint256)',
  'function balanceOf(address owner) view returns (uint256)',
  'function allowance(address owner, address spender) view returns (uint256)',

  // Write functions
  'function transfer(address to, uint256 amount) returns (bool)',
  'function approve(address spender, uint256 amount) returns (bool)',
  'function transferFrom(address from, address to, uint256 amount) returns (bool)',

  // Events
  'event Transfer(address indexed from, address indexed to, uint256 value)',
  'event Approval(address indexed owner, address indexed spender, uint256 value)'
];
```

### Create Contract Instance

```typescript
import { Contract } from 'ethers';

const tokenAddress = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'; // USDC on Base

// Read-only contract (with provider)
const tokenContract = new Contract(tokenAddress, ERC20_ABI, provider);

// Read-write contract (with signer)
const tokenContractWithSigner = new Contract(tokenAddress, ERC20_ABI, signer);
```

### Read from Contract

```typescript
// Get token name
const name = await tokenContract.name();
console.log('Token name:', name); // "USD Coin"

// Get token symbol
const symbol = await tokenContract.symbol();
console.log('Token symbol:', symbol); // "USDC"

// Get decimals
const decimals = await tokenContract.decimals();
console.log('Decimals:', decimals); // 6

// Get user balance
const userAddress = '0x...';
const balance = await tokenContract.balanceOf(userAddress);
console.log('Balance:', ethers.formatUnits(balance, decimals), symbol);
// Output: Balance: 100.5 USDC
```

### Write to Contract

```typescript
// Approve token spending
const spenderAddress = '0x...';
const amount = ethers.parseUnits('100', 6); // 100 USDC (6 decimals)

const approveTx = await tokenContractWithSigner.approve(spenderAddress, amount);
console.log('Approve tx:', approveTx.hash);

await approveTx.wait();
console.log('Approval confirmed!');

// Transfer tokens
const recipientAddress = '0x...';
const transferAmount = ethers.parseUnits('50', 6); // 50 USDC

const transferTx = await tokenContractWithSigner.transfer(recipientAddress, transferAmount);
console.log('Transfer tx:', transferTx.hash);

await transferTx.wait();
console.log('Transfer confirmed!');
```

### Listen to Contract Events

```typescript
// Listen to Transfer events
tokenContract.on('Transfer', (from, to, amount, event) => {
  console.log('Transfer detected:');
  console.log('From:', from);
  console.log('To:', to);
  console.log('Amount:', ethers.formatUnits(amount, 6), 'USDC');
  console.log('Block:', event.log.blockNumber);
});

// Listen once
tokenContract.once('Transfer', (from, to, amount) => {
  console.log('First transfer detected!');
});

// Remove all listeners
tokenContract.removeAllListeners('Transfer');
```

### Query Past Events

```typescript
// Get Transfer events from last 1000 blocks
const currentBlock = await provider.getBlockNumber();
const filter = tokenContract.filters.Transfer(null, userAddress); // To user

const events = await tokenContract.queryFilter(
  filter,
  currentBlock - 1000,
  currentBlock
);

console.log(`Found ${events.length} transfers to ${userAddress}`);

events.forEach(event => {
  console.log('From:', event.args.from);
  console.log('Amount:', ethers.formatUnits(event.args.value, 6), 'USDC');
  console.log('Block:', event.blockNumber);
});
```

---

## 6) Common Utilities

### Working with Units

```typescript
import { parseEther, formatEther, parseUnits, formatUnits } from 'ethers';

// ETH (18 decimals)
const oneEth = parseEther('1.0');
console.log(oneEth); // 1000000000000000000n

const formatted = formatEther(1000000000000000000n);
console.log(formatted); // "1.0"

// Custom decimals (e.g., USDC with 6 decimals)
const hundredUsdc = parseUnits('100', 6);
console.log(hundredUsdc); // 100000000n

const formattedUsdc = formatUnits(100000000n, 6);
console.log(formattedUsdc); // "100.0"

// Gwei (gas prices)
const gasPrice = parseUnits('50', 'gwei');
console.log(gasPrice); // 50000000000n
```

### Address Utilities

```typescript
import { isAddress, getAddress } from 'ethers';

// Validate address
const addr = '0x742d35cc6634c0532925a3b844bc9e7595f0beb0';
console.log('Valid:', isAddress(addr)); // true

// Get checksummed address
const checksummed = getAddress(addr);
console.log(checksummed); // "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"

// Invalid address throws error
try {
  getAddress('0xinvalid');
} catch (error) {
  console.error('Invalid address');
}
```

### Hashing and Encoding

```typescript
import {
  keccak256,
  toUtf8Bytes,
  solidityPacked,
  solidityPackedKeccak256,
  id
} from 'ethers';

// Hash a string
const hash = keccak256(toUtf8Bytes('Hello'));
console.log(hash); // 0x06b3dfaec148fb1bb2b066f10ec285e7c9bf402ab32aa78a5d38e34566810cd2

// Solidity-style encoding
const encoded = solidityPacked(
  ['address', 'uint256'],
  ['0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0', 100n]
);

// Hash encoded data
const packedHash = solidityPackedKeccak256(
  ['address', 'uint256'],
  ['0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0', 100n]
);

// Function selector (first 4 bytes of keccak256 hash)
const selector = id('transfer(address,uint256)').slice(0, 10);
console.log(selector); // 0xa9059cbb
```

### Random Numbers (Secure)

```typescript
import { randomBytes, hexlify } from 'ethers';

// Generate random bytes
const random = randomBytes(32);
console.log('Random:', hexlify(random));

// Generate random BigInt
const randomBigInt = BigInt(hexlify(randomBytes(32)));
console.log('Random number:', randomBigInt);
```

---

## 7) Advanced Patterns

### Handle BigInt in JavaScript

```typescript
// BigInt arithmetic
const a = 1000000000000000000n; // 1 ETH
const b = 500000000000000000n;  // 0.5 ETH

const sum = a + b;
console.log(sum); // 1500000000000000000n

const diff = a - b;
console.log(diff); // 500000000000000000n

const product = a * 2n;
console.log(product); // 2000000000000000000n

const quotient = a / 2n;
console.log(quotient); // 500000000000000000n

// Convert to Number (lose precision for large values!)
const asNumber = Number(a) / 1e18;
console.log(asNumber); // 1

// Compare
console.log(a > b); // true
console.log(a === 1000000000000000000n); // true
```

### Batch Multiple Calls

```typescript
// Use Promise.all for parallel calls
const [name, symbol, decimals, totalSupply] = await Promise.all([
  tokenContract.name(),
  tokenContract.symbol(),
  tokenContract.decimals(),
  tokenContract.totalSupply()
]);

console.log(`${name} (${symbol}) - ${decimals} decimals`);
console.log(`Total Supply: ${ethers.formatUnits(totalSupply, decimals)}`);
```

### Error Handling

```typescript
import { ErrorCode } from 'ethers';

try {
  const tx = await signer.sendTransaction({
    to: '0x...',
    value: ethers.parseEther('100')
  });
  await tx.wait();
} catch (error: any) {
  // User rejected transaction
  if (error.code === 'ACTION_REJECTED') {
    console.log('User rejected transaction');
  }
  // Insufficient funds
  else if (error.code === 'INSUFFICIENT_FUNDS') {
    console.log('Insufficient balance');
  }
  // Network error
  else if (error.code === 'NETWORK_ERROR') {
    console.log('Network connection issue');
  }
  // Contract revert
  else if (error.code === 'CALL_EXCEPTION') {
    console.log('Transaction reverted:', error.reason);
  }
  else {
    console.error('Transaction failed:', error.message);
  }
}
```

### Estimate Gas

```typescript
// Estimate gas for transaction
const gasEstimate = await signer.estimateGas({
  to: '0x...',
  value: ethers.parseEther('0.1')
});

console.log('Estimated gas:', gasEstimate.toString());

// Estimate gas for contract call
const transferGas = await tokenContract.transfer.estimateGas(
  '0x...',
  ethers.parseUnits('100', 6)
);

console.log('Transfer gas:', transferGas.toString());

// Add 10% buffer
const gasWithBuffer = (transferGas * 110n) / 100n;
```

### Using Interface for ABI Encoding/Decoding

```typescript
import { Interface } from 'ethers';

const iface = new Interface([
  'function transfer(address to, uint256 amount)'
]);

// Encode function data
const data = iface.encodeFunctionData('transfer', [
  '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0',
  ethers.parseUnits('100', 6)
]);

console.log('Encoded data:', data);
// 0xa9059cbb000000000000000000000000742d35cc...

// Decode function data
const decoded = iface.decodeFunctionData('transfer', data);
console.log('To:', decoded[0]);
console.log('Amount:', decoded[1].toString());
```

---

## 8) Real-World Examples

### Example 1: Check DAO Token Balance

```typescript
// File: frontend/src/lib/web3/contracts.ts
import { ethers, Contract } from 'ethers';
import { provider } from './config';

const DAO_TOKEN_ADDRESS = '0x...';
const DAO_TOKEN_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function decimals() view returns (uint8)',
  'function symbol() view returns (string)'
];

export async function getDaoTokenBalance(userAddress: string): Promise<string> {
  try {
    const contract = new Contract(DAO_TOKEN_ADDRESS, DAO_TOKEN_ABI, provider);

    const [balance, decimals, symbol] = await Promise.all([
      contract.balanceOf(userAddress),
      contract.decimals(),
      contract.symbol()
    ]);

    const formatted = ethers.formatUnits(balance, decimals);
    return `${formatted} ${symbol}`;
  } catch (error) {
    console.error('Error fetching balance:', error);
    return '0';
  }
}
```

### Example 2: Send Transaction with Retry

```typescript
// File: frontend/src/lib/web3/transactions.ts
import { BrowserProvider } from 'ethers';

export async function sendEthWithRetry(
  provider: BrowserProvider,
  to: string,
  amount: string,
  maxRetries: number = 3
): Promise<string> {
  const signer = await provider.getSigner();

  for (let i = 0; i < maxRetries; i++) {
    try {
      const tx = await signer.sendTransaction({
        to,
        value: ethers.parseEther(amount)
      });

      console.log(`Transaction sent: ${tx.hash} (attempt ${i + 1})`);

      const receipt = await tx.wait();

      if (receipt.status === 1) {
        console.log('Transaction successful!');
        return tx.hash;
      } else {
        throw new Error('Transaction failed');
      }
    } catch (error: any) {
      if (error.code === 'ACTION_REJECTED') {
        throw error; // Don't retry if user rejected
      }

      if (i === maxRetries - 1) {
        throw error; // Last attempt, throw error
      }

      console.log(`Attempt ${i + 1} failed, retrying...`);
      await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2s
    }
  }

  throw new Error('All retry attempts failed');
}
```

### Example 3: Listen to NFT Transfers

```typescript
// File: frontend/src/lib/web3/nftListener.ts
import { Contract } from 'ethers';
import { provider } from './config';

const NFT_ADDRESS = import.meta.env.VITE_CYBERDYNE_ACCESS_NFT_ADDRESS;
const NFT_ABI = [
  'event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)'
];

export function listenToNFTTransfers(
  userAddress: string,
  onReceived: (tokenId: bigint) => void
) {
  const contract = new Contract(NFT_ADDRESS, NFT_ABI, provider);

  // Listen for NFTs received by user
  const filter = contract.filters.Transfer(null, userAddress);

  contract.on(filter, (from, to, tokenId, event) => {
    console.log(`NFT #${tokenId} received from ${from}`);
    onReceived(tokenId);
  });

  // Return cleanup function
  return () => {
    contract.removeAllListeners(filter);
  };
}
```

### Example 4: Format Balance with Proper Decimals

```typescript
// File: frontend/src/lib/web3/formatting.ts
import { ethers } from 'ethers';

export function formatTokenBalance(
  balance: bigint,
  decimals: number,
  maxDecimals: number = 4
): string {
  const formatted = ethers.formatUnits(balance, decimals);
  const num = parseFloat(formatted);

  if (num === 0) return '0';
  if (num < 0.0001) return '< 0.0001';
  if (num < 1) return num.toFixed(maxDecimals);
  if (num < 1000) return num.toFixed(2);
  if (num < 1000000) return `${(num / 1000).toFixed(2)}K`;

  return `${(num / 1000000).toFixed(2)}M`;
}

// Usage
const balance = 1234567890000000000n; // 1.23 ETH
console.log(formatTokenBalance(balance, 18)); // "1.23"

const largeBalance = 1234567890000000000000000n; // 1,234,567 tokens
console.log(formatTokenBalance(largeBalance, 18)); // "1.23M"
```

### Example 5: Multi-call Pattern (Read Multiple Contracts)

```typescript
// File: frontend/src/lib/web3/multicall.ts
import { Contract } from 'ethers';
import { provider } from './config';

interface TokenInfo {
  address: string;
  balance: string;
  symbol: string;
  decimals: number;
}

const ERC20_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)'
];

export async function getUserTokenBalances(
  userAddress: string,
  tokenAddresses: string[]
): Promise<TokenInfo[]> {
  // Create contract instances
  const contracts = tokenAddresses.map(
    addr => new Contract(addr, ERC20_ABI, provider)
  );

  // Batch all calls
  const results = await Promise.all(
    contracts.map(async (contract, i) => {
      try {
        const [balance, symbol, decimals] = await Promise.all([
          contract.balanceOf(userAddress),
          contract.symbol(),
          contract.decimals()
        ]);

        return {
          address: tokenAddresses[i],
          balance: ethers.formatUnits(balance, decimals),
          symbol,
          decimals
        };
      } catch (error) {
        console.error(`Error fetching token ${tokenAddresses[i]}:`, error);
        return null;
      }
    })
  );

  // Filter out failed calls
  return results.filter((r): r is TokenInfo => r !== null);
}
```

### Example 6: Check if Wallet Owns NFT (Access Control)

```typescript
// File: frontend/src/lib/web3/nftAccess.ts
import { ethers, Contract } from 'ethers';
import { provider } from './config';

const NFT_ADDRESS = import.meta.env.VITE_CYBERDYNE_ACCESS_NFT_ADDRESS;

// ERC-721 NFT ABI
const NFT_ABI = [
  'function balanceOf(address owner) view returns (uint256)',
  'function ownerOf(uint256 tokenId) view returns (address)',
  'function tokenOfOwnerByIndex(address owner, uint256 index) view returns (uint256)',
  'function name() view returns (string)',
  'function symbol() view returns (string)',
  'function totalSupply() view returns (uint256)'
];

/**
 * Check if a wallet owns a specific NFT by token ID
 */
export async function ownsSpecificNFT(
  walletAddress: string,
  tokenId: bigint
): Promise<boolean> {
  try {
    const contract = new Contract(NFT_ADDRESS, NFT_ABI, provider);

    // Get the owner of this token ID
    const owner = await contract.ownerOf(tokenId);

    // Compare addresses (case-insensitive)
    return owner.toLowerCase() === walletAddress.toLowerCase();
  } catch (error: any) {
    // Token doesn't exist or contract error
    console.error('Error checking NFT ownership:', error);
    return false;
  }
}

/**
 * Check if a wallet owns ANY NFT from the collection
 * (useful for access control - does user have access?)
 */
export async function hasAccessNFT(walletAddress: string): Promise<boolean> {
  try {
    const contract = new Contract(NFT_ADDRESS, NFT_ABI, provider);

    // Get how many NFTs this wallet owns
    const balance = await contract.balanceOf(walletAddress);

    // If balance > 0, wallet has at least one NFT
    return balance > 0n;
  } catch (error) {
    console.error('Error checking NFT access:', error);
    return false;
  }
}

/**
 * Get the count of NFTs owned by a wallet
 */
export async function getNFTCount(walletAddress: string): Promise<number> {
  try {
    const contract = new Contract(NFT_ADDRESS, NFT_ABI, provider);
    const balance = await contract.balanceOf(walletAddress);

    return Number(balance);
  } catch (error) {
    console.error('Error getting NFT count:', error);
    return 0;
  }
}

/**
 * Get all NFT token IDs owned by a wallet
 * Note: This requires the contract to implement ERC-721 Enumerable extension
 */
export async function getAllOwnedTokenIds(
  walletAddress: string
): Promise<bigint[]> {
  try {
    const contract = new Contract(NFT_ADDRESS, NFT_ABI, provider);

    // Get the count of NFTs owned
    const balance = await contract.balanceOf(walletAddress);
    const count = Number(balance);

    if (count === 0) {
      return [];
    }

    // Get all token IDs by index
    const tokenIds: bigint[] = [];
    const promises = [];

    for (let i = 0; i < count; i++) {
      promises.push(contract.tokenOfOwnerByIndex(walletAddress, i));
    }

    const results = await Promise.all(promises);
    return results;
  } catch (error) {
    console.error('Error getting owned token IDs:', error);
    return [];
  }
}

/**
 * Get complete NFT access information for a wallet
 */
export async function getNFTAccessInfo(walletAddress: string) {
  try {
    const contract = new Contract(NFT_ADDRESS, NFT_ABI, provider);

    // Batch all calls
    const [balance, name, symbol] = await Promise.all([
      contract.balanceOf(walletAddress),
      contract.name(),
      contract.symbol()
    ]);

    const count = Number(balance);
    const hasAccess = count > 0;

    // Get token IDs if user has any
    let tokenIds: bigint[] = [];
    if (hasAccess) {
      const promises = [];
      for (let i = 0; i < count; i++) {
        promises.push(contract.tokenOfOwnerByIndex(walletAddress, i));
      }
      tokenIds = await Promise.all(promises);
    }

    return {
      hasAccess,
      nftCount: count,
      tokenIds,
      collectionName: name,
      collectionSymbol: symbol,
      contractAddress: NFT_ADDRESS
    };
  } catch (error) {
    console.error('Error getting NFT access info:', error);
    return {
      hasAccess: false,
      nftCount: 0,
      tokenIds: [],
      collectionName: 'Unknown',
      collectionSymbol: 'Unknown',
      contractAddress: NFT_ADDRESS
    };
  }
}
```

**Usage in Svelte Component:**

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { walletAddress } from '$lib/stores/web3Store';
  import { hasAccessNFT, getNFTAccessInfo } from '$lib/web3/nftAccess';

  let hasAccess = false;
  let nftInfo: any = null;
  let loading = true;

  async function checkAccess() {
    if (!$walletAddress) return;

    loading = true;
    try {
      // Simple check
      hasAccess = await hasAccessNFT($walletAddress);

      // Or get full info
      nftInfo = await getNFTAccessInfo($walletAddress);
      hasAccess = nftInfo.hasAccess;

      console.log('NFT Access Info:', nftInfo);
    } catch (error) {
      console.error('Error checking access:', error);
    } finally {
      loading = false;
    }
  }

  // Check when wallet connects
  $: if ($walletAddress) {
    checkAccess();
  }
</script>

{#if loading}
  <div>Checking NFT access...</div>
{:else if hasAccess}
  <div class="access-granted">
    ✅ Access Granted!
    <p>You own {nftInfo.nftCount} {nftInfo.collectionSymbol} NFT(s)</p>
    <p>Token IDs: {nftInfo.tokenIds.map(id => `#${id}`).join(', ')}</p>
  </div>
{:else}
  <div class="access-denied">
    ❌ Access Denied
    <p>You need a {nftInfo?.collectionName || 'Cyberdyne Access'} NFT to access this feature.</p>
    <a href="/marketplace">Get NFT</a>
  </div>
{/if}
```

**Alternative: Check Specific NFT Ownership:**

```typescript
// Check if user owns NFT #42
const tokenId = 42n;
const owns = await ownsSpecificNFT($walletAddress, tokenId);

if (owns) {
  console.log('User owns NFT #42');
} else {
  console.log('User does not own NFT #42');
}
```

**Performance Tip:** Cache the results and only re-check when needed:

```typescript
// File: frontend/src/lib/stores/nftAccessStore.ts
import { writable, derived } from 'svelte/store';
import { walletAddress } from './web3Store';
import { hasAccessNFT } from '$lib/web3/nftAccess';

export const nftAccessCache = writable<{
  address: string;
  hasAccess: boolean;
  timestamp: number;
} | null>(null);

// Check access with 5-minute cache
export async function checkAndCacheAccess(address: string): Promise<boolean> {
  const cached = get(nftAccessCache);
  const now = Date.now();
  const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  // Return cached result if still valid
  if (cached?.address === address && (now - cached.timestamp) < CACHE_DURATION) {
    return cached.hasAccess;
  }

  // Check on-chain
  const hasAccess = await hasAccessNFT(address);

  // Update cache
  nftAccessCache.set({
    address,
    hasAccess,
    timestamp: now
  });

  return hasAccess;
}
```

---

## 9) Migration from v5

If you're migrating from ethers v5, here are the key changes:

### BigNumber → BigInt

```typescript
// ❌ v5
import { BigNumber } from 'ethers';
const amount = BigNumber.from('1000000000000000000');

// ✅ v6
const amount = 1000000000000000000n; // Native BigInt
```

### Provider Changes

```typescript
// ❌ v5
import { ethers } from 'ethers';
const provider = new ethers.providers.Web3Provider(window.ethereum);

// ✅ v6
import { BrowserProvider } from 'ethers';
const provider = new BrowserProvider(window.ethereum);
```

### Contract Factory

```typescript
// ❌ v5
import { ContractFactory } from 'ethers';

// ✅ v6
import { ContractFactory } from 'ethers';
// Still the same, but uses BigInt internally
```

### Format Units

```typescript
// ❌ v5
import { utils } from 'ethers';
const formatted = utils.formatEther(balance);

// ✅ v6
import { formatEther } from 'ethers';
const formatted = formatEther(balance);
```

---

## 10) Best Practices

### ✅ DO

1. **Always validate addresses**
   ```typescript
   import { isAddress, getAddress } from 'ethers';

   if (!isAddress(userInput)) {
     throw new Error('Invalid address');
   }

   const checksummed = getAddress(userInput);
   ```

2. **Handle errors gracefully**
   ```typescript
   try {
     await tx.wait();
   } catch (error: any) {
     if (error.code === 'ACTION_REJECTED') {
       alert('Transaction rejected');
     } else {
       alert('Transaction failed: ' + error.message);
     }
   }
   ```

3. **Use correct decimals**
   ```typescript
   // ETH: 18 decimals
   const ethAmount = ethers.parseEther('1.5');

   // USDC: 6 decimals
   const usdcAmount = ethers.parseUnits('100', 6);
   ```

4. **Estimate gas before sending**
   ```typescript
   const gasEstimate = await contract.transfer.estimateGas(to, amount);
   const gasWithBuffer = (gasEstimate * 120n) / 100n; // Add 20%

   await contract.transfer(to, amount, { gasLimit: gasWithBuffer });
   ```

5. **Wait for confirmations**
   ```typescript
   const tx = await signer.sendTransaction({ to, value });
   await tx.wait(3); // Wait for 3 confirmations
   ```

### ❌ DON'T

1. **Don't use Number for large values**
   ```typescript
   // ❌ Bad - loses precision
   const amount = Number(balance) / 1e18;

   // ✅ Good - use formatEther
   const amount = ethers.formatEther(balance);
   ```

2. **Don't hardcode gas limits**
   ```typescript
   // ❌ Bad
   await contract.transfer(to, amount, { gasLimit: 100000 });

   // ✅ Good - estimate first
   const gas = await contract.transfer.estimateGas(to, amount);
   await contract.transfer(to, amount, { gasLimit: gas });
   ```

3. **Don't ignore transaction failures**
   ```typescript
   // ❌ Bad
   const tx = await signer.sendTransaction({ to, value });
   // Transaction might fail!

   // ✅ Good
   const tx = await signer.sendTransaction({ to, value });
   const receipt = await tx.wait();
   if (receipt.status !== 1) {
     throw new Error('Transaction failed');
   }
   ```

4. **Don't expose private keys**
   ```typescript
   // ❌ NEVER do this
   const wallet = new ethers.Wallet('0xPRIVATE_KEY', provider);

   // ✅ Use wallet providers (MetaMask, Web3Auth)
   const provider = new BrowserProvider(window.ethereum);
   const signer = await provider.getSigner();
   ```

---

## Summary

You now have a comprehensive guide to ethers.js v6!

### Key Takeaways:

- **Providers** for reading blockchain data (read-only)
- **Signers** for signing and sending transactions (write)
- **Contracts** for interacting with smart contracts
- **BigInt** instead of BigNumber (native JavaScript)
- **parseEther/formatEther** for unit conversion
- **Error handling** is critical for good UX
- **Estimate gas** before transactions
- **Wait for confirmations** for security

### Next Steps:

1. Explore the [official ethers.js v6 docs](https://docs.ethers.org/v6/)
2. Check out the [Base network documentation](https://docs.base.org)
3. Build your first contract interaction in your DAO app
4. Test on Base Sepolia testnet first

---

**Questions?** Refer to the official docs or check the examples in `frontend/src/lib/web3/`.
