# <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20Places/Cloud%20with%20Lightning%20and%20Rain.png" alt="Cloud" width="45" height="45" /> AirLyst: The Future of AQI Forecasting

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MLOps](https://img.shields.io/badge/MLOps-Hopsworks-orange?style=for-the-badge&logo=git&logoColor=white)](https://www.hopsworks.ai/)
[![Deep Learning](https://img.shields.io/badge/Deep--Learning-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

### 🌬️ "Predicting the air you breathe, before you step out."

**AirLyst** is a state-of-the-art MLOps pipeline designed for Islamabad's high-precision AQI forecasting. It bridges the gap between raw environmental data and actionable health insights using a robust feature store and advanced time-series modeling.

[Explore Docs](#) • [Report Bug](#) • [Request Feature](#)

</div>

---

## 🚀 Key Features

- 🎯 **72-Hour Multi-step Forecasting**: Beyond just 'next-hour' predictions; we forecast the full 3-day horizon.
- 🤖 **Hybrid Model Support**: Engineered for both **Random Forest** (high accuracy) and **Stacked LSTM** (sequence memory).
- 📊 **Elite Feature Engineering**: Automated pipeline for 21+ features including AQI/PM2.5 Lags (1h-24h) and Rolling Averages.
- ☁️ **Hopsworks Integration**: Production-grade Feature Store for centralized data versioning and model registry.
- ⚡ **Real-time Ingestion**: Seamlessly fuses Open-Meteo weather data with Global Air Quality feeds.

---

## 🏗️ Project Architecture

```mermaid
graph LR
    subgraph "Data Ingestion"
    A[Weather API] --> C{Data Merger}
    B[Air Quality API] --> C
    end
    
    subgraph "Feature Pipeline"
    C --> D[Feature Engineer]
    D --> E((Hopsworks Feature Store))
    end
    
    subgraph "ML Engine"
    E --> F[Training Pipeline]
    F --> G[Model Registry]
    G --> H[Inference Service]
    end
    
    subgraph "Delivery"
    H --> I[React Dashboard]
    H --> J[API Endpoints]
    end

    style E fill:#f96,stroke:#333,stroke-width:4px
```

---

## 📂 Project Structure Walkthrough

```bash
AirLyst/
├── 📂 backend/                 # Core logic and API
│   ├── 📂 src/
│   │   ├── 📂 data_ingestion/  # Raw API clients (Weather/AQI)
│   │   ├── 📂 feature_pipeline/# The heart of feature engineering
│   │   ├── 📂 models/          # Model architectures (LSTM, RF)
│   │   └── 📂 utils/           # Shared loggers and configs
├── 📂 notebooks/               # Research, EDA & Experiments
├── 📄 .env                     # Secrets (Ignored by Git)
├── 📄 .gitignore               # Multi-layer exclusion rules
├── 📄 requirements.txt         # Production dependencies
└── 📄 README.md                # Project documentation
```

---

## 🖼️ Model Performance Showcase

<div align="center">
  
  | Feature | Importance | Model | R2 Score |
  | :--- | :--- | :--- | :--- |
  | **us_aqi_lag_1h** | 0.9595 | **Random Forest** | **0.99** |
  | **pm2_5_rolling_24h**| 0.0146 | **LSTM** | **0.59** |
  | **hour** | 0.0038 | **XGBoost** | *Upcoming* |

</div>

---

## 🛠️ Installation & Setup

### 1. Clone & Environment
```bash
git clone https://github.com/21Afnan/AirLyst.git
cd AirLyst
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
```

### 2. Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline
```bash
# Engineer the "Certified" feature set
python backend/src/feature_pipeline/feature_engineer.py
```

---

## 📬 Connect & Collaborate

<div align="center">
  <p>Looking for collaborations or technical discussions on MLOps!</p>

  <a href="https://linkedin.com/in/afnanshoukat" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  &nbsp;&nbsp;
  <a href="mailto:afnanshoukat35@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/21Afnan" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />
  </a>

  <br><br>
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20Places/Rocket.png" alt="Rocket" width="80" />
  
  <p><b>Crafted with Precision by Afnan Shoukat</b></p>
</div>
