from flask import Flask
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Abhijeet@123',  # Replace with your MySQL password
    'database': 'weather'  # Replace with your database name
}

def create_table():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Updated schema query for the new table structure
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_data (
            name VARCHAR(255) NOT NULL,
            datetime DATE NOT NULL,
            tempmax FLOAT,
            tempmin FLOAT,
            temp FLOAT,
            humidity FLOAT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully with updated schema.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/')
def home():
    create_table()
    return "Database table created successfully with updated schema!"

if __name__ == '__main__':
    app.run(debug=True)
