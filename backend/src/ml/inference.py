import sys
import requests
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from src.utils.config import settings
from src.utils.constants import WEATHER_VARIABLES, AIR_QUALITY_VARIABLES
from src.feature_pipeline.feature_engineer import FeatureEngineer
from src.ml.training import get_aqi_status
from src.utils.logger import get_logger

logger = get_logger("Inference")

# ──────────────────────────────────────────────────────────────
# 1. DATA FETCHING (past 2 days + next 3 days = context + future)
# ──────────────────────────────────────────────────────────────

def fetch_forecast_weather() -> pd.DataFrame:
    """Fetches weather data: past 2 days (for lags) + next 3 days (forecast)."""
    params = {
        "latitude": settings.LATITUDE,
        "longitude": settings.LONGITUDE,
        "hourly": WEATHER_VARIABLES,
        "past_days": 2,
        "forecast_days": 3,
        "timezone": "auto"
    }
    try:
        resp = requests.get(settings.FORECAST_URL, params=params, timeout=15)
        resp.raise_for_status()
        df = pd.DataFrame(resp.json().get("hourly", {}))
        df["time"] = pd.to_datetime(df["time"])
        logger.info(f"Weather forecast fetched: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Weather forecast fetch failed: {e}")
        return pd.DataFrame()


def fetch_forecast_air_quality() -> pd.DataFrame:
    """Fetches air quality data: past 2 days (for lags) + next 3 days (forecast)."""
    params = {
        "latitude": settings.LATITUDE,
        "longitude": settings.LONGITUDE,
        "hourly": AIR_QUALITY_VARIABLES,
        "past_days": 2,
        "forecast_days": 3,
        "timezone": "auto"
    }
    try:
        resp = requests.get(settings.AIR_URL, params=params, timeout=15)
        resp.raise_for_status()
        df = pd.DataFrame(resp.json().get("hourly", {}))
        df["time"] = pd.to_datetime(df["time"])
        logger.info(f"Air quality forecast fetched: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Air quality forecast fetch failed: {e}")
        return pd.DataFrame()


# ──────────────────────────────────────────────────────────────
# 2. LOAD MODEL + SCALER (from Hopsworks Model Registry)
# ──────────────────────────────────────────────────────────────

def load_model_and_scaler():
    """Downloads the latest registered model and scaler from Hopsworks Model Registry."""
    import hopsworks
    project  = hopsworks.login()
    mr       = project.get_model_registry()

    # get_model() with no version → automatically fetches the latest version
    hw_model = mr.get_model("aqi_forecast_model")
    model_dir = Path(hw_model.download())  # downloads all files to a temp dir

    model    = joblib.load(model_dir / "best_model.joblib")
    scaler   = joblib.load(model_dir / "scaler.joblib")
    metadata = joblib.load(model_dir / "best_model_metadata.joblib")

    logger.info(f"Loaded model from Hopsworks: {metadata['model_name']} (v{hw_model.version})")
    return model, scaler, metadata["feature_cols"]


# get_aqi_status imported directly from training.py — no redundancy


# ──────────────────────────────────────────────────────────────
# 4. MAIN INFERENCE FUNCTION
# ──────────────────────────────────────────────────────────────

def run_inference() -> list[dict]:
    """
    End-to-end inference pipeline:
    1. Fetch weather + air quality forecast (past 2 days + next 3 days)
    2. Merge and deduplicate on time
    3. Run FeatureEngineer (reuse existing module, no redundancy)
    4. Filter to only FUTURE hours (after now)
    5. Scale + Predict using saved model
    6. Return clean list of predictions
    """
    logger.info("Starting inference pipeline...")

    # Step 1: Fetch both data sources
    weather_df = fetch_forecast_weather()
    aqi_df     = fetch_forecast_air_quality()

    if weather_df.empty or aqi_df.empty:
        logger.error("Inference aborted: could not fetch forecast data.")
        return []

    # Step 2: Merge on time, deduplicate, sort
    merged_df = pd.merge(weather_df, aqi_df, on="time", how="inner")
    merged_df = merged_df.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
    logger.info(f"Merged forecast dataset: {len(merged_df)} rows")

    # Step 3: Feature Engineering (reusing existing FeatureEngineer module)
    engineer = FeatureEngineer()
    featured_df = engineer.add_features(merged_df)
    if featured_df.empty:
        logger.error("Inference aborted: feature engineering returned empty dataframe.")
        return []

    # Step 4: Filter only FUTURE rows (after current time)
    now = pd.Timestamp.now()
    future_df = featured_df[featured_df["time"] > now].copy()
    logger.info(f"Future rows for prediction: {len(future_df)} hours")

    if future_df.empty:
        logger.error("Inference aborted: no future rows available after feature engineering.")
        return []

    # Step 5: Load model and scaler, then predict
    model, scaler, feature_cols = load_model_and_scaler()

    X = future_df[feature_cols]
    X_scaled = scaler.transform(X)
    raw_preds = model.predict(X_scaled)

    # Step 6: Build clean output list
    predictions = []
    for i, (_, row) in enumerate(future_df.iterrows()):
        our_aqi        = max(0, int(round(raw_preds[i])))
        openmeteo_aqi  = max(0, int(round(row["us_aqi"])))
        predictions.append({
            "time":           row["time"].strftime("%Y-%m-%d %H:%M"),
            "aqi":            our_aqi,
            "status":         get_aqi_status(our_aqi),
            "hazardous":      our_aqi > 150,
            "open_meteo_aqi": openmeteo_aqi,
        })

    logger.info(f"Inference complete. Total predictions: {len(predictions)} hours")
    return predictions


# ──────────────────────────────────────────────────────────────
# 5. QUICK LOCAL TEST
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    results = run_inference()
    if results:
        print(f"\n{'='*75}")
        print(f"   72h AQI FORECAST FOR {settings.CITY.upper()} — Actual vs Predicted")
        print(f"{'='*75}")
        print(f"{'Time':<22} {'Open-Meteo':>10}  {'Our Model':>10}  {'Diff':>5}  {'Status'}")
        print(f"{'-'*75}")
        for r in results:
            diff = r['aqi'] - r['open_meteo_aqi']
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            print(
                f"{r['time']:<22} "
                f"{r['open_meteo_aqi']:>10}  "
                f"{r['aqi']:>10}  "
                f"{diff_str:>5}  "
                f"{r['status']}"
            )
        print(f"{'='*75}")
        print(f"Total: {len(results)} hour predictions\n")

