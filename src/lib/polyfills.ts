// Polyfills for Node.js modules in browser environment
import { Buffer } from 'buffer';

// Make Buffer available globally
if (typeof window !== 'undefined') {
  (window as any).Buffer = Buffer;
  (window as any).global = window;
  (window as any).process = {
    env: {},
    nextTick: (fn: Function) => setTimeout(fn, 0),
    browser: true,
    version: '',
    versions: {},
    platform: 'browser'
  };
}

console.log('[POLYFILLS] Browser polyfills loaded successfully');