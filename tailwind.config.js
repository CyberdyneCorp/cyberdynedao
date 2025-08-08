/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      fontFamily: {
        'mono': ['Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', 'monospace'],
      },
      colors: {
        'retro-bg': '#4338ca',
        'retro-blue': '#3b82f6',
        'retro-purple': '#8b5cf6',
        'retro-pink': '#ec4899',
        'retro-cyan': '#06b6d4',
        'retro-green': '#10b981',
        'retro-yellow': '#f59e0b',
        'retro-orange': '#f97316',
      },
      animation: {
        'pixel-grid': 'pixel-grid 20s linear infinite',
      },
      keyframes: {
        'pixel-grid': {
          '0%': { transform: 'translate(0, 0)' },
          '100%': { transform: 'translate(20px, 20px)' },
        }
      }
    },
  },
  plugins: [],
}