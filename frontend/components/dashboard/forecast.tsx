'use client';

import { AQITrendData } from '@/lib/api/types';
import { getAQIColor, getAQILevel } from '@/lib/api/mock-data';

interface ForecastProps {
  data: AQITrendData[];
}

export function Forecast({ data }: ForecastProps) {
  // Group data by day
  const dayGroups: { [key: string]: AQITrendData[] } = {};
  
  if (data && Array.isArray(data)) {
    data.forEach((item) => {
      if (!item || !item.time) return;
      
      const timeParts = item.time.split(':');
      const hours = parseInt(timeParts[0] || '0');
      const hourDiff = Math.abs(hours - new Date().getHours());
      const dayKey = hourDiff <= 24 ? 'Today' : hourDiff <= 48 ? 'Tomorrow' : 'Day 3';
      
      if (!dayGroups[dayKey]) {
        dayGroups[dayKey] = [];
      }
      dayGroups[dayKey].push(item);
    });
  }

  const days = ['Today', 'Tomorrow', 'Day 3'];
  const dayData = days.map((day) => {
    const items = dayGroups[day] || [];
    const avgAQI = items.length > 0 ? Math.round(items.reduce((sum, item) => sum + item.aqi, 0) / items.length) : 0;
    const minAQI = items.length > 0 ? Math.min(...items.map((item) => item.aqi)) : 0;
    const maxAQI = items.length > 0 ? Math.max(...items.map((item) => item.aqi)) : 0;
    return { day, avgAQI, minAQI, maxAQI, items };
  });

  return (
    <div className="relative overflow-hidden rounded-3xl bg-white/70 dark:bg-slate-900/60 backdrop-blur-xl border border-blue-200/40 dark:border-blue-900/40 p-8 shadow-2xl col-span-1 md:col-span-2 animate-slide-in">
      {/* Background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-50/30 via-blue-50/20 to-transparent dark:from-cyan-950/30 dark:via-blue-950/20 dark:to-transparent" />
      <div className="absolute -top-32 -right-32 w-64 h-64 bg-gradient-to-br from-cyan-400/10 to-blue-400/10 dark:from-cyan-500/5 dark:to-blue-500/5 rounded-full blur-3xl" />

      <div className="relative z-10">
        {/* Header */}
        <div className="mb-8">
          <h3 className="text-sm font-bold text-blue-900 dark:text-blue-100 uppercase tracking-wider">
            3-Day Hourly Forecast
          </h3>
          <p className="text-xs text-blue-600/70 dark:text-blue-300/60 mt-1">AQI predictions by hour for the next 3 days</p>
        </div>

        {/* Day Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {dayData.map((dayInfo, dayIndex) => (
            <div
              key={dayInfo.day}
              className="group relative overflow-hidden rounded-2xl bg-gradient-to-br from-white/60 to-blue-50/40 dark:from-slate-800/60 dark:to-blue-950/30 backdrop-blur-lg border border-blue-200/40 dark:border-blue-900/40 p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-2 animate-slide-in"
              style={{ animationDelay: `${dayIndex * 0.15}s` }}
            >
              {/* Glow effect */}
              <div className="absolute -top-20 -right-20 w-40 h-40 bg-gradient-to-br from-cyan-300/10 to-blue-300/10 dark:from-cyan-500/5 dark:to-blue-500/5 rounded-full blur-2xl group-hover:blur-3xl transition-all" />

              {/* Day Label */}
              <div className="relative z-10 mb-4">
                <h4 className="text-lg font-bold text-slate-900 dark:text-white">{dayInfo.day}</h4>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                  {dayInfo.items.length} hourly readings
                </p>
              </div>

              {/* AQI Statistics */}
              <div className="relative z-10 space-y-3 mb-6">
                {/* Average AQI */}
                <div className="bg-gradient-to-r from-blue-100/50 to-cyan-100/50 dark:from-blue-900/30 dark:to-cyan-900/30 rounded-xl p-4 border border-blue-200/30 dark:border-blue-800/30">
                  <p className="text-xs font-semibold text-blue-900/70 dark:text-blue-200/70 uppercase mb-2">
                    Average AQI
                  </p>
                  <div className="flex items-baseline gap-2">
                    <span
                      className="text-3xl font-bold"
                      style={{ color: getAQIColor(dayInfo.avgAQI) }}
                    >
                      {dayInfo.avgAQI}
                    </span>
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      {getAQILevel(dayInfo.avgAQI)}
                    </span>
                  </div>
                </div>

                {/* Min/Max Range */}
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-gradient-to-br from-green-100/50 to-emerald-100/50 dark:from-green-900/30 dark:to-emerald-900/30 rounded-lg p-3 border border-green-200/30 dark:border-green-800/30">
                    <p className="text-xs font-semibold text-green-900/70 dark:text-green-200/70 uppercase mb-1">
                      Min
                    </p>
                    <p className="text-2xl font-bold text-green-700 dark:text-green-300">
                      {dayInfo.minAQI}
                    </p>
                  </div>
                  <div className="bg-gradient-to-br from-red-100/50 to-orange-100/50 dark:from-red-900/30 dark:to-orange-900/30 rounded-lg p-3 border border-red-200/30 dark:border-red-800/30">
                    <p className="text-xs font-semibold text-red-900/70 dark:text-red-200/70 uppercase mb-1">
                      Max
                    </p>
                    <p className="text-2xl font-bold text-red-700 dark:text-red-300">
                      {dayInfo.maxAQI}
                    </p>
                  </div>
                </div>
              </div>

              {/* Hourly Preview - Simplified bar chart */}
              <div className="relative z-10">
                <p className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase mb-3 mb-3">
                  Hourly Trend
                </p>
                <div className="flex items-end gap-1 h-16 bg-blue-50/30 dark:bg-blue-950/20 rounded-lg p-2 border border-blue-200/20 dark:border-blue-800/20">
                  {dayInfo.items.slice(0, 12).map((item, idx) => (
                    <div
                      key={idx}
                      className="flex-1 rounded-t transition-all hover:scale-110"
                      style={{
                        height: `${(item.aqi / Math.max(...dayInfo.items.map((i) => i.aqi))) * 100}%`,
                        backgroundColor: getAQIColor(item.aqi),
                        opacity: 0.7,
                      }}
                      title={`${item.time}: AQI ${item.aqi}`}
                    />
                  ))}
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
                  Showing first 12 hours
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Summary Note - Islamabad Specific */}
        <div className="relative z-10 space-y-3">
          <div className="bg-blue-50/40 dark:bg-blue-950/30 rounded-xl p-4 border border-blue-200/30 dark:border-blue-800/30 flex items-start gap-3">
            <div className="w-2 h-2 rounded-full bg-blue-500 mt-1.5 flex-shrink-0 animate-pulse" />
            <div>
              <p className="text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">
                Rush Hour Alert
              </p>
              <p className="text-xs text-blue-800/70 dark:text-blue-200/70">
                Islamabad experiences peak air pollution during morning (7-10 AM) and evening (4-8 PM) rush hours. Plan outdoor activities for midday (11 AM-3 PM) or after 9 PM.
              </p>
            </div>
          </div>

          <div className="bg-amber-50/40 dark:bg-amber-950/30 rounded-xl p-4 border border-amber-200/30 dark:border-amber-800/30 flex items-start gap-3">
            <div className="w-2 h-2 rounded-full bg-amber-500 mt-1.5 flex-shrink-0 animate-pulse" />
            <div>
              <p className="text-sm font-semibold text-amber-900 dark:text-amber-100 mb-1">
                Winter Season Notice
              </p>
              <p className="text-xs text-amber-800/70 dark:text-amber-200/70">
                October to March is Islamabad's peak pollution season. During these months, AQI levels are typically 30-40% higher. Exercise caution and use air purifiers indoors.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
