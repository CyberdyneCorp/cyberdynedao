import { describe, it, expect } from 'vitest';
import { en, type Messages } from '$lib/i18n/locales/en';
import { ptBR } from '$lib/i18n/locales/pt-BR';
import { es } from '$lib/i18n/locales/es';
import { fr } from '$lib/i18n/locales/fr';

/**
 * Regression guard against the most likely i18n bug: a translation that
 * drifts out of sync with the English source — a missing key, an empty
 * string, or a dropped `{placeholder}` (which would silently break
 * interpolation). TypeScript already enforces the key set at build time;
 * these tests also catch empties and placeholder mismatches that the
 * compiler can't see.
 */
const enKeys = Object.keys(en).sort();

const PLACEHOLDER = /\{(\w+)\}/g;
function placeholders(value: string): string[] {
	return (value.match(PLACEHOLDER) ?? []).sort();
}

const locales: [string, Messages][] = [
	['pt-BR', ptBR],
	['es', es],
	['fr', fr]
];

describe('catalog parity', () => {
	for (const [name, catalog] of locales) {
		describe(name, () => {
			it('has exactly the same keys as English', () => {
				expect(Object.keys(catalog).sort()).toEqual(enKeys);
			});

			it('has no empty translations', () => {
				for (const [key, value] of Object.entries(catalog)) {
					expect(value.trim(), key).not.toBe('');
				}
			});

			it('preserves every interpolation placeholder', () => {
				for (const key of enKeys) {
					expect(placeholders(catalog[key as keyof Messages]), key).toEqual(
						placeholders(en[key as keyof Messages])
					);
				}
			});
		});
	}
});
