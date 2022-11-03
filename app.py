from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:madman13@localhost:5432/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/front", methods=["POST"])
def front():
    username = request.form["name"]
    password = request.form["password"]
    sql = "INSERT INTO users (name, password) VALUES (:username, :password)"
    db.session.execute(sql, {"name":username, "password":password})
    db.session.commit()
    return render_template("front.html", name=request.form["name"])

if __name__ == "__main__":
    app.run(port=8080)