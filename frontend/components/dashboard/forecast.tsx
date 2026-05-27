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

  const getDayCardStyles = (aqi: number) => {
    if (aqi <= 50) {
      return {
        bg: "from-emerald-50/80 to-green-50/40 dark:from-emerald-950/25 dark:to-green-950/15",
        border: "border-emerald-200/50 dark:border-emerald-900/40 hover:border-emerald-400 dark:hover:border-emerald-500",
        glow: "from-emerald-300/20 to-green-300/20 dark:from-emerald-500/10 dark:to-green-500/5",
        shadowHover: "hover:shadow-[0_0_30px_rgba(16,185,129,0.5)]",
        avgBg: "from-emerald-100/50 to-green-100/50 dark:from-emerald-900/30 dark:to-green-900/30",
        avgBorder: "border-emerald-200/40 dark:border-emerald-800/30"
      };
    }
    if (aqi <= 100) {
      return {
        bg: "from-amber-50/80 to-yellow-50/40 dark:from-amber-950/25 dark:to-yellow-950/15",
        border: "border-amber-200/50 dark:border-amber-900/40 hover:border-amber-400 dark:hover:border-amber-500",
        glow: "from-amber-300/20 to-yellow-300/20 dark:from-amber-500/10 dark:to-yellow-500/5",
        shadowHover: "hover:shadow-[0_0_30px_rgba(234,179,8,0.5)]",
        avgBg: "from-amber-100/50 to-yellow-100/50 dark:from-amber-900/30 dark:to-yellow-900/30",
        avgBorder: "border-amber-200/40 dark:border-amber-800/30"
      };
    }
    if (aqi <= 150) {
      return {
        bg: "from-orange-50/80 to-red-50/40 dark:from-orange-950/25 dark:to-red-950/15",
        border: "border-orange-200/50 dark:border-orange-900/40 hover:border-orange-400 dark:hover:border-orange-500",
        glow: "from-orange-300/20 to-red-300/20 dark:from-orange-500/10 dark:to-orange-500/5",
        shadowHover: "hover:shadow-[0_0_30px_rgba(249,115,22,0.5)]",
        avgBg: "from-orange-100/50 to-red-100/50 dark:from-orange-900/30 dark:to-red-900/30",
        avgBorder: "border-orange-200/40 dark:border-orange-800/30"
      };
    }
    if (aqi <= 200) {
      return {
        bg: "from-red-50/80 to-rose-50/40 dark:from-red-950/25 dark:to-rose-950/15",
        border: "border-red-200/50 dark:border-red-900/40 hover:border-red-400 dark:hover:border-red-500",
        glow: "from-red-300/20 to-rose-300/20 dark:from-red-500/10 dark:to-rose-500/5",
        shadowHover: "hover:shadow-[0_0_30px_rgba(239,68,68,0.5)]",
        avgBg: "from-red-100/50 to-rose-100/50 dark:from-red-900/30 dark:to-rose-900/30",
        avgBorder: "border-red-200/40 dark:border-red-800/30"
      };
    }
    return {
      bg: "from-purple-50/80 to-indigo-50/40 dark:from-purple-950/25 dark:to-indigo-950/15",
      border: "border-purple-200/50 dark:border-purple-900/40 hover:border-purple-400 dark:hover:border-purple-500",
      glow: "from-purple-300/20 to-indigo-300/20 dark:from-purple-500/10 dark:to-indigo-500/5",
      shadowHover: "hover:shadow-[0_0_30px_rgba(168,85,247,0.5)]",
      avgBg: "from-purple-100/50 to-indigo-100/50 dark:from-purple-900/30 dark:to-indigo-900/30",
      avgBorder: "border-purple-200/40 dark:border-purple-800/30"
    };
  };

  const days = ['Today', 'Tomorrow', 'Day 3'];
  const dayData = days.map((day) => {
    const items = dayGroups[day] || [];
    const avgAQI = items.length > 0 ? Math.round(items.reduce((sum, item) => sum + item.predicted_aqi, 0) / items.length) : 0;
    const minAQI = items.length > 0 ? Math.min(...items.map((item) => item.predicted_aqi)) : 0;
    const maxAQI = items.length > 0 ? Math.max(...items.map((item) => item.predicted_aqi)) : 0;
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
          {dayData.map((dayInfo, dayIndex) => {
            const styles = getDayCardStyles(dayInfo.avgAQI);
            return (
              <div
                key={dayInfo.day}
                className={`group relative overflow-hidden rounded-2xl bg-gradient-to-br ${styles.bg} backdrop-blur-lg border ${styles.border} p-6 ${styles.shadowHover} transition-all duration-500 hover:-translate-y-2 animate-slide-in`}
                style={{ animationDelay: `${dayIndex * 0.15}s` }}
              >
                {/* Dynamic Glow effect */}
                <div className={`absolute -top-20 -right-20 w-40 h-40 bg-gradient-to-br ${styles.glow} rounded-full blur-2xl group-hover:blur-3xl transition-all`} />

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
                  <div className={`bg-gradient-to-r ${styles.avgBg} rounded-xl p-4 border ${styles.avgBorder} transition-all duration-300`}>
                    <p className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase mb-2">
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
                  <p className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase mb-3">
                    Hourly Trend
                  </p>
                  <div className="flex items-end gap-1 h-16 bg-blue-50/30 dark:bg-blue-950/20 rounded-lg p-2 border border-blue-200/20 dark:border-blue-800/20">
                    {dayInfo.items.slice(0, 12).map((item, idx) => (
                      <div
                        key={idx}
                        className="flex-1 rounded-t transition-all hover:scale-110"
                        style={{
                          height: `${(item.predicted_aqi / Math.max(...dayInfo.items.map((i) => i.predicted_aqi))) * 100}%`,
                          backgroundColor: getAQIColor(item.predicted_aqi),
                          opacity: 0.7,
                        }}
                        title={`${item.time}: AQI ${item.predicted_aqi}`}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
                    Showing first 12 hours
                  </p>
                </div>
              </div>
            );
          })}
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
