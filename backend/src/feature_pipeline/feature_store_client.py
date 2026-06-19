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
        """Creates or updates a feature group, inserts data and returns metrics dict."""
        if self.fs is None:
            logger.error("No active Feature Store connection. Call connect() first.")
            return {
                "success": False,
                "error": "No active Feature Store connection.",
                "count_before": 0,
                "count_after": 0,
                "num_appended": 0,
                "num_updated": 0
            }

        try:
            logger.info(f"Preparing Feature Group: '{group_name}' (v{version})...")
            
            # 1. Define the Feature Group with online_enabled=True
            aqi_fg = self.fs.get_or_create_feature_group(
                name=group_name,
                version=version,
                primary_key=['time'],
                event_time='time',
                online_enabled=True,
                description="Engineered AQI and Weather features for Islamabad (72h Forecast Pipeline)"
            )

            # 2. Get existing data from the Online Store to calculate metrics
            count_before = 0
            existing_times_str = set()
            try:
                df_before = aqi_fg.read(online=True)
                if df_before is not None and not df_before.empty:
                    count_before = len(df_before)
                    if 'time' in df_before.columns:
                        df_before['time'] = pd.to_datetime(df_before['time'])
                        existing_times_str = set(df_before['time'].dt.strftime('%Y-%m-%d %H:%M:%S'))
            except Exception as e:
                logger.warning(f"Could not read existing data for count comparison: {e}. Assuming empty.")

            # 3. Calculate how many rows will be Appended vs Updated
            incoming_df = df.copy()
            incoming_df['time'] = pd.to_datetime(incoming_df['time'])
            incoming_times_str = set(incoming_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S'))
            
            num_updated = len([t for t in incoming_times_str if t in existing_times_str])
            num_appended = len([t for t in incoming_times_str if t not in existing_times_str])

            # 4. Insert Data
            # Disable automatic materialization to avoid the 415 SDK error on trigger
            aqi_fg.insert(df, write_options={"start_offline_materialization": False})
            
            # Now trigger the materialization job manually, passing env_vars={} to force JSON content-type
            logger.info("Manually launching materialization job with JSON payload...")
            try:
                job_run = aqi_fg.materialization_job.run(
                    args=aqi_fg.materialization_job.config.get("defaultArgs", ""),
                    await_termination=False,
                    env_vars={}  # Forces the SDK to use application/json content-type
                )
                if job_run is None:
                    logger.info("Materialization job is already running. Skipping new launch.")
                else:
                    logger.info("Materialization job successfully launched.")
            except Exception as job_err:
                logger.warning(f"Could not trigger materialization job: {job_err}")

            logger.info(f"SUCCESS: Data successfully pushed to '{group_name}'")
            
            # 5. Get actual count after upload
            count_after = count_before
            try:
                df_after = aqi_fg.read(online=True)
                if df_after is not None and not df_after.empty:
                    count_after = len(df_after)
            except Exception as e:
                logger.warning(f"Could not read data after upload to verify count: {e}. Estimating.")
                count_after = count_before + num_appended

            return {
                "success": True,
                "count_before": count_before,
                "count_after": count_after,
                "num_appended": num_appended,
                "num_updated": num_updated,
                "error": None
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"FAILED to upload data: {error_msg}")
            return {
                "success": False,
                "count_before": 0,
                "count_after": 0,
                "num_appended": 0,
                "num_updated": 0,
                "error": error_msg
            }

    def read_data(self, group_name: str, version: int = 1) -> pd.DataFrame:
        """Reads data from a feature group and returns it as a DataFrame."""
        if self.fs is None:
            logger.error("No active Feature Store connection. Call connect() first.")
            return pd.DataFrame()

        try:
            logger.info(f"Reading data from Feature Group: '{group_name}' (v{version})...")
            fg = self.fs.get_feature_group(name=group_name, version=version)
            df = fg.read(online=True)
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
