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
    sql = "INSERT INTO receipts (restaurant_id, dishes, price, additional_info) VALUES (:restaurant_id, :dishes, :price, :additional_info)"
    db.session.execute(sql, {"restaurant_id":restaurant_id, "dishes":dishes, "price":price, "additional_info":additional_info})

def create_review(user_id, restaurant_id, review):
    sql = "INSERT INTO reviews (user_id, restaurant_id, review) VALUES (:user_id, :restaurant_id, :review)"
    db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id, "review":review})

def best_reviews():
    sql ="""
        SELECT reviews.id, restaurants.id as r_id, restaurants.name, reviews.review 
        FROM reviews, restaurants
        WHERE reviews.restaurant_id = restaurants.id
        """
    result = db.session.execute(sql)
    reviews = result.fetchall()
    return reviews


    
