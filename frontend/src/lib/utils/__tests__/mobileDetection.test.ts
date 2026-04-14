import { describe, it, expect, beforeEach } from 'vitest';
import {
	isMobileDevice,
	isTabletDevice,
	isSmallMobileDevice,
	getDeviceType,
	isBreakpoint,
	getCurrentBreakpoint,
	BREAKPOINTS
} from '../mobileDetection';

function setWidth(w: number) {
	Object.defineProperty(window, 'innerWidth', { configurable: true, value: w, writable: true });
}
function setUserAgent(ua: string) {
	Object.defineProperty(navigator, 'userAgent', { configurable: true, value: ua });
}

describe('mobileDetection', () => {
	beforeEach(() => {
		setWidth(1200);
		setUserAgent('Mozilla/5.0 Desktop');
		Object.defineProperty(navigator, 'maxTouchPoints', { configurable: true, value: 0 });
		// jsdom ships 'ontouchstart' on window; delete to simulate desktop default.
		delete (window as Window & { ontouchstart?: unknown }).ontouchstart;
	});

	it('exports breakpoints', () => {
		expect(BREAKPOINTS.mobile).toBe(768);
	});

	it('desktop when wide', () => {
		expect(getDeviceType()).toBe('desktop');
		expect(getCurrentBreakpoint()).toBe('desktop');
		expect(isBreakpoint('desktop')).toBe(true);
	});

	it('mobile small screen', () => {
		setWidth(400);
		expect(isSmallMobileDevice()).toBe(true);
		expect(getDeviceType()).toBe('mobile');
		expect(getCurrentBreakpoint()).toBe('mobile');
		expect(isBreakpoint('mobile')).toBe(true);
	});

	it('tablet range', () => {
		setWidth(900);
		expect(isTabletDevice()).toBe(true);
		expect(getDeviceType()).toBe('tablet');
		expect(getCurrentBreakpoint()).toBe('tablet');
		expect(isBreakpoint('tablet')).toBe(true);
	});

	it('detects mobile via user agent', () => {
		setWidth(1200);
		setUserAgent('Mozilla/5.0 iPhone');
		expect(isMobileDevice()).toBe(true);
	});

	it('detects mobile via touch support', () => {
		setWidth(1200);
		Object.defineProperty(navigator, 'maxTouchPoints', { configurable: true, value: 5 });
		expect(isMobileDevice()).toBe(true);
	});

	it('isBreakpoint unknown returns false', () => {
		// @ts-expect-error testing invalid value
		expect(isBreakpoint('foo')).toBe(false);
	});
});
