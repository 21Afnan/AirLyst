import sys
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from src.utils.config import settings
from src.utils.logger import get_logger
from src.feature_pipeline.data_merger import DataMerger
from src.feature_pipeline.feature_engineer import FeatureEngineer
from src.feature_pipeline.feature_store_client import FeatureStoreClient

logger = get_logger("RunFeaturePipeline")

def run_pipeline():
    """
    Runs the feature pipeline to fetch the last 7 days of data, engineer features, 
    and upload them to the Hopsworks Feature Store.
    """
    logger.info("Starting Feature Pipeline Execution...")

    # Determine Date Range: Fetch the last 7 days to compute lags and rolling windows correctly
    start_date, end_date = settings.get_update_dates(days=7)
    logger.info(f"Running in DAILY UPDATE mode from {start_date} to {end_date}")

    # 2. Merge Data
    merger = DataMerger()
    raw_df = merger.get_merged_dataset(start_date, end_date)
    if raw_df.empty:
        logger.error("Pipeline aborted: Merged raw dataset is empty.")
        sys.exit(1)

    # 3. Engineer Features
    engineer = FeatureEngineer()
    featured_df = engineer.add_features(raw_df)
    if featured_df.empty:
        logger.error("Pipeline aborted: Feature engineering returned empty dataset.")
        sys.exit(1)

    # Clean duplicates in time
    initial_len = len(featured_df)
    featured_df = featured_df.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
    if len(featured_df) < initial_len:
        logger.info(f"Dropped {initial_len - len(featured_df)} duplicate rows on time column.")

    # 4. Upload to Hopsworks
    store = FeatureStoreClient()
    logger.info("Connecting to Hopsworks...")
    if store.connect():
        logger.info("Uploading data to Hopsworks Feature Group...")
        store.upload_data(featured_df, group_name="aqi_islamabad_feat")
    else:
        logger.warning("Hopsworks connection failed. Will only update the local fallback CSV.")

    # 5. Update local CSV fallback
    local_data_dir = BACKEND_DIR / "data"
    local_data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = local_data_dir / "engineered_features.csv"

    existing_rows = 0
    new_total_rows = 0
    added_rows = 0
    file_existed = csv_path.exists()

    # If the file exists, merge the new features with existing local data and drop duplicates to keep history
    if file_existed:
        try:
            logger.info("Merging new features with local CSV database...")
            existing_df = pd.read_csv(csv_path)
            existing_rows = len(existing_df)
            
            existing_df["time"] = pd.to_datetime(existing_df["time"])
            featured_df["time"] = pd.to_datetime(featured_df["time"])
            
            combined_df = pd.concat([existing_df, featured_df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
            combined_df.to_csv(csv_path, index=False)
            new_total_rows = len(combined_df)
            added_rows = new_total_rows - existing_rows
        except Exception as e:
            logger.error(f"Error merging with local CSV: {e}")
            featured_df.to_csv(csv_path, index=False)
            new_total_rows = len(featured_df)
            added_rows = len(featured_df)
    else:
        featured_df.to_csv(csv_path, index=False)
        new_total_rows = len(featured_df)
        added_rows = len(featured_df)

    # Print summary of pipeline execution
    print("\n" + "="*65)
    print("           📊 FEATURE PIPELINE EXECUTION SUMMARY 📊")
    print("="*65)
    print(f"Data Fetching Window:   {start_date} to {end_date}")
    print(f"Engineered Time Range:  {featured_df['time'].min()} to {featured_df['time'].max()}")
    print(f"New Rows Engineered:    {len(featured_df)}")
    print(f"Local Database Before:  {existing_rows} rows")
    print(f"Local Database After:   {new_total_rows} rows (Total Dataset Size)")
    print(f"New Unique Rows Added:  {added_rows} rows")
    print(f"Hopsworks Status:       Pushed {len(featured_df)} rows to Feature Store")
    print("="*65 + "\n")

if __name__ == "__main__":
    run_pipeline()
