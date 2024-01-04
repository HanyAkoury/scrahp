import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('scrahp.db')
c = conn.cursor()

# Example 1: Select all columns from the articles table
c.execute('SELECT * FROM articles')
rows = c.fetchall()

print("Example 1: Select all columns from the articles table")
for row in rows:
    print(row)

# Example 2: Select specific columns from the articles table
c.execute('SELECT title, url FROM articles')
rows = c.fetchall()

print("\nExample 2: Select specific columns from the articles table")
for row in rows:
    print(row)

# Example 3: Select rows based on a condition (e.g., where title contains 'news')
c.execute("SELECT * FROM articles WHERE title LIKE '%news%'")
rows = c.fetchall()

print("\nExample 3: Select rows based on a condition")
for row in rows:
    print(row)

# Close the connection
conn.close()
