import { writable, get } from 'svelte/store';

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
	isSlideHidden: boolean;
	originalX?: number;
	originalY?: number;
	content: 'read' | 'shop' | 'cart' | 'investments' | 'watch' | 'listen' | 'substack' | 'contact' | 'dao' | 'products' | 'team' | 'terminal' | 'services' | 'cyberdyne';
}

export const windows = writable<WindowState[]>([]);

export function createWindow(content: WindowState['content'], title: string) {
	windows.update(wins => {
		// Calculate screen dimensions (using browser window if available)
		const screenWidth = (typeof globalThis !== 'undefined' && globalThis.innerWidth) ? globalThis.innerWidth : 1920;
		const screenHeight = (typeof globalThis !== 'undefined' && globalThis.innerHeight) ? globalThis.innerHeight : 1080;

		let x, y, width, height;

		// Position cart windows in bottom right corner by default
		if (content === 'cart') {
			width = Math.min(350, Math.max(280, screenWidth - 32));
			height = Math.min(650, screenHeight - 100);
			x = Math.max(16, screenWidth - width - 20);
			y = Math.max(16, screenHeight - height - 60);
		} else {
			// Default desired size, clamped to fit viewport with sensible margins
			width = Math.min(800, Math.max(280, screenWidth - 32));
			height = Math.min(600, Math.max(200, screenHeight - 120));
			const cascade = wins.length * 30;
			x = Math.max(16, Math.min(100 + cascade, screenWidth - width - 16));
			y = Math.max(16, Math.min(50 + cascade, screenHeight - height - 16));
		}

		const newWindow: WindowState = {
			id: `window-${Date.now()}`,
			title,
			x,
			y,
			width,
			height,
			zIndex: 100 + wins.length,
			minimized: false,
			maximized: false,
			isSlideHidden: false,
			content
		};
		return [...wins, newWindow];
	});
}

export function closeWindow(id: string) {
	windows.update(wins => wins.filter(w => w.id !== id));
}

export function closeAllWindows() {
	windows.set([]);
}


export function bringToFront(id: string) {
	windows.update(wins => wins.map(w => 
		w.id === id ? { ...w, zIndex: wins.reduce((max, win) => Math.max(max, win.zIndex), 0) + 1 } : w
	));
}

export function slideWindowsToEdges() {
	windows.update(wins => 
		wins.map(windowItem => {
			if (windowItem.minimized || windowItem.isSlideHidden) return windowItem;

			// Store original position if not already stored
			if (windowItem.originalX === undefined) {
				windowItem.originalX = windowItem.x;
				windowItem.originalY = windowItem.y;
			}

			// Calculate screen dimensions (using browser window if available)
			const screenWidth = (typeof globalThis !== 'undefined' && globalThis.innerWidth) ? globalThis.innerWidth : 1920;
			const screenHeight = (typeof globalThis !== 'undefined' && globalThis.innerHeight) ? globalThis.innerHeight : 1080;
			
			// Calculate center of window
			const windowCenterX = windowItem.x + windowItem.width / 2;
			const windowCenterY = windowItem.y + windowItem.height / 2;
			
			// Calculate distances to each edge
			const distanceToLeft = windowCenterX;
			const distanceToRight = screenWidth - windowCenterX;
			const distanceToTop = windowCenterY;
			const distanceToBottom = screenHeight - windowCenterY;
			
			// Find the closest edge
			const minDistance = Math.min(distanceToLeft, distanceToRight, distanceToTop, distanceToBottom);
			
			let newX = windowItem.x;
			let newY = windowItem.y;
			
			if (minDistance === distanceToLeft) {
				// Slide to left edge
				newX = -windowItem.width * 0.8;
			} else if (minDistance === distanceToRight) {
				// Slide to right edge
				newX = screenWidth - windowItem.width * 0.2;
			} else if (minDistance === distanceToTop) {
				// Slide to top edge
				newY = -windowItem.height * 0.8;
			} else {
				// Slide to bottom edge
				newY = screenHeight - windowItem.height * 0.2;
			}
			
			return {
				...windowItem,
				x: newX,
				y: newY,
				isSlideHidden: true
			};
		})
	);
}

export function slideWindowsBack() {
	windows.update(wins => 
		wins.map(windowItem => {
			if (!windowItem.isSlideHidden || windowItem.originalX === undefined) return windowItem;
			
			return {
				...windowItem,
				x: windowItem.originalX,
				y: windowItem.originalY!,
				isSlideHidden: false,
				originalX: undefined,
				originalY: undefined
			};
		})
	);
}

export function toggleWindowSlide() {
	const currentWindows = get(windows);
	const hasHiddenWindows = currentWindows.some(w => w.isSlideHidden);
	
	if (hasHiddenWindows) {
		slideWindowsBack();
	} else {
		slideWindowsToEdges();
	}
}

