import { Web3Auth } from "@web3auth/modal";
import { CHAIN_NAMESPACES, WEB3AUTH_NETWORK, WALLET_ADAPTERS } from "@web3auth/base";
import type { IProvider } from "@web3auth/base";
import { ethers } from "ethers";

const clientId = import.meta.env.VITE_WEB3AUTH_CLIENT_ID;

console.log('Web3Auth Client ID:', clientId ? `${clientId.substring(0, 10)}...` : 'NOT SET');

if (!clientId) {
  throw new Error("Web3Auth Client ID is not configured. Please check your environment variables.");
}

// Get network from environment or default to SAPPHIRE_DEVNET
const networkName = import.meta.env.VITE_WEB3AUTH_NETWORK || 'sapphire_devnet';
const web3AuthNetwork = WEB3AUTH_NETWORK[networkName.toUpperCase()] || WEB3AUTH_NETWORK.SAPPHIRE_DEVNET;

// Web3Auth v10 configuration - chainConfig and privateKeyProvider handled by dashboard
const web3auth = new Web3Auth({
  clientId,
  web3AuthNetwork: web3AuthNetwork,
  uiConfig: {
    appName: "Cyberdyne DAO Terminal",
    appUrl: import.meta.env.VITE_APP_URL || "http://localhost:5173",
    defaultLanguage: "en",
    mode: "dark",
    theme: {
      primary: "#00ff00", // Retro green theme
    },
    useLogoLoader: false,
  },
});

export interface UserInfo {
  email?: string;
  name?: string;
  profileImage?: string;
  aggregateVerifier?: string;
  verifier?: string;
  verifierId?: string;
  typeOfLogin?: string;
  dappShare?: string;
  oAuthIdToken?: string;
  oAuthAccessToken?: string;
  appState?: string;
  touchIDPreference?: string;
  isMfaEnabled?: boolean;
}

export enum LoginProvider {
  GOOGLE = "google",
  FACEBOOK = "facebook",
  TWITTER = "twitter",
  DISCORD = "discord",
  TWITCH = "twitch",
  APPLE = "apple",
  LINE = "line",
  GITHUB = "github",
  KAKAO = "kakao",
  LINKEDIN = "linkedin",
  WEIBO = "weibo",
  WECHAT = "wechat",
  EMAIL_PASSWORDLESS = "email_passwordless",
}

export interface Web3AuthError {
  code: string;
  message: string;
  details?: unknown;
}

export interface Web3AuthUser {
  userInfo: UserInfo;
  address: string;
  balance: string;
  provider: IProvider;
}

class Web3AuthService {
  private initialized = false;
  private provider: IProvider | null = null;
  private initPromise: Promise<void> | null = null;

  private createError(message: string, code: string, details?: unknown): Web3AuthError {
    return { code, message, details };
  }

  async initialize(): Promise<void> {
    if (this.initialized) return;
    
    // Prevent multiple simultaneous initialization attempts
    if (this.initPromise) {
      return this.initPromise;
    }

    this.initPromise = this._initialize();
    return this.initPromise;
  }

  private async _initialize(): Promise<void> {
    try {
      console.log('Starting Web3Auth initialization...');
      console.log('Client ID available:', !!clientId);
      console.log('Network:', WEB3AUTH_NETWORK.SAPPHIRE_DEVNET);
      
      await web3auth.init();
      this.initialized = true;
      console.log("Web3Auth initialized successfully");
    } catch (error) {
      console.error("Error initializing Web3Auth:", error);
      console.error("Error details:", {
        message: error.message,
        code: error.code,
        details: error
      });
      
      this.initPromise = null; // Reset promise on failure
      throw this.createError(
        "Failed to initialize Web3Auth",
        "INIT_ERROR",
        error
      );
    }
  }

