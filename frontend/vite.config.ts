import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

// Dev-only proxy: forwards browser fetches to `/api/auth/*` over to the
// real CyberdyneAuth host. Same shape as the nginx `location` block we
// ship in `frontend/Dockerfile` for prod — so the frontend code can
// always call `/api/auth/api/v1/auth/login` without worrying which
// environment it's running in.
const AUTH_UPSTREAM = process.env.CYBERDYNE_AUTH_URL
	?? 'https://auth.backend.coolify.cyberdynecorp.ai';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api/auth': {
				target: AUTH_UPSTREAM,
				changeOrigin: true,
				secure: true,
				// Strip the `/api/auth` prefix so the upstream sees `/api/v1/...`
				rewrite: (path: string) => path.replace(/^\/api\/auth/, '')
			}
		}
	},
	test: {
		environment: 'jsdom',
		globals: true,
		include: ['src/**/*.{test,spec}.{js,ts}'],
		setupFiles: ['./src/test-setup.ts'],
		coverage: {
			provider: 'v8',
			reporter: ['text', 'html', 'json-summary'],
			include: [
				'src/lib/viewmodels/**/*.ts',
				'src/lib/composables/**/*.ts',
				'src/lib/data/**/*.ts',
				'src/lib/auth/authToken.ts',
				'src/lib/auth/cyberdyneAuthService.ts',
				'src/lib/utils/formatters.ts',
				'src/lib/utils/validation.ts',
				'src/lib/utils/storage.ts',
				'src/lib/utils/dataHelpers.ts',
				'src/lib/utils/api.ts',
				'src/lib/utils/terminalCommands.ts',
				'src/lib/utils/mobileDetection.ts',
				'src/lib/stores/commonStore.ts',
				'src/lib/stores/windowStore.ts',
				'src/lib/stores/appKitStore.ts',
				'src/lib/constants/daoData.ts'
			],
			exclude: [
				'src/lib/web3/**',
				'src/lib/polyfills.ts',
				'src/lib/index.ts',
				'**/*.d.ts',
				'**/*.test.ts',
				'**/*.spec.ts',
				'**/__tests__/**'
			],
			thresholds: {
				lines: 90,
				functions: 90,
				branches: 90,
				statements: 90
			}
		}
	},
	define: {
		global: 'globalThis',
	},
	resolve: {
		alias: {
			buffer: 'buffer',
			crypto: 'crypto-browserify',
			stream: 'stream-browserify',
			assert: 'assert',
			util: 'util',
			vm: 'vm-browserify',
			process: 'process',
		},
	},
	optimizeDeps: {
		include: ['buffer', 'crypto-browserify', 'stream-browserify', 'assert', 'util', 'vm-browserify', 'process'],
	},
	ssr: {
		noExternal: ['buffer'],
	},
});
