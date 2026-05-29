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
notes = db.table('notes')

User = Query()
Notes = Query()

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    
    return redirect("/login")

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

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    

    userNotes = notes.search(Notes.username == session["user"])

    return render_template("dashboard.html", user=session["user"], notes=userNotes)

@app.route("/saveNote", methods=["POST"])
def saveNote():
    if request.method == "POST":
        data = request.form
        print(data)

        notes.insert({'username': session["user"], 'title': data["title"], 'content': data["content"]})

        return {"status": 200}

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()

    return {"status": 200}

if __name__ == "__main__":
    app.run(debug=True, port=5000)