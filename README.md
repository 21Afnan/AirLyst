<div align="center">

# 🌌 <span style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 3rem;">AirLyst: Precision AQI Engine</span>

### 🌬️ "Predicting the air you breathe, powered by state-of-the-art MLOps."

<div align="center">
  <h3>🚀 <a href="https://air-lyst.vercel.app" target="_blank"><b>Click Here to View the Live AirLyst Dashboard</b></a> 🚀</h3>
  <a href="https://air-lyst.vercel.app" target="_blank">
    <img src="https://img.shields.io/badge/🌐_Live_Dashboard-AirLyst_Web-00f2fe?style=for-the-badge&logo=vercel&logoColor=white&labelColor=0d1b2a" alt="Live Demo" />
  </a>
</div>
<br/>

<p align="center">
  <a href="https://github.com/21Afnan/AirLyst/actions/workflows/feature_pipeline.yml">
    <img src="https://github.com/21Afnan/AirLyst/actions/workflows/feature_pipeline.yml/badge.svg" alt="Feature Pipeline" />
  </a>
  <a href="https://github.com/21Afnan/AirLyst/actions/workflows/training_pipeline.yml">
    <img src="https://github.com/21Afnan/AirLyst/actions/workflows/training_pipeline.yml/badge.svg" alt="Training Pipeline" />
  </a>
