import csv
import mysql.connector
from datetime import datetime

# Database connection configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Abhijeet@123',
    'database': 'weather'
}

# Path to the CSV file
csv_file_path = "delhi.csv"

def insert_csv_data():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert query
        insert_query = """
        INSERT INTO weather_data (name, datetime, tempmax, tempmin, temp, humidity)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Open and read the CSV file
        with open(csv_file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows_to_insert = []
            
            for row in csv_reader:
                datetime_value = row['datetime']
                
                # Detect and handle date format
                try:
                    # If the format is DD-MM-YYYY, convert to YYYY-MM-DD
                    datetime_value = datetime.strptime(datetime_value, '%d-%m-%Y').strftime('%Y-%m-%d')
                except ValueError:
                    # If already in YYYY-MM-DD format, keep as is
                    datetime_value = datetime.strptime(datetime_value, '%Y-%m-%d').strftime('%Y-%m-%d')

                # Prepare row data
                rows_to_insert.append((
                    row['name'],
                    datetime_value,
                    float(row['tempmax']) if row['tempmax'] else None,
                    float(row['tempmin']) if row['tempmin'] else None,
                    float(row['temp']) if row['temp'] else None,
                    float(row['humidity']) if row['humidity'] else None
                ))
            
            # Insert all rows in bulk
            cursor.executemany(insert_query, rows_to_insert)
            connection.commit()

        print(f"Data from {csv_file_path} inserted successfully into the database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_csv_data()
