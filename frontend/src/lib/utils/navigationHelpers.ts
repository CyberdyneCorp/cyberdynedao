import { createWindow } from '$lib/stores/windowStore';
import { viewMap, type NavItem } from '$lib/constants/navigation';

/**
 * Shared handler for navigation item clicks
 * Used by both main page and sidebar components
 */
export function handleItemClick(item: NavItem): void {
	const view = viewMap[item.name] || item.name.toLowerCase();
	createWindow(view, item.name);
}