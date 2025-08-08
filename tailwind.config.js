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
      spacing: {
        '18': '4.5rem',    // 72px
        '20': '5rem',       // 80px
        '22': '5.5rem',     // 88px
        '24': '6rem',       // 96px
        '26': '6.5rem',     // 104px
        '28': '7rem',       // 112px
        '30': '7.5rem',     // 120px
        '32': '8rem',       // 128px
        '36': '9rem',       // 144px
        '40': '10rem',      // 160px
        '44': '11rem',      // 176px
        '48': '12rem',      // 192px
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