  async login(loginProvider?: LoginProvider): Promise<Web3AuthUser | null> {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      // Web3Auth v10 uses connect() without parameters for modal
      const web3authProvider = await web3auth.connect();
      
      if (!web3authProvider) {
        throw this.createError(
          "Failed to connect to Web3Auth",
          "CONNECTION_FAILED"
        );
      }

      this.provider = web3authProvider;
      const userInfo = await web3auth.getUserInfo();
      
      // Get user's Ethereum address and balance
      const ethersProvider = new ethers.BrowserProvider(web3authProvider);
      const signer = await ethersProvider.getSigner();
      const address = await signer.getAddress();
      const balance = await ethersProvider.getBalance(address);
      const balanceInEth = ethers.formatEther(balance);

      const user: Web3AuthUser = {
        userInfo,
        address,
        balance: balanceInEth,
        provider: web3authProvider,
      };

      console.log("User logged in successfully:", {
        address,
        provider: userInfo.typeOfLogin || userInfo.verifier || 'unknown',
        email: userInfo.email,
      });

      return user;
    } catch (error) {
      console.error("Error during Web3Auth login:", error);
      
      // Reset provider on login failure
      this.provider = null;
      
      throw this.createError(
        "Login failed",
        "LOGIN_ERROR",
        error
      );
    }
  }

  // Provider-specific login methods for better UX
  async loginWithGoogle(): Promise<Web3AuthUser | null> {
    return this.login(LoginProvider.GOOGLE);
  }

  async loginWithFacebook(): Promise<Web3AuthUser | null> {
    return this.login(LoginProvider.FACEBOOK);
  }

  async loginWithApple(): Promise<Web3AuthUser | null> {
    return this.login(LoginProvider.APPLE);
  }

  async loginWithEmail(): Promise<Web3AuthUser | null> {
    return this.login(LoginProvider.EMAIL_PASSWORDLESS);
  }

  async logout(): Promise<void> {
    if (!this.initialized) return;

    try {
      await web3auth.logout();
      this.provider = null;
      console.log("User logged out successfully");
    } catch (error) {
      console.error("Error during logout:", error);
      // Clean up state even if logout fails
      this.provider = null;
      throw this.createError(
        "Logout failed",
        "LOGOUT_ERROR",
        error
      );
    }
  }

  async getUserInfo(): Promise<UserInfo | null> {
    if (!this.initialized || !web3auth.connected) {
      return null;
    }

    try {
      return await web3auth.getUserInfo();
    } catch (error) {
      console.error("Error getting user info:", error);
      return null;
    }
  }

  async getAccounts(): Promise<string[]> {
    if (!this.provider) {
      throw new Error("Provider not initialized. Please login first.");
    }

    try {
      const ethersProvider = new ethers.BrowserProvider(this.provider);
      const signer = await ethersProvider.getSigner();
      const address = await signer.getAddress();
      return [address];
    } catch (error) {
      console.error("Error getting accounts:", error);
      throw error;
    }
  }

  async getBalance(address?: string): Promise<string> {
    if (!this.provider) {
      throw new Error("Provider not initialized. Please login first.");
    }

    try {
      const ethersProvider = new ethers.BrowserProvider(this.provider);
      let targetAddress = address;
      
      if (!targetAddress) {
        const signer = await ethersProvider.getSigner();
        targetAddress = await signer.getAddress();
      }

      const balance = await ethersProvider.getBalance(targetAddress);
      return ethers.formatEther(balance);
    } catch (error) {
      console.error("Error getting balance:", error);
      throw error;
    }
  }

  async signMessage(message: string): Promise<string> {
    if (!this.provider) {
      throw new Error("Provider not initialized. Please login first.");
    }

    try {
      const ethersProvider = new ethers.BrowserProvider(this.provider);
      const signer = await ethersProvider.getSigner();
      return await signer.signMessage(message);
    } catch (error) {
      console.error("Error signing message:", error);
      throw error;
    }
  }

  // Helper method to check if user is authenticated
  async checkAuthStatus(): Promise<Web3AuthUser | null> {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!web3auth.connected) {
      return null;
    }

    try {
      const userInfo = await this.getUserInfo();
      if (!userInfo) return null;

      const accounts = await this.getAccounts();
      const balance = await this.getBalance();

      return {
        userInfo,
        address: accounts[0],
        balance,
        provider: this.provider!,
      };
    } catch (error) {
      console.error("Error checking auth status:", error);
      return null;
    }
  }

  // Check if Web3Auth is connected
  isConnected(): boolean {
    return this.initialized && web3auth.connected;
  }

  // Get the current provider instance
  getProvider(): IProvider | null {
    return this.provider;
  }
}

// Export singleton instance
export const web3AuthService = new Web3AuthService();
export default web3AuthService;