import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
from src.utils.logger import get_logger

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

logger = get_logger("ConfigLoader")

class Settings:
    """
    Loads and validates all environment variables from .env
    Acts as the single source of truth for the backend.
    """
    def __init__(self):
        # 1. LOAD THE .ENV FILE
        self.ENV_PATH = ROOT_DIR / ".env"
        load_dotenv(self.ENV_PATH)
        
        try:
            # 2. EXTRACT VARIABLES
            self.APP_NAME = os.getenv("APP_NAME", "AirLyst")
            self.ENV = os.getenv("ENV", "development")
            
            # Hopsworks
            self.HOPSWORKS_KEY = os.getenv("HOPSWORKS_API_KEY")
            self.HOPSWORKS_PROJECT = os.getenv("HOPSWORKS_PROJECT")
            self.HOPSWORKS_HOST = os.getenv("HOPSWORKS_HOST")
            
            # Location
            self.CITY = os.getenv("CITY", "Islamabad")
            self.LATITUDE = float(os.getenv("LATITUDE", 33.72))
            self.LONGITUDE = float(os.getenv("LONGITUDE", 73.04))
            
            # Open-Meteo Endpoints
            self.WEATHER_URL = os.getenv("WEATHER_URL")
            self.AIR_URL = os.getenv("AIR_URL")
            self.FORECAST_URL = os.getenv("FORECAST_URL")

            # Gemini Key
            self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
            
            # 3. CRITICAL CHECKS
            if not self.HOPSWORKS_KEY:
                raise ValueError("HOPSWORKS_API_KEY is missing!")
            
            if not self.WEATHER_URL or not self.AIR_URL:
                raise ValueError("API URLs are missing!")
            
            logger.info(f"SUCCESS: All settings loaded for {self.APP_NAME} in {self.CITY}")
            
        except Exception as e:
            logger.error(f"ERROR: Configuration Error: {e}")
            sys.exit(1)

    def get_backfill_dates(self, years=1.5):
        """Calculates dates for Phase 2: Historical Data"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=int(years * 365))
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    def get_update_dates(self, days=7):
        """Calculates start and end dates for incremental daily updates."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    def print_settings(self):
        """Debug function to verify loaded settings."""
        print("\n--- [DEBUG] CURRENT LOADED SETTINGS ---")
        print(f"App Name:    {self.APP_NAME}")
        print(f"City:        {self.CITY} ({self.LATITUDE}, {self.LONGITUDE})")
        print(f"Hopsworks:   {self.HOPSWORKS_PROJECT} at {self.HOPSWORKS_HOST}")
        print(f"Weather URL: {self.WEATHER_URL}")
        print(f"Air URL:     {self.AIR_URL}")
        if self.HOPSWORKS_KEY:
             print(f"API Key:     {self.HOPSWORKS_KEY[:8]}********")
        print("---------------------------------------\n")

# Instantiate once
settings = Settings()

# Only print settings if we are running this file directly
if __name__ == "__main__":
    settings.print_settings()
