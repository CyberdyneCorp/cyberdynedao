/**
 * Utility functions for browser storage with error handling
 */

/**
 * Safely get item from localStorage with JSON parsing
 */
export function getStorageItem<T>(key: string, defaultValue: T): T {
	if (typeof window === 'undefined') {
		return defaultValue;
	}
	
	try {
		const item = localStorage.getItem(key);
		return item ? JSON.parse(item) : defaultValue;
	} catch {
		return defaultValue;
	}
}

/**
 * Safely set item to localStorage with JSON stringification
 */
export function setStorageItem<T>(key: string, value: T): boolean {
	if (typeof window === 'undefined') {
		return false;
	}
	
	try {
		localStorage.setItem(key, JSON.stringify(value));
		return true;
	} catch {
		return false;
	}
}

/**
 * Remove item from localStorage
 */
export function removeStorageItem(key: string): boolean {
	if (typeof window === 'undefined') {
		return false;
	}
	
	try {
		localStorage.removeItem(key);
		return true;
	} catch {
		return false;
	}
}

/**
 * Clear all items from localStorage
 */
export function clearStorage(): boolean {
	if (typeof window === 'undefined') {
		return false;
	}
	
	try {
		localStorage.clear();
		return true;
	} catch {
		return false;
	}
}

/**
 * Check if localStorage is available
 */
export function isStorageAvailable(): boolean {
	if (typeof window === 'undefined') {
		return false;
	}
	
	try {
		const test = '__storage_test__';
		localStorage.setItem(test, 'test');
		localStorage.removeItem(test);
		return true;
	} catch {
		return false;
	}
}