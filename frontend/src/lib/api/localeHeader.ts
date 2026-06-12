/**
 * Module-level holder for the active request locale (BCP-47 tag).
 *
 * Mirrors the `authToken.ts` pattern: API clients need synchronous,
 * non-reactive access to the current locale from arbitrary call sites
 * to stamp `Accept-Language` onto outgoing requests. The i18n `locale`
 * store updates this via {@link setRequestLocale} on every change — no
 * reactive code should read it directly.
 *
 * The backend may ignore the header today; sending it now means
 * localized course content (a later change) works without touching the
 * client again.
 */

let currentLocale: string | null = null;

export function setRequestLocale(tag: string | null): void {
	currentLocale = tag;
}

export function getRequestLocale(): string | null {
	return currentLocale;
}

/**
 * Returns a `Headers` instance with `Accept-Language` attached if a
 * locale is set. Caller's headers win — only adds the header if the
 * caller didn't already set one. Safe to pass any `HeadersInit`.
 */
export function withLocale(init?: HeadersInit): Headers {
	const headers = new Headers(init ?? {});
	if (currentLocale && !headers.has('accept-language')) {
		headers.set('Accept-Language', currentLocale);
	}
	return headers;
}
