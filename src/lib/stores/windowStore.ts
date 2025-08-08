import { writable } from 'svelte/store';

export interface WindowState {
	id: string;
	title: string;
	x: number;
	y: number;
	width: number;
	height: number;
	zIndex: number;
	minimized: boolean;
	maximized: boolean;
	content: 'read' | 'shop' | 'cart' | 'investments' | 'watch' | 'listen' | 'substack' | 'contact' | 'enigma';
}

export const windows = writable<WindowState[]>([]);
export const activeWindowId = writable<string | null>(null);
export const nextZIndex = writable(100);

export function createWindow(content: WindowState['content'], title: string) {
	windows.update(wins => {
		const newWindow: WindowState = {
			id: `window-${Date.now()}`,
			title,
			x: 100 + wins.length * 30,
			y: 50 + wins.length * 30,
			width: 800,
			height: 600,
			zIndex: 100 + wins.length,
			minimized: false,
			maximized: false,
			content
		};
		return [...wins, newWindow];
	});
}

export function closeWindow(id: string) {
	windows.update(wins => wins.filter(w => w.id !== id));
}

export function minimizeWindow(id: string) {
	windows.update(wins => wins.map(w => 
		w.id === id ? { ...w, minimized: !w.minimized } : w
	));
}

export function maximizeWindow(id: string) {
	windows.update(wins => wins.map(w => 
		w.id === id ? { ...w, maximized: !w.maximized } : w
	));
}

export function bringToFront(id: string) {
	nextZIndex.update(z => z + 1);
	windows.update(wins => wins.map(w => 
		w.id === id ? { ...w, zIndex: wins.reduce((max, win) => Math.max(max, win.zIndex), 0) + 1 } : w
	));
	activeWindowId.set(id);
}