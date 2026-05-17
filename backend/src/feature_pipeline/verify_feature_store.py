import sys
import pandas as pd
from pathlib import Path

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.feature_pipeline.feature_store_client import FeatureStoreClient
from src.utils.logger import get_logger

logger = get_logger("VerifyFeatureStore")

def fetch_data(store: FeatureStoreClient, group_name: str, version: int = 1) -> pd.DataFrame:
    """
    Fetches the data from the feature group and prints the first few rows to verify successful storage.
    Returns the loaded DataFrame.
    """
    df = store.read_data(group_name=group_name, version=version)
    
    if not df.empty:
        print("\n" + "="*50)
        print(f"VERIFICATION SUCCESS: Data fetched from '{group_name}'")
        print("="*50)
        print(f"Shape: {df.shape}")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nColumns available:")
        print(df.columns.tolist())
        print("="*50 + "\n")
    else:
        logger.error("Fetched DataFrame is empty. Check if materialization is complete on Hopsworks.")
        
    return df

def verify_data():
    """
    Connects to Hopsworks, fetches the data from the feature group, 
    and prints the first few rows to verify successful storage.
    """
    store = FeatureStoreClient()
    
    if store.connect():
        fetch_data(store, "aqi_islamabad_feat")
    else:
        logger.error("Could not connect to Hopsworks for verification.")

if __name__ == "__main__":
    verify_data()
