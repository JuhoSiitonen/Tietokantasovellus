from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def add_admin(user_id):
    sql = "UPDATE users SET admin=TRUE WHERE id = :user_id"
    db.session.execute(sql, {"user_id":user_id})

def delete_reviews(review_id):
    sql = "UPDATE reviews SET visible=FALSE WHERE id = :review_id"
    db.session.execute(sql, {"review_id":review_id})

def delete_restaurant(restaurant_id):
    sql = "UPDATE restaurants SET visible=FALSE WHERE id = :restaurant_id"
    db.session.execute(sql, {"restaurant_id":restaurant_id})

def delete_dish(dish_id):
    sql = "UPDATE dishes SET visible=FALSE WHERE id = :dish_id"
    db.session.execute(sql, {"dish_id":dish_id})

def delete_user(user_id):
    sql = "UPDATE users SET visible=FALSE WHERE id = :user_id"
    db.session.execute(sql, {"user_id":user_id})
