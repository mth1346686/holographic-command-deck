/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        holo: {
          cyan: '#00F0FF',
          teal: '#00E5A3',
          violet: '#A855F7',
          amber: '#F59E0B',
          rose: '#F43F5E',
        },
        bg: {
          deep: '#050B14',
          card: 'rgba(15, 23, 42, 0.75)',
          hover: 'rgba(30, 41, 59, 0.85)',
        },
        border: {
          glass: 'rgba(0, 240, 255, 0.22)',
          glow: 'rgba(0, 240, 255, 0.6)',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Cairo', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        arabic: ['Cairo', 'sans-serif'],
      },
      backdropBlur: {
        glass: '16px',
        ultra: '24px',
      },
      animation: {
        'pulse-glow': 'pulseGlow 2.5s infinite',
        'laser-sweep': 'laserSweep 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { opacity: '0.4', transform: 'scale(1)' },
          '50%': { opacity: '0.9', transform: 'scale(1.05)' },
        },
        laserSweep: {
          '0%': { transform: 'translateX(-150%) skewX(-25deg)', opacity: '0' },
          '30%': { opacity: '1' },
          '100%': { transform: 'translateX(250%) skewX(-25deg)', opacity: '0' },
        }
      }
    },
  },
  plugins: [],
};
