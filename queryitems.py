import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('items.db')
c = conn.cursor()

# Query the database
c.execute("SELECT * FROM items")

# Fetch all results from the executed query
results = c.fetchall()

# Print results
for item in results:
    print(item)

# Close the connection
conn.close()
