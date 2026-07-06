import requests
from celery import Celery
from datetime import datetime
from models import SessionLocal, MonitoredCity, WeatherHistory
from config import Config

# Initialize Celery
celery_app = Celery(
    'tasks',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)


@celery_app.task(name='fetch_weather_for_all_cities')
def fetch_weather_for_all_cities():
    """Fetch weather for all monitored cities"""
    db = SessionLocal()
    
    try:
        # Get all cities
        cities = db.query(MonitoredCity).all()
        
        for city in cities:
            # Fetch weather from API
            params = {
                'latitude': city.latitude,
                'longitude': city.longitude,
                'current_weather': 'true'
            }
            
            response = requests.get(Config.WEATHER_API_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                current_weather = data.get('current_weather', {})
                
                # Store weather history
                weather = WeatherHistory(
                    city=city.city,
                    temperature=current_weather.get('temperature'),
                    wind_speed=current_weather.get('windspeed'),
                    weather_code=current_weather.get('weathercode'),
                    fetched_at=datetime.utcnow()
                )
                db.add(weather)
                db.commit()
                
        return {'status': 'success', 'cities_processed': len(cities)}
        
    except Exception as e:
        db.rollback()
        return {'status': 'error', 'message': str(e)}
    finally:
        db.close()