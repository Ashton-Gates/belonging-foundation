import os
import sys
import pyodbc

def test_database_connection():
    connection_string = os.environ.get('DATABASE_CONNECTION_STRING')
    if not connection_string:
        print("DATABASE_CONNECTION_STRING environment variable is not set.")
        sys.exit(1)
    
    try:
        with pyodbc.connect(connection_string, timeout=10) as conn:
            print("Successfully connected to the database.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_database_connection()
