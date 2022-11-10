from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql ="SELECT id, password FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, admin, visible, created_at) VALUES (:username, :password, FALSE, TRUE, NOW())"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def logout():
    del session["user_id"]

def user_receipts(user_id):
    sql = "SELECT * FROM receipts WHERE user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    receipts = result.fetchall()
    return receipts

def user_reviews(user_id):
    sql = """
        SELECT reviews.id, restaurants.name, reviews.review
        FROM reviews, restaurants 
        WHERE reviews.user_id = :user_id and reviews.restaurant_id = restaurants.id
        """
    result = db.session.execute(sql, {"user_id":user_id})
    reviews = result.fetchall()
    return reviews

def modify_review(review_id):
    sql = "UPDATE reviews SET visibility=FALSE WHERE id = :review_id"
    db.session.execute(sql, {"review_id":review_id})
    db.session.commit()
    
