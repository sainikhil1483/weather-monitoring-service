from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from models import SessionLocal, MonitoredCity, WeatherHistory
from tasks import fetch_weather_for_all_cities
import uvicorn

app = FastAPI(title="Weather Monitoring Service")


# Pydantic models
class CityCreate(BaseModel):
    city: str
    latitude: float
    longitude: float


class CityResponse(BaseModel):
    id: int
    city: str
    latitude: float
    longitude: float
    created_at: datetime


class WeatherHistoryResponse(BaseModel):
    id: int
    city: str
    temperature: float
    wind_speed: float
    weather_code: int
    fetched_at: datetime


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities", response_model=CityResponse, status_code=201)
def add_city(city_data: CityCreate, db: Session = Depends(get_db)):
    """Add a new city to monitor"""
    # Check if city already exists
    existing = db.query(MonitoredCity).filter(MonitoredCity.city == city_data.city).first()
    if existing:
        raise HTTPException(status_code=400, detail="City already exists")
    
    # Create new city
    city = MonitoredCity(
        city=city_data.city,
        latitude=city_data.latitude,
        longitude=city_data.longitude
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    
    return city


@app.get("/cities", response_model=List[CityResponse])
def list_cities(db: Session = Depends(get_db)):
    """List all monitored cities"""
    cities = db.query(MonitoredCity).all()
    return cities


@app.get("/cities/{city}/history", response_model=List[WeatherHistoryResponse])
def get_weather_history(city: str, db: Session = Depends(get_db)):
    """Get weather history for a specific city"""
    # Check if city exists
    city_exists = db.query(MonitoredCity).filter(MonitoredCity.city == city).first()
    if not city_exists:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Get weather history
    history = db.query(WeatherHistory).filter(WeatherHistory.city == city).all()
    return history


@app.get("/")
def root():
    return {
        "service": "Weather Monitoring Service",
        "endpoints": {
            "POST /cities": "Add a city to monitor",
            "GET /cities": "List all monitored cities",
            "GET /cities/{city}/history": "Get weather history for a city"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)