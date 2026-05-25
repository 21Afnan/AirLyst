'use client';

import Link from 'next/link';
import { AirLystLogo } from './airlyst-logo';

export function Navigation() {
  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl border-b border-blue-200/30 dark:border-slate-800/50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 md:gap-3 hover-lift rounded-lg px-2 md:px-3 py-2 group">
            <div className="relative p-2 rounded-xl bg-gradient-to-br from-blue-100 to-cyan-100 dark:from-blue-900/30 dark:to-cyan-900/30 border border-blue-200/50 dark:border-cyan-800/30 group-hover:border-blue-300/80 dark:group-hover:border-cyan-700/50 transition-colors">
              <AirLystLogo className="w-5 h-5 md:w-6 md:h-6 text-blue-600 dark:text-cyan-400 transition-transform group-hover:scale-110" />
            </div>
            <div className="hidden sm:block">
              <h1 className="text-base md:text-lg font-bold bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-cyan-400 dark:to-blue-400 bg-clip-text text-transparent">
                AirLyst
              </h1>
              <p className="text-xs text-gray-600 dark:text-gray-400">Air Quality</p>
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
