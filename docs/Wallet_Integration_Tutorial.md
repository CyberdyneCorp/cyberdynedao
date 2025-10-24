# Wallet Integration Tutorial: WalletConnect & Web3Auth with Svelte

**Version:** 1.0
**Target Stack:** SvelteKit + Tailwind + Ethers.js v6
**Target Network:** Base (8453) & Base Sepolia (84532)

---

## Table of Contents

1. [Introduction to Web3 Wallets](#1-introduction-to-web3-wallets)
2. [How Wallets Work in Dapps](#2-how-wallets-work-in-dapps)
3. [Installation Guide](#3-installation-guide)
4. [Project Setup](#4-project-setup)
5. [WalletConnect (Reown AppKit) Implementation](#5-walletconnect-reown-appkit-implementation)
6. [Web3Auth Implementation](#6-web3auth-implementation)
7. [Complete Integration Example](#7-complete-integration-example)
8. [Best Practices & Security](#8-best-practices--security)
9. [Troubleshooting](#9-troubleshooting)

---

## 1) Introduction to Web3 Wallets

### What is a Web3 Wallet?

A Web3 wallet is a software application that allows users to:
- **Store and manage cryptocurrency** (Ethereum, tokens, NFTs)
- **Sign transactions** without exposing private keys
- **Authenticate identity** on decentralized applications (Dapps)
- **Interact with blockchain networks** securely

### Types of Wallets

**Browser Extension Wallets:**
- MetaMask, Coinbase Wallet, Rainbow
- Inject `window.ethereum` provider
- Desktop/browser-based

**Mobile Wallets:**
- MetaMask Mobile, Trust Wallet, Rainbow
- Connected via WalletConnect protocol
- Scan QR code to connect

**Embedded/Social Wallets:**
- Web3Auth, Magic, Privy
- Email/social login
- Non-custodial but easier onboarding

### Key Concepts

**Private Key:** Secret cryptographic key that proves ownership (never share!)

**Public Address:** Your wallet's identifier (like an account number): `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`

**Signing:** Creating a cryptographic proof using your private key to authorize actions

**Provider:** JavaScript object that communicates with blockchain (reads data, sends transactions)

**Signer:** Extension of provider that can sign transactions with your wallet

---

## 2) How Wallets Work in Dapps

### The Connection Flow

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   User      │────────▶│  Dapp (UI)   │────────▶│   Wallet    │
│  (Browser)  │  Click  │  (SvelteKit) │ Request │ (MetaMask/  │
│             │ Connect │              │  Auth   │  Mobile)    │
└─────────────┘         └──────────────┘         └─────────────┘
                               │                        │
                               │◀───────────────────────┘
                               │    Approve & Sign
                               │
                               ▼
                        ┌──────────────┐
                        │  Blockchain  │
                        │    (Base)    │
                        └──────────────┘
```

### What Happens When You Connect

1. **User clicks "Connect Wallet"** in your Dapp
2. **Connection request** is sent to wallet (via injected provider or WalletConnect bridge)
3. **User approves** the connection in their wallet
4. **Wallet returns** the user's public address and chain ID
5. **Dapp stores** this information (usually in a Svelte store)
6. **User is authenticated** - can now sign messages and send transactions

### Common Wallet Operations

**Read-Only Operations** (no signature needed):
- View wallet balance
- Check token holdings
- Read smart contract data
- Query transaction history

**Write Operations** (signature required):
- Send transactions (transfer tokens)
- Call smart contract functions that modify state
- Sign messages for authentication
- Approve token spending

### Why Multiple Wallet Options?

Different users prefer different wallets:
- **Desktop users:** Often use MetaMask extension
- **Mobile users:** Need WalletConnect for mobile wallet apps
- **New users:** Prefer Web3Auth for familiar email/social login
- **Privacy-focused:** Use hardware wallets via WalletConnect

By supporting both **WalletConnect** and **Web3Auth**, you cover all user types.

---

## 3) Installation Guide

### Prerequisites

```bash
# Initialize SvelteKit project
npm create svelte@latest cyberdyne-dao
cd cyberdyne-dao

# Select: Skeleton project, TypeScript, ESLint, Prettier
```

### Core Dependencies

```bash
# Install core Web3 libraries
npm install ethers@6

# Install WalletConnect AppKit (Reown)
npm install @reown/appkit @reown/appkit-adapter-ethers

# Install Web3Auth
npm install @web3auth/modal @web3auth/base @web3auth/ethereum-provider

# Install UI dependencies
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Development Dependencies

```bash
# Optional: Type definitions
npm install -D @types/node

# Optional: Icons
npm install lucide-svelte
```

### Configure for Static Build

```bash
# Install static adapter
npm install -D @sveltejs/adapter-static
```

**svelte.config.js:**
```js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: 'index.html',
      precompress: false,
      strict: true
    }),
    trailingSlash: 'always',
    prerender: {
      handleHttpError: 'warn'
    }
  }
};

export default config;
```

### Environment Variables

Create `.env` file:
```bash
# Public variables (embedded in static build)
PUBLIC_WALLETCONNECT_PROJECT_ID=your_project_id_here
PUBLIC_WEB3AUTH_CLIENT_ID=your_client_id_here
PUBLIC_RPC_BASE=https://mainnet.base.org
PUBLIC_RPC_BASE_SEPOLIA=https://sepolia.base.org
PUBLIC_CHAIN_ID=8453
```

**Get your credentials:**
- WalletConnect: [https://cloud.reown.com](https://cloud.reown.com) (formerly WalletConnect Cloud)
- Web3Auth: [https://dashboard.web3auth.io](https://dashboard.web3auth.io)

---

## 4) Project Setup

### Directory Structure

```
src/
├── lib/
│   ├── web3/
│   │   ├── chains.ts          # Chain configurations
│   │   ├── provider.ts        # Ethers.js provider utilities
│   │   ├── walletconnect.ts   # WalletConnect setup
│   │   ├── web3auth.ts        # Web3Auth setup
│   │   └── wallet.ts          # Unified wallet interface
│   ├── stores/
│   │   └── wallet.ts          # Svelte wallet store
│   └── components/
│       └── wallet/
│           ├── ConnectButton.svelte
│           ├── AccountMenu.svelte
│           └── NetworkBadge.svelte
├── routes/
│   ├── +layout.svelte
│   ├── +layout.ts
│   └── +page.svelte
```

### Chain Configuration

**src/lib/web3/chains.ts:**
```typescript
import { env } from '$env/dynamic/public';

export const CHAINS = {
  base: {
    id: 8453,
    name: 'Base',
    network: 'base',
    nativeCurrency: {
      name: 'Ethereum',
      symbol: 'ETH',
      decimals: 18
    },
    rpcUrls: {
      default: { http: [env.PUBLIC_RPC_BASE || 'https://mainnet.base.org'] },
      public: { http: ['https://mainnet.base.org'] }
    },
    blockExplorers: {
      default: { name: 'BaseScan', url: 'https://basescan.org' }
    }
  },
  baseSepolia: {
    id: 84532,
    name: 'Base Sepolia',
    network: 'base-sepolia',
    nativeCurrency: {
      name: 'Ethereum',
      symbol: 'ETH',
      decimals: 18
    },
    rpcUrls: {
      default: { http: [env.PUBLIC_RPC_BASE_SEPOLIA || 'https://sepolia.base.org'] },
      public: { http: ['https://sepolia.base.org'] }
    },
    blockExplorers: {
      default: { name: 'BaseScan', url: 'https://sepolia.basescan.org' }
    },
    testnet: true
  }
} as const;

export type ChainId = keyof typeof CHAINS;
export const DEFAULT_CHAIN = CHAINS.base;
```

### Ethers.js Provider Utilities

**src/lib/web3/provider.ts:**
```typescript
import { BrowserProvider, JsonRpcProvider } from 'ethers';
import type { Eip1193Provider } from 'ethers';

/**
 * Create a JSON-RPC provider for read-only operations
 */
export function createJsonProvider(rpcUrl: string): JsonRpcProvider {
  return new JsonRpcProvider(rpcUrl);
}

/**
 * Create a browser provider from an EIP-1193 compatible wallet
 */
export function createBrowserProvider(provider: Eip1193Provider): BrowserProvider {
  return new BrowserProvider(provider);
}

/**
 * Get a signer from a browser provider for signing transactions
 */
export async function getSigner(provider: BrowserProvider) {
  return await provider.getSigner();
}

/**
 * Check if the current network matches expected chain ID
 */
export async function checkNetwork(
  provider: BrowserProvider,
  expectedChainId: number
): Promise<boolean> {
  const network = await provider.getNetwork();
  return Number(network.chainId) === expectedChainId;
}

/**
 * Request network switch
 */
export async function switchNetwork(
  provider: Eip1193Provider,
  chainId: number
): Promise<void> {
  try {
    await provider.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: `0x${chainId.toString(16)}` }]
    });
  } catch (error: any) {
    // Chain not added, try adding it
    if (error.code === 4902) {
      throw new Error('Please add this network to your wallet first');
    }
    throw error;
  }
}
```

### Wallet Store

**src/lib/stores/wallet.ts:**
```typescript
import { writable, derived } from 'svelte/store';
import type { BrowserProvider } from 'ethers';

export type WalletConnector = 'walletconnect' | 'web3auth' | null;

export interface WalletState {
  address?: string;
  chainId?: number;
  connector?: WalletConnector;
  provider?: BrowserProvider;
  isConnecting?: boolean;
  error?: string;
}

// Create writable wallet store
export const wallet = writable<WalletState>({});

// Derived stores for convenience
export const isConnected = derived(wallet, ($wallet) => !!$wallet.address);
export const walletAddress = derived(wallet, ($wallet) => $wallet.address);
export const currentChainId = derived(wallet, ($wallet) => $wallet.chainId);

// Helper to update wallet state
export function updateWallet(updates: Partial<WalletState>) {
  wallet.update((state) => ({ ...state, ...updates }));
}

// Helper to reset wallet state
export function resetWallet() {
  wallet.set({});
}

// Persist to localStorage
if (typeof window !== 'undefined') {
  const stored = localStorage.getItem('wallet');
  if (stored) {
    try {
      const parsed = JSON.parse(stored);
      // Only restore address and connector, not provider
      wallet.set({
        address: parsed.address,
        chainId: parsed.chainId,
        connector: parsed.connector
      });
    } catch (e) {
      console.error('Failed to parse stored wallet', e);
    }
  }

  wallet.subscribe((state) => {
    if (state.address) {
      localStorage.setItem(
        'wallet',
        JSON.stringify({
          address: state.address,
          chainId: state.chainId,
          connector: state.connector
        })
      );
    } else {
      localStorage.removeItem('wallet');
    }
  });
}
```

---

## 5) WalletConnect (Reown AppKit) Implementation

### Setup WalletConnect

**src/lib/web3/walletconnect.ts:**
```typescript
import { createAppKit } from '@reown/appkit';
import { EthersAdapter } from '@reown/appkit-adapter-ethers';
import { env } from '$env/dynamic/public';
import { CHAINS } from './chains';
import { updateWallet, resetWallet } from '$lib/stores/wallet';
import { createBrowserProvider } from './provider';

let appKit: ReturnType<typeof createAppKit> | null = null;

/**
 * Initialize WalletConnect AppKit
 */
export function initWalletConnect() {
  if (appKit) return appKit;

  const projectId = env.PUBLIC_WALLETCONNECT_PROJECT_ID;
  if (!projectId) {
    throw new Error('WalletConnect Project ID not configured');
  }

  // Configure chains
  const chains = [CHAINS.base, CHAINS.baseSepolia];

  // Create Ethers adapter
  const ethersAdapter = new EthersAdapter();

  // Initialize AppKit
  appKit = createAppKit({
    adapters: [ethersAdapter],
    networks: chains,
    projectId,
    features: {
      analytics: true,
      email: false,
      socials: false
    },
    themeMode: 'dark',
    themeVariables: {
      '--w3m-accent': '#2D7CFF'
    }
  });

  // Listen to connection events
  appKit.subscribeProvider((state) => {
    if (state.isConnected && state.address) {
      const provider = createBrowserProvider(state.provider);
      updateWallet({
        address: state.address,
        chainId: state.chainId,
        connector: 'walletconnect',
        provider,
        isConnecting: false
      });
    } else {
      resetWallet();
    }
  });

  return appKit;
}

/**
 * Connect via WalletConnect
 */
export async function connectWalletConnect() {
  try {
    updateWallet({ isConnecting: true, error: undefined });

    const modal = initWalletConnect();
    await modal.open();

    // Modal handles connection state
  } catch (error: any) {
    updateWallet({
      error: error.message || 'Failed to connect',
      isConnecting: false
    });
    throw error;
  }
}

/**
 * Disconnect WalletConnect
 */
export async function disconnectWalletConnect() {
  if (appKit) {
    await appKit.disconnect();
  }
  resetWallet();
}

/**
 * Get current WalletConnect provider
 */
export function getWalletConnectProvider() {
  return appKit?.getWalletProvider();
}
```

### Usage Example

```typescript
import { connectWalletConnect, disconnectWalletConnect } from '$lib/web3/walletconnect';
import { wallet } from '$lib/stores/wallet';

// Connect
await connectWalletConnect();

// Access wallet state
$wallet.address // "0x..."
$wallet.chainId // 8453
$wallet.provider // BrowserProvider instance

// Disconnect
await disconnectWalletConnect();
```

---

## 6) Web3Auth Implementation

### Setup Web3Auth

**src/lib/web3/web3auth.ts:**
```typescript
import { Web3Auth } from '@web3auth/modal';
import { CHAIN_NAMESPACES, WEB3AUTH_NETWORK } from '@web3auth/base';
import { EthereumPrivateKeyProvider } from '@web3auth/ethereum-provider';
import { env } from '$env/dynamic/public';
import { CHAINS, DEFAULT_CHAIN } from './chains';
import { updateWallet, resetWallet } from '$lib/stores/wallet';
import { createBrowserProvider } from './provider';

let web3auth: Web3Auth | null = null;

/**
 * Initialize Web3Auth
 */
export async function initWeb3Auth() {
  if (web3auth) return web3auth;

  const clientId = env.PUBLIC_WEB3AUTH_CLIENT_ID;
  if (!clientId) {
    throw new Error('Web3Auth Client ID not configured');
  }

  // Configure chain
  const chainConfig = {
    chainNamespace: CHAIN_NAMESPACES.EIP155,
    chainId: `0x${DEFAULT_CHAIN.id.toString(16)}`,
    rpcTarget: DEFAULT_CHAIN.rpcUrls.default.http[0],
    displayName: DEFAULT_CHAIN.name,
    blockExplorerUrl: DEFAULT_CHAIN.blockExplorers.default.url,
    ticker: DEFAULT_CHAIN.nativeCurrency.symbol,
    tickerName: DEFAULT_CHAIN.nativeCurrency.name,
    logo: 'https://cryptologos.cc/logos/ethereum-eth-logo.png'
  };

  // Create private key provider
  const privateKeyProvider = new EthereumPrivateKeyProvider({
    config: { chainConfig }
  });

  // Initialize Web3Auth
  web3auth = new Web3Auth({
    clientId,
    web3AuthNetwork: WEB3AUTH_NETWORK.SAPPHIRE_MAINNET,
    privateKeyProvider,
    chainConfig,
    uiConfig: {
      appName: 'Cyberdyne DAO',
      mode: 'dark',
      loginMethodsOrder: ['google', 'github', 'twitter', 'discord'],
      defaultLanguage: 'en',
      theme: {
        primary: '#2D7CFF'
      }
    }
  });

  await web3auth.initModal();

  return web3auth;
}

/**
 * Connect via Web3Auth
 */
export async function connectWeb3Auth() {
  try {
    updateWallet({ isConnecting: true, error: undefined });

    const web3authInstance = await initWeb3Auth();
    const provider = await web3authInstance.connect();

    if (!provider) {
      throw new Error('Failed to connect');
    }

    // Get user info
    const user = await web3authInstance.getUserInfo();

    // Create Ethers provider
    const ethersProvider = createBrowserProvider(provider);
    const signer = await ethersProvider.getSigner();
    const address = await signer.getAddress();
    const network = await ethersProvider.getNetwork();

    updateWallet({
      address,
      chainId: Number(network.chainId),
      connector: 'web3auth',
      provider: ethersProvider,
      isConnecting: false
    });

    return { address, user };
  } catch (error: any) {
    console.error('Web3Auth connection failed:', error);
    updateWallet({
      error: error.message || 'Failed to connect',
      isConnecting: false
    });
    throw error;
  }
}

/**
 * Disconnect Web3Auth
 */
export async function disconnectWeb3Auth() {
  if (web3auth) {
    await web3auth.logout();
  }
  resetWallet();
}

/**
 * Get current Web3Auth provider
 */
export function getWeb3AuthProvider() {
  return web3auth?.provider;
}

/**
 * Check if Web3Auth is connected
 */
export function isWeb3AuthConnected(): boolean {
  return web3auth?.connected ?? false;
}
```

### Usage Example

```typescript
import { connectWeb3Auth, disconnectWeb3Auth } from '$lib/web3/web3auth';
import { wallet } from '$lib/stores/wallet';

// Connect
const { address, user } = await connectWeb3Auth();
console.log('Connected:', address);
console.log('User:', user.email); // from social login

// Access wallet state
$wallet.address // "0x..."
$wallet.provider // BrowserProvider instance

// Disconnect
await disconnectWeb3Auth();
```

---

## 7) Complete Integration Example

### Unified Wallet Interface

**src/lib/web3/wallet.ts:**
```typescript
import { get } from 'svelte/store';
import { wallet, resetWallet } from '$lib/stores/wallet';
import { connectWalletConnect, disconnectWalletConnect } from './walletconnect';
import { connectWeb3Auth, disconnectWeb3Auth } from './web3auth';
import { switchNetwork, checkNetwork } from './provider';
import { DEFAULT_CHAIN } from './chains';

/**
 * Connect wallet with specified method
 */
export async function connect(method: 'walletconnect' | 'web3auth') {
  switch (method) {
    case 'walletconnect':
      return await connectWalletConnect();
    case 'web3auth':
      return await connectWeb3Auth();
    default:
      throw new Error(`Unknown wallet method: ${method}`);
  }
}

/**
 * Disconnect current wallet
 */
export async function disconnect() {
  const currentWallet = get(wallet);

  switch (currentWallet.connector) {
    case 'walletconnect':
      await disconnectWalletConnect();
      break;
    case 'web3auth':
      await disconnectWeb3Auth();
      break;
  }

  resetWallet();
}

/**
 * Ensure user is on correct network
 */
export async function ensureNetwork() {
  const currentWallet = get(wallet);

  if (!currentWallet.provider) {
    throw new Error('No provider connected');
  }

  const isCorrect = await checkNetwork(currentWallet.provider, DEFAULT_CHAIN.id);

  if (!isCorrect) {
    const ethereumProvider =
      currentWallet.connector === 'walletconnect'
        ? await import('./walletconnect').then((m) => m.getWalletConnectProvider())
        : await import('./web3auth').then((m) => m.getWeb3AuthProvider());

    if (ethereumProvider) {
      await switchNetwork(ethereumProvider, DEFAULT_CHAIN.id);
    }
  }
}

/**
 * Sign a message
 */
export async function signMessage(message: string): Promise<string> {
  const currentWallet = get(wallet);

  if (!currentWallet.provider) {
    throw new Error('No wallet connected');
  }

  const signer = await currentWallet.provider.getSigner();
  return await signer.signMessage(message);
}

/**
 * Send a transaction
 */
export async function sendTransaction(tx: {
  to: string;
  value?: bigint;
  data?: string;
}) {
  const currentWallet = get(wallet);

  if (!currentWallet.provider) {
    throw new Error('No wallet connected');
  }

  await ensureNetwork();

  const signer = await currentWallet.provider.getSigner();
  const transaction = await signer.sendTransaction(tx);
  return await transaction.wait();
}
```

### Connect Button Component

**src/lib/components/wallet/ConnectButton.svelte:**
```svelte
<script lang="ts">
  import { wallet, isConnected } from '$lib/stores/wallet';
  import { connect, disconnect } from '$lib/web3/wallet';
  import { Wallet, ChevronDown } from 'lucide-svelte';

  let showDropdown = false;
  let isLoading = false;
  let error = '';

  async function handleConnect(method: 'walletconnect' | 'web3auth') {
    try {
      isLoading = true;
      error = '';
      await connect(method);
      showDropdown = false;
    } catch (e: any) {
      error = e.message;
    } finally {
      isLoading = false;
    }
  }

  async function handleDisconnect() {
    try {
      await disconnect();
    } catch (e: any) {
      error = e.message;
    }
  }

  function formatAddress(addr: string): string {
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
  }
</script>

{#if !$isConnected}
  <div class="relative">
    <button
      on:click={() => (showDropdown = !showDropdown)}
      disabled={isLoading}
      class="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-white hover:shadow-glowPrimary transition disabled:opacity-50"
    >
      <Wallet size={20} />
      <span>{isLoading ? 'Connecting...' : 'Connect Wallet'}</span>
      <ChevronDown size={16} />
    </button>

    {#if showDropdown}
      <div
        class="absolute right-0 mt-2 w-64 rounded-xl bg-surface border border-border shadow-brand overflow-hidden z-50"
      >
        <button
          on:click={() => handleConnect('walletconnect')}
          disabled={isLoading}
          class="w-full px-4 py-3 text-left hover:bg-surface-2 transition flex items-center gap-3"
        >
          <div class="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
            <Wallet size={18} class="text-primary" />
          </div>
          <div>
            <div class="font-medium text-text">WalletConnect</div>
            <div class="text-sm text-muted">MetaMask, Rainbow, Trust</div>
          </div>
        </button>

        <button
          on:click={() => handleConnect('web3auth')}
          disabled={isLoading}
          class="w-full px-4 py-3 text-left hover:bg-surface-2 transition flex items-center gap-3 border-t border-border"
        >
          <div class="w-8 h-8 rounded-lg bg-accent/20 flex items-center justify-center">
            <Wallet size={18} class="text-accent" />
          </div>
          <div>
            <div class="font-medium text-text">Web3Auth</div>
            <div class="text-sm text-muted">Email, Google, Social</div>
          </div>
        </button>
      </div>
    {/if}

    {#if error}
      <div class="absolute right-0 mt-2 w-64 px-4 py-2 rounded-lg bg-error/10 border border-error text-error text-sm">
        {error}
      </div>
    {/if}
  </div>
{:else}
  <div class="flex items-center gap-2">
    <div class="px-4 py-2 rounded-xl bg-surface-2 border border-border">
      <span class="font-mono text-sm text-text">{formatAddress($wallet.address || '')}</span>
    </div>
    <button
      on:click={handleDisconnect}
      class="px-4 py-2 rounded-xl border border-border text-text/90 hover:bg-surface-2 transition"
    >
      Disconnect
    </button>
  </div>
{/if}

<style>
  /* Ensure dropdown is positioned correctly */
  .relative {
    position: relative;
  }
</style>
```

### Network Badge Component

**src/lib/components/wallet/NetworkBadge.svelte:**
```svelte
<script lang="ts">
  import { wallet } from '$lib/stores/wallet';
  import { CHAINS } from '$lib/web3/chains';
  import { AlertCircle, CheckCircle } from 'lucide-svelte';

  $: chain = $wallet.chainId
    ? Object.values(CHAINS).find((c) => c.id === $wallet.chainId)
    : null;
  $: isCorrectNetwork = $wallet.chainId === CHAINS.base.id;
</script>

{#if $wallet.chainId && chain}
  <div
    class="flex items-center gap-2 px-3 py-1.5 rounded-lg {isCorrectNetwork
      ? 'bg-success/10 border border-success/30'
      : 'bg-warning/10 border border-warning/30'}"
  >
    {#if isCorrectNetwork}
      <CheckCircle size={14} class="text-success" />
    {:else}
      <AlertCircle size={14} class="text-warning" />
    {/if}
    <span class="text-sm font-medium" class:text-success={isCorrectNetwork} class:text-warning={!isCorrectNetwork}>
      {chain.name}
    </span>
  </div>
{/if}
```

### Layout Integration

**src/routes/+layout.svelte:**
```svelte
<script lang="ts">
  import '../app.css';
  import ConnectButton from '$lib/components/wallet/ConnectButton.svelte';
  import NetworkBadge from '$lib/components/wallet/NetworkBadge.svelte';
  import { onMount } from 'svelte';
  import { wallet } from '$lib/stores/wallet';
  import { initWalletConnect } from '$lib/web3/walletconnect';
  import { initWeb3Auth } from '$lib/web3/web3auth';

  // Initialize wallet connections on mount
  onMount(async () => {
    // Initialize based on stored connector
    if ($wallet.connector === 'walletconnect') {
      try {
        initWalletConnect();
      } catch (e) {
        console.error('Failed to reconnect WalletConnect:', e);
      }
    } else if ($wallet.connector === 'web3auth') {
      try {
        await initWeb3Auth();
      } catch (e) {
        console.error('Failed to reconnect Web3Auth:', e);
      }
    }
  });
</script>

<div class="min-h-screen bg-bg text-text">
  <header class="border-b border-border/50 bg-surface/50 backdrop-blur-sm sticky top-0 z-40">
    <div class="container mx-auto px-4 py-4 flex items-center justify-between">
      <div class="flex items-center gap-8">
        <a href="/" class="text-xl font-bold">
          <span class="text-primary">Cyberdyne</span> DAO
        </a>
        <nav class="hidden md:flex items-center gap-6">
          <a href="/products" class="text-muted hover:text-text transition">Products</a>
          <a href="/marketplace" class="text-muted hover:text-text transition">Marketplace</a>
          <a href="/treasury" class="text-muted hover:text-text transition">Treasury</a>
          <a href="/governance" class="text-muted hover:text-text transition">Governance</a>
        </nav>
      </div>

      <div class="flex items-center gap-3">
        <NetworkBadge />
        <ConnectButton />
      </div>
    </div>
  </header>

  <main>
    <slot />
  </main>
</div>
```

**src/routes/+layout.ts:**
```typescript
export const prerender = true;
export const ssr = false;
```

### Example Page Using Wallet

**src/routes/treasury/+page.svelte:**
```svelte
<script lang="ts">
  import { wallet, isConnected } from '$lib/stores/wallet';
  import { Contract } from 'ethers';
  import { onMount } from 'svelte';
  import { CHAINS } from '$lib/web3/chains';

  let balance = '0';
  let loading = true;

  const ERC20_ABI = [
    'function balanceOf(address) view returns (uint256)',
    'function decimals() view returns (uint8)',
    'function symbol() view returns (string)'
  ];

  async function loadBalance() {
    if (!$wallet.provider || !$wallet.address) return;

    try {
      loading = true;

      // Get native ETH balance
      const ethBalance = await $wallet.provider.getBalance($wallet.address);
      balance = (Number(ethBalance) / 1e18).toFixed(4);

      // Optional: Load ERC-20 balances
      // const usdcAddress = '0x...';
      // const usdc = new Contract(usdcAddress, ERC20_ABI, $wallet.provider);
      // const usdcBalance = await usdc.balanceOf($wallet.address);

    } catch (error) {
      console.error('Failed to load balance:', error);
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    if ($isConnected) {
      loadBalance();
    }
  });

  // Reload when wallet changes
  $: if ($wallet.address) {
    loadBalance();
  }
</script>

<div class="container mx-auto px-4 py-12">
  <h1 class="text-4xl font-bold mb-8">Treasury Dashboard</h1>

  {#if !$isConnected}
    <div class="rounded-2xl bg-surface border border-border p-8 text-center">
      <p class="text-muted mb-4">Connect your wallet to view treasury data</p>
    </div>
  {:else if loading}
    <div class="rounded-2xl bg-surface border border-border p-8">
      <div class="animate-pulse">Loading...</div>
    </div>
  {:else}
    <div class="rounded-2xl bg-surface border border-border p-8">
      <h2 class="text-2xl font-semibold mb-4">Your Balance</h2>
      <div class="flex items-baseline gap-2">
        <span class="text-4xl font-bold text-primary">{balance}</span>
        <span class="text-xl text-muted">ETH</span>
      </div>
      <p class="text-sm text-muted mt-2">on {CHAINS.base.name}</p>
    </div>
  {/if}
</div>
```

---

## 8) Best Practices & Security

### Security Guidelines

**Never expose private keys:**
```typescript
// ❌ NEVER do this
const privateKey = "0x...";

// ✅ Always use wallet providers
const signer = await provider.getSigner();
```

**Validate addresses:**
```typescript
import { isAddress, getAddress } from 'ethers';

function validateAddress(addr: string): boolean {
  return isAddress(addr);
}

// Always checksum addresses
const checksummed = getAddress(userInput);
```

**Verify network before transactions:**
```typescript
import { ensureNetwork } from '$lib/web3/wallet';

async function sendTokens(to: string, amount: bigint) {
  await ensureNetwork(); // Ensure user on Base
  // ... send transaction
}
```

**Handle errors gracefully:**
```typescript
try {
  await sendTransaction({ to, value });
} catch (error: any) {
  if (error.code === 'ACTION_REJECTED') {
    toast.error('Transaction rejected by user');
  } else if (error.code === 'INSUFFICIENT_FUNDS') {
    toast.error('Insufficient funds');
  } else {
    toast.error('Transaction failed');
  }
}
```

### Performance Tips

**Lazy load wallet libraries:**
```typescript
// Only load when needed
async function connectWallet() {
  const { connectWalletConnect } = await import('$lib/web3/walletconnect');
  await connectWalletConnect();
}
```

**Cache provider instances:**
```typescript
let cachedProvider: BrowserProvider | null = null;

export function getProvider(): BrowserProvider {
  if (!cachedProvider) {
    cachedProvider = createBrowserProvider(window.ethereum);
  }
  return cachedProvider;
}
```

**Use multicall for batch reads:**
```typescript
// Instead of multiple calls
const balance1 = await token1.balanceOf(address);
const balance2 = await token2.balanceOf(address);

// Use Promise.all
const [balance1, balance2] = await Promise.all([
  token1.balanceOf(address),
  token2.balanceOf(address)
]);
```

### UX Best Practices

**Show loading states:**
```svelte
{#if $wallet.isConnecting}
  <div class="animate-pulse">Connecting...</div>
{/if}
```

**Provide helpful error messages:**
```typescript
const ERROR_MESSAGES = {
  'user rejected': 'You declined the connection request',
  'already pending': 'Please check your wallet for a pending request',
  'network mismatch': 'Please switch to Base network'
};
```

**Auto-reconnect on page load:**
```typescript
onMount(async () => {
  const stored = localStorage.getItem('wallet');
  if (stored) {
    await reconnect();
  }
});
```

---

## 9) Troubleshooting

### Common Issues

**WalletConnect QR not showing:**
```typescript
// Ensure modal is initialized before opening
await initWalletConnect();
await modal.open();
```

**Web3Auth popup blocked:**
```typescript
// Open immediately on user click (not in async callback)
button.onclick = () => connectWeb3Auth();
```

**Wrong network after connecting:**
```typescript
// Always check and prompt switch
await ensureNetwork();
```

**Provider not defined:**
```typescript
// Check for window.ethereum
if (typeof window !== 'undefined' && window.ethereum) {
  // Safe to use
}
```

**Transaction fails with "nonce too high":**
```typescript
// Reset nonce by reconnecting wallet
await disconnect();
await connect('walletconnect');
```

### Debugging Tips

**Log provider events:**
```typescript
provider.on('accountsChanged', (accounts) => {
  console.log('Accounts changed:', accounts);
});

provider.on('chainChanged', (chainId) => {
  console.log('Chain changed:', chainId);
});

provider.on('disconnect', () => {
  console.log('Provider disconnected');
});
```

**Check network status:**
```typescript
const network = await provider.getNetwork();
console.log('Connected to:', network.name, network.chainId);
```

**Inspect transactions:**
```typescript
const tx = await signer.sendTransaction({ to, value });
console.log('TX sent:', tx.hash);
const receipt = await tx.wait();
console.log('TX mined:', receipt.status); // 1 = success
```

### Testing Locally

**Use Base Sepolia testnet:**
```bash
# Set testnet in .env
PUBLIC_CHAIN_ID=84532
PUBLIC_RPC_BASE_SEPOLIA=https://sepolia.base.org
```

**Get testnet ETH:**
- Base Sepolia Faucet: https://www.coinbase.com/faucets/base-ethereum-goerli-faucet
- Bridge from Sepolia: https://bridge.base.org

---

## Conclusion

You now have a complete wallet integration setup with:

✅ **WalletConnect** for desktop/mobile wallet support
✅ **Web3Auth** for social login onboarding
✅ **Ethers.js v6** for blockchain interactions
✅ **Base Network** configuration
✅ **Svelte stores** for state management
✅ **Reusable components** for UI
✅ **Security best practices** built-in

### Next Steps

1. **Test both wallet connectors** on desktop and mobile
2. **Add transaction signing** for your specific use case
3. **Implement smart contract interactions** (ERC-20, NFTs, etc.)
4. **Add analytics** to track wallet connections
5. **Build treasury dashboard** reading on-chain data
6. **Deploy to IPFS** with static build

### Resources

- **WalletConnect (Reown):** https://docs.reown.com
- **Web3Auth:** https://web3auth.io/docs
- **Ethers.js:** https://docs.ethers.org/v6
- **Base Network:** https://docs.base.org
- **SvelteKit:** https://kit.svelte.dev

---

**Questions?** Check the troubleshooting section or open an issue in the project repository.
