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
    start_date, end_date = settings.get_backfill_dates(years=1.5)
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
    
    count_before = 0
    count_after = 0
    
    if store.connect():
        logger.info("Uploading data to Hopsworks Feature Group...")
        count_before, count_after = store.upload_data(featured_df, group_name="aqi_islamabad_feat")
    else:
        logger.error("Hopsworks connection failed. ABORTING pipeline to prevent silent failure.")
        sys.exit(1)

    # Print summary of pipeline execution
    print("\n" + "="*65)
    print("           [FEATURE PIPELINE EXECUTION SUMMARY]")
    print("="*65)
    print(f"Data Fetching Window:   {start_date} to {end_date}")
    print(f"Engineered Time Range:  {featured_df['time'].min()} to {featured_df['time'].max()}")
    print(f"New Rows Engineered:    {len(featured_df)}")
    print(f"Hopsworks DB Before:    {count_before} rows")
    print(f"Hopsworks DB After:     {count_after} rows (Total Dataset Size)")
    print(f"New Unique Rows Added:  {count_after - count_before} rows")
    print("="*65 + "\n")

if __name__ == "__main__":
    run_pipeline()
