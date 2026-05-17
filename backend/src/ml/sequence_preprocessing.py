import sys
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.ml.preprocessing import DataPreprocessor

class SequencePreprocessor:
    """
    Handles fetching and formatting the data into 3D sequences specifically 
    for training Deep Learning models like LSTMs and GRUs.
    """
    def __init__(self, time_steps=24):
        self.time_steps = time_steps
        self.base_preprocessor = DataPreprocessor()
        self.y_scaler = StandardScaler()

    def create_sequences(self, X, y):
        Xs, ys = [], []
        for i in range(len(X) - self.time_steps):
            Xs.append(X[i:(i + self.time_steps)])
            ys.append(y[i + self.time_steps])
        return np.array(Xs), np.array(ys)

    def load_and_preprocess(self):
        # Re-use existing tabular preprocessing (handles NaN dropping, scaling X, fetching)
        data = self.base_preprocessor.load_and_preprocess()
        if data is None:
            return None

        # Scale the target variable y for stable neural network training
        y_train_scaled = self.y_scaler.fit_transform(data["y_train"].reshape(-1, 1)).flatten()
        y_test_scaled = self.y_scaler.transform(data["y_test"].reshape(-1, 1)).flatten()

        X_train_seq, y_train_seq = self.create_sequences(data["X_train"], y_train_scaled)
        X_test_seq, y_test_seq = self.create_sequences(data["X_test"], y_test_scaled)

        return {
            "X_train_seq": X_train_seq,
            "y_train_seq": y_train_seq,
            "X_test_seq": X_test_seq,
            "y_test_seq": y_test_seq,
            "y_scaler": self.y_scaler,
            "feature_names": data["feature_names"]
        }
