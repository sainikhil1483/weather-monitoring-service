# Weather Monitoring Service

## Overview

This project is a Weather Monitoring Service built using FastAPI, Celery, Redis, and SQLite.

The application allows users to register cities to monitor. A Celery Beat scheduler runs every minute and triggers a Celery worker to fetch the latest weather data from the Open-Meteo API. The fetched weather information is stored in the database and can be retrieved using REST APIs.

---

## Technologies Used

- Python 3.x
- FastAPI
- SQLAlchemy
- SQLite
- Celery
- Redis
- Requests
- Pydantic
- Python Dotenv

---

## Project Structure

```
weather_monitor/
│
├── app.py
├── models.py
├── tasks.py
├── celery_worker.py
├── config.py
├── .env
├── requirements.txt
├── README.md
├── weather.db
```

---

## Installation

Clone the project or extract the ZIP file.

Create a virtual environment.

Windows

```bash
python -m venv venv
```

Activate the virtual environment.

Command Prompt

```bash
venv\Scripts\activate
```

PowerShell

```powershell
venv\Scripts\Activate.ps1
```

Install all dependencies.

```bash
pip install -r requirements.txt
```

---

## Configuration

Edit the `.env` file if required.

Example:

```
SECRET_KEY=mysecretkey
DATABASE_URL=sqlite:///weather.db
REDIS_URL=redis://localhost:6379/0
WEATHER_API_URL=https://api.open-meteo.com/v1/forecast
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## Database

The application uses SQLite.

The following tables are automatically created.

### monitored_cities

| Column | Type |
|--------|------|
| id | Integer |
| city | String |
| latitude | Float |
| longitude | Float |
| created_at | DateTime |

### weather_history

| Column | Type |
|--------|------|
| id | Integer |
| city | String |
| temperature | Float |
| wind_speed | Float |
| weather_code | Integer |
| fetched_at | DateTime |

---

## Running the FastAPI Application

Run the application.

```bash
uvicorn app:app --reload
```

Server URL

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

## Running Redis

Start the Redis server.

```bash
redis-server
```

Verify Redis is running.

```bash
redis-cli ping
```

Expected Output

```
PONG
```

---

## Running the Celery Worker

Open a new terminal.

```bash
celery -A tasks.celery_app worker --loglevel=info
```

---

## Running Celery Beat Scheduler

Open another terminal.

```bash
celery -A celery_worker.celery_app beat --loglevel=info
```

The scheduler executes every one minute and fetches weather information for all monitored cities.

---

## API Endpoints

### Add City

```
POST /cities
```

Request Body

```json
{
    "city":"Hyderabad",
    "latitude":17.385,
    "longitude":78.4867
}
```

---

### List Cities

```
GET /cities
```

---

### Weather History

```
GET /cities/{city}/history
```

Example

```
GET /cities/Hyderabad/history
```

---

## Weather API

Weather data is fetched using the Open-Meteo API.

```
https://api.open-meteo.com/v1/forecast
```

No API key is required.

---

## Testing

1. Start Redis.
2. Start the FastAPI server.
3. Start the Celery worker.
4. Start Celery Beat.
5. Add a city using POST `/cities`.
6. Wait one minute.
7. Call GET `/cities/{city}/history`.
8. Verify weather data has been stored.

---

## Author

Sai Nikhil