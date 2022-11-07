from db import db
from flask import session

def restaurant_list():
    sql = "SELECT name, id FROM restaurants"
    result = db.session.execute(sql)
    listing = result.fetchall()
    return listing

def dishes_list(restaurant_id):
    sql = "SELECT dish_name, price, id FROM dishes WHERE restaurant_id =:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    listing = result.fetchall()
    return listing