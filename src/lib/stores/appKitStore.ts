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
  instance: AppKit | null
  isInitialized: boolean
  isLoading: boolean
  error: string | null
  walletInfo: WalletInfo
}

// Initial state
const initialState: AppKitState = {
  instance: null,
  isInitialized: false,
  isLoading: false,
  error: null,
  walletInfo: {
    isConnected: false
  }
}

// Main AppKit store
export const appKitStore = writable<AppKitState>(initialState)

// Derived stores for convenient access
export const appKitInstance = derived(appKitStore, $store => $store.instance)
export const isAppKitInitialized = derived(appKitStore, $store => $store.isInitialized)
export const isAppKitLoading = derived(appKitStore, $store => $store.isLoading)
export const appKitError = derived(appKitStore, $store => $store.error)
export const appKitWalletInfo = derived(appKitStore, $store => $store.walletInfo)

// Store actions
export const appKitActions = {
  // Set AppKit instance
  setInstance: (instance: AppKit) => {
    appKitStore.update(state => ({
      ...state,
      instance
    }))
  },

  // Set initialization status
  setInitialized: (isInitialized: boolean) => {
    appKitStore.update(state => ({
      ...state,
      isInitialized
    }))
  },

  // Set loading state
  setLoading: (isLoading: boolean) => {
    appKitStore.update(state => ({
      ...state,
      isLoading
    }))
  },

  // Set error message
  setError: (error: string | null) => {
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

  // Set chain ID only
  setChainId: (chainId: number) => {
    appKitStore.update(state => ({
      ...state,
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
        isConnected: false
      }
    }))
  },

  // Reset store to initial state
  reset: () => {
    appKitStore.set(initialState)
  }
}