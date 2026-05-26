// The callback page reads `window.location.hash` and pokes into
// `sessionStorage` — both are client-only. Prerendering would dump a
// static HTML at build time, which is fine, but we explicitly opt out
// of SSR so the SvelteKit runtime never tries to import the auth VM in
// a Node context.
export const prerender = true;
export const ssr = false;
