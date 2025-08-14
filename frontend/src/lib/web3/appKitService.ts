/**
 * Reown AppKit Service - Handles wallet connections via WalletConnect protocol
 * 
 * This service provides a comprehensive interface for Reown AppKit operations:
 * - AppKit initialization with proper configuration
 * - QR code modal for mobile wallet connections (MetaMask Mobile, etc.)
 * - Multi-chain support (Ethereum, Polygon, Arbitrum)
 * - Connection state management
 * - Error handling and logging
 */

import { createAppKit } from '@reown/appkit'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum, polygon, base } from '@reown/appkit/networks'
import type { AppKit, AppKitNetwork } from '@reown/appkit'
import { 
  appKitInstance, 
  appKitActions, 
  setValidatedWalletInfo,
  type WalletInfo
} from '../stores/appKitStore'
import { get } from 'svelte/store'

// AppKit configuration interface
interface AppKitConfig {
  projectId: string
  networks: AppKitNetwork[]
  defaultNetwork: AppKitNetwork
  metadata: {
    name: string
    description: string
    url: string
    icons: string[]
  }
  features?: {
    analytics?: boolean
    email?: boolean
    socials?: string[]
  }
  themeMode?: 'light' | 'dark' | 'auto'
  themeVariables?: Record<string, string>
}

class AppKitService {
  private appKit: AppKit | null = null
  private wagmiAdapter: WagmiAdapter | null = null
  private isInitializing = false

  /**
   * Initialize Reown AppKit with environment configuration
   * @returns Promise<boolean> - Success status
   */
  async initialize(): Promise<boolean> {
    console.log('AppKit initialize called, current state:', {
      isInitializing: this.isInitializing,
      hasAppKit: !!this.appKit,
      serviceInstance: !!this
    })

    // Prevent multiple initialization attempts
    if (this.isInitializing) {
      console.log('AppKit initialization already in progress')
      return false
    }

    // Check if already initialized
    if (this.appKit) {
      console.log('AppKit already initialized')
      appKitActions.setInitialized(true)
      return true
    }

    try {
      this.isInitializing = true
      appKitActions.setLoading(true)
      appKitActions.clearError()

      // Validate required environment variables
      const projectId = import.meta.env.VITE_REOWN_PROJECT_ID
      console.log('Project ID from env:', projectId)
      
      if (!projectId || projectId === 'your_reown_project_id') {
        throw new Error('VITE_REOWN_PROJECT_ID is not configured. Please set your Reown project ID in the .env file.')
      }

      // Define supported networks
      const networks = [mainnet, arbitrum, polygon, base]

      // Initialize Wagmi adapter
      this.wagmiAdapter = new WagmiAdapter({ 
        networks, 
        projectId 
      })

      // Create AppKit configuration
      const config: AppKitConfig = {
        projectId,
        networks,
        defaultNetwork: base, // Use Base as default since we're configured for it
        metadata: {
          name: import.meta.env.VITE_REOWN_APP_NAME || 'Cyberdyne DAO Terminal',
          description: import.meta.env.VITE_REOWN_APP_DESCRIPTION || 'Retro terminal interface for DAO operations',
          url: import.meta.env.VITE_REOWN_APP_URL || 'https://cyberdyne-dao.com',
          icons: [import.meta.env.VITE_REOWN_APP_ICON || 'https://cyberdyne-dao.com/icon.png']
        },
        features: {
          analytics: true,
          email: false, // Disable email since we have Web3Auth for social login
          socials: [] // Disable social login since we have Web3Auth
        },
        themeMode: 'dark', // Match the retro terminal theme
        themeVariables: {
          '--w3m-color-mix': '#00ff00',
          '--w3m-color-mix-strength': 20,
          '--w3m-accent': '#00ff00',
          '--w3m-border-radius-master': '4px',
          '--w3m-font-family': '"JetBrains Mono", "IBM Plex Mono", monospace',
          '--w3m-background': '#000000',
          '--w3m-foreground': '#00ff00'
        }
      }

      // Initialize AppKit
      this.appKit = createAppKit({
        adapters: [this.wagmiAdapter],
        networks: config.networks,
        defaultNetwork: config.defaultNetwork,
        projectId: config.projectId,
        metadata: config.metadata,
        features: config.features,
        themeMode: config.themeMode,
        themeVariables: config.themeVariables,
        featuredWalletIds: [
          'c57ca95b47569778a828d19178114f4db188b89b763c899ba0be274e97267d96', // MetaMask
          'fd20dc426fb37566d803205b19bbc1d4096b248ac04548e3cfb6b3a38bd033aa', // Coinbase Wallet
          '4622a2b2d6af1c9844944291e5e7351a6aa24cd7b23099efac1b2fd875da31a0', // Trust Wallet
          '38f5d18bd8522c244bdd70cb4a68e0e718865155811c043f052fb9f1c51de662'  // Bitget Wallet
        ]
      })

      // Store instance and update state
      appKitInstance.set(this.appKit)
      appKitActions.setInitialized(true)

      // Set up event listeners
      this.setupEventListeners()

      console.log('Reown AppKit initialized successfully')
      return true

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to initialize Reown AppKit'
      console.error('AppKit initialization error:', errorMessage)
      appKitActions.setError(errorMessage)
      return false

    } finally {
      this.isInitializing = false
      appKitActions.setLoading(false)
    }
  }

