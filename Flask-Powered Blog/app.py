from flask import Flask, render_template, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'blog.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        if not os.path.exists(DATABASE):
            init_db()
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT)')
    cur.execute('INSERT INTO posts (title, content) VALUES (?, ?)', ("First Post", "Hello from Flask!"))
    conn.commit()
    conn.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    cur = get_db().cursor()
    cur.execute("SELECT id, title FROM posts")
    posts = cur.fetchall()
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def post(post_id):
    cur = get_db().cursor()
    cur.execute("SELECT title, content FROM posts WHERE id = ?", (post_id,))
    post = cur.fetchone()
    return render_template("post.html", title=post[0], content=post[1])

if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
