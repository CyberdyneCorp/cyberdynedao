import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright config for responsive / device E2E tests.
 *
 * Goal: prove the retro-desktop shell and its windows render correctly and
 * stay reactive on iOS phones and iPads — without regressing the desktop
 * UI/UX that ships today. WebKit is used for the iOS device projects so the
 * emulation matches Safari (the only real browser engine on iOS); a Chromium
 * desktop project acts as the non-touch baseline.
 *
 * Each project carries `metadata.formFactor` ('phone' | 'tablet' | 'desktop')
 * and `metadata.touch` so the specs can assert the layout the app is expected
 * to pick for that class of device (single-column launcher on touch, two
 * columns on desktop).
 */
const PORT = 4173;
const baseURL = `http://localhost:${PORT}`;

export default defineConfig({
	testDir: './e2e',
	// Layout assertions are deterministic; a tight timeout keeps the loop fast.
	timeout: 30_000,
	expect: { timeout: 7_000 },
	fullyParallel: true,
	forbidOnly: !!process.env.CI,
	retries: process.env.CI ? 1 : 0,
	reporter: process.env.CI ? [['github'], ['html', { open: 'never' }]] : [['list'], ['html', { open: 'never' }]],
	use: {
		baseURL,
		trace: 'on-first-retry',
		screenshot: 'only-on-failure'
	},
	projects: [
		{
			name: 'iphone-se',
			use: { ...devices['iPhone SE'] },
			metadata: { formFactor: 'phone', touch: true, label: 'iPhone SE (375×667)' }
		},
		{
			name: 'iphone-13',
			use: { ...devices['iPhone 13'] },
			metadata: { formFactor: 'phone', touch: true, label: 'iPhone 13 (390×844)' }
		},
		{
			name: 'iphone-14-pro-max',
			use: { ...devices['iPhone 14 Pro Max'] },
			metadata: { formFactor: 'phone', touch: true, label: 'iPhone 14 Pro Max (430×932)' }
		},
		{
			name: 'ipad-mini',
			use: { ...devices['iPad Mini'] },
			metadata: { formFactor: 'tablet', touch: true, label: 'iPad Mini (768×1024)' }
		},
		{
			name: 'ipad-gen7',
			use: { ...devices['iPad (gen 7)'] },
			metadata: { formFactor: 'tablet', touch: true, label: 'iPad (gen 7) 810×1080' }
		},
		{
			name: 'ipad-pro-11',
			use: { ...devices['iPad Pro 11'] },
			metadata: { formFactor: 'tablet', touch: true, label: 'iPad Pro 11 (834×1194)' }
		},
		{
			name: 'ipad-pro-11-landscape',
			use: { ...devices['iPad Pro 11 landscape'] },
			metadata: { formFactor: 'tablet', touch: true, label: 'iPad Pro 11 landscape (1194×834)' }
		},
		{
			name: 'desktop-baseline',
			use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } },
			metadata: { formFactor: 'desktop', touch: false, label: 'Desktop 1280×800' }
		}
	],
	webServer: {
		// Serve the production static build (the real IPFS artifact) rather than the
		// Vite dev server: dev does on-demand dependency optimisation + HMR reloads
		// that race with parallel workers and intermittently return 500s. preview is
		// stable and representative of what ships.
		command: `npm run build && npm run preview -- --port ${PORT} --strictPort`,
		url: baseURL,
		reuseExistingServer: !process.env.CI,
		timeout: 240_000
	}
});
