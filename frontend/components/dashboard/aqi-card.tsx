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

  const getHoverStyles = (aqi: number) => {
    if (aqi <= 50) return {
      hoverBorder: "hover:border-emerald-400 dark:hover:border-emerald-500",
      hoverShadow: "hover:shadow-[0_0_35px_rgba(16,185,129,0.5)]"
    };
    if (aqi <= 100) return {
      hoverBorder: "hover:border-amber-400 dark:hover:border-amber-500",
      hoverShadow: "hover:shadow-[0_0_35px_rgba(234,179,8,0.5)]"
    };
    if (aqi <= 150) return {
      hoverBorder: "hover:border-orange-400 dark:hover:border-orange-500",
      hoverShadow: "hover:shadow-[0_0_35px_rgba(249,115,22,0.5)]"
    };
    if (aqi <= 200) return {
      hoverBorder: "hover:border-red-400 dark:hover:border-red-500",
      hoverShadow: "hover:shadow-[0_0_35px_rgba(239,68,68,0.5)]"
    };
    return {
      hoverBorder: "hover:border-purple-400 dark:hover:border-purple-500",
      hoverShadow: "hover:shadow-[0_0_35px_rgba(168,85,247,0.5)]"
    };
  };

  const hoverStyles = getHoverStyles(data.aqi);

  return (
    <div className={`relative overflow-hidden rounded-3xl bg-gradient-to-br from-sky-50/80 via-cyan-50/60 to-blue-50/40 dark:from-slate-900/70 dark:via-blue-900/50 dark:to-cyan-900/40 backdrop-blur-2xl border border-cyan-200/50 dark:border-cyan-900/40 p-8 shadow-2xl transition-all duration-500 animate-slide-in group col-span-1 md:col-span-2 ${hoverStyles.hoverBorder} ${hoverStyles.hoverShadow}`}>
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
              <span className="text-5xl font-black font-mono" style={{ color }}>
                {data.aqi}
              </span>
              <span className="text-xs font-bold text-slate-500 dark:text-slate-400 mt-0.5 uppercase tracking-wider">
                Predicted
              </span>
              {data.actual_aqi !== undefined && (
                <span className="text-xs font-semibold text-slate-600 dark:text-slate-300 mt-1">
                  Actual: <span className="font-bold">{data.actual_aqi}</span>
                </span>
              )}
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
            <div className="grid grid-cols-3 gap-3 mt-6">
              {/* PM2.5 - Indigo/Violet card with neon glow */}
              <div className="group/pollutant bg-gradient-to-br from-indigo-50/80 to-blue-50/50 dark:from-indigo-950/40 dark:to-blue-950/40 hover:from-indigo-100 hover:to-blue-100/80 dark:hover:from-indigo-900/60 dark:hover:to-blue-900/60 rounded-2xl p-4 border border-indigo-200/50 dark:border-indigo-800/50 backdrop-blur-sm transition-all duration-300 hover:border-indigo-400 dark:hover:border-indigo-600 hover:shadow-[0_0_25px_rgba(99,102,241,0.45)] hover:-translate-y-1 animate-slide-in">
                <p className="text-xs font-bold text-indigo-900/70 dark:text-indigo-200/70 uppercase tracking-wider mb-2">
                  PM 2.5
                </p>
                <p className="text-2xl font-black text-indigo-950 dark:text-indigo-100">
                  {data.pm25.toFixed(1)}
                </p>
                <p className="text-xs text-indigo-700/60 dark:text-indigo-300/60 mt-1">μg/m³</p>
              </div>

              {/* PM10 - Cyan/Teal card with neon glow */}
              <div className="group/pollutant bg-gradient-to-br from-cyan-50/80 to-teal-50/50 dark:from-cyan-950/40 dark:to-teal-950/40 hover:from-cyan-100 hover:to-teal-100/80 dark:hover:from-cyan-900/60 dark:hover:to-teal-900/60 rounded-2xl p-4 border border-cyan-200/50 dark:border-cyan-800/50 backdrop-blur-sm transition-all duration-300 hover:border-cyan-400 dark:hover:border-cyan-600 hover:shadow-[0_0_25px_rgba(6,182,212,0.45)] hover:-translate-y-1 animate-slide-in"
                style={{ animationDelay: '0.1s' }}>
                <p className="text-xs font-bold text-cyan-900/70 dark:text-cyan-200/70 uppercase tracking-wider mb-2">
                  PM 10
                </p>
                <p className="text-2xl font-black text-cyan-950 dark:text-cyan-100">
                  {data.pm10.toFixed(1)}
                </p>
                <p className="text-xs text-cyan-700/60 dark:text-cyan-300/60 mt-1">μg/m³</p>
              </div>

              {/* NO2 - Emerald/Teal card with neon glow */}
              <div className="group/pollutant bg-gradient-to-br from-emerald-50/80 to-teal-50/50 dark:from-emerald-950/40 dark:to-teal-950/40 hover:from-emerald-100 hover:to-teal-100/80 dark:hover:from-emerald-900/60 dark:hover:to-teal-900/60 rounded-2xl p-4 border border-emerald-200/50 dark:border-emerald-800/50 backdrop-blur-sm transition-all duration-300 hover:border-emerald-400 dark:hover:border-emerald-600 hover:shadow-[0_0_25px_rgba(16,185,129,0.45)] hover:-translate-y-1 animate-slide-in"
                style={{ animationDelay: '0.2s' }}>
                <p className="text-xs font-bold text-emerald-900/70 dark:text-emerald-200/70 uppercase tracking-wider mb-2">
                  NO₂
                </p>
                <p className="text-2xl font-black text-emerald-950 dark:text-emerald-100">
                  {data.no2.toFixed(1)}
                </p>
                <p className="text-xs text-emerald-700/60 dark:text-emerald-300/60 mt-1">ppb</p>
              </div>
            </div>
          </div>
        </div>

        {/* Additional Pollutants with Custom Glows */}
        <div className="grid grid-cols-2 gap-4 mb-6 py-6 border-t border-b border-cyan-200/30 dark:border-cyan-900/30">
          {/* SO2 - Purple/Pink card */}
          <div className="group/mini bg-gradient-to-br from-purple-50/90 to-pink-50/50 dark:from-purple-950/40 dark:to-pink-950/30 rounded-xl p-4 border border-purple-200/40 dark:border-purple-800/40 transition-all duration-300 hover:scale-[1.03] hover:-translate-y-1 hover:border-purple-400 dark:hover:border-purple-700 hover:shadow-[0_0_20px_rgba(168,85,247,0.4)]">
            <p className="text-xs font-bold text-purple-900/80 dark:text-purple-300/80 mb-1">SO₂</p>
            <p className="text-xl font-extrabold text-purple-950 dark:text-purple-100">{data.so2.toFixed(1)}</p>
            <p className="text-xs text-purple-700/60 dark:text-purple-400/60 mt-0.5">ppb</p>
          </div>
          {/* CO - Amber/Orange card */}
          <div className="group/mini bg-gradient-to-br from-amber-50/90 to-orange-50/50 dark:from-amber-950/40 dark:to-orange-950/30 rounded-xl p-4 border border-amber-200/40 dark:border-amber-800/40 transition-all duration-300 hover:scale-[1.03] hover:-translate-y-1 hover:border-amber-400 dark:hover:border-amber-700 hover:shadow-[0_0_20px_rgba(245,158,11,0.4)]">
            <p className="text-xs font-bold text-amber-900/80 dark:text-amber-300/80 mb-1">CO</p>
            <p className="text-xl font-extrabold text-amber-950 dark:text-amber-100">{data.co.toFixed(2)}</p>
            <p className="text-xs text-amber-700/60 dark:text-amber-400/60 mt-0.5">ppm</p>
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
