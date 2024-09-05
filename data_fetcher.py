import requests
import psycopg2
from psycopg2 import sql
import time
from datetime import datetime

# Weatherstack API configuration
API_KEY = 'abe70bd41f186b0edb7781fed437bc19'
BASE_URL = 'http://api.weatherstack.com/current'

# Database configuration
DB_NAME = 'weather_db'
DB_USER = 'postgres'
DB_PASSWORD = 'crownmetheking'
DB_HOST = 'localhost'

# List of cities to fetch weather data for
CITIES = [
    ('New York', 'US'),
    ('London', 'GB'),
    ('Tokyo', 'JP'),
    ('Sydney', 'AU'),
    ('Paris', 'FR'),
    ('Mumbai', 'IN'),
    ('Shanghai', 'CN')
]


def connect_to_db():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)


def insert_cities(conn, cities):
    with conn.cursor() as cur:
        for city, country in cities:
            cur.execute(
                "INSERT INTO cities (name, country) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (city, country)
            )
    conn.commit()


def fetch_weather_data(city, country):
    params = {
        'access_key': API_KEY,
        'query': f"{city},{country}",
        'units': 'm'
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()


def insert_weather_data(conn, city, country, data):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM cities WHERE name = %s AND country = %s", (city, country))
        city_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO weather_data 
            (city_id, temperature, feels_like, humidity, wind_speed, wind_direction, weather_description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (city_id, data['current']['temperature'], data['current']['feelslike'],
             data['current']['humidity'], data['current']['wind_speed'],
             data['current']['wind_dir'], data['current']['weather_descriptions'][0])
        )
    conn.commit()


def main():
    conn = connect_to_db()
    insert_cities(conn, CITIES)

    while True:
        for city, country in CITIES:
            data = fetch_weather_data(city, country)
            insert_weather_data(conn, city, country, data)
            print(f"Inserted weather data for {city}, {country} at {datetime.now()}")

        time.sleep(3600)  # Wait for 1 hour before the next update


if __name__ == "__main__":
    main()