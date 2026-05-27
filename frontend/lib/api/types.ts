/**
 * API types for Airlyst Air Quality Dashboard
 * These define the data structures for the dashboard
 */

export interface AirQualityData {
  aqi: number;
  actual_aqi?: number;
  level: 'Good' | 'Fair' | 'Moderate' | 'Poor' | 'Very Poor' | 'Hazardous';
  pm25: number;
  pm10: number;
  no2: number;
  so2: number;
  o3: number;
  co: number;
  timestamp: string;
}

export interface WeatherData {
  temperature: number;
  feelsLike: number;
  humidity: number;
  pressure: number;
  windSpeed: number;
  windDirection: number;
  description: string;
  icon: string;
  timestamp: string;
}

export interface AQITrendData {
  time: string;
  predicted_aqi: number;
  actual_aqi: number;
  status?: string;
}

export interface LocationData {
  city: string;
  country: string;
  latitude: number;
  longitude: number;
}

export interface ForecastData {
  label: string;
  date: string;
  time_range?: string;
  aqi: number;
  status: string;
  explanation: string;
}

export interface DashboardData {
  location: LocationData;
  currentAirQuality: AirQualityData;
  currentWeather: WeatherData;
  forecast24h: AQITrendData[];
  forecast: ForecastData[];
}
