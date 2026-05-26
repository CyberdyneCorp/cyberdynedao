import { describe, expect, it, beforeEach } from 'vitest';
import { clearAuthToken, getAuthToken, setAuthToken, withAuth } from '../authToken';

describe('authToken', () => {
	beforeEach(() => clearAuthToken());

	it('round-trips set / get / clear', () => {
		expect(getAuthToken()).toBe(null);
		setAuthToken('abc123');
		expect(getAuthToken()).toBe('abc123');
		setAuthToken(null);
		expect(getAuthToken()).toBe(null);
	});

	it('withAuth adds the Authorization header when a token is set', () => {
		setAuthToken('tok');
		const h = withAuth({ 'content-type': 'application/json' });
		expect(h.get('authorization')).toBe('Bearer tok');
		expect(h.get('content-type')).toBe('application/json');
	});

	it('withAuth leaves a caller-provided Authorization header alone', () => {
		setAuthToken('tok');
		const h = withAuth({ authorization: 'Bearer override' });
		expect(h.get('authorization')).toBe('Bearer override');
	});

	it('withAuth omits Authorization when no token is set', () => {
		const h = withAuth({});
		expect(h.has('authorization')).toBe(false);
	});

	it('withAuth handles undefined init', () => {
		setAuthToken('tok');
		const h = withAuth();
		expect(h.get('authorization')).toBe('Bearer tok');
	});
});
