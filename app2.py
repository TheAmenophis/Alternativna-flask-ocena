from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB, Query
from werkzeug.utils import secure_filename
import os

app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)
app.secret_key = "superduperskrivnost2"

UPLOAD_FOLDER = "static2/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = TinyDB('db2.json')
users = db.table('users')
posts = db.table("posts")

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
        
        users.insert({"username" : username, "password": password})
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/index")
def index():
    if "user" not in session:
        return redirect("/login")
    
    vse_objave = posts.all()
    vse_objave.reverse()

    return render_template("index.html", user=session['user'], posts=vse_objave)

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

    posts.insert({
        "username": session["user"],
        "text": text,
        "image": image_path
    })

    return redirect("/index")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")

@app.route("/delete_post/<int:doc_id>")
def delete_post(doc_id):
    if "user" not in session:
        return redirect("/login")

    post = posts.get(doc_id=doc_id)

    if post is None:
        return redirect("/index")

    if post["username"] == session["user"]:
        posts.remove(doc_ids=[doc_id])
        if post["image"]:
            path = os.path.join("static2", post["image"])

            if os.path.exists(path):
                os.remove(path)

    return redirect("/index")

if __name__ == "__main__":
    app.run(debug=True, port=5000)