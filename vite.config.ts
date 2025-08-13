import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	define: {
		global: 'globalThis',
	},
	optimizeDeps: {
		include: ['buffer']
	},
	resolve: {
		alias: {
			buffer: 'buffer',
		}
	}
});
