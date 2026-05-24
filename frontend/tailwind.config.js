/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
  safelist: [
    'bg-emerald-50', 'text-emerald-700', 'border-emerald-200', 'from-emerald-400/20', 'text-emerald-500',
    'bg-amber-50', 'text-amber-700', 'border-amber-200', 'from-amber-400/20', 'text-amber-500',
    'bg-orange-50', 'text-orange-700', 'border-orange-200', 'from-orange-400/20', 'text-orange-500',
    'bg-rose-50', 'text-rose-700', 'border-rose-200', 'from-rose-400/20', 'text-rose-500',
    'bg-purple-50', 'text-purple-700', 'border-purple-200', 'from-purple-400/20', 'text-purple-500',
    'bg-slate-50', 'text-slate-700', 'border-slate-200', 'from-slate-400/10', 'text-slate-500',
  ]
}
