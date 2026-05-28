/**
 * Shared types for the custom StartMenu component. Lives in a sibling
 * .ts file because Svelte 5 runes-mode <script> can't export interfaces.
 */

export interface StartMenuEntry {
	id: string;
	label: string;
	icon: string;
	badge?: number;
	children?: StartMenuEntry[];
}

export interface StartMenuSection {
	id: string;
	label: string;
	items: StartMenuEntry[];
}
