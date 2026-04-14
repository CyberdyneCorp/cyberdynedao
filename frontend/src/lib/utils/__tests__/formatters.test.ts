import { describe, it, expect } from 'vitest';
import {
	formatDate,
	formatDateObject,
	formatPrice,
	formatNumber,
	formatPercentage,
	truncateText
} from '../formatters';

describe('formatters', () => {
	describe('formatDate', () => {
		it('formats ISO date string to readable US format', () => {
			expect(formatDate('2024-01-15')).toMatch(/Jan\s+(14|15),\s+2024/);
		});
	});

	describe('formatDateObject', () => {
		it('formats Date object to readable US format', () => {
			const date = new Date('2024-05-20T12:00:00Z');
			expect(formatDateObject(date)).toMatch(/May\s+20,\s+2024/);
		});
	});

	describe('formatPrice', () => {
		it('returns $X for values under 1000', () => {
			expect(formatPrice(99)).toBe('$99');
			expect(formatPrice(999)).toBe('$999');
		});
		it('returns $X.Xk for 1000 and above', () => {
			expect(formatPrice(1000)).toBe('$1.0k');
			expect(formatPrice(2499)).toBe('$2.5k');
			expect(formatPrice(12000)).toBe('$12.0k');
		});
	});

	describe('formatNumber', () => {
		it('returns M suffix for millions', () => {
			expect(formatNumber(1_500_000)).toBe('1.5M');
		});
		it('returns K suffix for thousands', () => {
			expect(formatNumber(2500)).toBe('2.5K');
		});
		it('returns plain string for small numbers', () => {
			expect(formatNumber(42)).toBe('42');
		});
	});

	describe('formatPercentage', () => {
		it('formats with 2 decimal places and % suffix', () => {
			expect(formatPercentage(12.3456)).toBe('12.35%');
			expect(formatPercentage(0)).toBe('0.00%');
		});
	});

	describe('truncateText', () => {
		it('truncates and adds ellipsis when over maxLength', () => {
			expect(truncateText('hello world', 5)).toBe('hello...');
		});
		it('returns unchanged when within maxLength', () => {
			expect(truncateText('hi', 10)).toBe('hi');
		});
	});
});
