from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB, Query

app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)
app.secret_key = "superduperskrivnost2"

db = TinyDB('db2.json')
users = db.table('users')

User = Query()

@app.route("/")
def home():
    if "user" in session:
        return redirect("/index")
    
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(User.username == username)
        if user and user["password"] == password:
            session["user"] = username
            return redirect("/index")
        return "Napaka pri loginu"
    
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.search(User.username == username):
            return "Uporabnik obstaja"
        
        users.insert({"username" : username, "password": password, "note" : ""})
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/index")
def index():
    if "user" not in session:
        return redirect("/login")
    
    return render_template("index.html", user=session['user'])

if __name__ == "__main__":
    app.run(debug=True, port=5000)