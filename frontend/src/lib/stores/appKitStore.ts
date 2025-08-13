/**
 * Reown AppKit Store - Manages WalletConnect state and actions
 * 
 * This store manages the state for Reown AppKit (WalletConnect) integration:
 * - AppKit instance and initialization status
 * - Connection state and wallet information
 * - Loading states and error handling
 * - Actions for connecting/disconnecting wallets
 */

import { writable, derived } from 'svelte/store'
import type { AppKit } from '@reown/appkit'

// WalletConnect wallet information interface
export interface WalletInfo {
  isConnected: boolean
  address?: string
  chainId?: number
  balance?: string
}

// AppKit store state interface
interface AppKitState {
  initialized: boolean
  loading: boolean
  error: string | null
  walletInfo: WalletInfo
  chainId: number | null
}

// Initial state
const initialState: AppKitState = {
  initialized: false,
  loading: false,
  error: null,
  walletInfo: {
    isConnected: false,
    address: undefined,
    chainId: undefined,
    balance: undefined
  },
  chainId: null
}

// Main AppKit store
export const appKitStore = writable<AppKitState>(initialState)

// Separate AppKit instance store (as expected by the service)
export const appKitInstance = writable<AppKit | null>(null)

// Derived stores for convenient access
export const isAppKitInitialized = derived(appKitStore, $store => $store.initialized)
export const isAppKitLoading = derived(appKitStore, $store => $store.loading)
export const appKitError = derived(appKitStore, $store => $store.error)
export const walletInfo = derived(appKitStore, $store => $store.walletInfo)
export const isWalletConnected = derived(walletInfo, $walletInfo => $walletInfo.isConnected)
export const connectedAddress = derived(walletInfo, $walletInfo => $walletInfo.address)
export const connectedChainId = derived(walletInfo, $walletInfo => $walletInfo.chainId)
export const walletBalance = derived(walletInfo, $walletInfo => $walletInfo.balance)

// Store actions
export const appKitActions = {
  // Set initialization status
  setInitialized: (initialized: boolean) => {
    appKitStore.update(state => ({
      ...state,
      initialized
    }))
  },

  // Set loading state
  setLoading: (loading: boolean) => {
    appKitStore.update(state => ({
      ...state,
      loading
    }))
  },

  // Set error message
  setError: (error: string) => {
    appKitStore.update(state => ({
      ...state,
      error
    }))
  },

  // Clear error
  clearError: () => {
    appKitStore.update(state => ({
      ...state,
      error: null
    }))
  },

  // Set wallet information
  setWalletInfo: (walletInfo: WalletInfo) => {
    appKitStore.update(state => ({
      ...state,
      walletInfo
    }))
  },

  // Set chain ID
  setChainId: (chainId: number) => {
    appKitStore.update(state => ({
      ...state,
      chainId,
      walletInfo: {
        ...state.walletInfo,
        chainId
      }
    }))
  },

  // Set disconnected state
  setDisconnected: () => {
    appKitStore.update(state => ({
      ...state,
      walletInfo: {
        isConnected: false,
        address: undefined,
        chainId: undefined,
        balance: undefined
      }
    }))
  },

  // Reset store to initial state
  reset: () => {
    appKitStore.set(initialState)
  }
}

// Utility functions
export const formatAddress = (address?: string): string => {
  if (!address) return ''
  return `${address.slice(0, 6)}...${address.slice(-4)}`
}

export const formatBalance = (balance?: string): string => {
  if (!balance) return '0'
  
  try {
    const num = parseFloat(balance)
    if (num === 0) return '0'
    if (num < 0.0001) return '< 0.0001'
    if (num < 1) return num.toFixed(4)
    if (num < 1000) return num.toFixed(3)
    return `${(num / 1000).toFixed(2)}k`
  } catch {
    return balance
  }
}

// Chain ID to network name mapping
export const getNetworkName = (chainId?: number): string => {
  const networks: Record<number, string> = {
    1: 'Ethereum',
    8453: 'Base',
    137: 'Polygon',
    42161: 'Arbitrum One',
    10: 'Optimism',
    56: 'BNB Smart Chain',
    43114: 'Avalanche',
    250: 'Fantom'
  }
  
  return networks[chainId || 0] || `Chain ${chainId || 'Unknown'}`
}