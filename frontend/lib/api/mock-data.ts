/**
 * Mock data service for Airlyst
 * Replace with actual API calls in lib/api/client.ts when ready
 */

import { DashboardData, AQITrendData, ForecastData } from './types';

export const mockDashboardData: DashboardData = {
  location: {
    city: 'Islamabad',
    country: 'Pakistan',
    latitude: 33.6844,
    longitude: 73.0479,
  },
  currentAirQuality: {
    aqi: 82,
    actual_aqi: 78,
    level: 'Moderate',
    pm25: 48.5,
    pm10: 75.2,
    no2: 42.5,
    so2: 18.3,
    o3: 38.8,
    co: 1.2,
    timestamp: new Date().toISOString(),
  },
  currentWeather: {
    temperature: 28,
    feelsLike: 31,
    humidity: 72,
    pressure: 1009,
    windSpeed: 8,
    windDirection: 180,
    description: 'Hazy',
    icon: '50d',
    timestamp: new Date().toISOString(),
  },
  forecast24h: generateAQITrend(),
  forecast: [
    {
      label: 'Day 1',
      date: 'Tomorrow',
      aqi: 82,
      status: 'Moderate',
      explanation: 'Driven mainly by pollution carrying over from previous hours combined with fine dust (PM2.5).',
    },
    {
      label: 'Day 2',
      date: 'Day After',
      aqi: 74,
      status: 'Moderate',
      explanation: 'Driven mainly by vehicle exhaust traffic fumes combined with ambient temperature variations.',
    },
    {
      label: 'Day 3',
      date: 'In 3 Days',
      aqi: 65,
      status: 'Moderate',
      explanation: 'Driven mainly by stable atmospheric conditions and standard urban emissions.',
    }
  ],
};

function generateAQITrend(): AQITrendData[] {
  const trend = [];
  const now = new Date();
  
  // Islamabad-specific AQI patterns: higher in winter, peaks during rush hours
  // Current season-aware baseline (typically higher Oct-Mar)
  const month = now.getMonth();
  const isWinterSeason = month >= 9 || month <= 3; // Oct-Mar is winter pollution season
  const seasonalMultiplier = isWinterSeason ? 1.3 : 0.9;

  // Generate 72 hours (3 days) of hourly AQI data
  for (let i = 72; i >= 0; i--) {
    const time = new Date(now);
    time.setHours(time.getHours() - i);
    const hour = time.getHours();
    
    // Islamabad-specific patterns:
    // Morning rush hour (7-10am) - high traffic, trapped pollution
    // Evening rush hour (4-8pm) - peak pollution
    // Night time (11pm-6am) - lower traffic, pollution disperses
    let baseAQI = 70;
    
    if (hour >= 7 && hour <= 10) {
      baseAQI = 95 + Math.random() * 25; // Morning rush
    } else if (hour >= 16 && hour <= 20) {
      baseAQI = 110 + Math.random() * 30; // Evening rush (peak)
    } else if (hour >= 21 || hour <= 6) {
      baseAQI = 50 + Math.random() * 20; // Night time - cleaner air
    } else {
      baseAQI = 75 + Math.random() * 15; // Daytime baseline
    }

    // Apply seasonal multiplier
    let hourlyAQI = baseAQI * seasonalMultiplier;
    
    // Add some realistic variation
    hourlyAQI += (Math.sin(i * 0.15) * 5);
    hourlyAQI = Math.max(25, Math.min(180, hourlyAQI));

    trend.push({
      time: time.toLocaleTimeString('en-US', { 
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      }),
      predicted_aqi: Math.round(hourlyAQI),
      actual_aqi: Math.round(hourlyAQI + (Math.random() * 12 - 6)),
    });
  }

  return trend;
}


export function getAQIColor(aqi: number): string {
  if (aqi <= 50) return '#10b981'; // Good - Green
  if (aqi <= 100) return '#eab308'; // Fair - Yellow
  if (aqi <= 150) return '#f97316'; // Moderate - Orange
  if (aqi <= 200) return '#ef4444'; // Poor - Red
  if (aqi <= 300) return '#991b1b'; // Very Poor - Dark Red
  return '#4b0082'; // Hazardous - Indigo
}

export function getAQILevel(aqi: number): string {
  if (aqi <= 50) return 'Good';
  if (aqi <= 100) return 'Moderate';
  if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
  if (aqi <= 200) return 'Unhealthy';
  if (aqi <= 300) return 'Very Unhealthy';
  return 'Hazardous';
}

export function getAQILabel(aqi: number): string {
  if (aqi <= 50) return '✓ Good - Air quality is satisfactory';
  if (aqi <= 100) return '⚠ Fair - Acceptable air quality';
  if (aqi <= 150) return '⚠ Moderate - Unhealthy for sensitive groups';
  if (aqi <= 200) return '✕ Poor - Unhealthy air quality';
  if (aqi <= 300) return '✕ Very Poor - Very unhealthy';
  return '✕ Hazardous - Hazardous to health';
}

export function getAQICondition(aqi: number): string {
  if (aqi <= 50) return 'Good';
  if (aqi <= 100) return 'Fair';
  if (aqi <= 150) return 'Moderate';
  if (aqi <= 200) return 'Poor';
  if (aqi <= 300) return 'Very Poor';
  return 'Hazardous';
}