  /**
   * Open the AppKit connection modal
   * This will show the QR code for mobile wallets like MetaMask Mobile
   * @returns Promise<void>
   */
  async openModal(): Promise<void> {
    try {
      console.log('AppKit openModal called, current state:', {
        hasAppKit: !!this.appKit,
        isInitializing: this.isInitializing,
        serviceInstance: !!this
      })

      // Ensure AppKit is initialized
      if (!this.appKit) {
        console.log('AppKit not initialized, attempting to initialize...')
        const initialized = await this.initialize()
        if (!initialized) {
          throw new Error('Failed to initialize AppKit')
        }
      }

      appKitActions.setLoading(true)
      appKitActions.clearError()

      // Open the connection modal
      console.log('Opening AppKit modal...')
      this.appKit?.open()

      console.log('AppKit modal opened successfully')

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to open AppKit modal'
      console.error('Open modal error:', errorMessage)
      console.error('Full error object:', error)
      appKitActions.setError(errorMessage)
    } finally {
      appKitActions.setLoading(false)
    }
  }

  /**
   * Open the AppKit modal with specific view
   * @param view - The view to open ('Connect', 'Account', 'Networks', etc.)
   */
  async openModalView(view: string): Promise<void> {
    try {
      if (!this.appKit) {
        const initialized = await this.initialize()
        if (!initialized) {
          throw new Error('Failed to initialize AppKit')
        }
      }

      this.appKit?.open({ view })
      console.log(`AppKit modal opened with view: ${view}`)

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : `Failed to open AppKit modal with view ${view}`
      console.error('Open modal view error:', errorMessage)
      appKitActions.setError(errorMessage)
    }
  }

  /**
   * Close the AppKit modal
   */
  closeModal(): void {
    this.appKit?.close()
  }

  /**
   * Get current wallet connection state
   * @returns WalletInfo | null
   */
  getWalletInfo(): WalletInfo | null {
    if (!this.appKit) {
      return null
    }

    const state = this.appKit.getState()
    
    // Extract chain ID from caipAddress if selectedNetworkId is undefined
    let chainId = state.selectedNetworkId
    if (!chainId && state.selectedAccount?.caipAddress) {
      // Parse CAIP-10 format: "eip155:42161:0x..."
      const match = state.selectedAccount.caipAddress.match(/^eip155:(\d+):/)
      if (match) {
        chainId = parseInt(match[1], 10)
      }
    }
    
    // Only consider connected if we have both a valid address AND chain ID
    const hasValidAddress = !!state.selectedAccount?.address;
    const hasValidChainId = !!chainId;
    const isFullyConnected = hasValidAddress && hasValidChainId;
    
    return {
      isConnected: isFullyConnected,
      address: state.selectedAccount?.address,
      chainId: chainId,
      balance: state.selectedAccount?.balance
    }
  }

  /**
   * Disconnect the current wallet
   * @returns Promise<boolean> - Success status
   */
  async disconnect(): Promise<boolean> {
    console.log('WalletConnect disconnect initiated...');
    
    try {
      if (!this.appKit) {
        console.warn('AppKit not initialized, clearing state anyway');
        appKitActions.setDisconnected();
        this.clearWalletConnectStorage();
        return true;
      }

      console.log('Calling AppKit disconnect...');
      await this.appKit.disconnect();
      
      // Update store state
      appKitActions.setDisconnected();
      
      // Clear WalletConnect related storage
      this.clearWalletConnectStorage();

      console.log('Successfully disconnected from WalletConnect wallet');
      return true;

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to disconnect wallet';
      console.error('WalletConnect disconnect error:', errorMessage);
      
      // Even if disconnect fails, clear local state and storage
      appKitActions.setDisconnected();
      this.clearWalletConnectStorage();
      
      // Don't throw error - we want to clear state regardless
      console.log('Cleared WalletConnect state despite disconnect error');
      return true; // Return true since we cleared the state
    }
  }

  /**
   * Clear WalletConnect related browser storage
   * @private
   */
  private clearWalletConnectStorage(): void {
    if (typeof window === 'undefined') return;
    
    try {
      console.log('Clearing WalletConnect storage...');
      
      // Clear localStorage items
      const localKeysToRemove = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && (
          key.startsWith('wc@') || 
          key.startsWith('walletconnect') ||
          key.startsWith('@w3m') ||
          key.startsWith('reown') ||
          key.includes('wagmi') ||
          key.includes('appkit') ||
          key.includes('connector')
        )) {
          localKeysToRemove.push(key);
        }
      }
      
      localKeysToRemove.forEach(key => {
        localStorage.removeItem(key);
        console.log(`Cleared localStorage key: ${key}`);
      });
      
