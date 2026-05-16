from pydantic import BaseModel
from datetime import datetime

class WeatherData(BaseModel):
    """
    Schema for validating hourly weather data from Open-Meteo.
    """
    time: datetime
    temperature_2m: float
    surface_pressure: float
    wind_speed_10m: float

class AirQualityData(BaseModel):
    """
    Schema for validating hourly air quality data from Open-Meteo.
    """
    time: datetime
    pm2_5: float
    pm10: float
    sulphur_dioxide: float
    carbon_monoxide: float
    nitrogen_dioxide: float
    us_aqi: int
