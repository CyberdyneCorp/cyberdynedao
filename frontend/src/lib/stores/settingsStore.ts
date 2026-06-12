/**
 * User-facing app preferences surfaced in the Settings window.
 *
 * Language lives in `$lib/i18n` (its own persisted store); this module
 * holds the "other easy things" — currently just a motion toggle. Each
 * preference is a `createPersistedStore` so it survives reloads.
 */
import { createPersistedStore } from './commonStore';

/**
 * When true, the shell drops the animated retro background (grid, glow,
 * digital rain, ASCII logo) — for users who prefer reduced motion or
 * weaker hardware. Persisted under `cyberdyne.reduceMotion`.
 */
export const reduceMotion = createPersistedStore<boolean>('cyberdyne.reduceMotion', false);
