'use client';

import { useState, useEffect } from 'react';
import { AQICard } from '@/components/dashboard/aqi-card';
import { WeatherWidget } from '@/components/dashboard/weather-widget';
import { AQITrendChart } from '@/components/dashboard/aqi-trend-chart';
import { getDashboardData } from '@/lib/api/client';
import { DashboardData } from '@/lib/api/types';
import { RefreshCw, ShieldAlert, Sparkles } from 'lucide-react';

export default function Home() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const dashboardData = await getDashboardData();
      setData(dashboardData);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Error loading data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    
    // Auto-refresh data every 5 minutes (300,000 ms)
    const interval = setInterval(loadData, 300000);
    return () => clearInterval(interval);
  }, []);

  if (isLoading && !data) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-slate-950 dark:to-blue-950">
        <div className="text-center animate-scale-in">
          <div className="w-16 h-16 border-4 border-blue-200 dark:border-blue-800 border-t-blue-500 dark:border-t-blue-400 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400 font-medium">Loading live air quality data...</p>
        </div>
      </main>
    );
  }

  if (error || !data) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-slate-950 dark:to-blue-950">
        <div className="text-center animate-scale-in">
          <div className="mb-4 text-5xl">⚠️</div>
          <p className="text-red-600 dark:text-red-400 font-semibold mb-4">{error || 'Unable to load data'}</p>
          <button
            onClick={loadData}
            className="px-6 py-2 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg hover-lift font-medium"
          >
            Try Again
          </button>
        </div>
      </main>
    );
  }

  // Helper function to resolve color scheme of summaries based on AQI
  const getStatusColor = (aqi: number) => {
    if (aqi <= 50) return { 
      color: 'from-emerald-500 to-green-500',
      bgGradient: 'from-emerald-500/10 to-green-500/10 dark:from-emerald-500/5 dark:to-green-500/5',
      label: 'Good', 
      border: 'border-emerald-200/50 dark:border-emerald-900/30',
      textColor: 'text-emerald-700 dark:text-emerald-400',
      hoverBorder: 'hover:border-emerald-400 dark:hover:border-emerald-500',
      hoverShadow: 'hover:shadow-[0_0_30px_rgba(16,185,129,0.45)]'
    };
    if (aqi <= 100) return { 
      color: 'from-amber-400 to-yellow-400',
      bgGradient: 'from-amber-400/10 to-yellow-400/10 dark:from-amber-400/5 dark:to-yellow-400/5',
      label: 'Moderate', 
      border: 'border-amber-200/40 dark:border-yellow-900/20',
      textColor: 'text-amber-800 dark:text-amber-300',
      hoverBorder: 'hover:border-amber-400 dark:hover:border-amber-500',
      hoverShadow: 'hover:shadow-[0_0_30px_rgba(234,179,8,0.45)]'
    };
    if (aqi <= 150) return { 
      color: 'from-orange-500 to-amber-500',
      bgGradient: 'from-orange-500/10 to-amber-500/10 dark:from-orange-500/5 dark:to-orange-500/5',
      label: 'Unhealthy (Sensitive)', 
      border: 'border-orange-200/40 dark:border-orange-900/20',
      textColor: 'text-orange-700 dark:text-orange-400',
      hoverBorder: 'hover:border-orange-400 dark:hover:border-orange-500',
      hoverShadow: 'hover:shadow-[0_0_30px_rgba(249,115,22,0.45)]'
    };
    return { 
      color: 'from-rose-500 to-red-500',
      bgGradient: 'from-rose-500/15 to-red-500/15 dark:from-rose-500/8 dark:to-red-500/8',
      label: 'Unhealthy', 
      border: 'border-rose-300/40 dark:border-rose-900/20',
      textColor: 'text-rose-700 dark:text-rose-400',
      hoverBorder: 'hover:border-rose-400 dark:hover:border-rose-500',
      hoverShadow: 'hover:shadow-[0_0_30px_rgba(239,68,68,0.45)]'
    };
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950 text-slate-900 dark:text-slate-100 relative overflow-x-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-blue-200/30 to-cyan-200/30 dark:from-blue-500/10 dark:to-cyan-500/10 rounded-full blur-3xl animate-air-flow"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-cyan-200/20 to-blue-200/20 dark:from-cyan-500/5 dark:to-blue-500/5 rounded-full blur-3xl"></div>
      </div>

      <div className="relative p-4 md:p-6 lg:p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          
          {/* Header Section */}
          <div className="flex items-center justify-between bg-white/40 dark:bg-slate-900/40 backdrop-blur-md p-4 md:p-6 rounded-3xl border border-blue-200/20 dark:border-blue-900/20 shadow-sm animate-slide-in">
            <div>
              <h1 className="text-xl md:text-3xl font-extrabold bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-400 dark:to-cyan-300 bg-clip-text text-transparent">
                {data.location.city}, {data.location.country}
              </h1>
              <p className="text-xs md:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                Live Air Quality Forecasting & SHAP-driven Insights
              </p>
            </div>
            <button
              onClick={loadData}
              disabled={isLoading}
              className="p-3 rounded-2xl bg-white dark:bg-slate-800 border border-blue-200/50 dark:border-blue-800/50 hover:bg-blue-50 dark:hover:bg-blue-950 transition-all shadow-md hover-lift flex items-center justify-center"
              title="Refresh data"
            >
              <RefreshCw className={`w-5 h-5 text-blue-600 dark:text-blue-400 ${isLoading ? 'animate-spin' : ''}`} />
            </button>
          </div>

          {/* Current State Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-slide-in" style={{ animationDelay: '0.1s' }}>
            {/* Main AQI Card (Spans 2 columns) */}
            <div className="lg:col-span-2">
              <AQICard data={data.currentAirQuality} />
            </div>
            {/* Weather Widget */}
            <div className="h-full">
              <WeatherWidget data={data.currentWeather} />
            </div>
          </div>

          {/* 3-Day Forecast Summaries with SHAP explanations */}
          <div className="space-y-4 animate-slide-in" style={{ animationDelay: '0.2s' }}>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <h2 className="text-lg font-bold text-slate-800 dark:text-slate-200">3-Day Predictions & SHAP Explainability</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {data.forecast.map((day, idx) => {
                const status = getStatusColor(day.aqi);
                return (
                  <div 
                    key={idx}
                    className={`group relative overflow-hidden rounded-3xl bg-gradient-to-br from-white/70 to-blue-50/30 dark:from-slate-900/70 dark:to-blue-950/30 backdrop-blur-xl border border-blue-200/20 dark:border-blue-900/20 p-6 md:p-8 transition-all duration-300 hover:-translate-y-1.5 flex flex-col justify-between ${status.hoverBorder} ${status.hoverShadow}`}
                  >
                    <div>
                      {/* Date & Title */}
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h4 className="text-sm font-extrabold uppercase tracking-widest text-slate-400 dark:text-slate-500">
                            {day.label}
                          </h4>
                          <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                            {day.date}
                          </p>
                        </div>
                        {/* Status Badge */}
                        <span className={`text-xs font-bold px-3 py-1 rounded-xl bg-white/50 dark:bg-slate-800/80 border ${status.border} ${status.textColor}`}>
                          {status.label}
                        </span>
                      </div>

                      {/* Average AQI */}
                      <div className="mb-4">
                        <span className={`text-5xl font-black bg-gradient-to-r ${status.color} bg-clip-text text-transparent tracking-tighter`}>
                          {day.aqi}
                        </span>
                        <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 block mt-1">Average Predicted AQI</span>
                      </div>
                    </div>

                    {/* SHAP non-technical explanation card */}
                    <div className="mt-4 pt-4 border-t border-blue-100/50 dark:border-blue-900/20 bg-blue-50/20 dark:bg-blue-950/10 p-3 rounded-2xl border border-blue-200/10 dark:border-blue-900/10">
                      <div className="flex items-center gap-1.5 mb-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-blue-500 dark:text-blue-400 animate-pulse" />
                        <span className="text-xs font-bold text-blue-700 dark:text-blue-400 uppercase tracking-wider">SHAP Explanation</span>
                      </div>
                      <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-medium">
                        {day.explanation}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 24-Hour Trend Chart (The exactly 1 graph requested) */}
          <div className="animate-slide-in" style={{ animationDelay: '0.3s' }}>
            <AQITrendChart data={data.forecast24h} />
          </div>

          {/* Footer */}
          <div className="text-center text-xs text-slate-500 dark:text-slate-500 py-6 border-t border-blue-200/20 dark:border-blue-900/20">
            <p>© {new Date().getFullYear()} AirLyst. All rights reserved. Powered by Hopsworks Model Registry & LightGBM.</p>
          </div>

        </div>
      </div>
    </main>
  );
}
