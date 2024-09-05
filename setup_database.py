import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
DB_NAME = 'weather_db'
DB_USER = 'postgres'
DB_PASSWORD = 'crownmetheking'
DB_HOST = 'localhost'

def create_tables():
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()

        # Create cities table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                country VARCHAR(2) NOT NULL,
                UNIQUE(name, country)
            )
        """)

        # Create weather_data table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                city_id INTEGER REFERENCES cities(id),
                temperature NUMERIC(5,2),
                feels_like NUMERIC(5,2),
                humidity INTEGER,
                wind_speed NUMERIC(5,2),
                wind_direction VARCHAR(10),
                weather_description VARCHAR(100),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Commit the changes
        conn.commit()
        print("Tables created successfully")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while creating tables: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()