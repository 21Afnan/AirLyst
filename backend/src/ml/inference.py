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

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_forecast_weather() -> pd.DataFrame:
    """Fetches weather data: past 2 days (for lags) + next 3 days (forecast)."""
    params = {
        "latitude": settings.LATITUDE,
        "longitude": settings.LONGITUDE,
        "hourly": WEATHER_VARIABLES,
        "past_days": 2,
        "forecast_days": 4,
        "timezone": "auto"
    }
    try:
        # verify=False handles local certificate mismatch or proxy issues on developer systems
        resp = requests.get(settings.FORECAST_URL, params=params, timeout=15, verify=False)
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
        "forecast_days": 4,
        "timezone": "auto"
    }
    try:
        # verify=False handles local certificate mismatch or proxy issues on developer systems
        resp = requests.get(settings.AIR_URL, params=params, timeout=15, verify=False)
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

from src.ml.model_loader import load_model_and_scaler as _load_model_and_scaler

def load_model_and_scaler():
    """Downloads/loads the latest registered model and scaler using the unified model loader."""
    model, scaler, metadata = _load_model_and_scaler()
    return model, scaler, metadata["feature_cols"]


# get_aqi_status imported directly from training.py — no redundancy


# ──────────────────────────────────────────────────────────────
# 4. MAIN INFERENCE FUNCTION
# ──────────────────────────────────────────────────────────────

def run_inference() -> dict:
    """
    End-to-end inference pipeline:
    1. Fetch weather + air quality forecast (past 2 days + next 3 days)
    2. Merge and deduplicate on time
    3. Run FeatureEngineer (reuse existing module, no redundancy)
    4. Filter to only FUTURE hours (after now)
    5. Scale + Predict using saved model
    6. Return clean dictionary of current and forecast predictions
    """
    logger.info("Starting inference pipeline...")

    # Step 1: Fetch both data sources
    weather_df = fetch_forecast_weather()
    aqi_df     = fetch_forecast_air_quality()

    if weather_df.empty or aqi_df.empty:
        logger.error("Inference aborted: could not fetch forecast data.")
        return {"current": None, "forecast": []}

    # Step 2: Merge on time, deduplicate, sort
    merged_df = pd.merge(weather_df, aqi_df, on="time", how="inner")
    merged_df = merged_df.drop_duplicates(subset=["time"]).sort_values("time").reset_index(drop=True)
    logger.info(f"Merged forecast dataset: {len(merged_df)} rows")

    # Step 3: Feature Engineering (reusing existing FeatureEngineer module)
    engineer = FeatureEngineer()
    featured_df = engineer.add_features(merged_df)
    if featured_df.empty:
        logger.error("Inference aborted: feature engineering returned empty dataframe.")
        return {"current": None, "forecast": []}

    # Step 4: Separate CURRENT vs FUTURE rows
    now = pd.Timestamp.now().floor('H')  # Round down to the nearest hour
    
    # Current is the row exactly at 'now' or the last one before 'now'
    current_df = featured_df[featured_df["time"] <= now].tail(1)
    # Future is everything after 'now'
    future_df = featured_df[featured_df["time"] > now].copy()
    
    logger.info(f"Context: {len(current_df)} current row, {len(future_df)} future hours.")

    if current_df.empty and future_df.empty:
        logger.error("Inference aborted: no data available after feature engineering.")
        return {"current": None, "forecast": []}

    # Step 5: Load model and scaler, then predict
    model, scaler, feature_cols = load_model_and_scaler()

    # Combine for prediction to avoid double loading
    to_predict_df = pd.concat([current_df, future_df], ignore_index=True)
    X = to_predict_df[feature_cols]
    X_scaled = pd.DataFrame(scaler.transform(X), columns=feature_cols)
    raw_preds = model.predict(X_scaled)

    # Calculate live SHAP values for the predictions
    shap_vals_arr = None
    try:
        import shap
        import numpy as np
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X_scaled)
        if hasattr(shap_vals, "values"):
            shap_vals_arr = shap_vals.values
        else:
            shap_vals_arr = shap_vals
        shap_vals_arr = np.array(shap_vals_arr)
    except Exception as e:
        logger.error(f"Failed to calculate live SHAP values during inference: {e}")

    # Step 6: Build clean output
    predictions = []
    for i, (_, row) in enumerate(to_predict_df.iterrows()):
        val = {
            "time":           row["time"].strftime("%Y-%m-%d %H:%M"),
            "aqi":            int(round(raw_preds[i])),
            "status":         get_aqi_status(raw_preds[i]),
            "hazardous":      bool(raw_preds[i] > 150),
            "open_meteo_aqi": int(round(row["us_aqi"])),
            "pm2_5":          float(row["pm2_5"]),
            "pm10":           float(row["pm10"]),
            "sulphur_dioxide": float(row["sulphur_dioxide"]),
            "nitrogen_dioxide": float(row["nitrogen_dioxide"]),
            "carbon_monoxide": float(row["carbon_monoxide"]),
            "temperature_2m":  float(row["temperature_2m"]),
            "surface_pressure": float(row["surface_pressure"]),
            "wind_speed_10m":  float(row["wind_speed_10m"]),
        }
        if shap_vals_arr is not None:
            val["shap"] = {
                feature_cols[col_idx]: float(shap_vals_arr[i, col_idx])
                for col_idx in range(len(feature_cols))
            }
        predictions.append(val)

    # Separate current and forecast in the returned list
    return {
        "current": predictions[0] if not current_df.empty else None,
        "forecast": predictions[1:] if not current_df.empty else predictions
    }


