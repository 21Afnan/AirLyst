from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
# pyrefly: ignore [missing-import]
import lightgbm as lgb

def get_models() -> dict:
    """
    Returns a dictionary of initialized models for the tournament.
    Includes Ridge, Random Forest, XGBoost, and LightGBM.
    """
    return {
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "XGBoost": xgb.XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "LightGBM": lgb.LGBMRegressor(n_estimators=100, random_state=42, n_jobs=-1, verbose=-1)
    }
