# <img src="docs/images/cloud_rain.png" alt="Cloud with Lightning and Rain" width="50" height="50" /> AirLyst: Advanced AQI Forecasting System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-LGBM-orange?style=for-the-badge)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

### 🌬️ "Predicting the air you breathe, before you step out."

**AirLyst** is a state-of-the-art Air Quality Index (AQI) forecasting pipeline. It leverages classical ML (XGBoost, LightGBM, Random Forest) and Deep Learning (LSTM, GRU) to provide accurate 72-hour forecasts.

[Explore Docs](#) • [Report Bug](#) • [Request Feature](#)

</div>

---

## ✨ Features

- 🎯 **72-Hour Multi-step Forecasting**: Precise hourly predictions for the next 3 days.
- 🤖 **Hybrid Model Architecture**: Supports XGBoost, LightGBM, Random Forest, and Attention-based LSTMs.
- 📊 **Feature Engineering Service**: Automated lag features, rolling windows, and weather integration.
- ☁️ **Hopsworks Integration**: Centralized feature store and model registry for production-grade ML.
- 🏥 **Health Insights**: Categorical AQI mapping (1-5) with actionable health recommendations.

---

## 🖼️ Project Showcase

<div align="center">
  <p align="center">
    <img src="docs/images/laptop.png" alt="Laptop" width="100" />
  </p>
  
  <table>
    <tr>
      <td width="50%">
        <img src="docs/images/dashboard.png" alt="Dashboard" style="border-radius: 10px;" />
        <p align="center"><i>Interactive Dashboard</i></p>
      </td>
      <td width="50%">
        <img src="docs/images/metrics.png" alt="Metrics" style="border-radius: 10px;" />
        <p align="center"><i>Model Performance Metrics</i></p>
      </td>
    </tr>
    <tr>
      <td width="50%">
        <img src="docs/images/features.png" alt="Features" style="border-radius: 10px;" />
        <p align="center"><i>SHAP Feature Importance</i></p>
      </td>
      <td width="50%">
        <img src="docs/images/api.png" alt="API" style="border-radius: 10px;" />
        <p align="center"><i>FastAPI Documentation</i></p>
      </td>
    </tr>
  </table>
</div>

---

## 🚀 Getting Started

### 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AirLyst.git
   cd AirLyst
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   HOPSWORKS_API_KEY=your_key_here
   WEATHER_API_KEY=your_key_here
   ```

5. **Run the Application**
   - **Start Backend:** `uvicorn backend.main:app --reload`
   - **Start Frontend:** Open `frontend-web/index.html` in your browser or run:
     ```bash
     python -m http.server 3000 --directory frontend-web
     ```

---

## 🏗️ Project Structure

```bash
AirLyst/
├── backend/            # FastAPI source code
│   ├── api/            # API endpoints
│   ├── ml/             # Model training & inference logic
│   └── services/       # Feature engineering & data services
├── notebooks/          # Experimental analysis
├── venv/               # Virtual environment (ignored)
└── .gitignore          # Git exclusion rules
```

---
---

## 🏗️ Detailed Project Architecture

<div align="center">
  <img src="docs/images/gear.png" alt="Gear" width="80" />
</div>

```mermaid
graph TD
    A["Raw Data Source"] --> B["Data Ingestion Service"]
    B --> C{"Feature Store"}
    C --> D["Feature Engineering"]
    D --> E["Model Training Pipeline"]
    E --> F(("Model Registry"))
    F --> G["FastAPI Inference Service"]
    G --> H["React Dashboard"]
    
    subgraph "Core Backend"
    B
    D
    G
    end
    
    subgraph "ML Infrastructure"
    E
    F
    end
```

### 📂 Directory Walkthrough

```bash
AirLyst/
├── 📂 frontend-web/            # Modern Web Dashboard
│   ├── 📄 index.html           # Main structure
│   ├── 📄 style.css            # Premium styling
│   └── 📄 script.js            # Frontend logic & charts
├── 📂 backend/                 # Core logic and API
│   ├── 📂 api/                 # FastAPI routes and middleware
│   │   └── 📄 main.py          # Entry point for the server
│   ├── 📂 ml/                  # Machine Learning core
│   │   ├── 📄 models.py        # Model definitions (LSTM, GRU, etc.)
│   │   └── 📄 trainer.py       # Training and evaluation logic
│   └── 📂 services/            # Business logic
│       ├── 📄 feature_eng.py   # Advanced feature engineering
│       └── 📄 data_fetcher.py  # External API integrations
├── 📂 notebooks/               # Research & EDA
│   └── 📄 experiment_v1.ipynb  # Initial prototyping
├── 📄 .env                     # Secrets (Ignored by Git)
├── 📄 .gitignore               # Exclusion rules
├── 📄 README.md                # Project documentation
```

---

## 🌟 Acknowledgments & Shoutouts

<div align="center">
  <img src="docs/images/clapping_hands.png" alt="Clapping Hands" width="60" />
  
  > "Innovation distinguishes between a leader and a follower. This project is a testament to the power of open-source and modern AI."
</div>

Special thanks to:
- **[Hopsworks](https://www.hopsworks.ai/)** for providing an incredible Feature Store infrastructure.
- **[FastAPI](https://fastapi.tiangolo.com/)** for the lightning-fast performance.
- All the open-source contributors whose libraries made this possible.

---

## 📬 Connect With Me

<div align="center">
  <p>Feel free to reach out for collaborations or just a friendly chat about AI!</p>

  <a href="https://linkedin.com/in/afnanshoukat" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  &nbsp;&nbsp;
  <a href="mailto:afnanshoukat35@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/21Afnan/21Afnan" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>

  <br><br>
  <img src="docs/images/rocket.png" alt="Rocket" width="100" />
  
  <p><b>Created with ❤️ by the AirLyst Team</b></p>
</div>
