'use client';

import Link from 'next/link';
import { AirLystLogo } from './airlyst-logo';

export function Navigation() {
  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl border-b border-blue-200/30 dark:border-slate-800/50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 hover-lift rounded-2xl px-4 py-3 group bg-white/80 dark:bg-slate-900/80 border border-slate-200/40 dark:border-slate-800/40 shadow-[0_8px_30px_rgb(255,237,213,0.3)] dark:shadow-[0_8px_30px_rgb(15,23,42,0.3)] transition-all duration-300 hover:shadow-[0_8px_30px_rgb(219,234,254,0.4)]">
            <div className="relative p-2.5 rounded-2xl bg-gradient-to-br from-cyan-50 to-blue-100 dark:from-cyan-950/40 dark:to-blue-900/40 border border-cyan-200/50 dark:border-cyan-800/30 group-hover:border-cyan-300/80 dark:group-hover:border-cyan-700/50 transition-all duration-300 shadow-sm">
              <AirLystLogo className="w-6 h-6 text-blue-600 dark:text-cyan-400 transition-transform duration-300 group-hover:scale-110" />
            </div>
            <div className="flex flex-col">
              <h1 className="text-xl font-extrabold text-[#007fff] dark:text-[#38bdf8] tracking-tight leading-none mb-1 transition-all duration-300 group-hover:translate-x-0.5">
                AirLyst
              </h1>
              <p className="text-[10px] font-bold text-slate-500 dark:text-slate-400 tracking-normal leading-none">
                Predicting Air Quality AQI of Islamabad
              </p>
            </div>
          </Link>

          {/* Only Dashboard */}
          <div className="hidden md:flex items-center gap-2">
            <Link
              href="/"
              className="flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-300 hover-lift group bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-950/50 dark:to-cyan-950/50 text-blue-700 dark:text-blue-300 border border-blue-200/50 dark:border-blue-800/50"
            >
              <span className="font-medium text-sm">Dashboard</span>
            </Link>
          </div>

          {/* Mobile Indicator */}
          <div className="md:hidden flex items-center gap-2">
            <div className="text-sm font-semibold text-blue-600 dark:text-blue-400">
              Dashboard
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
