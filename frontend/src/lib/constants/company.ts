// Company / legal constants for the public compliance pages (Privacy,
// Support, Landing). Single source of truth so the entity details, contact
// channels, and "last updated" date stay consistent across every page and
// are trivial to update in one place.
//
// The Privacy Policy content is drafted from CyberdyneAuth's PRIVACY.md
// (governance finding COMP-07) and should get counsel's final sign-off
// before the URL is entered into App Store Connect.

/** Registered legal entity that controls personal data ("the controller"). */
export const LEGAL_ENTITY = 'Ll Araujo dos Santos & Cia LTDA';

/** Brazilian company registry number (Cadastro Nacional da Pessoa Jurídica). */
export const CNPJ = '44.541.285/0001-43';

/** Registered address of the controller. */
export const REGISTERED_ADDRESS =
	'R. Visconde de Pirajá, 414, Sala 718 — Ipanema, Rio de Janeiro/RJ, 22.410-002, Brazil';

/** Privacy / data-protection contact. */
export const PRIVACY_EMAIL = 'privacy@cyberdynecorp.ai';

/** Support contact. */
export const SUPPORT_EMAIL = 'support@cyberdynecorp.ai';

/** Target first-response time for support requests. */
export const SUPPORT_RESPONSE_TIME = 'within 2 business days';

/** Support availability (staffed hours / timezone). */
export const SUPPORT_HOURS = 'Monday–Friday, 9:00–18:00 (BRT, UTC−3)';

/** Minimum age the service is directed to (privacy §9). */
export const MINIMUM_AGE = 16;

/**
 * Policy last-updated date (ISO). Bump when the Privacy Policy content
 * materially changes — the page surfaces it to users.
 */
export const POLICY_LAST_UPDATED = '2026-07-07';
