import { writable, derived, get, type Readable, type Writable } from 'svelte/store';

export type ConnectionType = 'web3auth' | 'walletconnect' | null;

export interface Web3AuthUserLike {
	address: string;
	balance: string;
	userInfo: { email?: string; name?: string };
}

export interface WalletConnectInfoLike {
	address?: string;
	balance?: string;
	chainId?: number;
	isConnected: boolean;
}

export interface Web3WalletState {
	walletConnected: boolean;
	isLoading: boolean;
	errorMessage: string;
	currentUser: Web3AuthUserLike | null;
	connectionType: ConnectionType;
	showDetails: boolean;
	showConnectionModal: boolean;
	showNFTTerminal: boolean;
	walletConnectInfo: WalletConnectInfoLike | null;
}

export interface Web3WalletDeps {
	connectWalletConnect: () => Promise<void>;
	connectWeb3Auth: () => Promise<Web3AuthUserLike | null>;
	disconnect: () => Promise<{ success: boolean; errors: string[]; warnings: string[] }>;
	checkAuthStatus: () => Promise<Web3AuthUserLike | null>;
	setGlobalWeb3Info?: (info: { address: string; balance: string; chainId: number; isConnected: boolean }) => void;
}

export interface Web3WalletViewModel {
	state: Readable<Web3WalletState>;
	walletConnected: Readable<boolean>;
	errorMessage: Readable<string>;
	isLoading: Readable<boolean>;
	currentUser: Readable<Web3AuthUserLike | null>;
	connectionType: Readable<ConnectionType>;
	showDetails: Readable<boolean>;
	showConnectionModal: Readable<boolean>;
	showNFTTerminal: Readable<boolean>;
	toggleDetails: () => void;
	openConnectionModal: () => void;
	closeConnectionModal: () => void;
	openNFTTerminal: () => void;
	closeNFTTerminal: () => void;
	clearError: () => void;
	handleWalletConnect: () => Promise<void>;
	handleWeb3AuthConnect: () => Promise<void>;
	handleDisconnect: () => Promise<void>;
	checkAuthStatus: () => Promise<void>;
	updateFromWalletConnect: (info: WalletConnectInfoLike) => void;
	resolveAddress: () => string;
	snapshot: () => Web3WalletState;
}

function initialState(): Web3WalletState {
	return {
		walletConnected: false,
		isLoading: false,
		errorMessage: '',
		currentUser: null,
		connectionType: null,
		showDetails: false,
		showConnectionModal: false,
		showNFTTerminal: false,
		walletConnectInfo: null
	};
}

export function createWeb3WalletViewModel(deps: Web3WalletDeps): Web3WalletViewModel {
	const state: Writable<Web3WalletState> = writable(initialState());

	function update(partial: Partial<Web3WalletState>) {
		state.update(s => ({ ...s, ...partial }));
	}

	const derive = <K extends keyof Web3WalletState>(key: K): Readable<Web3WalletState[K]> =>
		derived(state, (s) => s[key]);

	return {
		state,
		walletConnected: derive('walletConnected'),
		errorMessage: derive('errorMessage'),
		isLoading: derive('isLoading'),
		currentUser: derive('currentUser'),
		connectionType: derive('connectionType'),
		showDetails: derive('showDetails'),
		showConnectionModal: derive('showConnectionModal'),
		showNFTTerminal: derive('showNFTTerminal'),

		toggleDetails: () => state.update(s => ({ ...s, showDetails: !s.showDetails })),
		openConnectionModal: () => update({ showConnectionModal: true }),
		closeConnectionModal: () => update({ showConnectionModal: false }),
		openNFTTerminal: () => update({ showNFTTerminal: true }),
		closeNFTTerminal: () => update({ showNFTTerminal: false }),
		clearError: () => update({ errorMessage: '' }),

		handleWalletConnect: async () => {
			update({ isLoading: true, showConnectionModal: false });
			try {
				await deps.connectWalletConnect();
				update({ errorMessage: '' });
			} catch (err) {
				const msg = (err as { message?: string })?.message || String(err) || 'Unknown error';
				update({ errorMessage: `WalletConnect failed: ${msg}` });
			} finally {
				update({ isLoading: false });
			}
		},

		handleWeb3AuthConnect: async () => {
			update({ isLoading: true, showConnectionModal: false });
			try {
				const user = await deps.connectWeb3Auth();
				if (user) {
					update({
						currentUser: user,
						walletConnected: true,
						connectionType: 'web3auth',
						errorMessage: ''
					});
					deps.setGlobalWeb3Info?.({
						address: user.address,
						balance: user.balance,
						chainId: 8453,
						isConnected: true
					});
				}
			} catch (err) {
				const msg = (err as { message?: string })?.message || String(err) || 'Unknown error';
				update({
					errorMessage: `Login failed: ${msg}`,
					walletConnected: false,
					currentUser: null,
					connectionType: null
				});
			} finally {
				update({ isLoading: false });
			}
		},

		handleDisconnect: async () => {
			update({ isLoading: true });
			try {
				const result = await deps.disconnect();
				const reset: Partial<Web3WalletState> = {
					walletConnected: false,
					connectionType: null,
					currentUser: null,
					showDetails: false,
					walletConnectInfo: null
				};
				if (result.success) {
					update({ ...reset, errorMessage: '' });
				} else {
					update({ ...reset, errorMessage: `Disconnect completed with issues: ${result.errors.join(', ')}` });
				}
			} catch (err) {
				const msg = (err as { message?: string })?.message || 'Unknown error';
				update({
					walletConnected: false,
					connectionType: null,
					currentUser: null,
					showDetails: false,
					walletConnectInfo: null,
					errorMessage: `Unexpected disconnect error: ${msg}`
				});
			} finally {
				update({ isLoading: false });
			}
		},

		checkAuthStatus: async () => {
			try {
				const user = await deps.checkAuthStatus();
				if (user) {
					update({
						currentUser: user,
						walletConnected: true,
						connectionType: 'web3auth'
					});
					deps.setGlobalWeb3Info?.({
						address: user.address,
						balance: user.balance,
						chainId: 8453,
						isConnected: true
					});
				}
			} catch {
				// Swallow initial auth check failures silently.
			}
		},

		updateFromWalletConnect: (info) => {
			state.update(s => {
				const next: Web3WalletState = { ...s, walletConnectInfo: info };
				if (info.isConnected && s.connectionType !== 'web3auth') {
					next.walletConnected = true;
					next.connectionType = 'walletconnect';
				} else if (!info.isConnected && s.connectionType === 'walletconnect') {
					next.walletConnected = s.currentUser !== null;
					if (!s.currentUser) next.connectionType = null;
				}
				return next;
			});
		},

		resolveAddress: () => {
			const s = get(state);
			if (s.connectionType === 'web3auth') return s.currentUser?.address || '';
			if (s.connectionType === 'walletconnect') return s.walletConnectInfo?.address || '';
			return '';
		},

		snapshot: () => get(state)
	};
}
