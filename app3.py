from flask import Flask, render_template, request
from tinydb import TinyDB, Query

app = Flask(
    __name__,
    template_folder="templates3",
    static_folder="static3"
)
app.secret_key = "superduperskrivnost"

db = TinyDB('db.json')
users = db.table('users')
messages = db.table('messages')

User = Query()
Message = Query()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(User.username == username)
        if user and user["password"] == password:
            session["user"] = username
            return redirect("/dashboard")
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)