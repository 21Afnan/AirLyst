# <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20Places/Cloud%20with%20Lightning%20and%20Rain.png" alt="Cloud" width="50" height="50" /> AirLyst: Islamabad's Smart AQI Forecasting

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MLOps](https://img.shields.io/badge/MLOps-Hopsworks-orange?style=for-the-badge&logo=git&logoColor=white)](https://www.hopsworks.ai/)
[![Deep Learning](https://img.shields.io/badge/Deep--Learning-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)

### 🌬️ "Predicting the air you breathe, before you step out."

---

</div>

## 🚀 Key Features
- 🎯 **72-Hour Forecasting**: Precision hourly predictions for the 3-day horizon.
- 🤖 **Hybrid ML Engine**: Supports Random Forest and Stacked LSTM architectures.
- 📊 **Elite Features**: 21+ features including AQI/PM2.5 Lags and Rolling Windows.
- ☁️ **Cloud Feature Store**: Seamless integration with **Hopsworks**.

---

## 🏗️ Technical Architecture
```mermaid
graph LR
    A[Weather API] --> C{Data Merger}
    B[Air Quality API] --> C
    C --> D[Feature Engineer]
    D --> E((Hopsworks))
    E --> F[ML Engine]
```

---

## 🌿 Health Advisory Matrix
| AQI Range | Category | Health Recommendation 🏥 |
| :--- | :--- | :--- |
| **0 - 50** | 🟢 Good | Enjoy outdoor activities! |
| **51 - 100** | 🟡 Moderate | Sensitive individuals reduce outdoor exertion. |
| **101 - 150** | 🟠 Unhealthy | Children and seniors wear a mask. |
| **151 - 200** | 🔴 Unhealthy | Everyone limit outdoor time. |
| **300+** | 🟤 Hazardous | Stay indoors with windows closed. |

---

## 🛠️ Quick Start
```bash
git clone https://github.com/21Afnan/AirLyst.git
pip install -r requirements.txt
python backend/src/feature_pipeline/feature_engineer.py
```

---

## 📬 Connect & Collaborate
<div align="center">
  <a href="https://linkedin.com/in/afnanshoukat"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
  &nbsp;
  <a href="mailto:afnanshoukat35@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
  &nbsp;
  <a href="https://github.com/21Afnan"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" /></a>

  <br><br>
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20Places/Rocket.png" alt="Rocket" width="80" />
  
  <p><b>Crafted with Precision by Afnan Shoukat ❤️</b></p>
</div>
