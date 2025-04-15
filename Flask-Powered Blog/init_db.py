import sqlite3

conn = sqlite3.connect('blog.db')
cur = conn.cursor()
cur.execute('CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)')
cur.execute('INSERT INTO posts (title, content) VALUES (?, ?)', ("First Post", "Hello from Flask!"))
conn.commit()
conn.close()
print("Database initialized.")
