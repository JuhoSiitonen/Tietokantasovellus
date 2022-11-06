from app import app
from flask import render_template, request, redirect
import users
import restaurants

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/front", methods=["GET","POST"])
def front():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return render_template("front.html")
        else:
            render_template("error.html", txt="Käyttäjätunnusta ei löydy", link="/")
    else:
        return render_template("front.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="GET":
        return render_template("register.html")
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", txt="Salasanat eivät täsmää", link="/register")
        if users.register(username,password):
            return redirect("/front")

@app.route("/restaurants", methods=["GET","POST"])
def restaurant():
    if request.method =="GET":
        list = restaurants.restaurant_list()
        return render_template("restaurants.html", listing=list)

