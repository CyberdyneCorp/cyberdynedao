/**
 * Lightweight, dependency-free i18n for the Cyberdyne shell.
 *
 * Design goals (see PR plan):
 *  - Reuse the existing persisted-store pattern (`createPersistedStore`)
 *    so the chosen locale survives reloads via localStorage.
 *  - Runes-friendly: components read `$t('some.key')` and re-render when
 *    the locale changes (`t` is a derived store of a translator fn).
 *  - No build step, no codegen — catalogs are plain typed modules.
 *
 * Catalogs live in `./locales`. `en` is the source of truth and exports
 * the `Messages` type; the other locales are typed against it so the
 * compiler flags any missing/renamed key.
 */
import { derived, type Readable } from 'svelte/store';
import { createPersistedStore } from '$lib/stores/commonStore';
import { setRequestLocale } from '$lib/api/localeHeader';
import { en } from './locales/en';
import { ptBR } from './locales/pt-BR';
import { es } from './locales/es';
import { fr } from './locales/fr';
import type { Messages } from './locales/en';

export type Locale = 'en' | 'pt-BR' | 'es' | 'fr';

export interface LocaleMeta {
	code: Locale;
	/** English label (for accessibility / fallback). */
	label: string;
	/** Endonym — how speakers name their own language. */
	nativeLabel: string;
	/** Emoji flag used as a compact visual marker. */
	flag: string;
}

/** Ordered list backing the Settings language selector. */
export const SUPPORTED_LOCALES: readonly LocaleMeta[] = [
	{ code: 'en', label: 'English', nativeLabel: 'English', flag: '🇬🇧' },
	{ code: 'pt-BR', label: 'Portuguese (Brazil)', nativeLabel: 'Português (Brasil)', flag: '🇧🇷' },
	{ code: 'es', label: 'Spanish', nativeLabel: 'Español', flag: '🇪🇸' },
	{ code: 'fr', label: 'French', nativeLabel: 'Français', flag: '🇫🇷' }
];

const CATALOGS: Record<Locale, Messages> = {
	en,
	'pt-BR': ptBR,
	es,
	fr
};

const STORAGE_KEY = 'cyberdyne.locale';
const DEFAULT_LOCALE: Locale = 'en';

function isSupported(code: string): code is Locale {
	return SUPPORTED_LOCALES.some((l) => l.code === code);
}

/**
 * Best-effort match of a BCP-47 tag (e.g. `pt-BR`, `pt`, `es-419`) to a
 * supported locale. Exact match wins; otherwise the primary subtag is
 * compared (so `pt-PT` still resolves to our `pt-BR` catalogue).
 */
function matchLocale(tag: string | undefined | null): Locale | null {
	if (!tag) return null;
	if (isSupported(tag)) return tag;
	const primary = tag.toLowerCase().split('-')[0];
	const hit = SUPPORTED_LOCALES.find((l) => l.code.toLowerCase().split('-')[0] === primary);
	return hit?.code ?? null;
}

/**
 * Resolve the initial locale: a previously persisted choice wins, then
 * the browser's preferred languages, finally English. SSR-safe — falls
 * back to the default when there's no `window`/`navigator`.
 */
export function detectInitialLocale(): Locale {
	/* v8 ignore next */
	if (typeof window === 'undefined') return DEFAULT_LOCALE;

	try {
		const stored = localStorage.getItem(STORAGE_KEY);
		if (stored) {
			// createPersistedStore writes JSON, so a stored value is quoted.
			const parsed = JSON.parse(stored);
			if (typeof parsed === 'string' && isSupported(parsed)) return parsed;
		}
	} catch {
		/* ignore malformed storage */
	}

	const prefs = typeof navigator !== 'undefined' ? navigator.languages ?? [navigator.language] : [];
	for (const pref of prefs) {
		const matched = matchLocale(pref);
		if (matched) return matched;
	}
	return DEFAULT_LOCALE;
}

/** The active locale. Persisted to localStorage under `cyberdyne.locale`. */
export const locale = createPersistedStore<Locale>(STORAGE_KEY, detectInitialLocale());

/** Switch language. Ignores unknown codes so callers can pass raw input. */
export function setLocale(code: string): void {
	if (isSupported(code)) locale.set(code);
}

// Keep the document language attribute and the API request locale in
// sync with the active locale. Guarded for SSR / test environments.
locale.subscribe((code) => {
	setRequestLocale(code);
	/* v8 ignore next 3 */
	if (typeof document !== 'undefined') {
		document.documentElement.lang = code;
	}
});

export type TranslateParams = Record<string, string | number>;

function lookup(catalog: Messages, key: string): string | undefined {
	const value = (catalog as Record<string, unknown>)[key];
	return typeof value === 'string' ? value : undefined;
}

/** `{name}`-style interpolation. Missing params are left as-is. */
function interpolate(template: string, params?: TranslateParams): string {
	if (!params) return template;
	return template.replace(/\{(\w+)\}/g, (match, name: string) =>
		name in params ? String(params[name]) : match
	);
}

/**
 * Resolve `key` for `localeCode`, applying:
 *  - pluralization: when a numeric `count` param is present, prefer
 *    `key_one` / `key_other` (selected via `Intl.PluralRules`) over `key`;
 *  - fallback chain: active locale → English → the key itself;
 *  - `{param}` interpolation.
 */
export function translate(localeCode: Locale, key: string, params?: TranslateParams): string {
	const active = CATALOGS[localeCode] ?? en;

	let resolvedKey = key;
	if (params && typeof params.count === 'number') {
		const category = new Intl.PluralRules(localeCode).select(params.count);
		const pluralKey = `${key}_${category}`;
		if (lookup(active, pluralKey) !== undefined || lookup(en, pluralKey) !== undefined) {
			resolvedKey = pluralKey;
		} else if (lookup(active, `${key}_other`) !== undefined || lookup(en, `${key}_other`) !== undefined) {
			resolvedKey = `${key}_other`;
		}
	}

	const template = lookup(active, resolvedKey) ?? lookup(en, resolvedKey) ?? key;
	return interpolate(template, params);
}

export type TranslateFn = (key: string, params?: TranslateParams) => string;

/**
 * Reactive translator. Components use `$t('key')`; the function identity
 * changes whenever the locale changes, so Svelte re-runs dependent markup.
 */
export const t: Readable<TranslateFn> = derived(
	locale,
	($locale) => (key: string, params?: TranslateParams) => translate($locale, key, params)
);

export type { Messages };
