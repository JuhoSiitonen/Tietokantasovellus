from db import db
from flask import session

# Luonnokset Admin funktioista, ei vielä toiminnassa.
# Tulee vielä päättää poistetaanko käyttäjän arvostelut mikäli käyttäjä poistetaan

def add_admin(user_name):
    try:
        sql = "UPDATE users SET admin=TRUE WHERE username = :user_name"
        db.session.execute(sql, {"user_name":user_name})
        db.session.commit()
    except:
        return False
    return True

def add_restaurant(restaurant_name, restaurant_address):
    try:
        sql = "INSERT INTO restaurants (name, visible, address) VALUES (:restaurant_name, TRUE, :restaurant_address)"
        db.session.execute(sql, {"restaurant_name":restaurant_name, "restaurant_address":restaurant_address})
        db.session.commit()
    except:
        return False
    return True

def add_dish(restaurant_id, dish_name, price):
    try:
        sql = "INSERT INTO dishes (restaurant_id, dish_name, visible, price) VALUES (:restaurant_id, :dish_name, TRUE, :price)"
        db.session.execute(sql, {"restaurant_id":restaurant_id, "dish_name":dish_name, "price":price})
        db.session.commit()
    except:
        return False
    return True

def delete_reviews(review_id):
    sql = "UPDATE reviews SET visible=FALSE WHERE id = :review_id"
    db.session.execute(sql, {"review_id":review_id})
    db.session.commit()

def delete_restaurant(restaurant_id):
    sql = "UPDATE restaurants SET visible=FALSE WHERE id = :restaurant_id"
    db.session.execute(sql, {"restaurant_id":restaurant_id})
    db.session.commit()

def delete_dish(dish_id):
    sql = "UPDATE dishes SET visible=FALSE WHERE id = :dish_id"
    db.session.execute(sql, {"dish_id":dish_id})
    db.session.commit()

def delete_user(user_id):
    try:
        sql = "UPDATE users SET visible=FALSE WHERE id = :user_id"
        db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
    except:
        return False
    return True


def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()
    if user_id:
        return user_id[0]
    return 0 
