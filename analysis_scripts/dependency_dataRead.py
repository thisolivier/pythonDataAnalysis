import sqlite3
import pandas as pd

# -----------------
# Read from Database
# -----------------

def read_database():

    # Connect to the SQLite database (adjust the path if necessary)
    conn = sqlite3.connect('../debug_logs.db')

    # Query to fetch all data: event_name, sum, and timestamp from logs table
    query = """
    SELECT timestamp, event_name, sum
    FROM logs
    """
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df