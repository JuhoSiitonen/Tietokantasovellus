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
        if password == user.password:
            session["user_id"] = user.id
            return True
        else:
            return False

def register(username, password):
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":password})
    db.session.commit()
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
