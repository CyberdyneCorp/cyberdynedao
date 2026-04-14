import { describe, it, expect, vi } from 'vitest';
import { get } from 'svelte/store';
import {
	createWeb3WalletViewModel,
	type Web3AuthUserLike,
	type Web3WalletDeps
} from '../web3WalletViewModel';

function buildDeps(overrides: Partial<Web3WalletDeps> = {}): Web3WalletDeps {
	return {
		connectWalletConnect: vi.fn().mockResolvedValue(undefined),
		connectWeb3Auth: vi.fn().mockResolvedValue(null),
		disconnect: vi.fn().mockResolvedValue({ success: true, errors: [], warnings: [] }),
		checkAuthStatus: vi.fn().mockResolvedValue(null),
		setGlobalWeb3Info: vi.fn(),
		...overrides
	};
}

const user: Web3AuthUserLike = {
	address: '0xabc',
	balance: '1.0',
	userInfo: { email: 'x@y.z', name: 'X' }
};

describe('web3WalletViewModel', () => {
	it('initial state', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		expect(get(vm.walletConnected)).toBe(false);
		expect(get(vm.errorMessage)).toBe('');
		expect(get(vm.isLoading)).toBe(false);
	});

	it('toggleDetails flips flag', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		vm.toggleDetails();
		expect(get(vm.showDetails)).toBe(true);
		vm.toggleDetails();
		expect(get(vm.showDetails)).toBe(false);
	});

	it('connection modal open/close + NFT terminal open/close', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		vm.openConnectionModal();
		expect(get(vm.showConnectionModal)).toBe(true);
		vm.closeConnectionModal();
		expect(get(vm.showConnectionModal)).toBe(false);
		vm.openNFTTerminal();
		expect(get(vm.showNFTTerminal)).toBe(true);
		vm.closeNFTTerminal();
		expect(get(vm.showNFTTerminal)).toBe(false);
	});

	it('clearError clears', () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWalletConnect: vi.fn().mockRejectedValue(new Error('boom'))
		}));
		return vm.handleWalletConnect().then(() => {
			expect(get(vm.errorMessage)).toMatch(/boom/);
			vm.clearError();
			expect(get(vm.errorMessage)).toBe('');
		});
	});

	it('handleWalletConnect success clears error and stops loading', async () => {
		const deps = buildDeps();
		const vm = createWeb3WalletViewModel(deps);
		await vm.handleWalletConnect();
		expect(deps.connectWalletConnect).toHaveBeenCalled();
		expect(get(vm.errorMessage)).toBe('');
		expect(get(vm.isLoading)).toBe(false);
	});

	it('handleWalletConnect failure sets error', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWalletConnect: vi.fn().mockRejectedValue(new Error('network'))
		}));
		await vm.handleWalletConnect();
		expect(get(vm.errorMessage)).toMatch(/WalletConnect failed/);
	});

	it('handleWalletConnect failure with non-Error', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWalletConnect: vi.fn().mockRejectedValue('nope')
		}));
		await vm.handleWalletConnect();
		expect(get(vm.errorMessage)).toContain('nope');
	});

	it('handleWeb3AuthConnect with user updates state and global info', async () => {
		const setInfo = vi.fn();
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWeb3Auth: vi.fn().mockResolvedValue(user),
			setGlobalWeb3Info: setInfo
		}));
		await vm.handleWeb3AuthConnect();
		expect(get(vm.walletConnected)).toBe(true);
		expect(get(vm.connectionType)).toBe('web3auth');
		expect(setInfo).toHaveBeenCalledWith(expect.objectContaining({ address: user.address }));
	});

	it('handleWeb3AuthConnect without user does nothing', async () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		await vm.handleWeb3AuthConnect();
		expect(get(vm.walletConnected)).toBe(false);
	});

	it('handleWeb3AuthConnect failure resets state', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWeb3Auth: vi.fn().mockRejectedValue(new Error('oauth down'))
		}));
		await vm.handleWeb3AuthConnect();
		expect(get(vm.errorMessage)).toMatch(/Login failed/);
		expect(get(vm.walletConnected)).toBe(false);
	});

	it('handleWeb3AuthConnect failure with non-Error', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWeb3Auth: vi.fn().mockRejectedValue('oops')
		}));
		await vm.handleWeb3AuthConnect();
		expect(get(vm.errorMessage)).toContain('oops');
	});

	it('handleDisconnect success clears state', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWeb3Auth: vi.fn().mockResolvedValue(user)
		}));
		await vm.handleWeb3AuthConnect();
		await vm.handleDisconnect();
		expect(get(vm.walletConnected)).toBe(false);
		expect(get(vm.errorMessage)).toBe('');
	});

	it('handleDisconnect with result errors sets error message', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			disconnect: vi.fn().mockResolvedValue({ success: false, errors: ['e1'], warnings: [] })
		}));
		await vm.handleDisconnect();
		expect(get(vm.errorMessage)).toMatch(/e1/);
	});

	it('handleDisconnect with thrown error sets error', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			disconnect: vi.fn().mockRejectedValue(new Error('rpc'))
		}));
		await vm.handleDisconnect();
		expect(get(vm.errorMessage)).toMatch(/Unexpected/);
	});

	it('handleDisconnect with non-Error thrown', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			disconnect: vi.fn().mockRejectedValue(null)
		}));
		await vm.handleDisconnect();
		expect(get(vm.errorMessage)).toMatch(/Unknown/);
	});

	it('checkAuthStatus restores session when user found', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			checkAuthStatus: vi.fn().mockResolvedValue(user)
		}));
		await vm.checkAuthStatus();
		expect(get(vm.walletConnected)).toBe(true);
		expect(get(vm.currentUser)).toEqual(user);
	});

	it('checkAuthStatus swallows errors', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			checkAuthStatus: vi.fn().mockRejectedValue(new Error('x'))
		}));
		await expect(vm.checkAuthStatus()).resolves.toBeUndefined();
	});

	it('updateFromWalletConnect sets connected when walletconnect connects', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		vm.updateFromWalletConnect({ isConnected: true, address: '0x1', chainId: 1 });
		expect(get(vm.walletConnected)).toBe(true);
		expect(get(vm.connectionType)).toBe('walletconnect');
	});

	it('updateFromWalletConnect preserves web3auth connection', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWeb3Auth: vi.fn().mockResolvedValue(user)
		}));
		await vm.handleWeb3AuthConnect();
		vm.updateFromWalletConnect({ isConnected: true });
		expect(get(vm.connectionType)).toBe('web3auth');
	});

	it('updateFromWalletConnect on disconnect preserves web3auth', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWeb3Auth: vi.fn().mockResolvedValue(user)
		}));
		await vm.handleWeb3AuthConnect();
		vm.updateFromWalletConnect({ isConnected: false });
		expect(get(vm.walletConnected)).toBe(true);
	});

	it('updateFromWalletConnect on disconnect with no user clears all', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		vm.updateFromWalletConnect({ isConnected: true, address: '0x1' });
		vm.updateFromWalletConnect({ isConnected: false });
		expect(get(vm.walletConnected)).toBe(false);
		expect(get(vm.connectionType)).toBeNull();
	});

	it('resolveAddress branches', async () => {
		const vm = createWeb3WalletViewModel(buildDeps({
			connectWeb3Auth: vi.fn().mockResolvedValue(user)
		}));
		expect(vm.resolveAddress()).toBe('');

		await vm.handleWeb3AuthConnect();
		expect(vm.resolveAddress()).toBe(user.address);

		const vm2 = createWeb3WalletViewModel(buildDeps());
		vm2.updateFromWalletConnect({ isConnected: true, address: '0xWC' });
		expect(vm2.resolveAddress()).toBe('0xWC');
	});

	it('snapshot returns full state', () => {
		const vm = createWeb3WalletViewModel(buildDeps());
		const snap = vm.snapshot();
		expect(snap.walletConnected).toBe(false);
	});
});
