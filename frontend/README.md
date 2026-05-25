# CyberdyneCorp frontend

SvelteKit app styled with `@cyberdynecorp/svelte-ui-core` retro components.

## Setup

1. **GitHub Packages auth.** The retro component library is published to GitHub Packages, so `npm install` needs a personal access token with at least `read:packages` scope.

   The committed `.npmrc` only declares the `@cyberdynecorp` scope — it carries no token. Add the token via your user-level `~/.npmrc`:

   ```
   //npm.pkg.github.com/:_authToken=ghp_...
   ```

   or pass it inline:

   ```bash
   NPM_TOKEN=ghp_... npm install
   ```

   In CI/CD (Coolify), set `NPM_TOKEN` as a **build arg** — the Dockerfile appends it to `.npmrc` during the install step and scrubs it before the layer is finalized. Without the token you'll see a 401 from `https://npm.pkg.github.com/`.

2. **Dev server.**

   ```bash
   npm run dev        # http://localhost:5173
   ```

3. **Other commands.**

   ```bash
   npm run check      # svelte-check / tsc
   npm test           # vitest
   npm run coverage   # coverage report
   npm run build      # adapter-static production build
   ```

## Architecture

- **MVVM** — every view has a sibling `*ViewModel.ts` holding business logic and stores. Views only render.
- **Shell** — `src/routes/+page.svelte` delegates all logic to `createShellViewModel()` in `src/lib/viewmodels/shellViewModel.ts`.
- **Web3** — `Web3Wallet.svelte` wires through `createDefaultWeb3WalletViewModel()` from `web3WalletViewModelFactory.ts` so concrete services (`appKitService`, `web3AuthService`) stay out of the view.
- **Retro chrome** — `RetroWindow`, `Taskbar`, `StartMenu`, `DesktopGrid/Icon`, `ConnectWalletModal`, `LiquidityPositionCard`, `StatCard`, `PixelButton`, `PixelScrollArea`, `ErrorBoundary` all come from the library. Skin lives in `src/lib/styles/retroOverrides.css`.
- **Background animation** — the animated grid, glow particles, digital rain and ASCII hexagon logo live in `src/lib/styles/backgroundAnimations.css`.

## Testing

- **Unit tests** live in `src/lib/**/__tests__/*.test.ts`.
- Coverage target is >90% on the MVVM layer (currently 98% stmts / 90% branches; 245 tests).
- Component-level tests for the shell view and migrated views are not yet in place — considered follow-up work.

## Bundle notes

Gzipped production JS is ~2.1 MB total. Two chunks dominate:

| Chunk          | Gz size | Likely content                         |
| -------------- | ------- | -------------------------------------- |
| largest        | ~870 KB | web3 libs: wagmi, viem, reown-appkit   |
| 2nd largest    | ~438 KB | web3auth modal + ethereum providers    |
| core UI chunks | <150 KB | svelte-ui-core retro components + app  |

The retro component library itself is a small share of the total. If bundle size becomes a problem, lazy-load the wallet stack (dynamic `import()` inside `createDefaultWeb3WalletViewModel`) so the landing page no longer ships wagmi/web3auth upfront.
