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
    sql = "INSERT INTO receipts (restaurant_id, user_id, dishes, price, additional_info) values (:restaurant_id, :user_id, :dishes, :price)"
    db.session.execute(sql, {"restaurant_id":restaurant_id, "user_id":user_id, "dishes":dishes, "price":price})
    db.session.commit()

def restaurant_name(restaurant_id):
    sql = "SELECT name FROM restaurants WHERE id=:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    return result.fetchone()

def dish_name(dish_id):
    sql = "SELECT id, dish_name, price FROM dishes WHERE id=:dish_id"
    result = db.session.execute(sql, {"dish_id":dish_id})
    return result.fetchone()

def create_receipt(dishes, restaurant_id):
    user_id = users.user_id()
    sql = "INSERT INTO receipts (restaurant_id, user_id, dishes, price, additional_info) VALUES (:restaurant_id, :user_id, :dishes, :price, :additional_info)"
    db.session.execute(sql, {"restaurant_id":restaurant_id, "user_id":user_id, "dishes":dishes, "price":price, "additional_info":additional_info})
    db.session.commit()

def create_review(user_id, restaurant_id, review):
    sql = "INSERT INTO reviews (user_id, restaurant_id, review, visibility) VALUES (:user_id, :restaurant_id, :review, TRUE)"
    db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id, "review":review})
    db.session.commit()

def best_reviews():
    sql ="""
        SELECT DISTINCT restaurants.name, restaurants.id
        FROM reviews, restaurants
        WHERE reviews.restaurant_id = restaurants.id
        """
    result = db.session.execute(sql)
    reviews = result.fetchall()
    return reviews

def restaurant_reviews(restaurant_id):
    sql ="""
        SELECT restaurants.name, reviews.review 
        FROM reviews, restaurants
        WHERE reviews.restaurant_id = :restaurant_id 
        AND restaurants.id = :restaurant_id
        """
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    reviews = result.fetchall()
    return reviews


    
