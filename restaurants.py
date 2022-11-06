from db import db
from flask import session

def restaurant_list():
    sql = "SELECT name FROM restaurants"
    result = db.session.execute(sql)
    listing = result.fetchall()
    return listing