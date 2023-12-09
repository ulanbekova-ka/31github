import sqlite3
# import pandas as pd

conn = sqlite3.connect('books.db')

# csv_file_path = 'books.csv'
# df = pd.read_csv(csv_file_path, nrows=1)  # Read only the first row to get column names and types
# df.to_sql('your_table_name', conn, index=False, if_exists='replace', dtype={col: 'TEXT' for col in df.columns})
# conn.commit()
#
# df = pd.read_csv(csv_file_path)
# df.to_sql('your_table_name', conn, index=False, if_exists='append')
# conn.commit()

cursor = conn.cursor()
table_name = 'your_table_name'
cursor.execute(f'SELECT * FROM {table_name}')
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]
print(columns)
for row in rows:
    print(row)

conn.close()
