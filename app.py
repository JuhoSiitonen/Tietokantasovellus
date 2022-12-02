from flask import Flask, request, render_template, redirect, session
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes

