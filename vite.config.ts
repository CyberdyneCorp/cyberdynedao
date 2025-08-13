import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	define: {
		global: 'globalThis',
		'process.env': {},
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
});
