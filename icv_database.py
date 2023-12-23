# database.py
import sqlite3

def create_table(table_name):
    # Create a SQLite database connection
    conn = sqlite3.connect('./data/parsed_links.db')
    cursor = conn.cursor()

    # Create the specified table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            inner_text TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    pass

def insert_links(table_name, links):
    # Insert links into the specified table in a single batch
    conn = sqlite3.connect('./data/parsed_links.db')
    cursor = conn.cursor()

    try:
        cursor.executemany(f'INSERT OR IGNORE INTO {table_name} (url, inner_text) VALUES (?, ?)', links)
    except Exception as e:
        print(f"Error inserting links into the {table_name} table: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    pass