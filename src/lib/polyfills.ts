// Polyfills for Node.js modules in browser environment
import { Buffer } from 'buffer';
import process from 'process';

// Initialize polyfills immediately
console.log('[POLYFILLS] Initializing browser polyfills...');

// Make Buffer available globally
if (typeof window !== 'undefined') {
  // Override any placeholder with actual Buffer
  (window as any).Buffer = Buffer;
  (window as any).global = globalThis;
  (window as any).process = process;
  
  // Ensure process.env exists
  if (!process.env) {
    process.env = {};
  }
  
  console.log('[POLYFILLS] Buffer, process, and global polyfills loaded successfully');
  console.log('[POLYFILLS] Buffer available:', typeof window.Buffer !== 'undefined');
  console.log('[POLYFILLS] Process available:', typeof window.process !== 'undefined');
}