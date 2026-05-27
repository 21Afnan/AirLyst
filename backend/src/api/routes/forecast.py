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
from src.utils.config import settings

# Initialize the router
router = APIRouter(
    prefix="/api/forecast",
    tags=["Forecast"]
)

# Global dictionary mapping for clean feature explanation translations
FEATURE_MAP = {
    "lag_1h": "pollution already floating in the air from previous hours",
    "lag_3h": "pollution already floating in the air from previous hours",
    "lag_24h": "pollution already floating in the air from previous hours",
    "rolling": "fine dust and smoke particles",
    "pm2_5": "fine dust and smoke particles",
    "pm10": "fine dust and smoke particles",
    "nitrogen_dioxide": "smoke and exhaust fumes from traffic",
    "sulphur_dioxide": "factory/industrial emissions",
    "carbon_monoxide": "smoke from burning fuels",
    "temperature_2m": "warm weather trapping dirty air near the ground",
    "wind_speed_10m": "still winds that fail to blow away the dust"
}

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



            reasons = []
            if avg_shaps:
                # Sort features by absolute impact and take top 2 drivers
                sorted_feats = sorted(avg_shaps.items(), key=lambda x: abs(x[1]), reverse=True)
                for feat_name, shap_val in sorted_feats[:2]:
                    # Find matching description from dictionary
                    matched = next((val for key, val in FEATURE_MAP.items() if key in feat_name), None)
                    if matched:
                        reasons.append(matched)

            if not reasons:
                reasons.append("normal weather and everyday city emissions")

            # --- DYNAMIC OPENROUTER LLM INTEGRATION ---
            explanation = None
            if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
                try:
                    import requests
                    import json
                    
                    # Design a highly structured prompt to get a clean, friendly 1-sentence response
                    prompt = (
                        f"Based on the air quality drivers: {', '.join(reasons)}. "
                        f"Write a friendly, simple 2-sentence summary of what is causing the air quality. "
                        f"Rules: Do not use markdown, do not use bullet points, do not exceed 15 words, and do not use greeting words."
                    )
                    
                    headers = {
                        "Authorization": f"Bearer {settings.GEMINI_API_KEY.strip()}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": "google/gemini-2.5-flash",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 50
                    }
                    
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        data=json.dumps(data),
                        timeout=10
                    )
                    
                    if response.ok:
                        explanation = response.json()["choices"][0]["message"]["content"].strip()
                except Exception as e:
                    # Fallback if API key is invalid or request fails
                    explanation = None

            # Standard simple fallback logic if Gemini is offline, key is missing, or package is not installed:
            if not explanation:
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
    Calculated dynamically from real-time inference data.
    """
    try:
        # Try to calculate dynamically first from live forecast data
        try:
            data = run_inference()
            all_items = []
            if data.get("current"):
                all_items.append(data["current"])
            if data.get("forecast"):
                all_items.extend(data["forecast"])
                
            shaps_list = [item["shap"] for item in all_items if "shap" in item]
            if shaps_list:
                # We have live SHAP values! Let's aggregate them
                feature_sums = {}
                for sh in shaps_list:
                    for feat, val in sh.items():
                        feature_sums[feat] = feature_sums.get(feat, 0.0) + abs(val)
                
                num_records = len(shaps_list)
                feature_avg = {feat: val / num_records for feat, val in feature_sums.items()}
                
                # Sort features by impact
                sorted_features = sorted(feature_avg.items(), key=lambda x: x[1], reverse=True)
                
                # Format feature importance list
                feature_importance = []
                for i, (feat, impact) in enumerate(sorted_features):
                    matched = next((val for key, val in FEATURE_MAP.items() if key in feat), feat)
                    feature_importance.append({
                        "rank": str(i + 1),
                        "feature": feat,
                        "friendly_name": matched,
                        "impact": round(impact, 4)
                    })
                
                # Generate dynamic report content
                report_lines = [
                    "======================================================================",
                    "                  [AQI MODEL LIVE SHAP EXPLANATION REPORT]",
                    "======================================================================",
                    "",
                    "Model Explained:    LightGBM",
                    f"Dataset Size:       {num_records} live forecast records",
                    "",
                    "Mean Absolute SHAP Values (Feature Impact on Predicted AQI):",
                    "----------------------------------------------------------------------"
                ]
                for item in feature_importance:
                    report_lines.append(f"{item['rank']:<2} | {item['feature']:<25} | Impact: ~{item['impact']:.4f} AQI points")
                report_lines.append("----------------------------------------------------------------------")
                report_lines.append("")
                report_lines.append("Top Live Feature Interpretations:")
                report_lines.append("----------------------------")
                
                for item in feature_importance[:3]:
                    report_lines.append(
                        f"- {item['feature']}: On average, this feature shifts the predicted AQI by {item['impact']:.2f} points.\n"
                        f"  -> Friendly translation: {item['friendly_name'].capitalize()}"
                    )
                
                raw_report = "\n".join(report_lines)
                
                return {
                    "model_name": "LightGBM",
                    "raw_report": raw_report,
                    "feature_importance": feature_importance
                }
        except Exception as e:
            # If dynamic calculation fails, fall back to file/hardcoded
            pass

        # Fallback to static file
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
                        {"rank": "1", "feature": "us_aqi_lag_1h", "friendly_name": "pollution already floating in the air from previous hours", "impact": 27.77},
                        {"rank": "2", "feature": "us_aqi_lag_3h", "friendly_name": "pollution already floating in the air from previous hours", "impact": 2.93},
                        {"rank": "3", "feature": "pm2_5_rolling_24h", "friendly_name": "fine dust and smoke particles", "impact": 2.72},
                        {"rank": "4", "feature": "hour", "friendly_name": "hour of the day", "impact": 0.63},
                        {"rank": "5", "feature": "temperature_2m", "friendly_name": "warm weather trapping dirty air near the ground", "impact": 0.60}
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
                    matched = next((val for key, val in FEATURE_MAP.items() if key in feature), feature)
                    feature_importance.append({
                        "rank": rank,
                        "feature": feature,
                        "friendly_name": matched,
                        "impact": impact
                    })

        return {
            "model_name": "LightGBM",
            "raw_report": content,
            "feature_importance": feature_importance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

