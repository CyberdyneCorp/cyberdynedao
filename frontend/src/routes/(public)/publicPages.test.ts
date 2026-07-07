import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import {
	CNPJ,
	LEGAL_ENTITY,
	MINIMUM_AGE,
	POLICY_LAST_UPDATED,
	PRIVACY_EMAIL,
	REGISTERED_ADDRESS,
	SUPPORT_EMAIL,
	SUPPORT_HOURS,
	SUPPORT_RESPONSE_TIME
} from '$lib/constants/company';

const here = dirname(fileURLToPath(import.meta.url));
const read = (rel: string) => readFileSync(resolve(here, rel), 'utf8');

// The public compliance pages (Privacy §265, Support §266, Landing §267) go
// into App Store Connect and must render *real* values — never the drafting
// placeholders. These guards fail loudly if an unfilled placeholder or a blank
// value ever ships, and if the required cross-links between the pages regress.

const CONSTANTS: Record<string, string | number> = {
	LEGAL_ENTITY,
	CNPJ,
	REGISTERED_ADDRESS,
	PRIVACY_EMAIL,
	SUPPORT_EMAIL,
	SUPPORT_RESPONSE_TIME,
	SUPPORT_HOURS,
	MINIMUM_AGE,
	POLICY_LAST_UPDATED
};

describe('company constants', () => {
	it('carry no unresolved drafting placeholders', () => {
		for (const [name, value] of Object.entries(CONSTANTS)) {
			const s = String(value);
			expect(s.length, `${name} is empty`).toBeGreaterThan(0);
			expect(s, `${name} still holds a __PENDING__ placeholder`).not.toContain('__PENDING__');
			// Angle-bracket placeholders like <Legal entity name> from the draft.
			expect(s, `${name} still holds an <angle-bracket> placeholder`).not.toMatch(/<[^>]+>/);
		}
	});

	it('are well-formed', () => {
		expect(PRIVACY_EMAIL).toMatch(/^[^@\s]+@[^@\s]+\.[^@\s]+$/);
		expect(SUPPORT_EMAIL).toMatch(/^[^@\s]+@[^@\s]+\.[^@\s]+$/);
		expect(CNPJ).toMatch(/^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/);
		expect(POLICY_LAST_UPDATED).toMatch(/^\d{4}-\d{2}-\d{2}$/);
		expect(MINIMUM_AGE).toBe(16);
		expect(REGISTERED_ADDRESS).toContain('Rio de Janeiro');
	});
});

describe('public page sources', () => {
	const pages = {
		layout: read('+layout.svelte'),
		privacy: read('privacy/+page.svelte'),
		support: read('support/+page.svelte'),
		welcome: read('welcome/+page.svelte')
	};

	it('contain no leftover placeholders or TODO markers', () => {
		for (const [name, src] of Object.entries(pages)) {
			expect(src, `${name} contains __PENDING__`).not.toContain('__PENDING__');
			expect(src, `${name} contains a TODO/FIXME`).not.toMatch(/\b(TODO|FIXME)\b/);
			expect(src, `${name} contains an <placeholder>`).not.toMatch(/<placeholder|angle bracket/i);
		}
	});

	it('cross-link the required pages (App Store criteria)', () => {
		// Landing links to both Privacy and Support.
		expect(pages.welcome).toContain('/privacy');
		expect(pages.welcome).toContain('/support');
		// Support links to the Privacy Policy.
		expect(pages.support).toContain('/privacy');
		// The shared header exposes all three public routes.
		for (const path of ['/welcome', '/privacy', '/support']) {
			expect(pages.layout).toContain(path);
		}
	});

	it('render the legally required specifics on the privacy page', () => {
		// Sourced from the shared constants, and the Brazil-specific DPA.
		expect(pages.privacy).toContain('PRIVACY_EMAIL');
		expect(pages.privacy).toContain('CNPJ');
		expect(pages.privacy).toContain('ANPD');
	});
});
