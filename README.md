# 🌬️ AirLyst: High-Precision AQI Forecasting Pipeline

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/MLOps-Hopsworks-orange?style=for-the-badge&logo=git" />
  <img src="https://img.shields.io/badge/Status-Production--Ready-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Data-Open--Meteo-blueviolet?style=for-the-badge" />
</div>

---

## 🚀 Overview
**AirLyst** is an end-to-end MLOps pipeline for high-precision time-series AQI forecasting in Islamabad. It integrates real-time air quality and weather data via a **Hopsworks Feature Store**, automating the full data lifecycle—from ingestion to advanced feature engineering—to deliver reliable 72-hour air quality predictions.

---

## 🏗️ Project Architecture
```mermaid
graph TD
    A[Weather API] --> C[Data Merger]
    B[Air Quality API] --> C
    C --> D[Feature Engineer]
    D --> E[Hopsworks Feature Store]
    E --> F[Model Training - LSTM/RF]
    F --> G[72h Forecast Inferences]
    G --> H[Frontend Dashboard]
```

---

## ✨ Key Features
- **🎯 Super-Slim Pipeline:** Engineered 21+ elite features including temporal markers (hour, day, month), AQI lags (1h-24h), and PM2.5 rolling averages.
- **☁️ Cloud-Native Feature Store:** Seamless integration with Hopsworks for data versioning and consistent training/inference.
- **🧠 Advanced Forecasting:** Support for both high-performance Random Forest and Deep Learning (Stacked LSTM) architectures.
- **⚡ Real-time Ingestion:** Automated data fetching and cleaning for Islamabad city metrics.

---

## 🛠️ Technology Stack
- **Languages:** ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- **Frameworks:** ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
- **MLOps:** ![Hopsworks](https://img.shields.io/badge/Hopsworks-FeatureStore-orange?style=for-the-badge)
- **Data:** ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

---

## 🚀 Getting Started

### 1. Installation
```bash
git clone https://github.com/21Afnan/AirLyst.git
cd AirLyst
pip install -r requirements.txt
```

### 2. Run Feature Pipeline
```bash
python backend/src/feature_pipeline/feature_engineer.py
```

### 3. Train Model
```bash
python backend/src/models/lstm_trainer.py
```

---

## 📊 Model Performance
| Model | MAE | RMSE | R2 Score |
| :--- | :--- | :--- | :--- |
| Random Forest | ~1.5 | ~2.8 | 0.99 |
| LSTM (20 Epochs) | 12.2 | 16.4 | 0.59 |

---

## 🗺️ Roadmap
- [x] Data Ingestion & Backfill
- [x] Feature Engineering (Top 15 Elite)
- [x] LSTM Baseline Training
- [ ] Hopsworks Feature Store Sync (Phase 3)
- [ ] Interactive Streamlit Dashboard
- [ ] Daily Automated Forecasting Jobs

---

<div align="center">
  Developed with ❤️ for a cleaner Islamabad 🌿
</div>
