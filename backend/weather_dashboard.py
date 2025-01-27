from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# OpenWeather API Key
API_KEY = "e9c764a4f9117dedce3fb966509b8f25"

# Database connection configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Abhijeet@123',  # Replace with your MySQL password
    'database': 'weather'  # Replace with your database name
}

# Endpoint to fetch current weather data
@app.route('/weather', methods=['POST'])
def get_weather():
    """Fetch current weather data for a given city."""
    data = request.get_json()
    city = data.get('city')

    if not city:
        return jsonify({"error": "City name is required"}), 400

    try:
        # Fetch weather data directly using city name
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Return the weather data
        return jsonify({
            "city": city,
            "weather": weather_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

# New endpoint to fetch historical weather data
@app.route('/weatherhistory', methods=['POST'])
def get_weather_history():
    """Fetch historical weather data for a given city and date."""
    data = request.get_json()
    city = data.get('city')
    date = data.get('date')  # Date format: 'YYYY-MM-DD'

    if not city or not date:
        return jsonify({"error": "City name and date are required"}), 400

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query to fetch weather data from the database
        query = """
        SELECT name, datetime, tempmax, tempmin, temp, humidity 
        FROM weather_data 
        WHERE name = %s AND datetime = %s;
        """
        cursor.execute(query, (city, date))
        result = cursor.fetchall()

        if result:
            return jsonify({
                "city": city,
                "date": date,
                "weather_data": result
            })
        else:
            return jsonify({"error": "No data found for the specified city and date"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# New endpoint to fetch historical weather data for a date range
@app.route('/weatherhistoryrange', methods=['POST'])
def get_weather_history_range():
    """Fetch historical weather data for a given city and date range."""
    data = request.get_json()
    city = data.get('city')
    start_date = data.get('startDate')  # Start date format: 'YYYY-MM-DD'
    end_date = data.get('endDate')  # End date format: 'YYYY-MM-DD'

    if not city or not start_date or not end_date:
        return jsonify({"error": "City name, start date, and end date are required"}), 400

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query to fetch weather data from the database within the date range
        query = """
        SELECT name, datetime, tempmax, tempmin, temp, humidity 
        FROM weather_data 
        WHERE name = %s AND datetime BETWEEN %s AND %s
        ORDER BY datetime;
        """
        cursor.execute(query, (city, start_date, end_date))
        result = cursor.fetchall()

        if result:
            return jsonify({
                "city": city,
                "start_date": start_date,
                "end_date": end_date,
                "weather_data": result
            })
        else:
            return jsonify({"error": "No data found for the specified city and date range"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)
