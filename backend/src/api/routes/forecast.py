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

# Helper function to find average of a list of numbers
def calculate_average(numbers_list):
    total = sum(numbers_list)
    count = len(numbers_list)
    return total / count

@router.get("")
def get_forecast():
    """
    Returns 72-hour AQI Forecast.
    Gives daily summaries (averages) and raw hourly forecasts.
    """
    try:
        # 1. Run the ML model inference to get hourly predictions
        hourly_predictions = run_inference()
        
        if not hourly_predictions:
            raise HTTPException(status_code=404, detail="No predictions found.")
        
        # 2. Group hourly predictions by their Date (YYYY-MM-DD)
        daily_groups = {}
        for item in hourly_predictions:
            # Extract date part (YYYY-MM-DD) from the time string
            date_key = item["time"].split(" ")[0]
            
            # If the date is not yet in our dictionary, create an empty list
            if date_key not in daily_groups:
                daily_groups[date_key] = []
            
            # Add this hour's prediction to the list for this date
            daily_groups[date_key].append(item)
            
        # 3. Calculate daily averages using simple loops
        daily_summaries = []
        for date_key in sorted(daily_groups.keys()):
            hours_data = daily_groups[date_key]
            
            # Collect all AQI scores for this specific day
            our_aqis = []
            open_meteo_aqis = []
            for h in hours_data:
                our_aqis.append(h["aqi"])
                open_meteo_aqis.append(h["open_meteo_aqi"])
                
            # Find the average AQI score for both models
            avg_our_aqi = calculate_average(our_aqis)
            avg_open_meteo = calculate_average(open_meteo_aqis)
            
            # Convert decimal average to nearest round integer
            rounded_our_aqi = int(round(avg_our_aqi))
            rounded_open_meteo = int(round(avg_open_meteo))
            
            # Get the AQI health status category (e.g. Good, Moderate)
            status_desc = get_aqi_status(rounded_our_aqi)
            
            # Set hazardous flag if average AQI is above 150
            is_hazardous = False
            if rounded_our_aqi > 150:
                is_hazardous = True
                
            # Create a simple dictionary summary for this day
            day_summary = {
                "date": date_key,
                "avg_aqi": rounded_our_aqi,
                "avg_open_meteo_aqi": rounded_open_meteo,
                "status": status_desc,
                "hazardous": is_hazardous
            }
            daily_summaries.append(day_summary)
            
        # 4. Return combined response back to frontend
        return {
            "success": True,
            "daily_forecast": daily_summaries,
            "hourly_forecast": hourly_predictions
        }
        
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/latest")
def get_latest():
    """
    Returns the latest single prediction (current hour).
    """
    try:
        # Run ML model inference to get predictions
        hourly_predictions = run_inference()
        
        if not hourly_predictions:
            raise HTTPException(status_code=404, detail="No predictions available.")
            
        # The first item in the list represents the current/nearest hour prediction
        latest_prediction = hourly_predictions[0]
        
        return {
            "success": True,
            "latest": latest_prediction
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
