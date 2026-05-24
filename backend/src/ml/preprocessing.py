import sys
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import joblib

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent  # Workspace Root: AirLyst
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from src.feature_pipeline.feature_store_client import FeatureStoreClient
from src.utils.logger import get_logger

logger = get_logger("MLPreprocessing")

def load_data(group_name: str = "aqi_islamabad_feat", version: int = 1) -> pd.DataFrame:
    """Fetches data from Hopsworks. Falls back to local CSV if connection fails."""
    logger.info("Fetching data from feature store...")
    store = FeatureStoreClient()
    
    if store.connect():
        from src.feature_pipeline.verify_feature_store import fetch_data as fetch_hopsworks
        df = fetch_hopsworks(store, group_name, version)
        if not df.empty:
            return df
            
    logger.warning("Falling back to local CSV data...")
    return pd.read_csv(ROOT_DIR / "backend/data/engineered_features.csv")

def split_and_scale(df: pd.DataFrame, target_col: str = "us_aqi", split_ratio: float = 0.8):
    """Sorts, splits chronologically, scales features, and saves the scaler."""
    # 1. Sort by time
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values("time").reset_index(drop=True)

    # 2. Extract features and target (drop NaNs to prevent errors)
    ignore_cols = ["time", "aqi_status", target_col]
    feature_cols = [col for col in df.columns if col not in ignore_cols]
    
    df_clean = df.dropna(subset=feature_cols + [target_col]).copy()
    
    # 3. Chronological Split (prevents time-series leakage / overfitting)
    split_idx = int(len(df_clean) * split_ratio)
    train_df = df_clean.iloc[:split_idx]
    test_df = df_clean.iloc[split_idx:]
    
    X_train, y_train = train_df[feature_cols].copy(), train_df[target_col].copy()
    X_test, y_test = test_df[feature_cols].copy(), test_df[target_col].copy()
    logger.info(f"Chronological split done. Train: {len(X_train)} | Test: {len(X_test)}")

    # 4. Scale numeric features (fit on train ONLY to avoid data leakage)
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_cols)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=feature_cols)

    # 5. Save the scaler for inference
    scaler_path = ROOT_DIR / "backend/models/scaler.joblib"
    scaler_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, scaler_path)
    logger.info(f"Scaler saved to {scaler_path}")

    return X_train_scaled, X_test_scaled, y_train, y_test, feature_cols

if __name__ == "__main__":
    try:
        raw_df = load_data()
        X_train, X_test, y_train, y_test, features = split_and_scale(raw_df)
        print("\n--- [EASY PREPROCESSING TEST SUCCESS] ---")
        print(f"X_train shape: {X_train.shape} | X_test shape: {X_test.shape}")
        print("-------------------------------------------\n")
    except Exception as e:
        logger.error(f"Test failed: {e}")

