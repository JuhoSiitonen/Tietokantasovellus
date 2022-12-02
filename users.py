import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql ="SELECT id, password, admin FROM users WHERE username = :username AND visible = TRUE"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["csrf_token"] = secrets.token_hex(16)
        if user.admin:
            session["user_role"] = "1"
        return True
    return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = """
            INSERT INTO users (username, password, admin, visible, created_at) 
            VALUES (:username, :password, FALSE, TRUE, NOW())
            """
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def is_admin():
    if session.get("user_role",0):
        return True
    return False

def csrf_token():
    return session.get("csrf_token",0)

def logout():
    del session["user_id"]
    del session["csrf_token"]
    if session.get("user_role",0):
        del session["user_role"]

def user_receipts(user_id):
    sql = """
        SELECT r.id, restaurants.name, r.price, r.additional_info, r.created_at 
        FROM receipts as r, restaurants 
        WHERE user_id = :user_id AND r.restaurant_id = restaurants.id 
        ORDER BY r.created_at
        """
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def inspect_receipt(receipt_id):
    sql = """
        SELECT r.id, r.restaurant_id, restaurants.name, r.price, r.additional_info, r.created_at, r.user_id
        FROM receipts as r, restaurants
        WHERE r.id = :receipt_id AND r.restaurant_id = restaurants.id 
        """
    result = db.session.execute(sql, {"receipt_id":receipt_id})
    return result.fetchone()

def receipt_dishes(receipt_id):
    sql = """
        SELECT r.receipt_id, d.dish_name, d.price FROM receiptdishes as r, dishes as d 
        WHERE r.dish_id = d.id AND r.receipt_id = :receipt_id ORDER BY d.price DESC
        """
    result = db.session.execute(sql, {"receipt_id":receipt_id})
    return result.fetchall()

def user_reviews(user_id):
    sql = """
        SELECT reviews.id, restaurants.name, reviews.review, reviews.stars
        FROM reviews, restaurants 
        WHERE reviews.user_id = :user_id AND reviews.restaurant_id = restaurants.id
        AND reviews.visible = TRUE
        ORDER BY reviews.created_at
        """
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def check_review_id(review_id):
    sql = "SELECT user_id FROM reviews WHERE id = :review_id"
    result = db.session.execute(sql, {"review_id":review_id})
    return result.fetchone()[0]

def modify_review(review_id, review, stars):
    userid = user_id()
    sql = """
        UPDATE reviews SET review = :review, stars = :stars 
        WHERE id = :review_id AND user_id = :userid
        """
    db.session.execute(sql, {"review":review, "stars":stars, "review_id":review_id, "userid":userid})
    db.session.commit()

def reviewable_restaurants(user_id):
    sql = """
        SELECT DISTINCT restaurants.name, restaurants.id FROM restaurants, receipts 
        WHERE receipts.user_id = :user_id and receipts.restaurant_id = restaurants.id 
        """
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()
