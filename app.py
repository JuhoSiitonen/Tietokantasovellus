from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2:///siitonju'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/front", methods=["POST"])
def front():
    username = request.form["username"]
    password = request.form["password"]
    if users.login():
        session["username"] = username
        return render_template("front.html")
    else:
        render_template("error.html", txt="Käyttäjätunnusta ei löydy", link="/")
    #return render_template("front.html", username=request.form["username"])

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="GET":
        return render_template("register.html")
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password == password2:
            sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
            db.session.execute(sql, {"username":username, "password":password})
            db.session.commit()
        else:
            return render_template("error.html", txt="Salasanat eivät täsmää", link="/register")
        return redirect("/front")

if __name__ == "__main__":
    app.run(port=8080)