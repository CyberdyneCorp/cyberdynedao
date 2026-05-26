import { writable, derived, get, type Readable, type Writable } from 'svelte/store';

/**
 * Three sign-in paths converge here:
 *
 *   - **cyberdyne**  — email/password or Google OAuth via CyberdyneAuth.
 *                      No wallet attached unless the user separately
 *                      connects one.
 *   - **walletconnect** — WalletConnect-connected wallet that also did the
 *                         SIWE handshake; the user has both an on-chain
 *                         address and a CyberdyneAuth session.
 *   - **null**       — signed out.
 *
 * The DAO/Investments/NFTTerminal screens use ``walletConnectInfo`` to
 * find the on-chain address. The /me/* APIs hit CyberdyneAuth using the
 * session token (stored in the authVM, not here).
 */
export type ConnectionType = 'cyberdyne' | 'walletconnect' | null;

/** CyberdyneAuth user profile surfaced for display (header chip, etc.). */
export interface CyberdyneUserLike {
	id: string;
	email: string;
	walletAddress?: string | null;
	displayName?: string | null;
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
	currentUser: CyberdyneUserLike | null;
	connectionType: ConnectionType;
	showDetails: boolean;
	showConnectionModal: boolean;
	showNFTTerminal: boolean;
	walletConnectInfo: WalletConnectInfoLike | null;
}

export interface Web3WalletDeps {
	/** Opens the AppKit (WalletConnect) modal. Does NOT do SIWE — that
	 *  happens reactively once ``updateFromWalletConnect`` sees an
	 *  ``isConnected`` transition while ``pendingSiwe`` is true. */
	connectWalletConnect: () => Promise<void>;

	/** Signs a message through the connected wallet provider. */
	signPersonalMessage: (message: string, address: string) => Promise<string>;

	/** CyberdyneAuth: email + password. */
	loginWithEmail: (email: string, password: string) => Promise<CyberdyneUserLike | null>;

	/** CyberdyneAuth: kicks off Google OAuth (redirects the browser). */
	startGoogleOAuth: () => Promise<void>;

	/** Signal CyberdyneAuth that the wallet wants a SIWE session. */
	loginWithWallet: (opts: {
		walletAddress: string;
		chainId: number;
		sign: (message: string) => Promise<string>;
	}) => Promise<CyberdyneUserLike | null>;

	/** Tears down both AppKit and the CyberdyneAuth session. */
	disconnect: () => Promise<{ success: boolean; errors: string[]; warnings: string[] }>;

	/** Restores an existing CyberdyneAuth session from sessionStorage. */
	restoreSession: () => Promise<CyberdyneUserLike | null>;

	/** Mirrors wallet info into the legacy ``web3Store`` so older code
	 *  paths (NFT lookups, on-chain reads) keep working unchanged. */
	setGlobalWeb3Info?: (info: {
		address: string;
		balance: string;
		chainId: number;
		isConnected: boolean;
	}) => void;
}

export interface Web3WalletViewModel {
	state: Readable<Web3WalletState>;
	walletConnected: Readable<boolean>;
	errorMessage: Readable<string>;
	isLoading: Readable<boolean>;
	currentUser: Readable<CyberdyneUserLike | null>;
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

	// Three entry points for the new modal.
	handleEmailLogin: (email: string, password: string) => Promise<void>;
	handleGoogleLogin: () => Promise<void>;
	handleWalletSignIn: () => Promise<void>;

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

	// True between the user clicking "Sign in with Wallet" and the SIWE
	// roundtrip finishing — keeps `updateFromWalletConnect` from firing
	// SIWE on every spurious AppKit state ping.
	let pendingSiwe = false;
	// Track which addresses we've already signed for so a wallet
	// reconnect (e.g. account switch) doesn't double-trigger SIWE.
	let lastSiweAddress: string | null = null;

	function update(partial: Partial<Web3WalletState>) {
		state.update((s) => ({ ...s, ...partial }));
	}

	const derive = <K extends keyof Web3WalletState>(key: K): Readable<Web3WalletState[K]> =>
		derived(state, (s) => s[key]);

	function errorMsg(err: unknown): string {
		return err instanceof Error ? err.message : String(err) || 'Unknown error';
	}

	async function runSiwe(address: string, chainId: number): Promise<void> {
		update({ isLoading: true });
		try {
			const user = await deps.loginWithWallet({
				walletAddress: address,
				chainId,
				sign: (msg) => deps.signPersonalMessage(msg, address)
			});
			lastSiweAddress = address;
			update({
				currentUser: user,
				walletConnected: true,
				connectionType: 'walletconnect',
				showConnectionModal: false,
				errorMessage: ''
			});
		} catch (err) {
			update({ errorMessage: `Wallet sign-in failed: ${errorMsg(err)}` });
		} finally {
			pendingSiwe = false;
			update({ isLoading: false });
		}
	}

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

