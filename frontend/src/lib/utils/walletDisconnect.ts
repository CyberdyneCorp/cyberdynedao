/**
 * Centralized wallet disconnect utility
 * 
 * This utility provides a single function to completely disconnect
 * from all wallet services and clean up all related state and storage.
 */

import { web3AuthService } from '../web3/web3AuthService';
import { appKitService } from '../web3/appKitService';
import { appKitActions } from '../stores/appKitStore';
import { web3Actions } from '../stores/web3Store';

export interface DisconnectResult {
  success: boolean;
  errors: string[];
  warnings: string[];
}

/**
 * Complete disconnect from all wallet services
 * Cleans up Web3Auth, WalletConnect, and all related browser storage
 */
export async function completeWalletDisconnect(): Promise<DisconnectResult> {
  console.log('🔌 Starting complete wallet disconnect...');
  
  const result: DisconnectResult = {
    success: true,
    errors: [],
    warnings: []
  };

  // Disconnect from Web3Auth
  try {
    console.log('Disconnecting Web3Auth...');
    await web3AuthService.logout();
    console.log('✅ Web3Auth disconnected successfully');
  } catch (error) {
    const errorMsg = `Web3Auth disconnect failed: ${error instanceof Error ? error.message : 'Unknown error'}`;
    console.warn('⚠️', errorMsg);
    result.warnings.push(errorMsg);
  }

  // Disconnect from WalletConnect/AppKit
  try {
    console.log('Disconnecting WalletConnect/AppKit...');
    await appKitService.disconnect();
    console.log('✅ WalletConnect/AppKit disconnected successfully');
  } catch (error) {
    const errorMsg = `WalletConnect disconnect failed: ${error instanceof Error ? error.message : 'Unknown error'}`;
    console.warn('⚠️', errorMsg);
    result.warnings.push(errorMsg);
  }

  // Reset all store states
  try {
    console.log('Resetting store states...');
    appKitActions.completeDisconnect();
    await web3Actions.completeDisconnect();
    console.log('✅ All store states reset');
  } catch (error) {
    const errorMsg = `Store state reset failed: ${error instanceof Error ? error.message : 'Unknown error'}`;
    console.error('❌', errorMsg);
    result.errors.push(errorMsg);
    result.success = false;
  }

  // Clear all wallet-related browser storage
  try {
    console.log('Clearing all wallet-related browser storage...');
    clearAllWalletStorage();
    console.log('✅ Browser storage cleared');
  } catch (error) {
    const errorMsg = `Storage cleanup failed: ${error instanceof Error ? error.message : 'Unknown error'}`;
    console.warn('⚠️', errorMsg);
    result.warnings.push(errorMsg);
  }

  // Final summary
  if (result.success) {
    console.log('🎉 Complete wallet disconnect finished successfully');
    if (result.warnings.length > 0) {
      console.log('⚠️ Warnings occurred:', result.warnings);
    }
  } else {
    console.error('❌ Complete wallet disconnect finished with errors:', result.errors);
  }

  return result;
}

/**
 * Clear all wallet-related items from browser storage
 * @private
 */
function clearAllWalletStorage(): void {
  if (typeof window === 'undefined') return;

  const walletStoragePatterns = [
    // Web3Auth patterns
    'Web3Auth',
    'openlogin',
    'torus',
    'web3auth',
    'auth-',
    
    // WalletConnect patterns  
    'wc@',
    'walletconnect',
    '@w3m',
    'reown',
    'wagmi',
    'appkit',
    'connector',
    
    // General wallet patterns
    'wallet',
    'metamask',
    'coinbase',
    'trust'
  ];

  // Clear localStorage
  const localKeysToRemove: string[] = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && walletStoragePatterns.some(pattern => 
      key.toLowerCase().includes(pattern.toLowerCase())
    )) {
      localKeysToRemove.push(key);
    }
  }

  localKeysToRemove.forEach(key => {
    try {
      localStorage.removeItem(key);
      console.log(`Cleared localStorage: ${key}`);
    } catch (error) {
      console.warn(`Failed to clear localStorage key ${key}:`, error);
    }
  });

  // Clear sessionStorage
  const sessionKeysToRemove: string[] = [];
  for (let i = 0; i < sessionStorage.length; i++) {
    const key = sessionStorage.key(i);
    if (key && walletStoragePatterns.some(pattern => 
      key.toLowerCase().includes(pattern.toLowerCase())
    )) {
      sessionKeysToRemove.push(key);
    }
  }

  sessionKeysToRemove.forEach(key => {
    try {
      sessionStorage.removeItem(key);
      console.log(`Cleared sessionStorage: ${key}`);
    } catch (error) {
      console.warn(`Failed to clear sessionStorage key ${key}:`, error);
    }
  });

  console.log(`Cleared ${localKeysToRemove.length} localStorage and ${sessionKeysToRemove.length} sessionStorage keys`);
}

/**
 * Check if any wallet connections exist
 */
export function hasWalletConnections(): boolean {
  try {
    // Check Web3Auth connection
    const web3authConnected = web3AuthService.isConnected();
    
    // Check WalletConnect/AppKit connection
    const appKitConnected = appKitService.isInitialized();
    
    return web3authConnected || appKitConnected;
  } catch (error) {
    console.warn('Error checking wallet connections:', error);
    return false;
  }
}

/**
 * Get current connection status
 */
export function getConnectionStatus(): {
  web3auth: boolean;
  walletConnect: boolean;
  hasAnyConnection: boolean;
} {
  try {
    const web3auth = web3AuthService.isConnected();
    const walletConnect = appKitService.isInitialized();
    
    return {
      web3auth,
      walletConnect,
      hasAnyConnection: web3auth || walletConnect
    };
  } catch (error) {
    console.warn('Error getting connection status:', error);
    return {
      web3auth: false,
      walletConnect: false,
      hasAnyConnection: false
    };
  }
}