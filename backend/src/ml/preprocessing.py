import sys
sys.dont_write_bytecode = True  # Prevents creation of __pycache__ folders

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import joblib

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Import the existing feature store client & verify module to completely avoid redundancy
from src.feature_pipeline.feature_store_client import FeatureStoreClient
from src.feature_pipeline.verify_feature_store import fetch_data
from src.utils.logger import get_logger

logger = get_logger("MLPreprocessing")

class DataPreprocessor:
    """
    Orchestrates the loading, chronological splitting, and scaling of 
    our dataset fetched directly from Hopsworks.
    """
    def __init__(self, group_name: str = "aqi_islamabad_feat", version: int = 1):
        self.group_name = group_name
        self.version = version
        self.scaler = StandardScaler()
        self.store = FeatureStoreClient()
        
    def load_and_preprocess(self, test_size: float = 0.2, scaler_save_path: str = "backend/models/scaler.joblib"):
        """
        Fetches data from Hopsworks, separates target, splits chronologically, 
        scales the features, and saves the fitted scaler.
        """
        # 1. Connect using existing FeatureStoreClient (The connect ftn from feature store!)
        if not self.store.connect():
            logger.error("Failed to connect to Hopsworks.")
            return None
            
        # 2. Fetch data using fetch_data from verify_feature_store (No redundancy, inherits verify outputs!)
        df = fetch_data(self.store, group_name=self.group_name, version=self.version)
        
        if df.empty:
            logger.error("Fetched dataset from Hopsworks is empty!")
            return None
            
        logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns from Hopsworks.")
        
        # 3. Chronological sorting (crucial for time-series data to maintain temporal order)
        df = df.sort_values(by="time").reset_index(drop=True)
        
        # 4. Handle null/missing values defensively (crucial for model training stability)
        initial_rows = df.shape[0]
        df = df.dropna().reset_index(drop=True)
        dropped_rows = initial_rows - df.shape[0]
        if dropped_rows > 0:
            logger.info(f"Dropped {dropped_rows} rows containing null/NaN values.")
            
        # 5. Separate target (continuous 'us_aqi')
        y = df['us_aqi'].values
        
        # 6. Separate features: drop target 'us_aqi', 'time', and 'aqi_status' (if present) to keep training strictly continuous
        cols_to_drop = ['us_aqi', 'time']
        if 'aqi_status' in df.columns:
            cols_to_drop.append('aqi_status')
            
        X_df = df.drop(columns=cols_to_drop)
        feature_names = X_df.columns.tolist()
        X = X_df.values
        
        # 7. Chronological split (no random shuffle to avoid lookahead data leakage)
        split_idx = int(len(df) * (1 - test_size))
        
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        logger.info(f"Chronological split complete: Train size = {len(X_train)}, Test size = {len(X_test)}")
        
        # 8. Fit & Transform Scaler
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 9. Save Scaler for evaluator/inference service to ensure consistent feature scaling
        save_path = Path(scaler_save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.scaler, save_path)
        logger.info(f"Fitted scaler successfully saved to {save_path}")
        
        return {
            "X_train": X_train_scaled,
            "X_test": X_test_scaled,
            "y_train": y_train,
            "y_test": y_test,
            "feature_names": feature_names
        }

if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = DataPreprocessor()
    data = preprocessor.load_and_preprocess()
    if data:
        print("\n" + "="*50)
        print("ML PREPROCESSING STEP SUCCESSFUL")
        print("="*50)
        print(f"X_train shape: {data['X_train'].shape}")
        print(f"X_test shape:  {data['X_test'].shape}")
        print(f"y_train shape: {data['y_train'].shape}")
        print(f"y_test shape:  {data['y_test'].shape}")
        print("Features used:", data['feature_names'])
        print("="*50 + "\n")