      // Clear sessionStorage items
      const sessionKeysToRemove = [];
      for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        if (key && (
          key.startsWith('wc@') || 
          key.startsWith('walletconnect') ||
          key.startsWith('@w3m') ||
          key.startsWith('reown') ||
          key.includes('wagmi') ||
          key.includes('appkit') ||
          key.includes('connector')
        )) {
          sessionKeysToRemove.push(key);
        }
      }
      
      sessionKeysToRemove.forEach(key => {
        sessionStorage.removeItem(key);
        console.log(`Cleared sessionStorage key: ${key}`);
      });
      
      console.log('WalletConnect storage cleared successfully');
    } catch (storageError) {
      console.warn('Error clearing WalletConnect storage:', storageError);
    }
  }

  /**
   * Get AppKit instance
   * @returns AppKit | null
   */
  getInstance(): AppKit | null {
    return this.appKit
  }

  /**
   * Check if AppKit is initialized
   * @returns boolean
   */
  isInitialized(): boolean {
    return !!this.appKit
  }

  /**
   * Set up event listeners for AppKit state changes
   * @private
   */
  private setupEventListeners(): void {
    if (!this.appKit) return

    // Listen to modal state changes
    this.appKit.subscribeState((state) => {
      console.log('AppKit full state object:', state)
      console.log('selectedNetworkId:', state.selectedNetworkId, 'type:', typeof state.selectedNetworkId)
      console.log('selectedAccount:', state.selectedAccount)
      
      // Extract chain ID from caipAddress if selectedNetworkId is undefined
      let chainId = state.selectedNetworkId
      if (!chainId && state.selectedAccount?.caipAddress) {
        // Parse CAIP-10 format: "eip155:42161:0x..."
        const match = state.selectedAccount.caipAddress.match(/^eip155:(\d+):/)
        if (match) {
          chainId = parseInt(match[1], 10)
          console.log('Extracted chainId from state caipAddress:', chainId)
        }
      }
      
      // Only consider connected if we have both a valid address AND chain ID
      const hasValidAddress = !!state.selectedAccount?.address;
      const hasValidChainId = !!chainId;
      const isFullyConnected = hasValidAddress && hasValidChainId;
      
      const walletInfo: WalletInfo = {
        isConnected: isFullyConnected,
        address: state.selectedAccount?.address,
        chainId: chainId,
        balance: state.selectedAccount?.balance
      }

      setValidatedWalletInfo(walletInfo)
      
      console.log('AppKit state changed:', {
        isConnected: walletInfo.isConnected,
        hasValidAddress,
        hasValidChainId,
        address: walletInfo.address,
        chainId: walletInfo.chainId,
        chainIdType: typeof walletInfo.chainId,
        isFullyConnected
      })
    })

    // Listen to account changes
    this.appKit.subscribeAccount((account) => {
      console.log('Account changed full object:', account)
      console.log('Account chainId:', account.chainId, 'type:', typeof account.chainId)
      console.log('Account address:', account.address)
      console.log('Account caipAddress:', account.caipAddress)
      console.log('Account isConnected:', account.isConnected)
      
      // Extract chain ID from caipAddress if chainId is undefined
      let chainId = account.chainId
      if (!chainId && account.caipAddress) {
        // Parse CAIP-10 format: "eip155:42161:0x..."
        const match = account.caipAddress.match(/^eip155:(\d+):/)
        if (match) {
          chainId = parseInt(match[1], 10)
          console.log('Extracted chainId from caipAddress:', chainId)
        }
      }
      
      // Only consider connected if we have both a valid address AND chain ID
      const hasValidAddress = !!account.address;
      const hasValidChainId = !!chainId;
      const isFullyConnected = account.isConnected && hasValidAddress && hasValidChainId;
      
      if (isFullyConnected) {
        const walletInfo: WalletInfo = {
          isConnected: true,
          address: account.address,
          chainId: chainId,
          balance: account.balance
        }
        console.log('Setting wallet info from account (fully connected):', walletInfo)
        setValidatedWalletInfo(walletInfo)
      } else {
        console.log('Account not fully connected:', {
          accountIsConnected: account.isConnected,
          hasValidAddress,
          hasValidChainId,
          address: account.address,
          chainId
        })
        appKitActions.setDisconnected()
      }
    })

    // Listen to chain changes
    this.appKit.subscribeChainId((chainId) => {
      console.log('Chain changed:', chainId, 'type:', typeof chainId)
      appKitActions.setChainId(chainId)
    })
  }
}

// Create singleton instance
export const appKitService = new AppKitService()

// Export service methods for convenience (preserve 'this' context)
export const initializeAppKit = () => appKitService.initialize()
export const openAppKitModal = () => appKitService.openModal()
export const openAppKitModalView = (view: string) => appKitService.openModalView(view)
export const closeAppKitModal = () => appKitService.closeModal()
export const disconnectWallet = () => appKitService.disconnect()
export const getWalletInfo = () => appKitService.getWalletInfo()
export const getAppKitInstance = () => appKitService.getInstance()
export const isAppKitInitialized = () => appKitService.isInitialized()