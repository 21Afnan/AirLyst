'use client';

import { AQITrendData } from '@/lib/api/types';
import { getAQIColor } from '@/lib/api/mock-data';

interface HourlyForecastProps {
  data: AQITrendData[];
}

export function HourlyForecast({ data }: HourlyForecastProps) {
  // Get the latest 24 hours for display
  const displayData = data.slice(-24);

  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-sky-50/80 via-cyan-50/60 to-blue-50/40 dark:from-slate-900/70 dark:via-blue-900/50 dark:to-cyan-900/40 backdrop-blur-2xl border border-cyan-200/50 dark:border-cyan-900/40 p-8 shadow-2xl animate-slide-in col-span-1 md:col-span-3" style={{ animationDelay: '0.2s' }}>
      {/* Background animation */}
      <div className="absolute inset-0 overflow-hidden rounded-3xl">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-cyan-400/15 to-blue-400/10 dark:from-cyan-500/8 dark:to-blue-500/3 rounded-full blur-3xl animate-air-flow" />
      </div>

      <div className="relative z-10">
        {/* Header */}
        <div className="mb-6">
          <h3 className="text-sm font-bold text-slate-700 dark:text-slate-200 uppercase tracking-widest">
            Next 24 Hours Forecast
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Hourly AQI predictions</p>
        </div>

        {/* Hourly Cards Carousel */}
        <div className="overflow-x-auto pb-4 scrollbar-hide">
          <div className="flex gap-3 min-w-min">
            {displayData.map((item, index) => {
              const color = getAQIColor(item.aqi);
              const isHighlight = index === displayData.length - 1;

              return (
                <div
                  key={index}
                  className={`flex-shrink-0 w-24 rounded-2xl border transition-all duration-300 hover:shadow-lg hover:-translate-y-1 ${
                    isHighlight
                      ? 'bg-gradient-to-br from-white to-cyan-50 dark:from-slate-800 dark:to-blue-900/50 border-cyan-400/60 dark:border-cyan-600/40 ring-2 ring-cyan-400/30 dark:ring-cyan-600/20'
                      : 'bg-white/50 dark:bg-slate-800/50 border-cyan-200/40 dark:border-cyan-900/30 backdrop-blur-sm'
                  } p-4 animate-slide-in`}
                  style={{ animationDelay: `${index * 0.02}s` }}
                >
                  {/* Time */}
                  <p className={`text-xs font-bold uppercase tracking-wider mb-3 ${
                    isHighlight 
                      ? 'text-slate-900 dark:text-white' 
                      : 'text-slate-600 dark:text-slate-300'
                  }`}>
                    {item.time}
                  </p>

                  {/* AQI Circle */}
                  <div className="mb-3">
                    <div
                      className="w-full aspect-square rounded-xl flex items-center justify-center font-bold text-white shadow-lg"
                      style={{
                        backgroundColor: color,
                        boxShadow: `0 4px 16px ${color}40`,
                      }}
                    >
                      <span className="text-lg">{item.aqi}</span>
                    </div>
                  </div>

                  {/* Status indicator */}
                  <div className="text-center">
                    <p className={`text-xs font-semibold ${
                      item.aqi <= 50 ? 'text-green-600 dark:text-green-400' :
                      item.aqi <= 100 ? 'text-yellow-600 dark:text-yellow-400' :
                      item.aqi <= 150 ? 'text-orange-600 dark:text-orange-400' :
                      'text-red-600 dark:text-red-400'
                    }`}>
                      {item.aqi <= 50 ? 'Good' : item.aqi <= 100 ? 'Fair' : item.aqi <= 150 ? 'Moderate' : 'Poor'}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Legend */}
        <div className="mt-6 pt-6 border-t border-cyan-200/30 dark:border-cyan-900/30">
          <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mb-3">AQI Levels</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#10b981' }} />
              <span className="text-xs text-slate-600 dark:text-slate-400">Good (0-50)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#eab308' }} />
              <span className="text-xs text-slate-600 dark:text-slate-400">Fair (51-100)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#f97316' }} />
              <span className="text-xs text-slate-600 dark:text-slate-400">Moderate (101-150)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#ef4444' }} />
              <span className="text-xs text-slate-600 dark:text-slate-400">Poor (151+)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
