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
            summaries.append({
                "label": f"Day {i+1}",
                "date": date,
                "avg_aqi": int(round(avg)),
                "status": get_aqi_status(avg)
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

