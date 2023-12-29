import os
import sqlite3

def is_database_initialized():
    return os.path.exists('db/initialized.flag')

def initialize_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('db/scrahp.db')
    c = conn.cursor()

    # Create tables and perform other initialization steps
    # Create a table for articles
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            url TEXT PRIMARY KEY,
            title TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Create a flag file to indicate that the initialization is complete
    with open('db/initialized.flag', 'w') as flag_file:
        flag_file.write('Initialization complete')

if not is_database_initialized():
    initialize_database()
    print("Database initialization complete.")
else:
    print("Database has already been initialized. Skipping initialization.")
