import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from datetime import datetime, timedelta

# Database configuration
DB_NAME = 'weather_db'
DB_USER = 'postgres'
DB_PASSWORD = 'crownmetheking'
DB_HOST = 'localhost'

# List of cities (ensure this matches the list in data_fetcher.py)
CITIES = [
    ('New York', 'US'),
    ('London', 'GB'),
    ('Tokyo', 'JP'),
    ('Sydney', 'AU'),
    ('Paris', 'FR'),
    ('Mumbai', 'IN'),
    ('Shanghai', 'CN')
]

logging.basicConfig(filename='visualizations.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def connect_to_db():
    try:
        return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    except psycopg2.Error as e:
        logging.error(f"Unable to connect to the database: {e}")
        return None


def fetch_avg_temperatures():
    conn = connect_to_db()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, AVG(w.temperature) as avg_temp, AVG(w.feels_like) as avg_feels_like
                FROM weather_data w
                JOIN cities c ON w.city_id = c.id
                GROUP BY c.name
                ORDER BY avg_temp DESC
            """)
            results = cur.fetchall()
            logging.info(f"Successfully fetched average temperature data for {len(results)} cities")
            return results
    except psycopg2.Error as e:
        logging.error(f"Error fetching average temperatures: {e}")
        return None
    finally:
        conn.close()


def fetch_wind_data():
    conn = connect_to_db()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, 
                       AVG(w.wind_speed) as avg_wind_speed, 
                       MODE() WITHIN GROUP (ORDER BY w.wind_direction) as common_wind_direction
                FROM weather_data w
                JOIN cities c ON w.city_id = c.id
                GROUP BY c.name
                ORDER BY avg_wind_speed DESC
            """)
            results = cur.fetchall()
            logging.info(f"Successfully fetched wind data for {len(results)} cities")
            return results
    except psycopg2.Error as e:
        logging.error(f"Error fetching wind data: {e}")
        return None
    finally:
        conn.close()


def fetch_temp_difference_humidity():
    conn = connect_to_db()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            seven_days_ago = datetime.now() - timedelta(days=7)
            cur.execute("""
                SELECT c.name, 
                       w.temperature - w.feels_like as temp_difference, 
                       w.humidity,
                       w.timestamp
                FROM weather_data w
                JOIN cities c ON w.city_id = c.id
                WHERE w.timestamp > %s
                ORDER BY c.name, w.timestamp DESC
            """, (seven_days_ago,))
            results = cur.fetchall()
            logging.info(f"Successfully fetched temperature difference and humidity data: {len(results)} records")
            return results
    except psycopg2.Error as e:
        logging.error(f"Error fetching temperature difference and humidity data: {e}")
        return None
    finally:
        conn.close()


def validate_data(data, expected_length):
    if not data or len(data) != expected_length:
        logging.warning(f"Data validation failed. Expected {expected_length} items, got {len(data) if data else 0}")
        return False
    return True


def plot_avg_temperatures(data):
    if not validate_data(data, len(CITIES)):
        return
    cities, temps, feels_like = zip(*data)

    plt.figure(figsize=(12, 6))
    x = range(len(cities))
    width = 0.35

    plt.bar([i - width / 2 for i in x], temps, width, label='Actual Temperature')
    plt.bar([i + width / 2 for i in x], feels_like, width, label='Feels Like')

    plt.title('Average Temperature vs Feels Like Temperature by City')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks(x, cities, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('avg_temperatures_comparison.png')
    plt.close()

    logging.info("Average temperature plot created successfully")


def plot_wind_data(data):
    if not validate_data(data, len(CITIES)):
        return
    cities, wind_speeds, wind_directions = zip(*data)

    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=cities, y=wind_speeds, s=100)

    for i, txt in enumerate(wind_directions):
        plt.annotate(txt, (i, wind_speeds[i]), xytext=(0, 5),
                     textcoords='offset points', ha='center', va='bottom')

    plt.title('Average Wind Speed and Common Wind Direction by City')
    plt.xlabel('City')
    plt.ylabel('Average Wind Speed (m/s)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('wind_data.png')
    plt.close()

    logging.info("Wind data plot created successfully")


def plot_temp_difference_humidity(data):
    if not data:
        logging.warning("No temperature difference and humidity data to plot")
        return

    plt.figure(figsize=(12, 8))
    for city in set(city for city, _, _, _ in data):
        city_data = [(temp_diff, humidity) for c, temp_diff, humidity, _ in data if c == city]
        temp_diffs, humidities = zip(*city_data)
        plt.scatter(temp_diffs, humidities, label=city, alpha=0.7)

    plt.title('Temperature Difference (Actual - Feels Like) vs Humidity')
    plt.xlabel('Temperature Difference (°C)')
    plt.ylabel('Humidity (%)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('temp_difference_vs_humidity.png')
    plt.close()

    logging.info("Temperature difference vs humidity plot created successfully")


def main():
    temp_data = fetch_avg_temperatures()
    wind_data = fetch_wind_data()
    temp_diff_humidity_data = fetch_temp_difference_humidity()

    plots_created = 0
    if temp_data and validate_data(temp_data, len(CITIES)):
        plot_avg_temperatures(temp_data)
        plots_created += 1
    if wind_data and validate_data(wind_data, len(CITIES)):
        plot_wind_data(wind_data)
        plots_created += 1
    if temp_diff_humidity_data:
        plot_temp_difference_humidity(temp_diff_humidity_data)
        plots_created += 1

    logging.info(f"Created {plots_created} visualizations")


if __name__ == "__main__":
    main()