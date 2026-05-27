import sys
from pathlib import Path
from fastapi import APIRouter, HTTPException

# --- PATH CONFIGURATION ---
# This matches the workspace directories so python can find our packages
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

# Import run_inference function and get_aqi_status function
from src.ml.inference import run_inference
from src.ml.training import get_aqi_status

# Initialize the router
router = APIRouter(
    prefix="/api/forecast",
    tags=["Forecast"]
)

@router.get("")
def get_forecast():
    """
    Main endpoint to return current AQI and future daily/hourly forecasts.
    """
    try:
        # 1. Fetch prediction data from the ML inference pipeline
        data = run_inference()
        
        current_aqi = data.get("current")
        forecast_list = data.get("forecast", [])
        
        # 2. Format the next 24 hours of forecast predictions
        forecast_24h = []
        for item in forecast_list[:24]:
            time_str = item["time"].split(" ")[1] if " " in item["time"] else item["time"]
            forecast_24h.append({
                "time": time_str,
                "predicted_aqi": item["aqi"],
                "actual_aqi": item.get("open_meteo_aqi", item["aqi"]),
                "status": item["status"]
            })

        # Group hourly predictions by date to calculate daily averages and aggregate SHAP values
        days_map = {}
        for item in forecast_list:
            day_name = item["time"].split(" ")[0]  # YYYY-MM-DD
            if day_name not in days_map:
                days_map[day_name] = {
                    "aqis": [],
                    "shaps": []
                }
            days_map[day_name]["aqis"].append(item["aqi"])
            if "shap" in item:
                days_map[day_name]["shaps"].append(item["shap"])

        # Calculate Average AQI and dynamic SHAP-based explanation for each day
        # Skip today's date so cards show tomorrow, day after, and in 3 days (full 24-hour averages)
        from datetime import datetime
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        summaries = []
        future_days = [(date, metrics) for date, metrics in sorted(days_map.items()) if date != today_str]
        
        for i, (date, metrics) in enumerate(future_days[:3]):
            aqis = metrics["aqis"]
            if not aqis:
                continue
            avg_aqi = sum(aqis) / len(aqis)
            rounded_avg = int(round(avg_aqi))
            status = get_aqi_status(rounded_avg)

            # Aggregate actual SHAP values for this day
            avg_shaps = {}
            if metrics["shaps"]:
                for feat in metrics["shaps"][0].keys():
                    feat_vals = [s[feat] for s in metrics["shaps"] if feat in s]
                    avg_shaps[feat] = sum(feat_vals) / len(feat_vals)

            # Map the top SHAP features of the LightGBM model to friendly descriptions
            reasons = []
            if avg_shaps:
                # Sort features by absolute impact
                sorted_feats = sorted(avg_shaps.items(), key=lambda x: abs(x[1]), reverse=True)
                
                # Take top 2 drivers
                for feat_name, shap_val in sorted_feats[:2]:
                    if "lag_1h" in feat_name or "lag_3h" in feat_name or "lag_24h" in feat_name:
                        reasons.append("pollution already floating in the air from previous hours")
                    elif "rolling" in feat_name or "pm2_5" in feat_name or "pm10" in feat_name:
                        reasons.append("soot and dust particles suspended in the atmosphere")
                    elif "nitrogen_dioxide" in feat_name:
                        reasons.append("smoke and exhaust fumes from traffic traffic")
                    elif "sulphur_dioxide" in feat_name:
                        reasons.append("harmful gases emitted from local industries")
                    elif "carbon_monoxide" in feat_name:
                        reasons.append("carbon monoxide gas from burning fuels")
                    elif "temperature_2m" in feat_name:
                        reasons.append("warm weather trapping dirty air near the ground")
                    elif "wind_speed_10m" in feat_name:
                        reasons.append("still winds that fail to blow away the dust")

            if not reasons:
                reasons.append("stable atmospheric conditions and standard urban emissions")

            explanation = f"Driven mainly by " + " combined with ".join(reasons) + "."

            # Calculate time range for this day
            day_items = [item for item in forecast_list if item["time"].startswith(date)]
            time_range = ""
            if day_items:
                def to_12h(t_str):
                    time_part = t_str.split(" ")[1] # "15:00"
                    h, m = map(int, time_part.split(":"))
                    suffix = "AM" if h < 12 else "PM"
                    h_12 = h if h <= 12 else h - 12
                    h_12 = 12 if h_12 == 0 else h_12
                    return f"{h_12} {suffix}"
                start_h = to_12h(day_items[0]["time"])
                end_h = to_12h(day_items[-1]["time"])
                time_range = f"{start_h} to {end_h}"

            summaries.append({
                "label": f"Day {i+1}",
                "date": date,
                "time_range": time_range,
                "avg_aqi": rounded_avg,
                "status": status,
                "is_hazardous": bool(rounded_avg > 150),
                "explanation": explanation
            })

        # 4. Return the simplified structured response with summaries
        return {
            "current": current_aqi,
            "forecast_24h": forecast_24h,
            "summaries": summaries
        }
        
    except Exception as e:
        # Catch unexpected errors and return a 500 status code
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/explain")
def get_shap_explanation():
    """
    Returns the textual SHAP explanation report and feature importances as JSON.
    """
    try:
        report_path = BACKEND_DIR / "reports/shap_explanation_report.txt"
        if not report_path.exists():
            # Trigger SHAP analysis if the report is not pre-generated
            try:
                from src.ml.shap_explanation import run_shap_analysis
                run_shap_analysis()
            except Exception:
                # Return fallback hardcoded SHAP statistics if package/data is missing
                return {
                    "model_name": "LightGBM",
                    "explanation": "SHAP explanation report is not ready. Showing pre-calculated feature importances.",
                    "feature_importance": [
                        {"rank": "1", "feature": "us_aqi_lag_1h", "impact": 27.77},
                        {"rank": "2", "feature": "us_aqi_lag_3h", "impact": 2.93},
                        {"rank": "3", "feature": "pm2_5_rolling_24h", "impact": 2.72},
                        {"rank": "4", "feature": "hour", "impact": 0.63},
                        {"rank": "5", "feature": "temperature_2m", "impact": 0.60}
                    ]
                }
        
        # Read the file
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse the feature importances to return as structured data for the frontend
        feature_importance = []
        lines = content.split("\n")
        start_parsing = False
        for line in lines:
            if "Mean Absolute SHAP Values" in line:
                start_parsing = True
                continue
            if start_parsing and "----" in line:
                if len(feature_importance) > 0:
                    start_parsing = False  # end of section
                continue
            if start_parsing and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    rank = parts[0].strip()
                    feature = parts[1].strip()
                    impact_str = parts[2].replace("Impact:", "").replace("AQI points", "").replace("~", "").strip()
                    try:
                        impact = float(impact_str)
                    except ValueError:
                        impact = 0.0
                    feature_importance.append({
                        "rank": rank,
                        "feature": feature,
                        "impact": impact
                    })

        return {
            "model_name": "LightGBM",
            "raw_report": content,
            "feature_importance": feature_importance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

