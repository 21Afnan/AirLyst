import sys
import requests
import pandas as pd
from pathlib import Path

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.config import settings
from src.utils.logger import get_logger
from src.utils.schemas import WeatherData
from src.utils.constants import WEATHER_VARIABLES

logger = get_logger("WeatherClient")

class WeatherClient:
    """
    Handles communication with the Open-Meteo Weather API.
    Provides data validation and type-safe DataFrame conversion.
    """
    def __init__(self):
        self.url = settings.WEATHER_URL
        self.latitude = settings.LATITUDE
        self.longitude = settings.LONGITUDE

    def fetch_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetches historical weather data and validates it via Pydantic.
        """
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": WEATHER_VARIABLES,
            "timezone": "auto"
        }

        try:
            logger.info(f"Requesting weather data for {settings.CITY} [{start_date} to {end_date}]")
            
            response = requests.get(self.url, params=params, timeout=15)
            response.raise_for_status()
            
            raw_data = response.json().get("hourly", {})
            df = pd.DataFrame(raw_data)
            
            # --- DATA VALIDATION LAYER ---
            validated_records = [
                WeatherData(**row).model_dump() 
                for row in df.to_dict('records')
            ]
            
            cleaned_df = pd.DataFrame(validated_records)
            logger.info(f"Successfully validated {len(cleaned_df)} records.")
            return cleaned_df

        except Exception as e:
            logger.error(f"Weather Fetching Error: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    # Test script execution
    client = WeatherClient()
    
    # Using the full 1.5-year window as defined in config.py
    # This will fetch approximately 13,000+ hourly records.
    start, end = settings.get_backfill_dates() # Default is 1.5 years
    
    weather_df = client.fetch_data(start, end)
    
    if not weather_df.empty:
        print(f"\n--- [FULL BACKFILL SUMMARY] ---")
        print(f"Total Hourly Records: {len(weather_df)}")
        print(f"Time Window:         {weather_df['time'].min()}  TO  {weather_df['time'].max()}")
        print(f"Columns Fetched:     {list(weather_df.columns)}")
        print(f"-------------------------------\n")
        
        print("Dataset Sample (First 5 rows):")
        print(weather_df.head())
        print("\nDataset Sample (Last 5 rows):")
        print(weather_df.tail())
