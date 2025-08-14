/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		screens: {
			'xs': '480px',
			'sm': '640px',
			'md': '768px',
			'lg': '1024px',
			'xl': '1280px',
			'2xl': '1536px',
		},
		extend: {
			fontFamily: {
				'mono': ['JetBrains Mono', 'Monaco', 'Menlo', 'monospace']
			},
			colors: {
				'retro-green': '#00ff00',
				'retro-green-dark': '#00dd00', 
				'retro-green-darker': '#00aa00',
				'retro-border': '#166534',
				'retro-bg': '#4338ca'
			},
			boxShadow: {
				'retro': '2px 2px 0px #000, 4px 4px 0px rgba(0,0,0,0.3)',
				'retro-hover': '1px 1px 0px #000, 2px 2px 0px rgba(0,0,0,0.3)',
				'retro-pressed': 'none',
				'retro-window': '4px 4px 0px #000, 8px 8px 0px rgba(0,0,0,0.3)'
			},
			backgroundImage: {
				'retro-gradient': 'linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%)',
				'pixel-dot': 'radial-gradient(circle at 25% 25%, rgba(255,255,255,0.15) 1px, transparent 1px), radial-gradient(circle at 75% 25%, rgba(255,255,255,0.1) 1px, transparent 1px), radial-gradient(circle at 25% 75%, rgba(255,255,255,0.1) 1px, transparent 1px), radial-gradient(circle at 75% 75%, rgba(255,255,255,0.05) 1px, transparent 1px)'
			},
			backgroundSize: {
				'pixel-dot': '20px 20px, 40px 40px, 60px 60px, 80px 80px'
			},
			width: {
				'15': '3.75rem',
				'10': '2.5rem',
				'12': '3rem',
				'16': '4rem',
				'20': '5rem'
			},
			height: {
				'15': '3.75rem', 
				'1/25': '4%',
				'10': '2.5rem',
				'12': '3rem',
				'16': '4rem',
				'20': '5rem'
			},
			spacing: {
				'15': '3.75rem',
				'18': '4.5rem',
				'22': '5.5rem',
				'28': '7rem',
				'32': '8rem',
				'36': '9rem',
				'40': '10rem'
			},
			fontSize: {
				'22': '22px',
				'32': '32px'
			},
			keyframes: {
				blink: {
					'0%, 50%': { opacity: '1' },
					'51%, 100%': { opacity: '0' }
				}
			},
			animation: {
				'blink': 'blink 1s infinite'
			}
		}
	},
	plugins: [
		require('@tailwindcss/forms'),
		function({ addUtilities }) {
			addUtilities({
				'.retro-window': {
					'background': '#ffffff',
					'border': '4px solid #000',
					'box-shadow': '4px 4px 0px #000, 8px 8px 0px rgba(0,0,0,0.3)'
				},
				'.retro-button': {
					'border': '2px solid #000',
					'box-shadow': '2px 2px 0px #000, 4px 4px 0px rgba(0,0,0,0.3)',
					'transition': 'all 0.1s ease',
					'background': 'linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%)'
				},
				'.retro-button:hover': {
					'transform': 'translate(1px, 1px)',
					'box-shadow': '1px 1px 0px #000, 2px 2px 0px rgba(0,0,0,0.3)'
				},
				'.retro-button:active': {
					'transform': 'translate(2px, 2px)',
					'box-shadow': 'none'
				},
				'.caret-retro-green': {
					'caret-color': '#00ff00 !important'
				},
				'.investment-icon': {
					'width': '80px',
					'height': '96px',
					'border': '2px solid #000',
					'position': 'relative',
					'background': 'linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%)',
					'box-shadow': '2px 2px 0px #000, 4px 4px 0px rgba(0,0,0,0.3)',
					'transition': 'all 0.1s ease'
				},
				'.investment-icon:hover': {
					'transform': 'translate(1px, 1px)',
					'box-shadow': '1px 1px 0px #000, 2px 2px 0px rgba(0,0,0,0.3)'
				},
				'.terminal-input': {
					'background-color': '#000 !important',
					'background': '#000 !important',
					'border': 'none !important',
					'outline': 'none !important',
					'box-shadow': 'none !important',
					'color': '#00ff00 !important',
					'caret-color': '#00ff00 !important',
					'font-family': 'JetBrains Mono, Monaco, Menlo, monospace !important',
					'font-size': '16px !important',
					'-webkit-appearance': 'none !important',
					'appearance': 'none !important',
					'width': '100% !important',
					'min-height': '20px !important'
				},
				'.terminal-input:focus': {
					'background-color': '#000 !important',
					'background': '#000 !important',
					'border': 'none !important',
					'outline': 'none !important',
					'box-shadow': 'none !important',
					'color': '#00ff00 !important',
					'caret-color': '#00ff00 !important'
				},
				'@media (max-width: 768px)': {
					'.terminal-input': {
						'font-size': '14px !important',
						'min-height': '24px !important'
					}
				},
				'@media (max-width: 480px)': {
					'.terminal-input': {
						'font-size': '13px !important',
						'min-height': '22px !important'
					}
				}
			})
		}
	]
}