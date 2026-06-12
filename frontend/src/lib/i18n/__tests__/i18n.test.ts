import { describe, it, expect, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import {
	translate,
	setLocale,
	locale,
	t,
	detectInitialLocale,
	SUPPORTED_LOCALES,
	type Locale
} from '$lib/i18n';
import { getRequestLocale } from '$lib/api/localeHeader';

const codes = SUPPORTED_LOCALES.map((l) => l.code);

describe('translate', () => {
	it('resolves a plain key', () => {
		expect(translate('en', 'common.close')).toBe('Close');
	});

	it('interpolates named params', () => {
		expect(translate('en', 'courses.lessonPosition', { index: 2, total: 5 })).toBe('Lesson 2 of 5');
	});

	it('leaves unknown params untouched', () => {
		expect(translate('en', 'courses.nextLesson', {})).toBe('Next lesson → {title}');
	});

	it('selects the plural form via Intl.PluralRules when count is present', () => {
		expect(translate('en', 'courses.lessonsCount', { count: 1 })).toBe('📘 1 lesson');
		expect(translate('en', 'courses.lessonsCount', { count: 4 })).toBe('📘 4 lessons');
	});

	it('uses the base key when count is present but no plural variants exist', () => {
		expect(translate('en', 'common.close', { count: 2 })).toBe('Close');
	});

	it('falls back to English for an unknown locale code', () => {
		expect(translate('xx' as Locale, 'common.close')).toBe('Close');
	});

	it('falls back to the key itself for an unknown key', () => {
		expect(translate('en', 'does.not.exist')).toBe('does.not.exist');
	});

	it('translates per locale', () => {
		expect(translate('pt-BR', 'common.close')).toBe('Fechar');
		expect(translate('es', 'common.close')).toBe('Cerrar');
		expect(translate('fr', 'common.close')).toBe('Fermer');
	});
});

describe('locale store', () => {
	beforeEach(() => {
		localStorage.clear();
		setLocale('en');
	});

	it('setLocale updates the store and persists to localStorage', () => {
		setLocale('es');
		expect(get(locale)).toBe('es');
		expect(JSON.parse(localStorage.getItem('cyberdyne.locale') as string)).toBe('es');
	});

	it('ignores unsupported codes', () => {
		setLocale('es');
		setLocale('klingon');
		expect(get(locale)).toBe('es');
	});

	it('mirrors the active locale into the API request header holder', () => {
		setLocale('fr');
		expect(getRequestLocale()).toBe('fr');
	});

	it('the reactive `t` translator reflects the active locale', () => {
		setLocale('fr');
		expect(get(t)('common.close')).toBe('Fermer');
		setLocale('pt-BR');
		expect(get(t)('common.close')).toBe('Fechar');
	});
});

describe('detectInitialLocale', () => {
	beforeEach(() => localStorage.clear());

	it('prefers a previously persisted choice', () => {
		localStorage.setItem('cyberdyne.locale', JSON.stringify('fr'));
		expect(detectInitialLocale()).toBe('fr');
	});

	it('ignores a persisted value that is not supported', () => {
		localStorage.setItem('cyberdyne.locale', JSON.stringify('klingon'));
		expect(codes).toContain(detectInitialLocale());
	});

	it('always returns a supported locale', () => {
		localStorage.clear();
		expect(codes).toContain(detectInitialLocale());
	});
});
