from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB, Query

app = Flask(
    __name__,
    template_folder="templates1",
    static_folder="static1"
)
app.secret_key = "superduperskrivnost"

db = TinyDB('db.json')
users = db.table('users')

User = Query()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)