// Polyfills for Node.js modules in browser environment
import { browser } from '$app/environment';

// Create a promise that resolves when polyfills are loaded
export const polyfillsReady = browser ? (async () => {
  try {
    console.log('[POLYFILLS] Initializing browser polyfills...');
    
    // Import buffer module and debug its structure
    const bufferModule = await import('buffer');
    console.log('[POLYFILLS] Full buffer module:', bufferModule);
    console.log('[POLYFILLS] bufferModule keys:', Object.keys(bufferModule));
    console.log('[POLYFILLS] bufferModule.Buffer:', bufferModule.Buffer);
    console.log('[POLYFILLS] bufferModule.default:', bufferModule.default);
    
    // Try to get Buffer from different possible exports
    let Buffer = null;
    
    if (bufferModule.Buffer) {
      Buffer = bufferModule.Buffer;
      console.log('[POLYFILLS] Using bufferModule.Buffer');
    } else if (bufferModule.default && bufferModule.default.Buffer) {
      Buffer = bufferModule.default.Buffer;
      console.log('[POLYFILLS] Using bufferModule.default.Buffer');
    } else if (typeof bufferModule.default === 'function') {
      Buffer = bufferModule.default;
      console.log('[POLYFILLS] Using bufferModule.default as function');
    } else {
      console.error('[POLYFILLS] Could not find Buffer in module:', bufferModule);
      throw new Error('Buffer not found in buffer module');
    }
    
    // Import process
    const processModule = await import('process');
    const process = processModule.default || processModule;
    
    console.log('[POLYFILLS] Buffer constructor:', Buffer);
    console.log('[POLYFILLS] Buffer.from available:', typeof Buffer?.from === 'function');
    console.log('[POLYFILLS] Process:', process);
    
    console.log('[POLYFILLS] Buffer type:', typeof Buffer);
    console.log('[POLYFILLS] Buffer.from type:', typeof Buffer?.from);
    console.log('[POLYFILLS] Buffer prototype:', Buffer?.prototype);
    console.log('[POLYFILLS] Buffer static methods:', Buffer ? Object.getOwnPropertyNames(Buffer) : 'None');
    
    // Validate that Buffer has the required methods
    if (!Buffer) {
      throw new Error('Buffer is null or undefined');
    }
    
    if (typeof Buffer !== 'function') {
      throw new Error(`Buffer is not a function, it's a ${typeof Buffer}`);
    }
    
    if (typeof Buffer.from !== 'function') {
      console.error('[POLYFILLS] Buffer.from is missing or not a function');
      console.error('[POLYFILLS] Available Buffer methods:', Object.getOwnPropertyNames(Buffer));
      throw new Error('Buffer.from is not a function - polyfill is not working correctly');
    }
    
    // Test Buffer.from functionality with different inputs
    try {
      console.log('[POLYFILLS] Testing Buffer.from with string...');
      const testBuffer1 = Buffer.from('test', 'utf8');
      console.log('[POLYFILLS] String test successful:', testBuffer1);
      
      console.log('[POLYFILLS] Testing Buffer.from with hex...');
      const testBuffer2 = Buffer.from('deadbeef', 'hex');
      console.log('[POLYFILLS] Hex test successful:', testBuffer2);
      
      console.log('[POLYFILLS] Testing Buffer.from with array...');
      const testBuffer3 = Buffer.from([1, 2, 3, 4]);
      console.log('[POLYFILLS] Array test successful:', testBuffer3);
      
    } catch (testError) {
      console.error('[POLYFILLS] Buffer functionality test failed:', testError);
      throw new Error(`Buffer polyfill is not functioning correctly: ${testError.message}`);
    }
    
    // Make polyfills available globally using multiple strategies
    console.log('[POLYFILLS] Setting Buffer globally...');
    
    // Set on globalThis
    (globalThis as any).Buffer = Buffer;
    (globalThis as any).global = globalThis;
    (globalThis as any).process = process;
    
    // Also set on window if available
    if (typeof window !== 'undefined') {
      (window as any).Buffer = Buffer;
      (window as any).global = globalThis;
      (window as any).process = process;
      console.log('[POLYFILLS] Set on window object');
    }
    
    // Set on global if it exists
    if (typeof global !== 'undefined') {
      (global as any).Buffer = Buffer;
      (global as any).process = process;
      console.log('[POLYFILLS] Set on global object');
    }
    
    // Ensure process.env exists
    if (!process.env) {
      process.env = {};
    }
    
    // Verify the global assignments worked
    console.log('[POLYFILLS] Verifying global assignments...');
    console.log('[POLYFILLS] globalThis.Buffer:', typeof globalThis.Buffer, globalThis.Buffer?.from ? '✓' : '✗');
    console.log('[POLYFILLS] window.Buffer:', typeof window?.Buffer, (window as any)?.Buffer?.from ? '✓' : '✗');
    console.log('[POLYFILLS] globalThis.process:', typeof globalThis.process ? '✓' : '✗');
    
    // Test that we can access Buffer from globalThis
    try {
      const globalTest = (globalThis as any).Buffer.from('global-test', 'utf8');
      console.log('[POLYFILLS] Global Buffer access test successful:', globalTest);
    } catch (globalTestError) {
      console.error('[POLYFILLS] Global Buffer access test failed:', globalTestError);
      throw new Error('Buffer is not accessible globally after assignment');
    }
    
    console.log('[POLYFILLS] Buffer, process, and global polyfills loaded successfully');
    
    return true;
  } catch (error) {
    console.error('[POLYFILLS] Failed to load polyfills:', error);
    throw error;
  }
})() : Promise.resolve(true);