</p>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Hopsworks](https://img.shields.io/badge/Hopsworks-Feature_Store-FF7F00?style=for-the-badge)](https://www.hopsworks.ai/)

</div>

---

## 📖 Executive Summary

The **AirLyst** project is a production-grade MLOps (Machine Learning Operations) system designed to provide 72-hour predictive insights into urban air quality. Unlike standard weather apps that offer only current observations, AirLyst leverages advanced regression models and real-time data pipelines to forecast pollution trends, helping users make informed decisions about their respiratory health. It features an automated data ingestion pipeline, cloud-based feature storage, a machine learning training tournament, explainable AI (SHAP), generative AI translations, and a high-performance web dashboard.

---

## ✨ Key Project Features

*   **72-Hour Predictions**: Hourly granularity for the next 3 days.
*   **AI-Powered Insights**: Real-time explanations of pollution drivers utilizing SHAP and Gemini 2.0 Flash.
*   **Professional Dashboard**: Includes interactive charts, EPA-standard color coding, and responsive design for mobile.
*   **Automated Pipeline**: The system is designed to update its data and predictions daily with zero manual effort.
*   **Model Tournament**: Retrains weekly. Competes Ridge, Random Forest, XGBoost, and LightGBM models using custom chronological time-series splitting to avoid future data leakage.

---

## 📷 Interactive Dashboard Showcase

Here is a visual walk-through of the premium **AirLyst Next.js Frontend Dashboard** showing real-time observations, 72-hour forecast charts, and local AI explanation widgets:

<div align="center">
  <table>
    <tr>
      <td width="33.3%" align="center">
        <img src="assets/ssfg/AeroVibe%20Main%20Dashboard.png" alt="AirLyst Main Dashboard" style="border-radius: 12px; border: 2px solid #3B82F6;" />
        <br />
        <b>1. Main Dashboard View</b>
        <p><i>Real-time AQI dials, weather metrics, and daily predictions.</i></p>
      </td>
      <td width="33.3%" align="center">
        <img src="assets/ssfg/AI%20Explanations%20&amp;%20SHAP%20Insights.png" alt="AI Explanations & SHAP Insights" style="border-radius: 12px; border: 2px solid #D946EF;" />
        <br />
        <b>2. AI SHAP Insights</b>
        <p><i>Local Shapley explanations translating variables to human language.</i></p>
      </td>
      <td width="33.3%" align="center">
        <img src="assets/ssfg/Hourly%20Predictions%20Chart.png" alt="Hourly Predictions Chart" style="border-radius: 12px; border: 2px solid #818CF8;" />
        <br />
        <b>3. Hourly Trends Chart</b>
        <p><i>EPA-banded 24-hour predictive line chart with tooltips.</i></p>
      </td>
    </tr>
  </table>
</div>

---

## ⚡ Interactive System Architecture

**AirLyst** uses a decoupled, dual-stage pipeline that integrates weather & air quality ingestion, sliding temporal window engineering, model tournament selection, cloud-hosted registries, and live SHAP-based local explainability.

```mermaid
flowchart TD
    %% Styling and Premium Palette
    classDef datasource fill:#1E293B,stroke:#3B82F6,stroke-width:2px,color:#F8FAFC;
    classDef featurestore fill:#1E1B4B,stroke:#818CF8,stroke-width:2px,color:#F8FAFC;
    classDef pipeline fill:#0F172A,stroke:#0EA5E9,stroke-width:2px,color:#F8FAFC;
    classDef mlops fill:#311042,stroke:#D946EF,stroke-width:2px,color:#F8FAFC;
    classDef ui fill:#022C22,stroke:#10B981,stroke-width:2px,color:#F8FAFC;

    %% Data Sources
    OM_Air["📡 Open-Meteo Air Quality API"]:::datasource
    OM_Weather["📡 Open-Meteo Weather API"]:::datasource

    subgraph FE [Daily Ingestion & Feature Engineering]
        DataMerger["Merged Data (data_merger.py)"]:::pipeline
        FeatureEng["Lag & Rolling features (feature_engineer.py)"]:::pipeline
        FSClient["FeatureStoreClient (feature_store_client.py)"]:::pipeline
    end

    Hopsworks["☁️ Hopsworks Online Feature Store"]:::featurestore

    subgraph ML [Training Tournament & Explainability]
        Prep["Scaler & Chronological Split (preprocessing.py)"]:::mlops
        Tournament["Tournament Selection (models.py)"]:::mlops
        Training["Model Registry Sync (training.py)"]:::mlops
        SHAP["SHAP global explanations (shap_explanation.py)"]:::mlops
    end

    ModelRegistry["📦 Hopsworks Model Registry"]:::featurestore

    subgraph API [FastAPI Service Layer]
        Inference["Inference Pipeline (inference.py)"]:::pipeline
        ForecastRouter["Forecast API Route (forecast.py)"]:::pipeline
        MainAPI["Main Web Server (main.py)"]:::pipeline
    end

    subgraph NextJS [Next.js Dashboard UI]
        APIClient["API client.ts (Mock Fallback)"]:::ui
        AQICard["AQICard Progress Widget"]:::ui
        TrendChart["Interactive Trend Chart"]:::ui
        AIInsights["Live SHAP AI Insights"]:::ui
    end

    %% Connections
    OM_Air & OM_Weather --> DataMerger
    DataMerger --> FeatureEng --> FSClient --> Hopsworks
    Hopsworks --> Prep --> Tournament --> Training --> ModelRegistry
    Training -.-> SHAP
    ModelRegistry --> Inference --> ForecastRouter --> MainAPI --> APIClient --> AQICard & TrendChart & AIInsights

    linkStyle default stroke:#64748B,stroke-width:2px;
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | Main logic and AI model development. |
| **Web Backend** | FastAPI | High-speed API for serving real-time forecasts. |
| **Frontend** | Next.js, TailwindCSS | Professional, responsive user dashboard. |
| **Database** | Hopsworks Feature Store | Cloud storage for consistent training and inference data. |
| **AI Models** | XGBoost, LightGBM, Ridge | High-accuracy regression for time-series forecasting. |
| **Explainability** | SHAP (Shapley Values) | Identifying which factors (wind, humidity) drive pollution. |
| **Generative AI**| Gemini 2.0 Flash / OpenRouter | Translating complex data into simple human insights. |

---

## ⚙️ Core MLOps Components & Directory Deep-Dive

* **Feature Store Integration (`src/feature_pipeline/`)**: AirLyst uses the **Hopsworks Feature Store** to store engineered targets, avoiding training-serving skew. The system computes sliding temporal lags (`1h`, `3h`, `6h`, `24h`) and moving averages.
* **Model Tournament (`src/ml/`)**: Trains models (Ridge, Random Forest, XGBoost, LightGBM) using chronological time-series splitting to avoid leakage. Selects the best performing model based on a Composite Rank Score (MAE, RMSE, R2) and promotes it to the Hopsworks Model Registry.
* **Dynamic AI Translations (`src/api/routes/forecast.py`)**: Integrates OpenRouter API with `google/gemini-2.5-flash` to dynamically translate technical air quality drivers (derived via SHAP) into friendly, 2-sentence explanations.
* **Live SHAP Explanations (`src/ml/inference.py`)**: The inference pipeline calculates absolute SHAP values across real-time hourly forecasts in memory, ensuring feature importance rankings adapt to live patterns instantly.
* **FastAPI Service (`src/api/`)**: Provides REST endpoints with CORS and automated fallback configurations, serving both real-time metrics and explainability insights.

---

## 🤖 Automated MLOps Pipelines & Hopsworks Integration

AirLyst leverages GitHub Actions for fully automated data ingestion and model training. The system seamlessly integrates with **Hopsworks** to manage the Feature Store and Model Registry.

### 1️⃣ Feature Pipeline Action (Daily)
Automated daily ingestion of weather and air quality data, feature engineering, and uploading to the Hopsworks Feature Store.

<div align="center">
  <b>Feature Pipeline Execution Logs:</b><br/>
  <br/>
  <img src="backend/Githubactions_ima_acc/feature_pipeline.png" alt="Feature Pipeline 1" style="border-radius: 8px; margin-bottom: 10px; max-width: 100%;" />
  <img src="backend/Githubactions_ima_acc/feat2.png" alt="Feature Pipeline 2" style="border-radius: 8px; margin-bottom: 10px; max-width: 100%;" />
  <img src="backend/Githubactions_ima_acc/feat3.png" alt="Feature Pipeline 3" style="border-radius: 8px; margin-bottom: 10px; max-width: 100%;" />
  <br/>
  <b>Hopsworks Feature Group:</b><br/>
  <img src="backend/Githubactions_ima_acc/featuregroup%20hopsworks%20.png" alt="Hopsworks Feature Group" style="border-radius: 8px; margin-top: 10px; max-width: 100%;" />
</div>

<br/>

### 2️⃣ Model Tournament & Training Action (Weekly)
Automated weekly chronological split training. Competes multiple models (Ridge, RF, XGBoost, LightGBM) and registers the champion model to the Hopsworks Model Registry.

**🏆 Current Model Tournament Results (Hopsworks):**

| Model | MAE | RMSE | R² Score | Composite Score | Rank |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LightGBM (Winner) 🥇** | **1.7290** | **3.2361** | **0.9860** | **4.0** | **1st** |
| Random Forest | 1.6628 | 3.5025 | 0.9836 | 7.0 | 2nd |
| XGBoost | 1.8900 | 3.4636 | 0.9840 | 7.0 | 2nd |
| Ridge Regression | 2.9303 | 4.7994 | 0.9693 | 12.0 | 4th |

*Composite score is calculated based on cumulative rank across MAE, RMSE, and R² (lower is better).*

<div align="center">
  <b>Model Tournament Execution Logs:</b><br/>
  <br/>
  <img src="backend/Githubactions_ima_acc/model_tournamaent%20action1.png" alt="Model Tournament 1" style="border-radius: 8px; margin-bottom: 10px; max-width: 100%;" />
  <img src="backend/Githubactions_ima_acc/model_actions2.png" alt="Model Tournament 2" style="border-radius: 8px; margin-bottom: 10px; max-width: 100%;" />
  <img src="backend/Githubactions_ima_acc/model_Action3.png" alt="Model Tournament 3" style="border-radius: 8px; margin-bottom: 10px; max-width: 100%;" />
  <img src="backend/Githubactions_ima_acc/modelaction4.png" alt="Model Tournament 4" style="border-radius: 8px; margin-bottom: 10px; max-width: 100%;" />
  <br/>
  <b>Hopsworks Model Registry:</b><br/>
  <img src="backend/Githubactions_ima_acc/hospworks%20model_registry.png" alt="Hopsworks Model Registry" style="border-radius: 8px; margin-top: 10px; max-width: 100%;" />
</div>

---

## 🚀 Setup & Execution Guide

### 🐍 Backend Service (FastAPI)
```bash
# Activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate # On Unix/MacOS

# Install requirements
pip install -r requirements.txt

# Run server
uvicorn backend.src.api.main:app --reload --port 8000
```
*Swagger docs run at: http://localhost:8000/docs*

### ⚛️ Frontend UI (Next.js)
```bash
cd frontend
pnpm install
pnpm dev
```
*Interactive dashboard runs at: http://localhost:3000*
*Hosted Interactive dashboard runs at: https://air-lyst.vercel.app*

---

## 👨‍💻 Built & Engineered By

<div align="center">

### **Afnan Shoukat**

<p>
  <a href="https://linkedin.com/in/afnanshoukat" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/21Afnan" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  &nbsp;&nbsp;
  <a href="mailto:afnanshoukat35@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail" />
  </a>
</p>
<p><i>Data Science Intern Project (10Pearls)</i></p>

</div>
