import '@testing-library/jest-dom/vitest';
// Rely on jsdom's built-in localStorage / sessionStorage so tests can spy on Storage.prototype.

// Tests run with an empty Vite import.meta.env by default, which makes
// API clients (contentApi, agentApi, ...) early-return because they
// treat the missing VITE_BACKEND_API_URL as "no backend configured".
// Pin a stable test value so request URLs are deterministic and the
// fetch mocks see them.
import.meta.env.VITE_BACKEND_API_URL = 'http://localhost:8000';
