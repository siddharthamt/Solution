# Assignment

## Tech Stacks
- Python
- Django REST Framework
- Sqlite
- Pandas

## Getting Started
- Basic Requirements: pip, git, and python>=3.9 working on your machine
- Create and activate a virtual environment
  - `python3 -m venv <venv_name>`
  - `source <venv_name>/bin/activate`
- Install required Python packages
  - `pip3 install -r requirements.txt`
- Set Django settings
  - `cd src`
  - `export DJANGO_SETTINGS_MODULE="assignment.settings"`
- Create database tables locally
  - `python3 manage.py migrate`


## Running Automated Test
- Execute the following command to run all tests across all apps within the project:
  - `pytest .`



## Ingestion
- Execute the following command to ingest weather data
  - `python manage.py ingest_data --weather`
- Execute the following command to ingest yield data
  - `python manage.py ingest_data --yield`
- This logs the output indicating start and end times and number of records ingested.

## Data Analysis
- Execute the following command to analyze the weather data
  - `python manage.py analyze_weather_data`

## Using the Django Admin Pages
- Create a superuser
  - `python3 manage.py createsuperuser`
  - Enter username, email, and password
- Start your local server
  - `python3 manage.py runserver`
- Paste the following url in your browser
  - `http://127.0.0.1:8000/admin/`
- Login with the superuser creds you just created
- Here you will have full CRUD abilities for all models



## Testing REST APIs in Postman
- Django REST Framework was used to develop the following 3 REST API GET endpoints:
  - /api/weather 
  - /api/yield
  - /api/weather/stats
- To use the API start your local server
  - Get Weather Data (With Pagination) - `http://127.0.0.1:8000/api/weather?format=json&limit=100&offset=100`
  - Get Weather Data (With Pagination, station_id and date filter) `http://127.0.0.1:8000/api/weather?format=json&limit=100&offset=100&station_id=USC00257715&date=1985-07-10`
  - Get Weather Statistics Data (With Pagination) - `http://127.0.0.1:8000/api/weather/stats?format=json&limit=100&offset=100`
  - Get Weather Statistics Data (With Pagination, station_id and date filter) `http://127.0.0.1:8000/api/weather/stats?format=json&limit=100&offset=100&station_id=USC00257715&date=1985-07-10`
  - Get Corn Yield Data - `http://127.0.0.1:8000/api/yield?format=json`
- These are all list APIs that have a default pagination size of 100


## Testing REST APIs in Django REST Framework
- Django REST Framework was used to develop the following 3 REST API GET endpoints:
  - /api/weather 
  - /api/yield
  - /api/weather/stats
- To use the API start your local server and paste the following urls in your browser
  - `http://127.0.0.1:8000/api/weather`
  - `http://127.0.0.1:8000/api/weather/stats`
  - `http://127.0.0.1:8000/api/yield`
- These are all list APIs that have a default pagination size of 100 and can be filtered using the Filters form on the page.
