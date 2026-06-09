# Responsive / device E2E tests

Playwright suite that proves the retro-desktop shell renders correctly and stays
reactive on **iOS phones and iPads** without regressing the desktop UI/UX.

## Run

```bash
npm run test:e2e            # all device projects (builds + previews automatically)
npm run test:e2e -- --project=iphone-13
npm run test:e2e:report     # open the last HTML report (screenshots attached)
```

The Playwright `webServer` runs `npm run build && npm run preview` so tests hit the
**production static build** (the real IPFS artifact) — not the Vite dev server, whose
on-demand dep optimisation + HMR reloads intermittently 500 under parallel load.

## Coverage

Device projects (`playwright.config.ts`), WebKit for the iOS ones so emulation
matches Safari, Chromium for the desktop baseline:

| Project                    | Form factor | Viewport   |
| -------------------------- | ----------- | ---------- |
| `iphone-se`                | phone       | 375×667    |
| `iphone-13`                | phone       | 390×844    |
| `iphone-14-pro-max`        | phone       | 430×932    |
| `ipad-mini`                | tablet      | 768×1024   |
| `ipad-gen7`                | tablet      | 810×1080   |
| `ipad-pro-11`              | tablet      | 834×1194   |
| `ipad-pro-11-landscape`    | tablet      | 1194×834   |
| `desktop-baseline`         | desktop     | 1280×800   |

What each spec asserts (`responsive.spec.ts`):

- **boots cleanly** — shell + topbar visible, no horizontal page overflow, no
  uncaught page errors (a desktop screenshot is attached to the report).
- **launcher + wallet reachable** — Start trigger fits inside the topbar.
- **column count** — touch devices get the single-column launcher, desktop keeps
  two columns (`--cy-dgrid-cols`).
- **launcher menu** — opens, lists items, panel fits the viewport.
- **every app window** — each launcher icon opens a window that fits within the
  viewport (width/height/right-edge), has no inner horizontal content overflow
  (its body content fits — catches clipped columns), surfaces in the taskbar,
  and closes.
- **content-heavy window (Academy)** — the widest window still clamps to fit a phone.
- **login modal** — the CONNECT modal's overlay renders *above* the desktop icons
  (regression: it was trapped below them by a stacking context) and introduces no
  horizontal overflow.

## CI

`.github/workflows/frontend-e2e.yml` runs this suite on every push to `main` and
on PRs touching `frontend/**`. It installs WebKit + Chromium, runs `npm run test:e2e`
(which builds + previews the app), and uploads the HTML report as an artifact.

Backend calls are stubbed (`helpers.ts › stubBackend`) so the suite runs offline and
deterministically — these tests assert layout/structure, not live data.
