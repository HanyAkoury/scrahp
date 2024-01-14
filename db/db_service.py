import os
import pdb
import sqlite3


def is_database_initialized() -> bool:
    """
    Check if the database has already been initialized.

    This function chcks if a flag file that indicates that the
    database initialization has been completed exists.

    Returns:
        bool: True if the database is initialized, False otherwise.
    """
    return os.path.exists("initialized.flag")


def initialize_database() -> None:
    """
    Initialize the SQLite database.

    This function creates the necessary SQLite database and tables
    if they don't already exist. It also creates a flag file upon
    successful initialization to prevent re-initialization.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect("scrahp.db")
    c = conn.cursor()

    # Create a table for articles
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            url TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            content TEXT
        )
    """
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Create a flag file to indicate that the initialization is complete
    with open("initialized.flag", "w") as flag_file:
        flag_file.write("Initialization complete")


# Main
if not is_database_initialized():
    initialize_database()
    print("Database initialization complete.")
else:
    print("Database has already been initialized. Skipping initialization.")
