'use client';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { AQITrendData } from '@/lib/api/types';

interface AQITrendChartProps {
  data: AQITrendData[];
}

export function AQITrendChart({ data }: AQITrendChartProps) {
  const displayData = data;

  return (
    <div className="relative overflow-hidden rounded-3xl bg-white/70 dark:bg-slate-900/60 backdrop-blur-xl border border-blue-200/40 dark:border-blue-900/40 p-8 shadow-2xl col-span-1 md:col-span-3 animate-slide-in">
      {/* Background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/30 via-cyan-50/20 to-transparent dark:from-blue-950/30 dark:via-cyan-950/20 dark:to-transparent" />
      <div className="absolute -bottom-32 -left-32 w-64 h-64 bg-gradient-to-tr from-cyan-400/10 to-blue-400/10 dark:from-cyan-500/5 dark:to-blue-500/5 rounded-full blur-3xl" />

      <div className="relative z-10">
        {/* Header */}
        <div className="mb-8">
          <h3 className="text-sm font-bold text-blue-900 dark:text-blue-100 uppercase tracking-wider">
            24-Hour Prediction Trend
          </h3>
          <p className="text-xs text-blue-600/70 dark:text-blue-300/60 mt-1">LightGBM model predictions for the next 24 hours</p>
        </div>

        {/* Chart */}
        <div className="bg-gradient-to-b from-white/40 to-blue-50/30 dark:from-slate-800/40 dark:to-blue-950/20 rounded-2xl p-6 border border-blue-200/30 dark:border-blue-900/30 backdrop-blur-sm">
          <ResponsiveContainer width="100%" height={380}>
            <LineChart
              data={displayData}
              margin={{ top: 20, right: 30, left: 0, bottom: 60 }}
            >
              <defs>
                <linearGradient id="colorAqi" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0288d1" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#0288d1" stopOpacity={0.1} />
                </linearGradient>
              </defs>
              <CartesianGrid
                strokeDasharray="4 4"
                stroke="currentColor"
                className="text-blue-200/30 dark:text-blue-900/30"
                vertical={false}
              />
              <XAxis
                dataKey="time"
                tick={{ fontSize: 12, fill: 'currentColor' }}
                className="text-slate-600 dark:text-slate-300"
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis
                tick={{ fontSize: 12, fill: 'currentColor' }}
                className="text-slate-600 dark:text-slate-300"
                domain={[0, 200]}
                label={{
                  value: 'AQI Index',
                  angle: -90,
                  position: 'insideLeft',
                  fill: 'currentColor',
                }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(15, 23, 42, 0.9)',
                  border: '1px solid rgba(2, 136, 209, 0.3)',
                  borderRadius: '12px',
                  color: '#e0f2fe',
                  boxShadow: '0 8px 32px rgba(2, 136, 209, 0.2)',
                }}
                formatter={(value) => [
                  <span key="aqi" className="font-semibold text-cyan-300">
                    {value} AQI
                  </span>,
                  'Quality',
                ]}
                labelFormatter={(label) => (
                  <span className="text-blue-200">{`Time: ${label}`}</span>
                )}
                cursor={{
                  stroke: 'rgba(2, 136, 209, 0.3)',
                  strokeWidth: 2,
                }}
              />

              {/* Reference Lines */}
              <ReferenceLine
                y={50}
                stroke="#10b981"
                strokeDasharray="6 4"
                opacity={0.4}
                label={{
                  value: 'Good',
                  position: 'left',
                  fill: '#10b981',
                  fontSize: 11,
                  fontWeight: 'bold',
                }}
              />
              <ReferenceLine
                y={100}
                stroke="#eab308"
                strokeDasharray="6 4"
                opacity={0.4}
                label={{
                  value: 'Fair',
                  position: 'left',
                  fill: '#eab308',
                  fontSize: 11,
                  fontWeight: 'bold',
                }}
              />
              <ReferenceLine
                y={150}
                stroke="#f97316"
                strokeDasharray="6 4"
                opacity={0.4}
                label={{
                  value: 'Moderate',
                  position: 'left',
                  fill: '#f97316',
                  fontSize: 11,
                  fontWeight: 'bold',
                }}
              />

              {/* Main Line */}
              <Line
                type="monotone"
                dataKey="aqi"
                stroke="#0288d1"
                strokeWidth={3}
                dot={{ fill: '#0288d1', r: 3, opacity: 0.7 }}
                activeDot={{
                  r: 7,
                  fill: '#0288d1',
                  shadow: '0 0 15px rgba(2, 136, 209, 0.6)',
                }}
                isAnimationActive={true}
                animationDuration={1500}
                fillOpacity={1}
                fill="url(#colorAqi)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Legend */}
        <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="flex items-center gap-2 text-sm">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#10b981' }} />
            <span className="text-slate-700 dark:text-slate-300">{'\u2264'}Good (50)</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#eab308' }} />
            <span className="text-slate-700 dark:text-slate-300">Fair (51-100)</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#f97316' }} />
            <span className="text-slate-700 dark:text-slate-300">Moderate (101-150)</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#ef4444' }} />
            <span className="text-slate-700 dark:text-slate-300">Poor (150+)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
