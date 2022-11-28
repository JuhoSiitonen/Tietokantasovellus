from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql ="SELECT id, password, admin FROM users WHERE username = :username AND visible = TRUE"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            if user.admin:
                session["user_role"] = "1"
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

def is_admin():
    if session.get("user_role",0):
        return True
    return False

def logout():
    del session["user_id"]
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
    receipts = result.fetchall()
    return receipts

def inspect_receipt(receipt_id):
    sql = """
        SELECT r.id, r.restaurant_id, restaurants.name, r.price, r.additional_info, r.created_at
        FROM receipts as r, restaurants
        WHERE r.id = :receipt_id AND r.restaurant_id = restaurants.id 
        """
    result = db.session.execute(sql, {"receipt_id":receipt_id})
    receipt = result.fetchone()
    return receipt

def receipt_dishes(receipt_id):
    sql = """
        SELECT r.receipt_id, d.dish_name, d.price FROM receiptdishes as r, dishes as d 
        WHERE r.dish_id = d.id AND r.receipt_id = :receipt_id ORDER BY d.price DESC
        """
    result = db.session.execute(sql, {"receipt_id":receipt_id})
    dishes = result.fetchall()
    return dishes

def user_reviews(user_id):
    sql = """
        SELECT reviews.id, restaurants.name, reviews.review
        FROM reviews, restaurants 
        WHERE reviews.user_id = :user_id AND reviews.restaurant_id = restaurants.id
        AND reviews.visible = TRUE
        ORDER BY reviews.created_at
        """
    result = db.session.execute(sql, {"user_id":user_id})
    reviews = result.fetchall()
    return reviews

# Arvioiden muokkaus on vielä kesken, ja logiikkaa ei ole vielä päätetty sen suhteen
# tulisiko aiempi arvio muokata update metodille vai muutta visible ehtoa ja luoda uusi

def modify_review(review_id, review):
    sql = "UPDATE reviews SET review = :review WHERE id = :review_id"
    db.session.execute(sql, {"review":review, "review_id":review_id})
    db.session.commit()
    
