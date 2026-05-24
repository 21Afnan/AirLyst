import sys
import time
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- SMART PATH LOGIC ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from src.utils.config import settings
from src.api.routes.forecast import router as forecast_router

app = FastAPI(
    title="AirLyst AQI Predictor API",
    description="FastAPI service for AirLyst AQI predictions in Islamabad.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the modular forecast router
app.include_router(forecast_router)

@app.get("/api/health")
def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "city": settings.CITY,
        "location": {"latitude": settings.LATITUDE, "longitude": settings.LONGITUDE},
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting AirLyst API Server on http://localhost:8000...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
