import { describe, it, expect } from 'vitest';
import {
	validateEmail,
	validateRequired,
	validateLength,
	validateNumberRange,
	validateWalletAddress,
	validateField
} from '../validation';

describe('validation', () => {
	describe('validateEmail', () => {
		it('accepts valid emails', () => {
			expect(validateEmail('user@example.com')).toBe(true);
		});
		it('rejects invalid emails', () => {
			expect(validateEmail('not-an-email')).toBe(false);
			expect(validateEmail('user@')).toBe(false);
			expect(validateEmail('')).toBe(false);
		});
	});

	describe('validateRequired', () => {
		it('returns true for non-empty strings', () => {
			expect(validateRequired('hello')).toBe(true);
		});
		it('returns false for whitespace or empty', () => {
			expect(validateRequired('   ')).toBe(false);
			expect(validateRequired('')).toBe(false);
		});
	});

	describe('validateLength', () => {
		it('accepts strings within bounds', () => {
			expect(validateLength('hello', 3, 10)).toBe(true);
		});
		it('rejects strings outside bounds', () => {
			expect(validateLength('hi', 3, 10)).toBe(false);
			expect(validateLength('this is long', 3, 5)).toBe(false);
		});
	});

	describe('validateNumberRange', () => {
		it('accepts numbers within range', () => {
			expect(validateNumberRange(5, 1, 10)).toBe(true);
		});
		it('rejects out of range', () => {
			expect(validateNumberRange(0, 1, 10)).toBe(false);
			expect(validateNumberRange(11, 1, 10)).toBe(false);
		});
	});

	describe('validateWalletAddress', () => {
		it('accepts valid Ethereum addresses', () => {
			expect(validateWalletAddress('0x' + 'a'.repeat(40))).toBe(true);
		});
		it('rejects invalid addresses', () => {
			expect(validateWalletAddress('0xabc')).toBe(false);
			expect(validateWalletAddress('not-an-address')).toBe(false);
		});
	});

	describe('validateField', () => {
		it('validates required field', () => {
			expect(validateField('', 'required').isValid).toBe(false);
			expect(validateField('x', 'required').isValid).toBe(true);
		});
		it('validates email field', () => {
			expect(validateField('', 'email').errors[0]).toMatch(/required/i);
			expect(validateField('bad', 'email').errors[0]).toMatch(/valid/i);
			expect(validateField('a@b.co', 'email').isValid).toBe(true);
		});
		it('validates wallet field', () => {
			expect(validateField('', 'wallet').errors[0]).toMatch(/required/i);
			expect(validateField('0xBAD', 'wallet').errors[0]).toMatch(/valid/i);
			expect(validateField('0x' + 'a'.repeat(40), 'wallet').isValid).toBe(true);
		});
		it('validates text field with bounds', () => {
			const r = validateField('a', 'text', { minLength: 3, maxLength: 5 });
			expect(r.isValid).toBe(false);
			expect(validateField('abcd', 'text', { minLength: 3, maxLength: 5 }).isValid).toBe(true);
		});
		it('text without options returns valid', () => {
			expect(validateField('x', 'text').isValid).toBe(true);
		});
		it('text with only minLength uses Infinity max', () => {
			expect(validateField('ab', 'text', { minLength: 5 }).isValid).toBe(false);
		});
	});
});
