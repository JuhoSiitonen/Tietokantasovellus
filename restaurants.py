from db import db
from flask import session
import users

def restaurant_list():
    sql = "SELECT name, id FROM restaurants"
    result = db.session.execute(sql)
    listing = result.fetchall()
    return listing

def dishes_list(restaurant_id):
    sql = "SELECT dish_name, price, id, restaurant_id FROM dishes WHERE restaurant_id =:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    listing = result.fetchall()
    return listing

def confirm_order(orders, restaurant_id):
    user = users.user_id()
    order_list = []
    for item in orders:
        order_list = order_list + "," + item
    sql = "INSERT INTO orders (restaurant_id, dishes, price) values (:restaurant_id, :dishes, :price)"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id, "dishes":dishes, "price":price})

def restaurant_name(restaurant_id):
    sql = "SELECT name FROM restaurants WHERE id=:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    return result.fetchone()

def dish_name(dish_id):
    sql = "SELECT dish_name, price FROM dishes WHERE id=:dish_id"
    result = db.session.execute(sql, {"dish_id":dish_id})
    return result.fetchone()

def create_receipt(dishes, restaurant_id):
    sql = "INSERT INTO receipts (restaurant_id, dishes, price, additional_info) values (:restaurant_id, :dishes, :price, :additional_info)"


    
