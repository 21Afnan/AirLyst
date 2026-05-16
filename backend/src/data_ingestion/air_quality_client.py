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
from src.utils.schemas import AirQualityData
from src.utils.constants import AIR_QUALITY_VARIABLES

logger = get_logger("AirQualityClient")

class AirQualityClient:
    """
    Handles communication with the Open-Meteo Air Quality API.
    Validates data against the AirQualityData Pydantic schema.
    """
    def __init__(self):
        self.url = settings.AIR_URL
        self.latitude = settings.LATITUDE
        self.longitude = settings.LONGITUDE

    def fetch_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetches historical air quality data and validates it.
        """
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": AIR_QUALITY_VARIABLES,
            "timezone": "auto"
        }

        try:
            logger.info(f"Requesting Air Quality data for {settings.CITY} [{start_date} to {end_date}]")
            
            response = requests.get(self.url, params=params, timeout=15)
            response.raise_for_status()
            
            raw_data = response.json().get("hourly", {})
            df = pd.DataFrame(raw_data)
            
            # --- DATA VALIDATION LAYER ---
            # Validate each row against the AirQualityData schema
            validated_records = [
                AirQualityData(**row).model_dump() 
                for row in df.to_dict('records')
            ]
            
            cleaned_df = pd.DataFrame(validated_records)
            logger.info(f"Successfully validated {len(cleaned_df)} air quality records.")
            return cleaned_df

        except Exception as e:
            logger.error(f"Air Quality Fetching Error: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    # Test script execution
    client = AirQualityClient()
    
    # Use the full backfill window defined in config.py
    start, end = settings.get_backfill_dates()
    
    aqi_df = client.fetch_data(start, end)
    
    if not aqi_df.empty:
        print(f"\n--- [AQI BACKFILL SUMMARY] ---")
        print(f"Total Hourly Records: {len(aqi_df)}")
        print(f"Time Window:         {aqi_df['time'].min()}  TO  {aqi_df['time'].max()}")
        print(f"Pollutants Fetched:  {list(aqi_df.columns)}")
        print(f"------------------------------\n")
        
        print("First 5 rows (Pollutants & AQI):")
        print(aqi_df.head())
