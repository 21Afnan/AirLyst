# <img src="docs/images/cloud_rain.png" alt="Cloud with Lightning and Rain" width="50" height="50" /> AirLyst: Advanced AQI Forecasting System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Hopsworks](https://img.shields.io/badge/Hopsworks-Feature_Store-FF7F00?style=for-the-badge)](https://www.hopsworks.ai/)

---

### 🌬️ "Predicting the air you breathe, before you step out."

**AirLyst** is a production-grade machine learning system designed to forecast hourly Air Quality Index (AQI) values up to 72 hours in advance. It features an automated end-to-end ML pipeline integrated with the **Hopsworks Feature Store** and a stunning Next.js-based web dashboard.

🌐 **[Live Hosted Frontend Web App](https://airlyst.vercel.app)** *(Update this link after deploying)*

[Explore Deep-Dive Docs](file:///c:/Users/Dell/Desktop/AirLyst/project_deep_dive_analysis.md) • [Report Bug](https://github.com/21Afnan/AirLyst/issues) • [Request Feature](https://github.com/21Afnan/AirLyst/issues)

</div>

---

## ✨ Features

- 🎯 **72-Hour Multi-step Forecasting**: Precise hourly predictions for the next 3 days using LightGBM, XGBoost, and Random Forest.
- 🤖 **Hybrid Model Tournament**: Automated training pipeline that compares models and registers the winner to the Model Registry.
- 📊 **Real-time SHAP Explanations**: Live Shapley value calculations to display the root causes of daily/hourly AQI trends (e.g., traffic exhaust, background emissions).
- ☁️ **Hopsworks Integration**: Centralized feature store and model registry to eliminate training-serving skew.
- 🌦️ **Open-Meteo API Integration**: Automatically fetches real-time meteorological and atmospheric air quality data.
- 🎨 **Premium UI/UX**: Stunning Next.js dashboard featuring clean data visualizations, glassmorphism design, and dark/light themes.

---

## 🖼️ Project Showcase

<div align="center">
  <table>
    <tr>
      <td width="50%">
        <img src="docs/images/dashboard.png" alt="AirLyst Dashboard" style="border-radius: 10px;" />
        <p align="center"><i>Interactive Next.js Dashboard</i></p>
      </td>
      <td width="50%">
        <img src="docs/images/features.png" alt="SHAP explanation" style="border-radius: 10px;" />
        <p align="center"><i>SHAP Feature Interpretations</i></p>
      </td>
    </tr>
  </table>
</div>

---

## 🏗️ Project Structure

```bash
AirLyst/
├── backend/                    # Python FastAPI Backend
│   ├── data/                   # Temporary data dumps
│   ├── logs/                   # Rotating execution log files
│   ├── models/                 # Local fallback model binaries (.joblib)
│   ├── reports/                # Static SHAP summary & importance reports
│   └── src/                    # Backend source code
│       ├── api/                # FastAPI routes (e.g., /api/forecast, /api/health)
│       ├── data_ingestion/     # External API clients (Open-Meteo)
│       ├── feature_pipeline/   # Lag features, rolling windows, Hopsworks clients
│       ├── ml/                 # Model registry, preprocessing, training, inference & SHAP
│       └── utils/              # Config validation (settings), schemas & logger
├── frontend/                   # Next.js 14 Web Application
│   ├── app/                    # Layout, styling, and main page routing
│   ├── components/             # Reusable UI widgets (AQICard, WeatherWidget, TrendChart)
│   ├── hooks/                  # Custom responsive and notification hooks
│   └── lib/                    # API client with fallback mock data & typings
├── .env                        # Local configurations and API keys
├── requirements.txt            # Python backend dependencies
└── README.md                   # Project landing page
```

---

## 🚀 Getting Started

### 🛠️ Backend Setup (FastAPI)

1. **Navigate to backend and create virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory (see [.env](file:///c:/Users/Dell/Desktop/AirLyst/.env)):
   ```env
   APP_NAME="AirLyst AQI Predictor"
   ENV="development"
   HOPSWORKS_API_KEY=your_hopsworks_api_key_here
   HOPSWORKS_PROJECT=Airlyst
   HOPSWORKS_HOST=eu-west.cloud.hopsworks.ai
   LATITUDE=33.72
   LONGITUDE=73.04
   CITY=Islamabad
   WEATHER_URL=https://archive-api.open-meteo.com/v1/archive
   AIR_URL=https://air-quality-api.open-meteo.com/v1/air-quality
   FORECAST_URL=https://api.open-meteo.com/v1/forecast
   ```

4. **Run Backend Application**
   ```bash
   # From the workspace root:
   uvicorn backend.src.api.main:app --reload --port 8000
   ```
   *Access the swagger documentation at http://localhost:8000/docs*

---

### 🎨 Frontend Setup (Next.js)

1. **Navigate to the frontend folder**
   ```bash
   cd frontend
   ```

2. **Install node dependencies**
   ```bash
   pnpm install
   # or npm install / yarn install
   ```

3. **Run the local development server**
   ```bash
   pnpm dev
   ```
   *Open http://localhost:3000 to interact with the web app dashboard.*

---

## 🚀 Deployment & Hosting

### Frontend (Next.js)
You can easily deploy the frontend to **Vercel**, **Netlify**, or **Cloudflare Pages**:
1. Push the code to GitHub.
2. Link your repository to Vercel.
3. Configure the build command as `pnpm build` and output directory as `.next`.
4. Add the backend environment variable (if needed for production server-side fetches) or update `frontend/lib/api/client.ts` to point to your hosted backend API.

### Backend (FastAPI)
Deploy the FastAPI backend to **Render**, **Heroku**, or **AWS**:
- Ensure all environment variables from `.env` are defined in your deployment configuration.
- Set the start command to: `uvicorn backend.src.api.main:app --host 0.0.0.0 --port $PORT`

---

## 🌟 Acknowledgments & Credits

- **[Hopsworks](https://www.hopsworks.ai/)** for their robust Feature Store and Model Registry.
- **[Open-Meteo](https://open-meteo.com/)** for providing open meteorological and air quality APIs.
- **[FastAPI](https://fastapi.tiangolo.com/)** and **[Next.js](https://nextjs.org/)** for building a high-performance modern web stack.

---
<p align="center"><b>Created with ❤️ by the AirLyst Team</b></p>
