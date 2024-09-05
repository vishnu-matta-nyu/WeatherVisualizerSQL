# Weather Analysis Project

## Overview
This project fetches real-time weather data from the Weatherstack API for multiple global cities, stores it in a PostgreSQL database, and generates insightful visualizations. It demonstrates skills in API integration, database management, data analysis, and data visualization using Python.

## Features
- Fetches current weather data for 7 major cities worldwide using the Weatherstack API
- Stores weather data in a PostgreSQL database
- Generates three types of data visualizations:
  1. Average Temperature vs. Feels Like Temperature by City
  2. Average Wind Speed and Common Wind Direction by City
  3. Temperature Difference vs. Humidity Analysis
- Implements error handling and logging for robust operation

## Technologies Used
- Python 3.x
- PostgreSQL
- Weatherstack API
- Libraries: psycopg2, requests, matplotlib, seaborn

## Project Structure
- `setup_database.py`: Script to set up the PostgreSQL database schema
- `data_fetcher.py`: Script to fetch data from Weatherstack API and store in the database
- `data_visualizer.py`: Script to generate visualizations from the stored data
- `requirements.txt`: List of Python package dependencies

## Setup and Installation
1. Clone the repository
2. Install required packages: `pip install -r requirements.txt`
3. Set up a PostgreSQL database
4. Run `setup_database.py` to create necessary tables
5. Update API key and database credentials in `data_fetcher.py` and `data_visualizer.py`

## Usage
1. Run `data_fetcher.py` to start collecting weather data:
   ```
   python data_fetcher.py
   ```
2. Run `data_visualizer.py` to generate visualizations:
   ```
   python data_visualizer.py
   ```

## Visualizations
- `avg_temperatures_comparison.png`: Bar chart comparing average and "feels like" temperatures
- `wind_data.png`: Scatter plot of average wind speeds with wind direction annotations
- `temp_difference_vs_humidity.png`: Scatter plot showing the relationship between temperature difference and humidity

## Key Learning Outcomes
- API Integration: Worked with RESTful APIs to fetch real-time data
- Database Management: Designed schema and managed data storage in PostgreSQL
- Data Analysis: Processed and analyzed weather data to extract meaningful insights
- Data Visualization: Created informative charts using matplotlib and seaborn
- Error Handling: Implemented robust error checking and logging
- Python Programming: Developed modular, maintainable code structure

## Future Improvements
- Implement a web interface to display real-time visualizations
- Add more cities and expand the range of weather metrics analyzed
- Incorporate historical data analysis and weather prediction features
- Optimize database queries for larger datasets

## Author
[Your Name]

## License
This project is open source and available under the [MIT License](LICENSE).
