/* eslint-disable no-console */
/**
 * API Client for AirLyst
 * Integrates with FastAPI backend endpoints
 */

import { DashboardData } from './types';
import { mockDashboardData } from './mock-data';

// Backend API base URL - configure based on environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ForecastResponse {
  current: {
    time: string;
    aqi: number;
    status: string;
    hazardous: boolean;
    open_meteo_aqi: number;
    pm2_5: number;
    pm10: number;
    sulphur_dioxide: number;
    nitrogen_dioxide: number;
    carbon_monoxide: number;
    temperature_2m: number;
    surface_pressure: number;
    wind_speed_10m: number;
  } | null;
  forecast_24h: Array<{
    time: string;
    predicted_aqi: number;
    actual_aqi: number;
    status: string;
  }>;
  summaries: Array<{
    label: string;
    date: string;
    time_range?: string;
    avg_aqi: number;
    status: string;
    is_hazardous: boolean;
    explanation: string;
  }>;
}

/**
 * Fetch forecast data from backend API
 * Converts backend response to frontend DashboardData format
 */
async function fetchForecastFromBackend(): Promise<DashboardData | null> {
  // If we are rendering on the Next.js server (SSR), skip fetch to prevent dev server crash overlays
  if (typeof window === 'undefined') {
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/forecast`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      console.warn(`[AirLyst] Backend API status is non-OK: ${response.status}. Using mock data fallback.`);
      return null;
    }

    const data: ForecastResponse = await response.json();
    if (!data || !data.current || !data.forecast_24h || !data.summaries) {
      console.warn('[AirLyst] Backend returned data, but format was invalid. Using mock data fallback.');
      return null;
    }

    // Transform backend response to frontend DashboardData
    const transformedData: DashboardData = {
      location: mockDashboardData.location, // Default to Islamabad config
      currentAirQuality: data.current ? {
        aqi: data.current.aqi,
        actual_aqi: data.current.open_meteo_aqi,
        level: data.current.status as any,
        pm25: data.current.pm2_5,
        pm10: data.current.pm10,
        o3: 35.0, // fallback
        no2: data.current.nitrogen_dioxide,
        so2: data.current.sulphur_dioxide,
        co: data.current.carbon_monoxide,
        timestamp: new Date(data.current.time).toISOString(),
      } : mockDashboardData.currentAirQuality,
      currentWeather: data.current ? {
        temperature: Math.round(data.current.temperature_2m),
        feelsLike: Math.round(data.current.temperature_2m),
        humidity: 65, // fallback
        pressure: Math.round(data.current.surface_pressure),
        windSpeed: Math.round(data.current.wind_speed_10m),
        windDirection: 180,
        description: 'Live',
        icon: '01d',
        timestamp: new Date(data.current.time).toISOString(),
      } : mockDashboardData.currentWeather,
      forecast24h: data.forecast_24h.map(item => ({
        time: item.time,
        predicted_aqi: item.predicted_aqi,
        actual_aqi: item.actual_aqi,
        status: item.status,
      })),
      forecast: data.summaries.map(item => ({
        label: item.label,
        date: item.date,
        time_range: item.time_range,
        aqi: item.avg_aqi,
        status: item.status,
        explanation: item.explanation
      }))
    };

    return transformedData;
  } catch (error) {
    console.warn('[AirLyst] Backend is offline or unreachable. Falling back to mock data.');
    return null;
  }
}

export async function getDashboardData(
  latitude?: number,
  longitude?: number
): Promise<DashboardData> {
  try {
    const backendData = await fetchForecastFromBackend();
    if (backendData) {
      return backendData;
    }
  } catch (error) {
    console.error('[v0] Backend fetch error, falling back to mock data:', error);
  }

  // Fallback to mock data if backend is unavailable
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        location: mockDashboardData.location,
        currentAirQuality: mockDashboardData.currentAirQuality,
        currentWeather: mockDashboardData.currentWeather,
        forecast24h: mockDashboardData.forecast24h.slice(0, 24).map(item => ({
          time: item.time,
          predicted_aqi: item.predicted_aqi,
          actual_aqi: item.actual_aqi,
          status: getStatusLabel(item.predicted_aqi)
        })),
        forecast: [
          {
            label: 'Day 1',
            date: 'Tomorrow',
            aqi: 82,
            status: 'Moderate',
            explanation: 'Driven by carry-over pollution from previous hours (~22.8 AQI points) and vehicle emissions.',
          },
          {
            label: 'Day 2',
            date: 'Day After',
            aqi: 74,
            status: 'Moderate',
            explanation: 'Driven by PM2.5 moving averages (~2.0 AQI points) and warm afternoon temperature.',
          },
          {
            label: 'Day 3',
            date: 'In 3 Days',
            aqi: 65,
            status: 'Moderate',
            explanation: 'Driven by lower vehicle congestion emissions and dispersing wind speeds.',
          }
        ]
      });
    }, 500);
  });
}

function getStatusLabel(aqi: number): string {
  if (aqi <= 50) return 'Good';
  if (aqi <= 100) return 'Moderate';
  if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
  return 'Unhealthy';
}

export async function getAirQualityForLocation(
  city: string
): Promise<DashboardData | null> {
  return getDashboardData();
}

export async function refreshDashboardData(): Promise<DashboardData> {
  try {
    const backendData = await fetchForecastFromBackend();
    if (backendData) {
      return backendData;
    }
  } catch (error) {
    console.error('[v0] Refresh error:', error);
  }

  return getDashboardData();
}

/**
 * Health check for backend API
 */
export async function checkBackendHealth(): Promise<boolean> {
  if (typeof window === 'undefined') {
    return false;
  }
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`, {
      method: 'GET',
    });
    return response.ok;
  } catch {
    return false;
  }
}
