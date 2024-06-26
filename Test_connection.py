# This application is to check wether the connection is established or not with the database using the .env file.
# imports
import os
import pyodbc
from dotenv import load_dotenv
# load the .env file
load_dotenv()
# Database connection parameters from .env file
server = os.getenv('AZURE_SERVER')
database = os.getenv('AZURE_DATABASE')
username = os.getenv('AZURE_USERNAME')
password = os.getenv('AZURE_PASSWORD')
driver = '{ODBC Driver 18 for SQL Server}'
# Function to fetch items from Azure SQL Database
def fetch_items_from_db():
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ItemID, ItemName, Category FROM Items")  # Adjust SQL query as needed
        items = []
        for row in cursor:
            items.append({'id': row[0], 'name': row[1], 'category': row[2], 'price': row[3]})
        return items
# test the connection
# fetch items from the database
items = fetch_items_from_db()
# print the items
print(items)



