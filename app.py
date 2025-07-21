from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    timestamp TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    reply_text TEXT NOT NULL,
                    timestamp TEXT,
                    FOREIGN KEY(post_id) REFERENCES posts(id))""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route('/post', methods=['POST'])
def post():
    text = request.form['text']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts (text, timestamp) VALUES (?, ?)", (text, timestamp))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    if request.method == 'POST':
        reply_text = request.form['reply']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute("INSERT INTO replies (post_id, reply_text, timestamp) VALUES (?, ?, ?)",
                  (post_id, reply_text, timestamp))
        conn.commit()
    c.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = c.fetchone()
    c.execute("SELECT * FROM replies WHERE post_id=? ORDER BY id ASC", (post_id,))
    replies = c.fetchall()
    conn.close()
    return render_template("post.html", post=post, replies=replies)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
