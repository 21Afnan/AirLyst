<div align="center">

# 🌌 <span style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 3rem;">AeroVibe: Precision AQI Engine</span>

### 🌬️ "Predicting the air you breathe, powered by state-of-the-art MLOps."

<p align="center">
  <a href="https://airlyst.vercel.app" target="_blank">
    <img src="https://img.shields.io/badge/Live_Dashboard-AeroVibe_Web-00f2fe?style=for-the-badge&logo=vercel&logoColor=white&labelColor=0d1b2a" alt="Live Demo" />
  </a>
</p>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Hopsworks](https://img.shields.io/badge/Hopsworks-Feature_Store-FF7F00?style=for-the-badge)](https://www.hopsworks.ai/)

</div>

---

## ⚡ Interactive System Architecture

**AeroVibe** (formerly AirLyst) uses a decoupled, dual-stage pipeline that integrates weather & air quality ingestion, sliding temporal window engineering, model tournament selection, cloud-hosted registries, and live SHAP-based local explainability.

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

## 📷 Interactive Dashboard Showcase

Here is a visual walk-through of the premium **AeroVibe Next.js Frontend Dashboard** showing real-time observations, 72-hour forecast charts, and local AI explanation widgets:

<div align="center">
  <table>
    <tr>
      <td width="33.3%" align="center">
        <img src="backend/dashbaord-images/AeroVibe%20Main%20Dashboard.png" alt="AeroVibe Main Dashboard" style="border-radius: 12px; border: 2px solid #3B82F6;" />
        <br />
        <b>1. Main Dashboard View</b>
        <p><i>Real-time AQI dials, weather metrics, and daily predictions.</i></p>
      </td>
      <td width="33.3%" align="center">
        <img src="backend/dashbaord-images/AI%20Explanations%20&amp;%20SHAP%20Insights.png" alt="AI Explanations & SHAP Insights" style="border-radius: 12px; border: 2px solid #D946EF;" />
        <br />
        <b>2. AI SHAP Insights</b>
        <p><i>Local Shapley explanations translating variables to human language.</i></p>
      </td>
      <td width="33.3%" align="center">
        <img src="backend/dashbaord-images/Hourly%20Predictions%20Chart.png" alt="Hourly Predictions Chart" style="border-radius: 12px; border: 2px solid #818CF8;" />
        <br />
        <b>3. Hourly Trends Chart</b>
        <p><i>EPA-banded 24-hour predictive line chart with tooltips.</i></p>
      </td>
    </tr>
  </table>
</div>

---

## ⚙️ Core MLOps Components Explained

* **Feature Store Integration**: AeroVibe uses the **Hopsworks Feature Store** to store engineered targets, avoiding training-serving skew.
* **Temporal Lags & Rolles**: Computes sliding temporal lags (`1h`, `3h`, `6h`, `24h`) and running statistics (6h & 24h moving averages of particulate concentrations).
* **Model Tournament**: Retrains weekly. Competes Ridge, Random Forest, XGBoost, and LightGBM models using custom chronological time-series splitting to avoid future data leakage.
* **Dynamic LLM Translations**: Integrates **OpenRouter API** with the **`google/gemini-2.5-flash`** model to translate technical air quality drivers into friendly, 1-sentence explanations dynamically.
* **Live SHAP Explanations**: The `/explain` endpoint dynamically aggregates and calculates the absolute SHAP values across all real-time hourly forecasts in memory, ensuring that the model's feature importance rankings instantly adapt to live weather and pollution patterns.

---

## 🚀 Setup & Execution Guide

### 🐍 Backend Service (FastAPI)
```bash
# Activate virtual environment
python -m venv venv
venv\Scripts\activate

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

</div>
