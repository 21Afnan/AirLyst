import sys
import joblib
from pathlib import Path

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent  # Workspace Root: AirLyst
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from src.utils.logger import get_logger

logger = get_logger("ModelLoader")

def load_model_and_scaler():
    """
    Downloads the latest registered model, scaler, and metadata from Hopsworks Model Registry.
    Falls back to locally stored models if Hopsworks connection fails.
    """
    try:
        import hopsworks
        from src.utils.config import settings
        logger.info("Connecting to Hopsworks Model Registry...")
        project = hopsworks.login(
            host=settings.HOPSWORKS_HOST,
            project=settings.HOPSWORKS_PROJECT,
            api_key_value=settings.HOPSWORKS_KEY
        )
        mr = project.get_model_registry()

        logger.info("Downloading latest 'aqi_forecast_model' from registry...")
        hw_model = mr.get_model("aqi_forecast_model")
        model_dir = Path(hw_model.download())
        
        model = joblib.load(model_dir / "best_model.joblib")
        scaler = joblib.load(model_dir / "scaler.joblib")
        metadata = joblib.load(model_dir / "best_model_metadata.joblib")
        
        logger.info(f"SUCCESS: Loaded model '{metadata['model_name']}' (v{hw_model.version}) from Hopsworks")
        return model, scaler, metadata
        
    except Exception as e:
        logger.error(f"FAILED to fetch model from Hopsworks: {e}")
        logger.warning("Attempting to load model from local fallback...")
        
        local_model_path = BACKEND_DIR / "models/best_model.joblib"
        local_scaler_path = BACKEND_DIR / "models/scaler.joblib"
        local_metadata_path = BACKEND_DIR / "models/best_model_metadata.joblib"
        
        if local_model_path.exists() and local_scaler_path.exists() and local_metadata_path.exists():
            model = joblib.load(local_model_path)
            scaler = joblib.load(local_scaler_path)
            metadata = joblib.load(local_metadata_path)
            logger.info(f"SUCCESS: Loaded local fallback model '{metadata['model_name']}'")
            return model, scaler, metadata
        else:
            logger.error("Local fallback model files not found. ABORTING.")
            raise FileNotFoundError("No model files found locally or on Hopsworks Model Registry.")
