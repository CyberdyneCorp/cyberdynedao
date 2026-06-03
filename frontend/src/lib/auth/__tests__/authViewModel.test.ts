import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// Mock the HTTP service so installSession's getProfile() is deterministic.
vi.mock('../cyberdyneAuthService', () => ({
	getProfile: vi.fn(),
	login: vi.fn(),
	logout: vi.fn(),
	refresh: vi.fn(),
	walletChallenge: vi.fn(),
	walletVerify: vi.fn()
}));

import { getProfile } from '../cyberdyneAuthService';
import { createAuthVM } from '../authViewModel.svelte';

const mockedGetProfile = vi.mocked(getProfile);

beforeEach(() => {
	sessionStorage.clear();
});

afterEach(() => {
	vi.restoreAllMocks();
	vi.clearAllMocks();
});

describe('authViewModel admin/editor detection', () => {
	// Regression: CyberdyneAuth now surfaces is_admin on GET /users/me
	// (issue CyberdyneAuth#12). The login flow must carry it through so
	// the System Admin surface unlocks. Before the upstream fix there was
	// no admin signal at all, so this path could not be covered.
	it('isAdmin is true when /users/me returns is_admin', async () => {
		mockedGetProfile.mockResolvedValue({
			id: '968a70af-8b4c-413c-a502-fe0fbe9ce3ad',
			email: 'leotest@test.com',
			is_admin: true
		});
		const vm = createAuthVM();
		await vm.installSession('access-token', 'refresh-token');
		expect(vm.isAdmin).toBe(true);
		expect(vm.isEditor).toBe(false);
	});

	it('isEditor is true when the profile carries the editor scope', async () => {
		mockedGetProfile.mockResolvedValue({
			id: 'u1',
			email: 'editor@test.com',
			scopes: ['editor']
		});
		const vm = createAuthVM();
		await vm.installSession('access-token', 'refresh-token');
		expect(vm.isEditor).toBe(true);
		expect(vm.isAdmin).toBe(false);
	});

	it('both are false for a plain authenticated user', async () => {
		mockedGetProfile.mockResolvedValue({
			id: 'u2',
			email: 'user@test.com'
		});
		const vm = createAuthVM();
		await vm.installSession('access-token', 'refresh-token');
		expect(vm.isAuthenticated).toBe(true);
		expect(vm.isAdmin).toBe(false);
		expect(vm.isEditor).toBe(false);
	});

	it('a preloaded admin user is honored without a profile fetch', async () => {
		const vm = createAuthVM();
		await vm.installSession('access-token', 'refresh-token', {
			id: 'u3',
			email: 'admin@test.com',
			is_admin: true
		});
		expect(vm.isAdmin).toBe(true);
		expect(mockedGetProfile).not.toHaveBeenCalled();
	});
});