# ──────────────────────────────────────────────────────────────
# 5. QUICK LOCAL TEST
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    results = run_inference()
    forecast = results.get("forecast", [])
    current = results.get("current")
    
    print("\n" + "="*80)
    print(f"               AEROVIBE: LOCAL INFERENCE RUN FOR {settings.CITY.upper()}")
    print("="*80)
    
    if current:
        print(f"\n[CURRENT AIR QUALITY STATUS - {current['time']}]")
        print(f"  - Actual Open-Meteo AQI: {current['open_meteo_aqi']}")
        print(f"  - Model Predicted AQI:   {current['aqi']}")
        diff = current['aqi'] - current['open_meteo_aqi']
        diff_str = f"+{diff}" if diff > 0 else str(diff)
        print(f"  - Prediction Difference: {diff_str} AQI points")
        print(f"  - Status Category:       {current['status']}")
        print(f"  - Temp: {current['temperature_2m']}°C | Wind: {current['wind_speed_10m']} mph | Pressure: {current['surface_pressure']} mb")
        print(f"  - PM2.5: {current['pm2_5']} ug/m3 | PM10: {current['pm10']} ug/m3 | NO2: {current['nitrogen_dioxide']} ppb")
    else:
        print("\n[WARNING] No current hour readings returned.")

    if forecast:
        # Group forecast hourly items by calendar date
        days_map = {}
        for r in forecast:
            day_date = r["time"].split(" ")[0] # YYYY-MM-DD
            if day_date not in days_map:
                days_map[day_date] = []
            days_map[day_date].append(r)
            
        # Get today's date to filter out (only show future next 3 days)
        from datetime import datetime
        today_str = datetime.now().strftime("%Y-%m-%d")
        future_days = sorted([(date, items) for date, items in days_map.items() if date != today_str])
        
        print(f"\nTotal Future Predictions Loaded: {len(forecast)} hours across {len(days_map)} calendar dates.")
        
        # Print hourly breakdowns and averages for the next 3 days
        for date, items in future_days[:3]:
            print("\n" + "-"*80)
            print(f" [DATE] FORECAST DATE: {date} (24h Daily Average)")
            print("-"*80)
            print(f"{'Time':<12} | {'Actual (Open-Meteo)':^22} | {'Predicted (Model)':^20} | {'Diff':^8} | {'Status'}")
            print("-"*80)
            
            actual_sum = 0
            pred_sum = 0
            
            for item in items:
                time_only = item["time"].split(" ")[1]
                actual = item["open_meteo_aqi"]
                predicted = item["aqi"]
                actual_sum += actual
                pred_sum += predicted
                
                diff = predicted - actual
                diff_str = f"+{diff}" if diff > 0 else str(diff)
                
                print(f"{time_only:<12} | {actual:^22} | {predicted:^20} | {diff_str:^8} | {item['status']}")
                
            avg_actual = round(actual_sum / len(items), 1)
            avg_pred = round(pred_sum / len(items), 1)
            print("-"*80)
            print(f" >>> DAILY AVERAGE: Actual: {avg_actual} AQI | Predicted: {avg_pred} AQI (Diff: {round(avg_pred - avg_actual, 1)})")
            print("-"*80)
            
    print("\n" + "="*80 + "\n")

