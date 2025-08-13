import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// Static adapter for IPFS deployment
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
			precompress: false,
			strict: true
		}),
		
		// Prerender all routes by default for static deployment
		prerender: {
			handleHttpError: 'warn',
			handleMissingId: 'warn',
			entries: ['*']
		},

		// Configure paths for IPFS
		paths: {
			base: '', // Leave empty for IPFS root deployment
			relative: true // Use relative paths for better IPFS compatibility
		}
	}
};

export default config;
