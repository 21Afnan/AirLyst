import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent  # Workspace Root: AirLyst
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from src.ml.preprocessing import load_data, split_and_scale
from src.ml.models import get_models
from src.utils.logger import get_logger

logger = get_logger("MLTraining")

def get_aqi_status(aqi: float) -> str:
    """Helper function to map numerical AQI values to US AQI categories."""
    aqi_val = int(round(aqi))
    if aqi_val <= 50:
        return "Good"
    elif aqi_val <= 100:
        return "Moderate"
    elif aqi_val <= 150:
        return "Unhealthy (SG)"  # Sensitive Groups
    elif aqi_val <= 200:
        return "Unhealthy"
    elif aqi_val <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def train_and_evaluate():
    """
    Runs the complete training pipeline:
    1. Loads preprocessed and split chronological datasets.
    2. Runs a tournament comparing Ridge, Random Forest, XGBoost, and LightGBM.
    3. Saves the best model and scaler binaries.
    4. Displays metrics and comparison tables.
    """
    logger.info("Starting ML Training Pipeline...")

    # 1. Load Data
    raw_df = load_data()
    X_train, X_test, y_train, y_test, feature_cols = split_and_scale(raw_df)

    # 2. Retrieve Candidate Models
    models = get_models()
    trained_models = {}
    metrics_summary = []

    # 3. Model Tournament: Loop and evaluate
    logger.info("Running model tournament...")
    for name, model in models.items():
        logger.info(f"Training {name}...")
        model.fit(X_train, y_train)
        
        # Inference on test set
        preds = model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        trained_models[name] = model
        metrics_summary.append({
            "Model": name,
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "R2 Score": round(r2, 4)
        })

    # 4. Show tournament metrics in tabular form
    summary_df = pd.DataFrame(metrics_summary)
    
    # Calculate ranks (lower is better for MAE/RMSE, higher is better for R2)
    summary_df["Rank_MAE"] = summary_df["MAE"].rank(ascending=True, method="min")
    summary_df["Rank_RMSE"] = summary_df["RMSE"].rank(ascending=True, method="min")
    summary_df["Rank_R2"] = summary_df["R2 Score"].rank(ascending=False, method="min")
    summary_df["Composite Score"] = summary_df["Rank_MAE"] + summary_df["Rank_RMSE"] + summary_df["Rank_R2"]
    
    # Sort by Composite Score (lowest score wins!)
    summary_df = summary_df.sort_values(by="Composite Score")
    
    print("\n" + "="*70)
    print("           🏆 MODEL TOURNAMENT SUMMARY (COMPOSITE RANK) 🏆")
    print("="*70)
    print(summary_df.to_string(index=False))
    print("="*70 + "\n")

    # 5. Identify and save the best model (overall winner)
    best_model_name = summary_df.iloc[0]["Model"]
    best_metrics = summary_df.iloc[0].to_dict()
    best_model = trained_models[best_model_name]
    
    print("*"*60)
    print(f"       🥇 OVERALL WINNER MODEL: {best_model_name} 🥇")
    print(f"       MAE: {best_metrics['MAE']} | RMSE: {best_metrics['RMSE']} | R2: {best_metrics['R2 Score']}")
    print(f"       Combined Rank Score: {best_metrics['Composite Score']} (Lowest is best)")
    print("*"*60 + "\n")
    
    logger.info(f"Winner model: {best_model_name} (Composite Score: {best_metrics['Composite Score']})")



    # Save model and metadata
    model_path = ROOT_DIR / "backend/models/best_model.joblib"
    metadata_path = ROOT_DIR / "backend/models/best_model_metadata.joblib"
    
    # Create models directory if it doesn't exist
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(best_model, model_path)
    joblib.dump({
        "model_name": best_model_name,
        "metrics": best_metrics,
        "feature_cols": feature_cols
    }, metadata_path)
    logger.info(f"Saved best model to {model_path}")
    logger.info(f"Saved metadata to {metadata_path}")

    # 6. Register to Hopsworks Model Registry
    register_to_hopsworks(best_model_name, best_metrics)

    # 7. Show test predictions vs actual values in a comparison table
    best_preds = best_model.predict(X_test)
    comparison_df = pd.DataFrame({
        "Actual AQI": y_test.values,
        "Actual Status": [get_aqi_status(val) for val in y_test.values],
        "Predicted AQI": np.round(best_preds).astype(int),
        "Predicted Status": [get_aqi_status(val) for val in best_preds],
        "Absolute Error": np.abs(y_test.values - best_preds).round().astype(int)
    })


    print("="*65)
    print("       📋 TEST SET SAMPLING: ACTUAL VS PREDICTED AQI 📋")
    print("="*65)
    print(comparison_df.head(15).to_string(index=True))
    print("="*65 + "\n")

def register_to_hopsworks(best_model_name: str, best_metrics: dict):
    """Registers the locally saved best model and scaler to the Hopsworks Model Registry."""
    logger.info("Registering the winning model to Hopsworks Model Registry...")
    try:
        import hopsworks
        project = hopsworks.login()
        mr = project.get_model_registry()

        # Create model entry in the registry (framework is implicitly Python for mr.python)
        hw_model = mr.python.create_model(
            name="aqi_forecast_model",
            metrics={
                "mae": best_metrics["MAE"],
                "rmse": best_metrics["RMSE"],
                "r2_score": best_metrics["R2 Score"]
            },
            description=f"Winning model ({best_model_name}) for Islamabad 72h AQI forecasting."
        )


        # Upload the entire models directory directly
        models_dir = str(ROOT_DIR / "backend/models")
        logger.info(f"Uploading files from directory: {models_dir} to Model Registry...")
        hw_model.save(models_dir)
        logger.info("SUCCESS: Model successfully registered and uploaded to Hopsworks Model Registry!")
    except Exception as e:
        logger.error(f"FAILED to register model to Hopsworks: {e}")

if __name__ == "__main__":
    train_and_evaluate()