		toggleDetails: () => state.update((s) => ({ ...s, showDetails: !s.showDetails })),
		openConnectionModal: () => update({ showConnectionModal: true, errorMessage: '' }),
		closeConnectionModal: () => {
			pendingSiwe = false;
			update({ showConnectionModal: false });
		},
		openNFTTerminal: () => update({ showNFTTerminal: true }),
		closeNFTTerminal: () => update({ showNFTTerminal: false }),
		clearError: () => update({ errorMessage: '' }),

		handleEmailLogin: async (email, password) => {
			update({ isLoading: true, errorMessage: '' });
			try {
				const user = await deps.loginWithEmail(email, password);
				update({
					currentUser: user,
					walletConnected: true,
					connectionType: 'cyberdyne',
					showConnectionModal: false
				});
			} catch (err) {
				update({ errorMessage: `Sign-in failed: ${errorMsg(err)}` });
			} finally {
				update({ isLoading: false });
			}
		},

		handleGoogleLogin: async () => {
			update({ isLoading: true, errorMessage: '' });
			try {
				await deps.startGoogleOAuth();
				// startGoogleOAuth navigates the page — control rarely
				// returns here. If we get back, the redirect didn't fire.
			} catch (err) {
				update({
					errorMessage: `Google sign-in failed: ${errorMsg(err)}`,
					isLoading: false
				});
			}
		},

		handleWalletSignIn: async () => {
			// Two steps: open AppKit modal; the SIWE step fires
			// reactively in ``updateFromWalletConnect`` once the wallet
			// finishes connecting.
			pendingSiwe = true;
			lastSiweAddress = null;
			update({ isLoading: true, showConnectionModal: false, errorMessage: '' });
			try {
				await deps.connectWalletConnect();
			} catch (err) {
				pendingSiwe = false;
				update({
					errorMessage: `WalletConnect failed: ${errorMsg(err)}`,
					isLoading: false
				});
			}
			// isLoading stays true until runSiwe finishes (or fails).
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
					update({
						...reset,
						errorMessage: `Disconnect completed with issues: ${result.errors.join(', ')}`
					});
				}
			} catch (err) {
				update({
					walletConnected: false,
					connectionType: null,
					currentUser: null,
					showDetails: false,
					walletConnectInfo: null,
					errorMessage: `Unexpected disconnect error: ${errorMsg(err)}`
				});
			} finally {
				lastSiweAddress = null;
				pendingSiwe = false;
				update({ isLoading: false });
			}
		},

		checkAuthStatus: async () => {
			try {
				const user = await deps.restoreSession();
				if (user) {
					update({
						currentUser: user,
						walletConnected: true,
						// Whether the restored session was wallet-bound or not
						// is encoded in the user record (``walletAddress``
						// non-null = SIWE-issued).
						connectionType: user.walletAddress ? 'walletconnect' : 'cyberdyne'
					});
					if (user.walletAddress) {
						deps.setGlobalWeb3Info?.({
							address: user.walletAddress,
							balance: '',
							chainId: 8453,
							isConnected: true
						});
					}
				}
			} catch {
				// Initial restore failure is non-fatal; user just stays signed out.
			}
		},

		updateFromWalletConnect: (info) => {
			let shouldFireSiwe = false;
			let siweAddress: string | null = null;
			let siweChainId: number | null = null;

			state.update((s) => {
				const next: Web3WalletState = { ...s, walletConnectInfo: info };
				if (info.isConnected && info.address) {
					next.walletConnected = true;
					next.connectionType = next.connectionType ?? 'walletconnect';
					if (pendingSiwe && info.address !== lastSiweAddress && info.chainId !== undefined) {
						shouldFireSiwe = true;
						siweAddress = info.address;
						siweChainId = info.chainId;
					}
				} else if (!info.isConnected && s.connectionType === 'walletconnect') {
					next.walletConnected = s.currentUser !== null;
					if (!s.currentUser) next.connectionType = null;
				}
				return next;
			});

			if (shouldFireSiwe && siweAddress && siweChainId !== null) {
				void runSiwe(siweAddress, siweChainId);
			}
		},

		resolveAddress: () => {
			const s = get(state);
			return s.walletConnectInfo?.address || s.currentUser?.walletAddress || '';
		},

		snapshot: () => get(state)
	};
}
