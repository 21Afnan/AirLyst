# <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20Places/Cloud%20with%20Lightning%20and%20Rain.png" alt="Cloud" width="45" height="45" /> AirLyst: Islamabad's Smart AQI Forecasting Engine

<div align="center">
  <img src="docs/images/header.png" alt="AirLyst Header" width="100%" style="border-radius: 15px; margin: 20px 0;" />

  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![MLOps](https://img.shields.io/badge/MLOps-Hopsworks-orange?style=for-the-badge&logo=git&logoColor=white)](https://www.hopsworks.ai/)
  [![Deep Learning](https://img.shields.io/badge/Deep--Learning-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

  ### 🌬️ "Predicting the air you breathe, before you step out."
</div>

---

## 🚀 Key Highlights
- 🎯 **72-Hour Forecasting**: Precision hourly predictions for the full 3-day horizon.
- 🤖 **Hybrid ML Engine**: Supports Random Forest (99% R2) and Stacked LSTM architectures.
- 📊 **Elite Features**: 21+ features including AQI/PM2.5 Lags (1h-24h) and Rolling Windows.
- ☁️ **Cloud Connectivity**: Seamless integration with **Hopsworks Feature Store**.

---

## 🏗️ Technical Architecture
```mermaid
graph LR
    subgraph "Data Ingestion"
    A[Weather API] --> C{Data Merger}
    B[Air Quality API] --> C
    end
    
    subgraph "Feature Pipeline"
    C --> D[Feature Engineer]
    D --> E((Hopsworks Store))
    end
    
    subgraph "ML Engine"
    E --> F[Training Pipeline]
    F --> G[Model Registry]
    G --> H[Inference Service]
    end

    style E fill:#f96,stroke:#333,stroke-width:4px
```

---

## 🌿 Health Advisory Matrix
| AQI Range | Category | Health Recommendation 🏥 |
| :--- | :--- | :--- |
| **0 - 50** | 🟢 Good | Enjoy outdoor activities! |
| **51 - 100** | 🟡 Moderate | Sensitive individuals should reduce outdoor exertion. |
| **101 - 150** | 🟠 Unhealthy (Sens.) | Children and seniors should wear a mask outdoors. |
| **151 - 200** | 🔴 Unhealthy | Everyone should limit outdoor time. Use air purifiers. |
| **201 - 300** | 🟣 Very Unhealthy | Avoid all outdoor physical activity. |
| **300+** | 🟤 Hazardous | Stay indoors with windows and doors closed. |

---

## 🛠️ Quick Start
```bash
# Clone & Setup
git clone https://github.com/21Afnan/AirLyst.git
cd AirLyst
pip install -r requirements.txt

# Run Pipeline
python backend/src/feature_pipeline/feature_engineer.py
```

---

## 📬 Connect & Collaborate
<div align="center">
  <a href="https://linkedin.com/in/afnanshoukat" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
  &nbsp;&nbsp;
  <a href="mailto:afnanshoukat35@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
  &nbsp;&nbsp;
  <a href="https://github.com/21Afnan" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" /></a>

  <br><br>
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20Places/Rocket.png" alt="Rocket" width="80" />
  
  <p><b>Crafted with Precision by Afnan Shoukat ❤️</b></p>
</div>
