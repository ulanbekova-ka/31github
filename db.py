import sqlite3

# conn = sqlite3.connect('example.db')
#
# # Step 2: Create a cursor object to execute SQL queries
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL,
#         email TEXT NOT NULL
#     )
# ''')
# # cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ('john_doe', 'john@example.com'))
# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
#
# conn.commit()
# conn.close()

# Connect to the SQLite database
with sqlite3.connect('db.sqlite3') as conn:
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Fetch the list of tables in the database
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # tables = cursor.fetchall()
    #
    # # Print the list of tables
    # for table in tables:
    #     print("Table:", table[0])
    #
    #     # Fetch and print the column names for each table
    #     cursor.execute(f"PRAGMA table_info({table[0]});")
    #     columns = cursor.fetchall()
    #     column_names = [col[1] for col in columns]
    #     print("Columns:", column_names)
    #
    #     # Fetch and print some sample data from each table
    #     cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5;")
    #     sample_data = cursor.fetchall()
    #     print("Sample Data:")
    #     for row in sample_data:
    #         print(row)
    #
    #     print("\n")
    cursor.execute('SELECT * FROM my_app_song')
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)
