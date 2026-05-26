import { describe, it, expect, vi } from 'vitest';
import { get } from 'svelte/store';
import {
	createWeb3WalletViewModel,
	type CyberdyneUserLike,
	type Web3WalletDeps
} from '../web3WalletViewModel';

function buildDeps(overrides: Partial<Web3WalletDeps> = {}): Web3WalletDeps {
	return {
		connectWalletConnect: vi.fn().mockResolvedValue(undefined),
		signPersonalMessage: vi.fn().mockResolvedValue('0xsignature'),
		loginWithEmail: vi.fn().mockResolvedValue(null),
		startGoogleOAuth: vi.fn().mockResolvedValue(undefined),
		loginWithWallet: vi.fn().mockResolvedValue(null),
		disconnect: vi.fn().mockResolvedValue({ success: true, errors: [], warnings: [] }),
		restoreSession: vi.fn().mockResolvedValue(null),
		setGlobalWeb3Info: vi.fn(),
		...overrides
	};
}

const user: CyberdyneUserLike = {
	id: 'u-1',
	email: 'x@y.z',
	walletAddress: '0xabc',
	displayName: 'Test User'
};

describe('web3WalletViewModel', () => {
	it('initial state is signed out', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		expect(get(vm.walletConnected)).toBe(false);
		expect(get(vm.errorMessage)).toBe('');
		expect(get(vm.isLoading)).toBe(false);
		expect(get(vm.connectionType)).toBe(null);
	});

	it('toggleDetails flips flag', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		vm.toggleDetails();
		expect(get(vm.showDetails)).toBe(true);
		vm.toggleDetails();
		expect(get(vm.showDetails)).toBe(false);
	});

	it('openConnectionModal clears any prior error', async () => {
		const vm = createWeb3WalletViewModel(
			buildDeps({ loginWithEmail: vi.fn().mockRejectedValue(new Error('bad creds')) })
		);
		await vm.handleEmailLogin('a@b.c', 'pw');
		expect(get(vm.errorMessage)).toMatch(/bad creds/);
		vm.openConnectionModal();
		expect(get(vm.errorMessage)).toBe('');
		expect(get(vm.showConnectionModal)).toBe(true);
	});

	it('handleEmailLogin happy path → connectionType=cyberdyne', async () => {
		const deps = buildDeps({ loginWithEmail: vi.fn().mockResolvedValue(user) });
		const vm = createWeb3WalletViewModel(deps);
		await vm.handleEmailLogin('x@y.z', 'pw');
		expect(deps.loginWithEmail).toHaveBeenCalledWith('x@y.z', 'pw');
		expect(get(vm.walletConnected)).toBe(true);
		expect(get(vm.connectionType)).toBe('cyberdyne');
		expect(get(vm.currentUser)?.email).toBe('x@y.z');
		expect(get(vm.showConnectionModal)).toBe(false);
	});

	it('handleEmailLogin surfaces errors and stays signed out', async () => {
		const vm = createWeb3WalletViewModel(
			buildDeps({ loginWithEmail: vi.fn().mockRejectedValue(new Error('401')) })
		);
		await vm.handleEmailLogin('a@b.c', 'pw');
		expect(get(vm.walletConnected)).toBe(false);
		expect(get(vm.errorMessage)).toMatch(/401/);
	});

	it('handleGoogleLogin invokes the OAuth start', async () => {
		const deps = buildDeps();
		const vm = createWeb3WalletViewModel(deps);
		await vm.handleGoogleLogin();
		expect(deps.startGoogleOAuth).toHaveBeenCalled();
	});

	it('handleGoogleLogin shows error if start fails', async () => {
		const vm = createWeb3WalletViewModel(
			buildDeps({ startGoogleOAuth: vi.fn().mockRejectedValue(new Error('network')) })
		);
		await vm.handleGoogleLogin();
		expect(get(vm.errorMessage)).toMatch(/network/);
	});

	it('handleWalletSignIn → wallet connect → fires SIWE reactively', async () => {
		const deps = buildDeps({ loginWithWallet: vi.fn().mockResolvedValue(user) });
		const vm = createWeb3WalletViewModel(deps);

		await vm.handleWalletSignIn();
		expect(deps.loginWithWallet).not.toHaveBeenCalled();
		expect(get(vm.showConnectionModal)).toBe(false);

		// Simulate AppKit reporting a successful connection.
		vm.updateFromWalletConnect({
			address: '0xabc',
			balance: '1.0',
			chainId: 8453,
			isConnected: true
		});
		// Two microtask flushes — one for the inner promise chain, one
		// for the awaited verify call.
		await Promise.resolve();
		await Promise.resolve();

		expect(deps.loginWithWallet).toHaveBeenCalledTimes(1);
		const call = (deps.loginWithWallet as ReturnType<typeof vi.fn>).mock.calls[0][0];
		expect(call.walletAddress).toBe('0xabc');
		expect(call.chainId).toBe(8453);
		expect(typeof call.sign).toBe('function');
	});

	it('SIWE failure surfaces in errorMessage and clears loading', async () => {
		const vm = createWeb3WalletViewModel(
			buildDeps({ loginWithWallet: vi.fn().mockRejectedValue(new Error('user rejected')) })
		);
		await vm.handleWalletSignIn();
		vm.updateFromWalletConnect({
			address: '0xabc',
			balance: '1',
			chainId: 8453,
			isConnected: true
		});
		await Promise.resolve();
		await Promise.resolve();
		expect(get(vm.errorMessage)).toMatch(/user rejected/);
		expect(get(vm.isLoading)).toBe(false);
	});

	it('updateFromWalletConnect without pending SIWE just records wallet info', () => {
		const deps = buildDeps();
		const vm = createWeb3WalletViewModel(deps);
		vm.updateFromWalletConnect({
			address: '0xdef',
			balance: '2',
			chainId: 1,
			isConnected: true
		});
		expect(deps.loginWithWallet).not.toHaveBeenCalled();
		expect(get(vm.walletConnected)).toBe(true);
		expect(vm.snapshot().walletConnectInfo?.address).toBe('0xdef');
	});

	it('updateFromWalletConnect disconnect drops wallet state when no cyberdyne session', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		vm.updateFromWalletConnect({ address: '0xabc', balance: '1', chainId: 1, isConnected: true });
		vm.updateFromWalletConnect({ isConnected: false });
		expect(get(vm.walletConnected)).toBe(false);
		expect(get(vm.connectionType)).toBe(null);
	});

	it('handleDisconnect resets state', async () => {
		const deps = buildDeps({ loginWithEmail: vi.fn().mockResolvedValue(user) });
		const vm = createWeb3WalletViewModel(deps);
		await vm.handleEmailLogin('x@y.z', 'pw');
		expect(get(vm.walletConnected)).toBe(true);
		await vm.handleDisconnect();
		expect(get(vm.walletConnected)).toBe(false);
		expect(get(vm.connectionType)).toBe(null);
		expect(get(vm.currentUser)).toBe(null);
	});

	it('handleDisconnect surfaces partial-failure issues', async () => {
		const deps = buildDeps({
			disconnect: vi
				.fn()
				.mockResolvedValue({ success: false, errors: ['rpc down'], warnings: [] })
		});
		const vm = createWeb3WalletViewModel(deps);
		await vm.handleDisconnect();
		expect(get(vm.errorMessage)).toMatch(/rpc down/);
	});

	it('checkAuthStatus restores a wallet-bound session', async () => {
		const deps = buildDeps({ restoreSession: vi.fn().mockResolvedValue(user) });
		const vm = createWeb3WalletViewModel(deps);
		await vm.checkAuthStatus();
		expect(get(vm.walletConnected)).toBe(true);
		expect(get(vm.connectionType)).toBe('walletconnect');
		expect(deps.setGlobalWeb3Info).toHaveBeenCalledWith({
			address: '0xabc',
			balance: '',
			chainId: 8453,
			isConnected: true
		});
	});

	it('checkAuthStatus restores a non-wallet session as cyberdyne', async () => {
		const cyberdyneOnly: CyberdyneUserLike = { ...user, walletAddress: null };
		const vm = createWeb3WalletViewModel(
			buildDeps({ restoreSession: vi.fn().mockResolvedValue(cyberdyneOnly) })
		);
		await vm.checkAuthStatus();
		expect(get(vm.connectionType)).toBe('cyberdyne');
	});

	it('clearError empties the error string', async () => {
		const vm = createWeb3WalletViewModel(
			buildDeps({ loginWithEmail: vi.fn().mockRejectedValue(new Error('boom')) })
		);
		await vm.handleEmailLogin('a@b.c', 'pw');
		expect(get(vm.errorMessage)).toMatch(/boom/);
		vm.clearError();
		expect(get(vm.errorMessage)).toBe('');
	});

	it('resolveAddress falls back to user.walletAddress when no AppKit info', async () => {
		const deps = buildDeps({ loginWithEmail: vi.fn().mockResolvedValue(user) });
		const vm = createWeb3WalletViewModel(deps);
		await vm.handleEmailLogin('x@y.z', 'pw');
		expect(vm.resolveAddress()).toBe('0xabc');
	});

	it('resolveAddress returns empty string when nothing is set', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		expect(vm.resolveAddress()).toBe('');
	});
});
