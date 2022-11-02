from flask import Flask, request, render_templates

app = Flask(__name__)

@app.route("/")
def index():
    return ""
