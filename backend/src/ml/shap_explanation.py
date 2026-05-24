import sys
import joblib
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent  # Workspace Root: AirLyst
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from src.ml.preprocessing import load_data
from src.utils.logger import get_logger

logger = get_logger("SHAPExplanation")

from src.ml.model_loader import load_model_and_scaler

def run_shap_analysis():
    """
    Loads the best model from Hopsworks, fetches the features,
    computes SHAP values, and saves interpretation plots.
    """
    # 1. Check/Install SHAP dependency
    try:
        import shap
    except ImportError:
        logger.error("The 'shap' package is not installed. Please run: pip install shap")
        print("\n" + "!"*60)
        print("ERROR: SHAP library is missing.")
        print("Please install it in your virtual environment by running:")
        print("  pip install shap")
        print("!"*60 + "\n")
        sys.exit(1)

    logger.info("Starting SHAP Explanation Pipeline...")

    # 2. Load Model, Scaler & Metadata (using unified loader)
    try:
        model, scaler, metadata = load_model_and_scaler()
        feature_cols = metadata["feature_cols"]
        model_name = metadata["model_name"]
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        sys.exit(1)

    # 3. Load preprocessed feature data
    logger.info("Loading preprocessed dataset...")
    raw_df = load_data()
    
    # Filter features and drop NaNs
    df_clean = raw_df.dropna(subset=feature_cols).copy()
    X = df_clean[feature_cols]
    
    if X.empty:
        logger.error("No valid data rows left for analysis. ABORTING.")
        sys.exit(1)
        
    logger.info(f"Dataset loaded successfully. Shape: {X.shape}")

    # 4. Scale features using the model's scaler
    logger.info("Scaling features...")
    X_scaled = pd.DataFrame(scaler.transform(X), columns=feature_cols)

    # 5. Initialize SHAP Explainer
    logger.info(f"Initializing SHAP Explainer for model type: {model_name}")
    
    # Choose explainer based on model type
    if "Ridge" in model_name:
        explainer = shap.LinearExplainer(model, X_scaled)
        shap_values = explainer.shap_values(X_scaled)
    elif any(tree_model in model_name for tree_model in ["Random Forest", "XGBoost", "LightGBM"]):
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_scaled)
    else:
        explainer = shap.Explainer(model, X_scaled)
        shap_values = explainer(X_scaled)

    # 6. Save SHAP Summary and Bar Plots
    reports_dir = BACKEND_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Summary Plot (Beeswarm)
    logger.info("Generating SHAP Beeswarm Summary Plot...")
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_scaled, show=False)
    summary_path = reports_dir / "shap_summary.png"
    plt.savefig(summary_path, bbox_inches="tight", dpi=300)
    plt.close()
    logger.info(f"Saved Beeswarm Plot to: {summary_path}")

    # Feature Importance Bar Plot
    logger.info("Generating SHAP Feature Importance Bar Plot...")
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_scaled, plot_type="bar", show=False)
    bar_path = reports_dir / "shap_bar.png"
    plt.savefig(bar_path, bbox_inches="tight", dpi=300)
    plt.close()
    logger.info(f"Saved Bar Plot to: {bar_path}")

    # 7. Generate Textual Explanations
    logger.info("Generating textual SHAP explanation report...")
    import numpy as np
    
    # Handle Explanation object vs raw array from SHAP
    if hasattr(shap_values, "values"):
        shap_values_arr = shap_values.values
    else:
        shap_values_arr = shap_values

    # Calculate mean absolute SHAP values for each feature
    mean_abs_shap = np.mean(np.abs(shap_values_arr), axis=0)
    
    # Map to feature names and sort
    feature_importance = pd.DataFrame({
        "Feature": feature_cols,
        "Mean_Abs_SHAP": mean_abs_shap
    }).sort_values(by="Mean_Abs_SHAP", ascending=False).reset_index(drop=True)

    # Save explanation text report
    report_path = reports_dir / "shap_explanation_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("="*70 + "\n")
        f.write("                  [AQI MODEL SHAP EXPLANATION REPORT]\n")
        f.write("="*70 + "\n\n")
        f.write(f"Model Explained:    {model_name}\n")
        f.write(f"Dataset Size:       {X_scaled.shape[0]} records\n\n")
        f.write("Mean Absolute SHAP Values (Feature Impact on Predicted AQI):\n")
        f.write("-" * 70 + "\n")
        for idx, row in feature_importance.iterrows():
            f.write(f"{idx+1:<2} | {row['Feature']:<25} | Impact: ~{row['Mean_Abs_SHAP']:.4f} AQI points\n")
        f.write("-" * 70 + "\n\n")
        f.write("Top Feature Interpretations:\n")
        f.write("-" * 28 + "\n")
        for idx, row in feature_importance.head(3).iterrows():
            feat = row["Feature"]
            val = row["Mean_Abs_SHAP"]
            f.write(f"- {feat}: On average, this feature shifts the predicted AQI by {val:.2f} points.\n")
            if "lag" in feat:
                f.write("  -> Interpretation: Past AQI values are highly predictive of future AQI (strong temporal dependency).\n")
            elif "rolling" in feat:
                f.write("  -> Interpretation: Recent trends and moving averages have a significant smoothing impact on forecasts.\n")
            elif "pm" in feat:
                f.write("  -> Interpretation: Particulate matter concentrations directly drive the US AQI scale calculation.\n")
            elif "temperature" in feat or "pressure" in feat or "wind" in feat:
                f.write("  -> Interpretation: Meteorological conditions affect the dispersion and accumulation of air pollutants.\n")
            f.write("\n")
            
    print("\n" + "="*70)
    print("         [SHAP MODEL INTERPRETABILITY ANALYSIS COMPLETE]")
    print("="*70)
    print(f"Model Explained:    {model_name}")
    print(f"Dataset Size:       {X_scaled.shape[0]} records")
    print(f"Beeswarm Plot:      {summary_path.relative_to(ROOT_DIR)}")
    print(f"Bar Plot:           {bar_path.relative_to(ROOT_DIR)}")
    print(f"Text Report:        {report_path.relative_to(ROOT_DIR)}")
    print("="*70)
    
    print("\n" + "="*70)
    print("             [TOP FEATURE EXPLANATIONS (SHAP VALUES)]")
    print("="*70)
    for idx, row in feature_importance.head(5).iterrows():
        feat = row["Feature"]
        val = row["Mean_Abs_SHAP"]
        print(f"{idx+1}. {feat:<25} : Changes AQI by ~{val:.2f} points on average.")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_shap_analysis()
