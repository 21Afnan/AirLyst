import sys
import hopsworks
import pandas as pd
from pathlib import Path

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.config import settings
from src.utils.logger import get_logger

logger = get_logger("FeatureStoreClient")

class FeatureStoreClient:
    """
    Handles connection and data insertion to the Hopsworks Feature Store.
    """
    def __init__(self):
        self.project = None
        self.fs = None

    def connect(self):
        """Authenticates and connects to the Hopsworks project."""
        try:
            logger.info("Connecting to Hopsworks Feature Store...")
            # Note: This will look for HOPSWORKS_API_KEY in .env or ask in terminal
            self.project = hopsworks.login()
            self.fs = self.project.get_feature_store()
            logger.info(f"SUCCESS: Connected to project '{self.project.name}'")
            return True
        except Exception as e:
            logger.error(f"FAILED to connect to Hopsworks: {str(e)}")
            return False

    def upload_data(self, df: pd.DataFrame, group_name: str, version: int = 1):
        """Creates or updates a feature group and inserts data."""
        if self.fs is None:
            logger.error("No active Feature Store connection. Call connect() first.")
            return

        try:
            logger.info(f"Preparing Feature Group: '{group_name}' (v{version})...")
            
            # 1. Define the Feature Group
            # We use 'time' as the primary key and event_time for time-series support
            aqi_fg = self.fs.get_or_create_feature_group(
                name=group_name,
                version=version,
                primary_key=['time'],
                event_time='time',
                description="Engineered AQI and Weather features for Islamabad (72h Forecast Pipeline)"
            )

            # 2. Insert Data
            logger.info(f"Inserting {len(df)} records into Feature Store...")
            aqi_fg.insert(df)
            
            logger.info(f"SUCCESS: Data successfully pushed to '{group_name}'")
            
        except Exception as e:
            logger.error(f"FAILED to upload data: {str(e)}")

    def read_data(self, group_name: str, version: int = 1) -> pd.DataFrame:
        """Reads data from a feature group and returns it as a DataFrame."""
        if self.fs is None:
            logger.error("No active Feature Store connection. Call connect() first.")
            return pd.DataFrame()

        try:
            logger.info(f"Reading data from Feature Group: '{group_name}' (v{version})...")
            fg = self.fs.get_feature_group(name=group_name, version=version)
            df = fg.read()
            logger.info(f"SUCCESS: Retrieved {len(df)} records from '{group_name}'")
            return df
        except Exception as e:
            logger.error(f"FAILED to read data from Feature Store: {str(e)}")
            return pd.DataFrame()

if __name__ == "__main__":
    # Test reading data from Feature Store
    store = FeatureStoreClient()
    
    if store.connect():
        df = store.read_data(group_name="aqi_islamabad_feat")
        
        if not df.empty:
            print("\n" + "="*50)
            print("SUCCESS: Data Fetched for Testing")
            print("="*50)
            print(f"Shape: {df.shape}")
            print(df.head())
            print("="*50)
        else:
            print("No data found in Feature Group.")
