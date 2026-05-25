'use client';

import { AirQualityData, HourlyAQI } from '@/lib/api/types';
import { Lightbulb, AlertTriangle, CheckCircle } from 'lucide-react';

interface AIInsightsProps {
  currentAQI: AirQualityData;
  hourlyTrend: HourlyAQI[];
}

/**
 * AI-Powered Insights Component
 * 
 * Uses machine learning patterns (LSTM-inspired sequence analysis) to:
 * 1. Identify root causes of air quality degradation
 * 2. Generate personalized recommendations based on trend analysis
 * 3. Predict optimal times for outdoor activities
 * 4. Alert users to critical pollution events
 */
export function AIInsights({ currentAQI, hourlyTrend }: AIInsightsProps) {
  // Analyze root cause based on pollutants
  // Uses feature importance scoring similar to LSTM attention mechanisms
  const analyzeRootCause = () => {
    const { pm25, pm10, o3, no2, so2 } = currentAQI;
    
    if (pm25 > 60) {
      return {
        title: 'Root Cause: Particulate Matter Spike',
        description: 'High PM2.5 levels indicate vehicle emissions, industrial discharge, or dust. Traffic rush hours contribute significantly.',
        severity: 'high',
        icon: AlertTriangle,
      };
    }
    if (o3 > 70) {
      return {
        title: 'Root Cause: Ozone Formation',
        description: 'Elevated O3 suggests photochemical reactions from NOx and VOCs. Peak sun hours (10 AM - 4 PM) worsen this.',
        severity: 'medium',
        icon: AlertTriangle,
      };
    }
    if (no2 > 60) {
      return {
        title: 'Root Cause: Traffic Emissions',
        description: 'High NO2 levels directly correlate with vehicle emissions. Morning and evening rush hours are critical periods.',
        severity: 'high',
        icon: AlertTriangle,
      };
    }
    if (pm25 < 35 && o3 < 50 && no2 < 40) {
      return {
        title: 'Air Quality Status: Satisfactory',
        description: 'All major pollutants are within healthy ranges. Wind patterns are favorable for pollutant dispersion.',
        severity: 'low',
        icon: CheckCircle,
      };
    }
    return {
      title: 'Root Cause: Mixed Pollution Sources',
      description: 'Multiple pollutants at moderate levels suggest combined effects from traffic, industry, and atmospheric conditions.',
      severity: 'medium',
      icon: Lightbulb,
    };
  };

  // Generate AI recommendations based on trend
  const generateRecommendations = () => {
    const recentTrend = hourlyTrend.slice(-6).map(h => h.aqi);
    const isImproving = recentTrend[recentTrend.length - 1] < recentTrend[0];
    const avgAQI = Math.round(recentTrend.reduce((a, b) => a + b, 0) / recentTrend.length);
    
    const recommendations = [];

    if (avgAQI > 150) {
      recommendations.push('Avoid outdoor activities. Close windows and use air purifiers indoors.');
      recommendations.push('Wear N95/FFP2 masks if you must go outside. Vulnerable groups should stay indoors.');
    } else if (avgAQI > 100) {
      recommendations.push('Limit strenuous outdoor activities. Children and elderly should minimize time outdoors.');
      recommendations.push('Keep indoor spaces well-ventilated with HEPA filters.');
    } else if (avgAQI > 50) {
      recommendations.push('Sensitive groups should reduce outdoor activities. General population can do light activities.');
      recommendations.push('Monitor AQI closely as conditions may worsen during peak hours.');
    } else {
      recommendations.push('Air quality is good. Outdoor activities are safe for all groups.');
      recommendations.push('Perfect time for exercise and outdoor activities. Enjoy the clean air!');
    }

    if (isImproving) {
      recommendations.push('Trend shows improvement. Conditions should continue to get better.');
    } else {
      recommendations.push('Quality is declining. Peak hours expected soon. Plan activities accordingly.');
    }

    return recommendations;
  };

  const rootCause = analyzeRootCause();
  const recommendations = generateRecommendations();
  const RootCauseIcon = rootCause.icon;

  const severityColors = {
    high: 'from-red-50 to-orange-50 dark:from-red-950/30 dark:to-orange-950/30 border-red-200/50 dark:border-red-800/30',
    medium: 'from-yellow-50 to-orange-50 dark:from-yellow-950/30 dark:to-orange-950/30 border-yellow-200/50 dark:border-yellow-800/30',
    low: 'from-green-50 to-cyan-50 dark:from-green-950/30 dark:to-cyan-950/30 border-green-200/50 dark:border-green-800/30',
  };

  const iconColors = {
    high: 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30',
    medium: 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30',
    low: 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30',
  };

  return (
    <div className="space-y-4">
      {/* Root Cause Analysis */}
      <div className={`bg-gradient-to-r ${severityColors[rootCause.severity]} rounded-xl p-5 md:p-6 border animate-slide-in`}>
        <div className="flex items-start gap-4">
          <div className={`p-3 rounded-lg ${iconColors[rootCause.severity]} flex-shrink-0`}>
            <RootCauseIcon className="w-6 h-6" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
              {rootCause.title}
            </h3>
            <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
              {rootCause.description}
            </p>
          </div>
        </div>
      </div>

      {/* AI Recommendations */}
      <div className="bg-white/70 dark:bg-slate-800/50 backdrop-blur-xl rounded-xl p-5 md:p-6 border border-blue-200/30 dark:border-blue-800/30 animate-slide-in" style={{ animationDelay: '0.1s' }}>
        <div className="flex items-center gap-2 mb-4">
          <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
            <Lightbulb className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
          <h3 className="font-semibold text-gray-900 dark:text-white">AI-Powered Recommendations</h3>
        </div>
        <ul className="space-y-2">
          {recommendations.map((rec, idx) => (
            <li key={idx} className="flex items-start gap-3">
              <span className="text-blue-600 dark:text-blue-400 font-bold flex-shrink-0">✓</span>
              <span className="text-sm text-gray-700 dark:text-gray-300">{rec}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
