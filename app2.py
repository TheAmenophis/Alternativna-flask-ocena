from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)
app.secret_key = "superduperskrivnost2"

UPLOAD_FOLDER = "static2/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_NAME = "db2.sqlite"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            text TEXT NOT NULL,
            image TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    if "user" in session:
        return redirect("/index")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and user["password"] == password:
            session["user"] = username
            return redirect("/index")

        return "Napaka pri loginu"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        existing_user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:
            conn.close()
            return "Uporabnik obstaja"

        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/index")
def index():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    posts = conn.execute(
        "SELECT * FROM posts ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", user=session["user"], posts=posts)


@app.route("/add_post", methods=["POST"])
def add_post():
    if "user" not in session:
        return redirect("/login")

    text = request.form["text"]
    image = request.files["image"]
    image_path = ""

    if image and image.filename != "":
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))
        image_path = "uploads/" + filename

    conn = get_db()
    conn.execute(
        "INSERT INTO posts (username, text, image) VALUES (?, ?, ?)",
        (session["user"], text, image_path)
    )
    conn.commit()
    conn.close()

    return redirect("/index")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")


@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    post = conn.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    ).fetchone()

    if post is None:
        conn.close()
        return redirect("/index")

    if post["username"] == session["user"]:
        conn.execute(
            "DELETE FROM posts WHERE id = ?",
            (post_id,)
        )
        conn.commit()

        if post["image"]:
            path = os.path.join("static2", post["image"])
            if os.path.exists(path):
                os.remove(path)

    conn.close()
    return redirect("/index")


if __name__ == "__main__":
    app.run(debug=True, port=5000)