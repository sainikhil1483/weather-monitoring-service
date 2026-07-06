from tasks import celery_app, fetch_weather_for_all_cities
from celery.schedules import crontab
import time

# Configure Celery Beat schedule
celery_app.conf.beat_schedule = {
    'fetch-weather-every-minute': {
        'task': 'fetch_weather_for_all_cities',
        'schedule': crontab(minute='*'),  # Every minute
    },
}

celery_app.conf.timezone = 'UTC'

if __name__ == '__main__':
    celery_app.start()