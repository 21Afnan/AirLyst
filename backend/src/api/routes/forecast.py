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

        # 2. Group hourly predictions by date to calculate daily averages
        days_map = {}
        for item in forecast_list:
            # Extract date (YYYY-MM-DD) from the time string
            day_name = item["time"].split(" ")[0] 
            if day_name not in days_map:
                days_map[day_name] = []
            # Append the AQI value to the list for this specific day
            days_map[day_name].append(item["aqi"])

        # 3. Calculate Average AQI and Status for each day
        summaries = []
        for i, (date, aqi_values) in enumerate(sorted(days_map.items())):
            # Calculate mean AQI for the day
            avg = sum(aqi_values) / len(aqi_values)
            rounded_avg = int(round(avg))
            summaries.append({
                "label": f"Day {i+1}",
                "date": date,
                "avg_aqi": rounded_avg,
                "status": get_aqi_status(rounded_avg),
                "is_hazardous": bool(rounded_avg > 150)
            })

        # 4. Return the structured response
        return {
            "current": current_aqi,
            "summaries": summaries,
            "raw_hourly": forecast_list
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

