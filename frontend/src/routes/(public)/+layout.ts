// The public compliance pages (Privacy, Support, Landing) are fully static:
// no auth, no data loading. Prerender them so the static/IPFS build emits
// plain HTML that is always reachable at a stable URL — exactly what the App
// Store Privacy Policy / Support URL fields require.
export const prerender = true;
export const ssr = true;
