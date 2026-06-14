from flask import Flask, render_template, request, session, redirect
from tinydb import TinyDB, Query

app = Flask(
    __name__,
    template_folder="templates3",
    static_folder="static3"
)
app.secret_key = "superduperskrivnost"

db = TinyDB('db3.json')
users = db.table('users')
messages = db.table('messages')

User = Query()
Message = Query()

@app.route("/", methods=["GET","POST"])
def index():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        messages.insert({
            "sender_id": session["user_id"],
            "receiver_id": int(request.form["receiver"]),
            "content": request.form["content"]
        })
        return redirect("/")
    
    inbox = messages.search(
        Message.receiver_id == session["user_id"]
    )
    all_users = users.all()

    return render_template(
        "index.html",
        inbox=inbox,
        users=all_users,
        users_table=users
    )

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(User.username == username)

        if user and user["password"] == password:
            session["user_id"] = user.doc_id
            return redirect("/")
        return "Napaka pri loginu"
    
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.search(User.username == username):
            return "Uporabnik obstaja"
        
        users.insert({"username" : username, "password": password})
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()

    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True, port=5000)