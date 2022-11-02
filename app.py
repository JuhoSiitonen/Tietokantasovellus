from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/zwolt'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/front", methods=["POST"])
def front():
    return render_template("front.html", name=request.form["name"])


if __name__ == "__main__":
    app.run(port=8080)