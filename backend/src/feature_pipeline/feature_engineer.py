import sys
import pandas as pd
from pathlib import Path

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.utils.logger import get_logger

logger = get_logger("FeatureEngineer")

class FeatureEngineer:
    """
    Finalized Feature Engineer based on Top 15 Feature Importance results.
    Transforms raw merged data into high-performance features for ML models.
    """
    def __init__(self):
        pass

    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies the most impactful features identified during research."""
        if df.empty:
            logger.error("Input DataFrame is empty.")
            return df

        logger.info(f"Engineering features for {len(df)} records...")
        
        # Defensive copy to avoid SettingWithCopy warnings
        df = df.copy()

        # 1. Temporal Markers (Daily, Weekly, and Seasonal Patterns)
        df['hour'] = df['time'].dt.hour
        df['day_of_week'] = df['time'].dt.dayofweek
        df['month'] = df['time'].dt.month
        
        # 2. AQI Lags (Critical for time-series memory)
        df['us_aqi_lag_1h'] = df['us_aqi'].shift(1)
        df['us_aqi_lag_3h'] = df['us_aqi'].shift(3)
        df['us_aqi_lag_6h'] = df['us_aqi'].shift(6)
        df['us_aqi_lag_24h'] = df['us_aqi'].shift(24)

        # 3. PM2.5 Lags (Important pollutant driver)
        df['pm2_5_lag_6h'] = df['pm2_5'].shift(6)
        df['pm2_5_lag_24h'] = df['pm2_5'].shift(24)

        # 4. PM2.5 Rolling Windows (Trend detection)
        df['pm2_5_rolling_6h'] = df['pm2_5'].rolling(window=6).mean()
        df['pm2_5_rolling_24h'] = df['pm2_5'].rolling(window=24).mean()

        # Final Cleanup: Remove NaN rows created by shifts/rolling
        initial_len = len(df)
        df = df.dropna()
        
        logger.info(f"Feature engineering complete. Total columns: {len(df.columns)}. Rows: {len(df)}")
        return df

if __name__ == "__main__":
    from src.feature_pipeline.data_merger import DataMerger
    from src.utils.config import settings

    # Test the pipeline
    merger = DataMerger()
    engineer = FeatureEngineer()
    
    start, end = settings.get_backfill_dates() 
    raw_df = merger.get_merged_dataset(start, end)
    
    featured_df = engineer.add_features(raw_df)
    
    if not featured_df.empty:
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)

        print(f"\n--- [DATASET SCHEMA & HEALTH] ---")
        print(featured_df.info())

        print(f"\n--- [FINAL FEATURE PIPELINE PREVIEW (TOP 10)] ---")
        print(featured_df.head(10))
        
        print(f"\nTotal Records:  {len(featured_df)}")
        print(f"Total Features: {len(featured_df.columns)}")
        print("--------------------------------------------------\n")
