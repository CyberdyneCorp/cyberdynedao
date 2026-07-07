# Public compliance pages (App Store URLs)

The Apple App Store requires publicly and always-accessible **Privacy Policy**
and **Support** URLs before an app with in-app purchases can be sold, plus an
optional **Marketing** URL. The frontend hosts all three as prerendered static
routes (no auth wall) under the `(public)` route group:

| Page | Route | App Store Connect field | Issue |
|------|-------|-------------------------|-------|
| Privacy Policy | `/privacy` | App Information → Privacy Policy URL (required) | #265 |
| Support | `/support` | App Information → Support URL (required) | #266 |
| Landing / marketing | `/welcome` | App Information → Marketing URL (optional) | #267 |

The app itself stays at `/` (the retro-terminal desktop); these are separate
lightweight pages that cross-link to each other via the shared
`src/routes/(public)/+layout.svelte` header/footer.

## Editing the content

All entity, contact, and policy values live in one place —
`src/lib/constants/company.ts` (legal entity + CNPJ, registered address,
privacy/support emails, support hours, minimum age, `POLICY_LAST_UPDATED`).
Edit there and every page updates. Bump `POLICY_LAST_UPDATED` whenever the
Privacy Policy content materially changes; the date is shown to users.

The prose is derived from `CyberdyneCorp/CyberdyneAuth` → `PRIVACY.md` /
`SUPPORT.md` (PR #69), grounded in the system's actual data inventory
(governance finding COMP-07).

## Before submitting to Apple

- ⚠️ **Legal sign-off**: the Privacy Policy content should be reviewed by
  qualified counsel before the URL is entered into App Store Connect (per #265).
  The controller is a Brazilian entity, so LGPD (ANPD) applies alongside GDPR
  for EU/UK users.
- Confirm the support hours in `company.ts` reflect the staffed reality.
- The pages are prerendered (`export const prerender = true`), so the static /
  IPFS build emits `privacy.html`, `support.html`, and `welcome.html` that are
  reachable without JavaScript or auth. Verify the deployed host serves
  `/privacy`, `/support`, `/welcome` with a `200` before handing the URLs to
  Apple.

## Tests

`src/routes/(public)/publicPages.test.ts` guards against shipping unfilled
draft placeholders and against the required cross-links regressing.
