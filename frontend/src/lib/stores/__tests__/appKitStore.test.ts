import { describe, it, expect, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import {
	appKitStore,
	appKitInstance,
	isAppKitInitialized,
	isAppKitLoading,
	appKitError,
	walletInfo,
	isWalletConnected,
	connectedAddress,
	connectedChainId,
	walletBalance,
	appKitActions,
	formatAddress,
	formatBalance,
	isValidWalletConnection,
	setValidatedWalletInfo,
	getNetworkName
} from '../appKitStore';

describe('appKitStore', () => {
	beforeEach(() => {
		appKitActions.reset();
		appKitInstance.set(null);
		localStorage.clear();
		sessionStorage.clear();
	});

	it('initial derived getters', () => {
		expect(get(isAppKitInitialized)).toBe(false);
		expect(get(isAppKitLoading)).toBe(false);
		expect(get(appKitError)).toBeNull();
		expect(get(isWalletConnected)).toBe(false);
		expect(get(connectedAddress)).toBeUndefined();
		expect(get(connectedChainId)).toBeUndefined();
		expect(get(walletBalance)).toBeUndefined();
	});

	it('appKitActions manipulate state', () => {
		appKitActions.setInitialized(true);
		expect(get(isAppKitInitialized)).toBe(true);

		appKitActions.setLoading(true);
		expect(get(isAppKitLoading)).toBe(true);

		appKitActions.setError('oops');
		expect(get(appKitError)).toBe('oops');
		appKitActions.clearError();
		expect(get(appKitError)).toBeNull();

		appKitActions.setWalletInfo({ isConnected: true, address: '0x1', chainId: 1, balance: '1' });
		expect(get(walletInfo).isConnected).toBe(true);

		appKitActions.setChainId(8453);
		expect(get(walletInfo).chainId).toBe(8453);

		appKitActions.setDisconnected();
		expect(get(walletInfo).isConnected).toBe(false);
	});

	it('reset restores initial state', () => {
		appKitActions.setInitialized(true);
		appKitActions.reset();
		expect(get(isAppKitInitialized)).toBe(false);
	});

	it('completeDisconnect clears wallet-related storage', () => {
		localStorage.setItem('wc@session', 'x');
		localStorage.setItem('keep-this', 'y');
		sessionStorage.setItem('walletconnect', 'z');

		appKitActions.completeDisconnect();

		expect(localStorage.getItem('wc@session')).toBeNull();
		expect(localStorage.getItem('keep-this')).toBe('y');
		expect(sessionStorage.getItem('walletconnect')).toBeNull();
	});

	it('formatAddress returns truncated form', () => {
		expect(formatAddress('0x1234567890abcdef')).toBe('0x1234...cdef');
		expect(formatAddress()).toBe('');
	});

	it('formatBalance formats various ranges', () => {
		expect(formatBalance()).toBe('0');
		expect(formatBalance('0')).toBe('0');
		expect(formatBalance('0.00001')).toBe('< 0.0001');
		expect(formatBalance('0.5')).toBe('0.5000');
		expect(formatBalance('12.3456')).toBe('12.346');
		expect(formatBalance('12345')).toBe('12.35k');
		// parseFloat returns NaN for unparseable input; function still produces a string.
		expect(typeof formatBalance('bad-number')).toBe('string');
	});

	it('isValidWalletConnection requires all fields', () => {
		expect(isValidWalletConnection({ isConnected: true, address: '0xabc', chainId: 1 })).toBe(true);
		expect(isValidWalletConnection({ isConnected: false, address: '0xabc', chainId: 1 })).toBe(false);
		expect(isValidWalletConnection({ isConnected: true, chainId: 1 })).toBe(false);
		expect(isValidWalletConnection({ isConnected: true, address: '0xabc', chainId: 0 })).toBe(false);
	});

	it('setValidatedWalletInfo accepts valid, disconnects invalid', () => {
		setValidatedWalletInfo({ isConnected: true, address: '0xabc', chainId: 8453 });
		expect(get(walletInfo).address).toBe('0xabc');

		setValidatedWalletInfo({ isConnected: true, address: '', chainId: 0 });
		expect(get(walletInfo).isConnected).toBe(false);
	});

	it('getNetworkName maps known ids', () => {
		expect(getNetworkName(1)).toBe('Ethereum');
		expect(getNetworkName(8453)).toBe('Base');
		expect(getNetworkName()).toContain('Unknown');
		expect(getNetworkName(99999)).toContain('99999');
	});
});
