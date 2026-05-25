'use client';

import { AirQualityData } from '@/lib/api/types';
import { getAQIColor, getAQILevel } from '@/lib/api/mock-data';

interface AQICardProps {
  data: AirQualityData;
}

export function AQICard({ data }: AQICardProps) {
  const color = getAQIColor(data.aqi);
  const level = getAQILevel(data.aqi);
  const percentage = (data.aqi / 500) * 100;

  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-sky-50/80 via-cyan-50/60 to-blue-50/40 dark:from-slate-900/70 dark:via-blue-900/50 dark:to-cyan-900/40 backdrop-blur-2xl border border-cyan-200/50 dark:border-cyan-900/40 p-8 shadow-2xl hover:shadow-3xl transition-all duration-500 animate-slide-in group col-span-1 md:col-span-2">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden rounded-3xl">
        <div className="absolute -top-32 -right-32 w-64 h-64 bg-gradient-to-br from-cyan-400/20 to-blue-400/15 dark:from-cyan-500/10 dark:to-blue-500/5 rounded-full blur-3xl animate-float" />
        <div className="absolute -bottom-32 -left-32 w-64 h-64 bg-gradient-to-tr from-sky-400/20 to-cyan-400/15 dark:from-sky-500/10 dark:to-cyan-500/5 rounded-full blur-3xl animate-float" style={{ animationDelay: '1.5s' }} />
      </div>

      <div className="relative z-10">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-700 dark:text-slate-200 uppercase tracking-widest">
                Current Air Quality
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Real-time monitoring</p>
            </div>
            <div className="flex items-center gap-2 px-3 py-1 bg-white/50 dark:bg-slate-800/50 rounded-full border border-cyan-200/30 dark:border-cyan-900/30 backdrop-blur">
              <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: color, boxShadow: `0 0 8px ${color}` }} />
              <p className="text-xs font-medium text-slate-600 dark:text-slate-300">Live</p>
            </div>
          </div>
        </div>

        {/* Main Display */}
        <div className="flex flex-col lg:flex-row items-center gap-8 mb-8">
          {/* Circular Progress with glow */}
          <div className="relative w-48 h-48 flex-shrink-0">
            {/* Glow background */}
            <div
              className="absolute inset-0 rounded-full animate-pulse-glow blur-2xl"
              style={{ backgroundColor: color, opacity: 0.2 }}
            />
            
            <svg className="w-full h-full -rotate-90 drop-shadow-lg relative z-10" viewBox="0 0 120 120">
              {/* Background circle */}
              <circle
                cx="60"
                cy="60"
                r="54"
                fill="none"
                stroke="currentColor"
                strokeWidth="8"
                className="text-cyan-100 dark:text-cyan-900/30"
              />
              {/* Animated progress circle */}
              <circle
                cx="60"
                cy="60"
                r="54"
                fill="none"
                stroke={color}
                strokeWidth="8"
                strokeDasharray={`${(percentage / 100) * 339.29} 339.29`}
                strokeLinecap="round"
                className="transition-all duration-1000 drop-shadow-lg"
              />
            </svg>
            
            {/* Center content */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-bold font-mono" style={{ color }}>
                {data.aqi}
              </span>
              <span className="text-sm font-semibold text-slate-600 dark:text-slate-300 mt-2">
                AQI Index
              </span>
            </div>
          </div>

          {/* Info Section */}
          <div className="flex-1">
            <div className="mb-6">
              <h4 className="text-4xl font-bold text-slate-900 dark:text-white mb-3">
                {level}
              </h4>
              <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300 font-medium">
                {data.aqi <= 50 && '✓ Air quality is satisfactory in Islamabad. Great day for outdoor activities!'}
                {data.aqi > 50 && data.aqi <= 100 && '⚠ Moderate air quality. Sensitive groups (children, elderly, asthma) should limit outdoor activity.'}
                {data.aqi > 100 && data.aqi <= 150 && '⚠ Unhealthy for sensitive groups. N95 masks recommended. Avoid strenuous exercise.'}
                {data.aqi > 150 && data.aqi <= 200 && '✕ Unhealthy. General public should limit outdoor activities. Masks essential.'}
                {data.aqi > 200 && '✕ Very unhealthy in Islamabad. Avoid all outdoor activities. Stay indoors.'}
              </p>
            </div>

            {/* Main Pollutants - Animated Cards */}
            <div className="grid grid-cols-3 gap-3">
              <div className="group/pollutant bg-gradient-to-br from-blue-100/60 to-blue-50/40 dark:from-blue-900/40 dark:to-blue-950/40 hover:from-blue-200/80 hover:to-blue-100/70 dark:hover:from-blue-800/60 dark:hover:to-blue-900/60 rounded-2xl p-4 border border-blue-200/50 dark:border-blue-800/50 backdrop-blur-sm transition-all duration-300 hover:shadow-lg hover:-translate-y-1 animate-slide-in">
                <p className="text-xs font-bold text-blue-900/70 dark:text-blue-200/70 uppercase tracking-wider mb-2">
                  PM 2.5
                </p>
                <p className="text-2xl font-bold text-blue-900 dark:text-blue-100">
                  {data.pm25.toFixed(1)}
                </p>
                <p className="text-xs text-blue-700/60 dark:text-blue-300/60 mt-1">μg/m³</p>
              </div>

              <div className="group/pollutant bg-gradient-to-br from-cyan-100/60 to-cyan-50/40 dark:from-cyan-900/40 dark:to-cyan-950/40 hover:from-cyan-200/80 hover:to-cyan-100/70 dark:hover:from-cyan-800/60 dark:hover:to-cyan-900/60 rounded-2xl p-4 border border-cyan-200/50 dark:border-cyan-800/50 backdrop-blur-sm transition-all duration-300 hover:shadow-lg hover:-translate-y-1 animate-slide-in"
                style={{ animationDelay: '0.1s' }}>
                <p className="text-xs font-bold text-cyan-900/70 dark:text-cyan-200/70 uppercase tracking-wider mb-2">
                  PM 10
                </p>
                <p className="text-2xl font-bold text-cyan-900 dark:text-cyan-100">
                  {data.pm10.toFixed(1)}
                </p>
                <p className="text-xs text-cyan-700/60 dark:text-cyan-300/60 mt-1">μg/m³</p>
              </div>

              <div className="group/pollutant bg-gradient-to-br from-teal-100/60 to-teal-50/40 dark:from-teal-900/40 dark:to-teal-950/40 hover:from-teal-200/80 hover:to-teal-100/70 dark:hover:from-teal-800/60 dark:hover:to-teal-900/60 rounded-2xl p-4 border border-teal-200/50 dark:border-teal-800/50 backdrop-blur-sm transition-all duration-300 hover:shadow-lg hover:-translate-y-1 animate-slide-in"
                style={{ animationDelay: '0.2s' }}>
                <p className="text-xs font-bold text-teal-900/70 dark:text-teal-200/70 uppercase tracking-wider mb-2">
                  O₃
                </p>
                <p className="text-2xl font-bold text-teal-900 dark:text-teal-100">
                  {data.o3.toFixed(1)}
                </p>
                <p className="text-xs text-teal-700/60 dark:text-teal-300/60 mt-1">ppb</p>
              </div>
            </div>
          </div>
        </div>

        {/* Additional Pollutants */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6 py-6 border-t border-b border-cyan-200/30 dark:border-cyan-900/30">
          <div className="group/mini bg-gradient-to-br from-blue-50/60 to-blue-50/30 dark:from-blue-950/40 dark:to-blue-950/20 rounded-xl p-3 border border-blue-100/50 dark:border-blue-900/40 transition-all hover:scale-105 hover:-translate-y-1 hover:shadow-md">
            <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1">NO₂</p>
            <p className="text-lg font-bold text-slate-900 dark:text-white">{data.no2.toFixed(1)}</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">ppb</p>
          </div>
          <div className="group/mini bg-gradient-to-br from-cyan-50/60 to-cyan-50/30 dark:from-cyan-950/40 dark:to-cyan-950/20 rounded-xl p-3 border border-cyan-100/50 dark:border-cyan-900/40 transition-all hover:scale-105 hover:-translate-y-1 hover:shadow-md">
            <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1">SO₂</p>
            <p className="text-lg font-bold text-slate-900 dark:text-white">{data.so2.toFixed(1)}</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">ppb</p>
          </div>
          <div className="group/mini bg-gradient-to-br from-teal-50/60 to-teal-50/30 dark:from-teal-950/40 dark:to-teal-950/20 rounded-xl p-3 border border-teal-100/50 dark:border-teal-900/40 transition-all hover:scale-105 hover:-translate-y-1 hover:shadow-md">
            <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1">CO</p>
            <p className="text-lg font-bold text-slate-900 dark:text-white">{data.co.toFixed(2)}</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">ppm</p>
          </div>
          <div className="group/mini bg-gradient-to-br from-sky-50/60 to-sky-50/30 dark:from-sky-950/40 dark:to-sky-950/20 rounded-xl p-3 border border-sky-100/50 dark:border-sky-900/40 transition-all hover:scale-105 hover:-translate-y-1 hover:shadow-md">
            <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1">Pressure</p>
            <p className="text-lg font-bold text-slate-900 dark:text-white">1013</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">hPa</p>
          </div>
        </div>

        {/* Update time */}
        <p className="text-xs text-slate-500 dark:text-slate-400 text-right">
          Last updated: {new Date(data.timestamp).toLocaleTimeString()}
        </p>
      </div>
    </div>
  );
}
