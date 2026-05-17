# backend/src/ml/trainer.py
import sys
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="joblib")

import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Prevent pycache folders and resolve importing from 'src'
sys.dont_write_bytecode = True
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Import preprocessors
from src.ml.preprocessing import DataPreprocessor
from src.ml.sequence_preprocessing import SequencePreprocessor

# Import models
from src.ml.models import get_model, LSTMModel, GRUModel
from src.utils.logger import get_logger

logger = get_logger("UnifiedTrainer")

def train_sequence_model(model, train_loader, epochs=30, lr=0.001):
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            epoch_loss += loss.item()
        if (epoch + 1) % 10 == 0:
            logger.info(f"Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss/len(train_loader):.4f}")
    return model

def evaluate_sequence_model(model, X_test, y_test_scaled, y_scaler):
    model.eval()
    with torch.no_grad():
        preds = model(X_test).numpy()
    
    # Unscale predictions and actuals
    preds_unscaled = y_scaler.inverse_transform(preds.reshape(-1, 1)).flatten()
    y_test_unscaled = y_scaler.inverse_transform(y_test_scaled.reshape(-1, 1)).flatten()
    
    mae = mean_absolute_error(y_test_unscaled, preds_unscaled)
    rmse = np.sqrt(mean_squared_error(y_test_unscaled, preds_unscaled))
    r2 = r2_score(y_test_unscaled, preds_unscaled)
    
    return preds_unscaled, mae, rmse, r2

def train_and_evaluate():
    logger.info("Initializing Preprocessors...")
    
    # 1. ML Data
    logger.info("Fetching and preprocessing data for Standard ML models...")
    ml_preprocessor = DataPreprocessor()
    ml_data = ml_preprocessor.load_and_preprocess()
    
    # 2. Sequence Data
    logger.info("Fetching and preprocessing data for Deep Learning Sequence models...")
    seq_preprocessor = SequencePreprocessor(time_steps=24)
    seq_data = seq_preprocessor.load_and_preprocess()
    
    if ml_data is None or seq_data is None:
        logger.error("Data preprocessing failed. Cannot continue.")
        return
        
    feature_names = ml_data["feature_names"]
    X_train_ml = pd.DataFrame(ml_data["X_train"], columns=feature_names)
    X_test_ml = pd.DataFrame(ml_data["X_test"], columns=feature_names)
    y_train_ml, y_test_ml = ml_data["y_train"], ml_data["y_test"]
    
    X_train_seq_t = torch.tensor(seq_data["X_train_seq"], dtype=torch.float32)
    y_train_seq_t = torch.tensor(seq_data["y_train_seq"], dtype=torch.float32)
    X_test_seq_t = torch.tensor(seq_data["X_test_seq"], dtype=torch.float32)
    
    train_dataset = TensorDataset(X_train_seq_t, y_train_seq_t)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=False)
    
    metrics = {}
    predictions = {}
    trained_models = {}
    
    # --- A. Train Standard ML Models ---
    ml_models = ["random_forest", "xgboost", "lightgbm", "gradient_boosting", "knn", "ridge"]
    for m_type in ml_models:
        logger.info(f"Training and Evaluating ML Model: {m_type.upper()}")
        model = get_model(m_type)
        model.fit(X_train_ml, y_train_ml)
        
        preds = model.predict(X_test_ml)
        
        # Align predictions to match sequence test size (to ensure fair evaluation)
        aligned_preds = preds[seq_preprocessor.time_steps:]
        aligned_y_test = y_test_ml[seq_preprocessor.time_steps:]
        
        mae = mean_absolute_error(aligned_y_test, aligned_preds)
        rmse = np.sqrt(mean_squared_error(aligned_y_test, aligned_preds))
        r2 = r2_score(aligned_y_test, aligned_preds)
        
        trained_models[m_type] = model
        metrics[m_type] = {"MAE": mae, "RMSE": rmse, "R2": r2}
        predictions[m_type] = aligned_preds
        
    # --- B. Train Deep Learning Sequence Models ---
    input_size = X_train_seq_t.shape[2]
    dl_models = {
        "LSTM": LSTMModel(input_size=input_size),
        "GRU": GRUModel(input_size=input_size)
    }
    
    for name, model in dl_models.items():
        logger.info(f"Training DL Model: {name}")
        train_sequence_model(model, train_loader, epochs=30)
        logger.info(f"Evaluating DL Model: {name}")
        
        preds_unscaled, mae, rmse, r2 = evaluate_sequence_model(
            model, X_test_seq_t, seq_data["y_test_seq"], seq_data["y_scaler"]
        )
        
        trained_models[name] = model
        metrics[name] = {"MAE": mae, "RMSE": rmse, "R2": r2}
        predictions[name] = preds_unscaled

    # --- C. Print Unified Comparison Table ---
    df_metrics = pd.DataFrame(metrics).T
    print("\n" + "="*60)
    print("        UNIFIED MODEL COMPARISON TABLE (ALL 8 MODELS)")
    print("="*60)
    print(df_metrics.round(4).to_string())
    print("="*60 + "\n")
    
    # --- D. Save Winner Model ---
    best_name = min(metrics, key=lambda k: metrics[k]["RMSE"])
    best_model = trained_models[best_name]
    best_rmse = metrics[best_name]["RMSE"]
    
    logger.info(f"OVERALL WINNER: {best_name.upper()} (RMSE: {best_rmse:.2f})")
    
    model_dir = Path("backend/models")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    if best_name in ml_models:
        joblib.dump(best_model, model_dir / "best_model.joblib")
    else:
        torch.save(best_model.state_dict(), model_dir / "best_model.pth")
        
    joblib.dump({"model_type": best_name, "rmse": best_rmse}, model_dir / "best_model_metadata.joblib")
    logger.info("Saved winner model and metadata successfully.")
    
    # --- E. Visuals & Final Actual vs Predicted ---
    best_preds = predictions[best_name]
    y_test_aligned = y_test_ml[seq_preprocessor.time_steps:]
    sample_df = pd.DataFrame({
        "Actual": y_test_aligned.astype(int),
        "Predicted": np.round(best_preds).astype(int),
        "Error": np.abs(y_test_aligned.astype(int) - np.round(best_preds).astype(int))
    })
    
    print("="*55)
    print(f"  ACTUAL VS PREDICTED (Overall Winner: {best_name.upper()}) - Last 10")
    print("="*55)
    print(sample_df.tail(10).to_string(index=False))
    print("="*55 + "\n")
    
    plt.figure(figsize=(10, 5))
    plt.plot(y_test_aligned[-150:], label="Actual US AQI", color="black", linewidth=2)
    plt.plot(best_preds[-150:], label=f"Predicted ({best_name.upper()})", color="orange", linestyle="--")
    plt.title(f"AirLyst Model: Actual vs Predicted AQI (Last 150 Hours)")
    plt.xlabel("Time Steps (Hours)")
    plt.ylabel("US AQI Value")
    plt.legend()
    plt.grid(True, linestyle=":")
    plt.tight_layout()
    plt.savefig(model_dir / "loss_curve.png", dpi=300)
    plt.close()
    logger.info("Saved visual loss curve successfully.")

if __name__ == "__main__":
    train_and_evaluate()
