'use client';

import { WeatherData } from '@/lib/api/types';

interface WeatherWidgetProps {
  data: WeatherData;
}

export function WeatherWidget({ data }: WeatherWidgetProps) {
  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-sky-50/80 via-cyan-50/60 to-blue-50/40 dark:from-slate-900/70 dark:via-blue-900/50 dark:to-cyan-900/40 backdrop-blur-2xl border border-cyan-200/50 dark:border-cyan-900/40 p-8 shadow-2xl hover:shadow-3xl transition-all duration-500 animate-slide-in" style={{ animationDelay: '0.1s' }}>
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden rounded-3xl">
        <div className="absolute -top-32 -right-32 w-64 h-64 bg-gradient-to-br from-cyan-400/20 to-blue-400/15 dark:from-cyan-500/10 dark:to-blue-500/5 rounded-full blur-3xl animate-float" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-sky-400/20 to-cyan-400/15 dark:from-sky-500/10 dark:to-cyan-500/5 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />
      </div>

      <div className="relative z-10 flex flex-col items-center gap-6">
        {/* Header */}
        <div className="text-center mb-2">
          <h3 className="text-sm font-bold text-blue-900 dark:text-blue-100 uppercase tracking-wider">
            Current Weather
          </h3>
        </div>

        {/* Temperature Display */}
        <div className="text-center">
          <div className="text-7xl font-black text-transparent bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-400 dark:to-cyan-400 bg-clip-text mb-2">
            {data.temperature}°
          </div>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Feels like <span className="font-bold text-slate-900 dark:text-white">{data.feelsLike}°</span>
          </p>
        </div>

        {/* Condition Description */}
        <div className="text-center bg-gradient-to-r from-blue-100/40 to-cyan-100/40 dark:from-blue-900/30 dark:to-cyan-900/30 rounded-2xl px-6 py-3 border border-blue-200/40 dark:border-blue-800/40 backdrop-blur-sm w-full">
          <p className="text-lg font-semibold text-slate-900 dark:text-white">
            {data.description}
          </p>
        </div>

        {/* Weather Details Grid */}
        <div className="grid grid-cols-2 gap-3 w-full mt-2">
          {/* Humidity */}
          <div className="group bg-gradient-to-br from-blue-100/50 to-blue-50/30 dark:from-blue-900/40 dark:to-blue-950/30 hover:from-blue-150/70 hover:to-blue-100/50 dark:hover:from-blue-800/60 dark:hover:to-blue-900/60 rounded-xl p-4 border border-blue-200/40 dark:border-blue-800/40 transition-all hover:shadow-lg hover:-translate-y-1 cursor-default">
            <p className="text-xs font-bold text-blue-900/70 dark:text-blue-200/70 uppercase tracking-wider mb-2">
              Humidity
            </p>
            <p className="text-2xl font-bold text-blue-900 dark:text-blue-100">
              {data.humidity}<span className="text-lg">%</span>
            </p>
          </div>

          {/* Pressure */}
          <div className="group bg-gradient-to-br from-cyan-100/50 to-cyan-50/30 dark:from-cyan-900/40 dark:to-cyan-950/30 hover:from-cyan-150/70 hover:to-cyan-100/50 dark:hover:from-cyan-800/60 dark:hover:to-cyan-900/60 rounded-xl p-4 border border-cyan-200/40 dark:border-cyan-800/40 transition-all hover:shadow-lg hover:-translate-y-1 cursor-default">
            <p className="text-xs font-bold text-cyan-900/70 dark:text-cyan-200/70 uppercase tracking-wider mb-2">
              Pressure
            </p>
            <p className="text-2xl font-bold text-cyan-900 dark:text-cyan-100">
              {data.pressure}<span className="text-sm">mb</span>
            </p>
          </div>

          {/* Wind Speed */}
          <div className="group bg-gradient-to-br from-teal-100/50 to-teal-50/30 dark:from-teal-900/40 dark:to-teal-950/30 hover:from-teal-150/70 hover:to-teal-100/50 dark:hover:from-teal-800/60 dark:hover:to-teal-900/60 rounded-xl p-4 border border-teal-200/40 dark:border-teal-800/40 transition-all hover:shadow-lg hover:-translate-y-1 cursor-default">
            <p className="text-xs font-bold text-teal-900/70 dark:text-teal-200/70 uppercase tracking-wider mb-2">
              Wind Speed
            </p>
            <p className="text-2xl font-bold text-teal-900 dark:text-teal-100">
              {data.windSpeed}<span className="text-sm">mph</span>
            </p>
          </div>

          {/* Direction */}
          <div className="group bg-gradient-to-br from-sky-100/50 to-sky-50/30 dark:from-sky-900/40 dark:to-sky-950/30 hover:from-sky-150/70 hover:to-sky-100/50 dark:hover:from-sky-800/60 dark:hover:to-sky-900/60 rounded-xl p-4 border border-sky-200/40 dark:border-sky-800/40 transition-all hover:shadow-lg hover:-translate-y-1 cursor-default">
            <p className="text-xs font-bold text-sky-900/70 dark:text-sky-200/70 uppercase tracking-wider mb-2">
              Direction
            </p>
            <p className="text-2xl font-bold text-sky-900 dark:text-sky-100">
              {data.windDirection}<span className="text-sm">°</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
