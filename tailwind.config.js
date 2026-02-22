/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#1d4ed8',
          700: '#1e3a8a',
          900: '#172554'
        },
        accent: '#10b981',
        softgray: '#e2e8f0',
        income: '#22c55e',
        expense: '#ef4444'
      },
      boxShadow: {
        card: '0 10px 30px rgba(15, 23, 42, 0.12)'
      },
      borderRadius: {
        xl2: '1.25rem'
      },
      keyframes: {
        floatIn: {
          '0%': { opacity: '0', transform: 'translateY(14px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        }
      },
      animation: {
        floatIn: 'floatIn 0.45s ease-out'
      }
    }
  },
  plugins: []
}
