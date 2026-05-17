import sys
sys.dont_write_bytecode = True  # Prevents creation of __pycache__ folders

from pathlib import Path
import joblib
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="joblib")
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
warnings.filterwarnings("ignore", category=UserWarning, module="lightgbm")

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Standard Machine Learning Regressors
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# PyTorch Deep Learning
import torch
import torch.nn as nn
import numpy as np
from src.utils.logger import get_logger

logger = get_logger("DeepLearningModels")

def get_model(model_type="random_forest", n_estimators=100, max_depth=None, learning_rate=0.1):
    """
    Simple helper function to initialize and return standard machine learning regressors.
    All returned models share standard Scikit-Learn API: `.fit(X, y)` and `.predict(X)`.
    """
    if model_type == "random_forest":
        return RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
    elif model_type == "xgboost":
        depth = max_depth if max_depth is not None else 6
        return XGBRegressor(
            n_estimators=n_estimators,
            max_depth=depth,
            learning_rate=learning_rate,
            random_state=42
        )
    elif model_type == "lightgbm":
        depth = max_depth if max_depth is not None else -1
        return LGBMRegressor(
            n_estimators=n_estimators,
            max_depth=depth,
            learning_rate=learning_rate,
            random_state=42,
            verbosity=-1
        )
    elif model_type == "gradient_boosting":
        return GradientBoostingRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth if max_depth is not None else 3,
            learning_rate=learning_rate,
            random_state=42
        )
    elif model_type == "knn":
        return KNeighborsRegressor(
            n_neighbors=5,
            weights='distance'
        )
    elif model_type == "ridge":
        return Ridge(
            alpha=1.0,
            random_state=42
        )
    else:
        raise ValueError(f"Unknown model_type: {model_type}. Choose 'random_forest', 'xgboost', 'lightgbm', 'gradient_boosting', 'knn', or 'ridge'.")

if __name__ == "__main__":
    # Test the simple function with dummy data
    import numpy as np
    X_dummy = np.random.rand(10, 5)
    y_dummy = np.random.rand(10) * 150
    
    print("\n" + "="*50)
    print("TESTING DIRECT MODELS VIA HELPER FUNCTION")
    print("="*50)
    
    # 1. Random Forest Regressor
    rf = get_model("random_forest", n_estimators=10)
    rf.fit(X_dummy, y_dummy)
    print(f"Random Forest Preds Shape: {rf.predict(X_dummy).shape}")
    
    # 2. XGBoost Regressor
    xgb = get_model("xgboost", n_estimators=10)
    xgb.fit(X_dummy, y_dummy)
    print(f"XGBoost Regressor Preds Shape: {xgb.predict(X_dummy).shape}")
    
    # 3. LightGBM Regressor
    lgbm = get_model("lightgbm", n_estimators=10)
    lgbm.fit(X_dummy, y_dummy)
    print(f"LightGBM Regressor Preds Shape: {lgbm.predict(X_dummy).shape}")
    
    # 4. Standard Joblib Saving and Loading
    save_path = Path("backend/models/test_direct_model.joblib")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save natively
    joblib.dump(lgbm, save_path)
    print("Native Save Successful.")
    
    # Load natively
    loaded_model = joblib.load(save_path)
    print(f"Loaded Model Preds Shape: {loaded_model.predict(X_dummy).shape}")
    
    # Clean up
    if save_path.exists():
        save_path.unlink()
        
    print("="*50 + "\n")

# --- Deep Learning PyTorch Models ---

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out.squeeze()

class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.gru(x)
        out = self.fc(out[:, -1, :])
        return out.squeeze()
