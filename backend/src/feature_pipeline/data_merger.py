import sys
import pandas as pd
from pathlib import Path

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.config import settings
from src.utils.logger import get_logger
from src.data_ingestion.weather_client import WeatherClient
from src.data_ingestion.air_quality_client import AirQualityClient

logger = get_logger("DataMerger")

class DataMerger:
    """
    Orchestrates the fetching and merging of weather and air quality data.
    Ensures a single, clean dataset for feature engineering.
    """
    def __init__(self):
        self.weather_client = WeatherClient()
        self.aqi_client = AirQualityClient()

    def get_merged_dataset(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetches data from both sources and performs an inner join on the 'time' column.
        """
        try:
            # 1. Fetching data
            weather_df = self.weather_client.fetch_data(start_date, end_date)
            aqi_df = self.aqi_client.fetch_data(start_date, end_date)

            if weather_df.empty or aqi_df.empty:
                logger.error("Merging failed: One or more datasets are empty.")
                return pd.DataFrame()

            # Log individual shapes for transparency
            logger.info(f"Raw Weather data: {weather_df.shape}")
            logger.info(f"Raw Air Quality data: {aqi_df.shape}")

            # 2. Merging Logic
            logger.info("Starting Inner Join on 'time' column...")
            merged_df = pd.merge(weather_df, aqi_df, on="time", how="inner")

            # 3. Quality Control
            initial_count = len(merged_df)
            merged_df = merged_df.drop_duplicates(subset=["time"])
            merged_df = merged_df.dropna()
            
            final_count = len(merged_df)
            if initial_count > final_count:
                logger.warning(f"Removed {initial_count - final_count} invalid/duplicate rows.")

            # Final Summary Log
            logger.info(f"SUCCESS: Merged Dataset created.")
            logger.info(f"-> Total Records:  {final_count}")
            logger.info(f"-> Total Features: {len(merged_df.columns)}")
            logger.info(f"-> Feature List:   {list(merged_df.columns)}")
            
            return merged_df

        except Exception as e:
            logger.error(f"Data Merging failed: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    merger = DataMerger()
    start, end = settings.get_backfill_dates()
    
    final_df = merger.get_merged_dataset(start, end)
    
    if not final_df.empty:
        print(f"\n--- [CLEAN MASTER DATASET PREVIEW] ---")
        print(final_df.head(10))
        print(f"\nShape: {final_df.shape}")
        print("--------------------------------------\n")
