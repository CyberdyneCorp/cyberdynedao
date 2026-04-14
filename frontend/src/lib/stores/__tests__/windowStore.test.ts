import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { get } from 'svelte/store';
import {
	windows,
	createWindow,
	closeWindow,
	closeAllWindows,
	bringToFront,
	slideWindowsToEdges,
	slideWindowsBack,
	toggleWindowSlide
} from '../windowStore';

describe('windowStore', () => {
	let nowCounter = 0;
	beforeEach(() => {
		closeAllWindows();
		nowCounter = 0;
		vi.spyOn(Date, 'now').mockImplementation(() => ++nowCounter);
		Object.defineProperty(window, 'innerWidth', { configurable: true, value: 1920 });
		Object.defineProperty(window, 'innerHeight', { configurable: true, value: 1080 });
	});
	afterEach(() => {
		vi.restoreAllMocks();
	});

	it('createWindow adds a default-positioned window', () => {
		createWindow('read', 'Read');
		const wins = get(windows);
		expect(wins).toHaveLength(1);
		expect(wins[0].title).toBe('Read');
		expect(wins[0].width).toBe(800);
	});

	it('createWindow("cart") uses bottom-right positioning', () => {
		createWindow('cart', 'Your Bag');
		const w = get(windows)[0];
		expect(w.width).toBe(350);
		expect(w.height).toBe(650);
	});

	it('closeWindow removes by id', () => {
		createWindow('read', 'a');
		createWindow('shop', 'b');
		const firstId = get(windows)[0].id;
		closeWindow(firstId);
		expect(get(windows)).toHaveLength(1);
	});

	it('closeAllWindows empties list', () => {
		createWindow('read', 'a');
		closeAllWindows();
		expect(get(windows)).toHaveLength(0);
	});

	it('bringToFront raises zIndex above others', () => {
		createWindow('read', 'a');
		createWindow('shop', 'b');
		const firstId = get(windows)[0].id;
		bringToFront(firstId);
		const updated = get(windows).find(w => w.id === firstId)!;
		const other = get(windows).find(w => w.id !== firstId)!;
		expect(updated.zIndex).toBeGreaterThan(other.zIndex);
	});

	it('slideWindowsToEdges marks isSlideHidden and stores original position', () => {
		createWindow('read', 'a');
		slideWindowsToEdges();
		const w = get(windows)[0];
		expect(w.isSlideHidden).toBe(true);
		expect(w.originalX).toBeDefined();
	});

	it('slideWindowsBack restores original position', () => {
		createWindow('read', 'a');
		const originalX = get(windows)[0].x;
		slideWindowsToEdges();
		slideWindowsBack();
		const w = get(windows)[0];
		expect(w.isSlideHidden).toBe(false);
		expect(w.x).toBe(originalX);
	});

	it('toggleWindowSlide slides then restores', () => {
		createWindow('read', 'a');
		toggleWindowSlide();
		expect(get(windows)[0].isSlideHidden).toBe(true);
		toggleWindowSlide();
		expect(get(windows)[0].isSlideHidden).toBe(false);
	});

	it('slideWindowsToEdges picks different edges based on center position', () => {
		createWindow('read', 'a');
		windows.update(ws => ws.map(w => ({ ...w, x: 1800, y: 100 })));
		slideWindowsToEdges();
		expect(get(windows)[0].isSlideHidden).toBe(true);

		slideWindowsBack();
		windows.update(ws => ws.map(w => ({ ...w, x: 50, y: 900 })));
		slideWindowsToEdges();
		expect(get(windows)[0].isSlideHidden).toBe(true);
	});

	it('slideWindowsToEdges skips minimized windows', () => {
		createWindow('read', 'a');
		windows.update(ws => ws.map(w => ({ ...w, minimized: true })));
		slideWindowsToEdges();
		expect(get(windows)[0].isSlideHidden).toBe(false);
	});
});
