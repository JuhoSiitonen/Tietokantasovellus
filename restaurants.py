from db import db
from flask import session
import users

# Sisältää kaikki ravintoloihin liittyvät funktiot
# Jatkossa kuitin ja arvostelun luomiseen liittyvät funktio varmaan siirrän users moduuliin

def restaurant_list():
    sql = "SELECT name, id, address FROM restaurants WHERE visible = TRUE"
    result = db.session.execute(sql)
    listing = result.fetchall()
    return listing

def dishes_list(restaurant_id):
    sql = "SELECT dish_name, price, id, restaurant_id FROM dishes WHERE restaurant_id =:restaurant_id AND visible = TRUE"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    listing = result.fetchall()
    return listing

def get_dish_id(restaurant_id, dish_name):
    try:
        sql = "SELECT id FROM dishes WHERE restaurant_id=:restaurant_id and dish_name=:dish_name"
        result = db.session.execute(sql, {"restaurant_id":restaurant_id, "dish_name":dish_name})
        dish_id = result.fetchone()
        return dish_id
    except:
        return 0

def get_restaurant_id(restaurant_name):
    try:
        sql = "SELECT id FROM restaurants WHERE name=:restaurant_name"
        result = db.session.execute(sql, {"restaurant_name":restaurant_name})
        restaurant_id = result.fetchone()
        return restaurant_id
    except:
        return 0

def restaurant_name(restaurant_id):
    sql = "SELECT name FROM restaurants WHERE id=:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    return result.fetchone()

def dish_name(dish_id):
    sql = "SELECT id, dish_name, price, restaurant_id FROM dishes WHERE id=:dish_id"
    result = db.session.execute(sql, {"dish_id":dish_id})
    return result.fetchone()

# Kuitin luomisessa tehdän lisäys tauluun Receipts ja Receiptdishes jotta tieto olisi 
# ACID mallin mukainen. 
# Commit tehdään vasta kun lisäykset on tehty molempiin tauluihin, mutta en ole varma onko se 
# paras tapa vai tulisiko commit tehdä jo Receipts tauluun lisäyksen jälkeen jotta 
# ei tulisi samanaikaisuus ongelmia. 

def create_receipt(order_info, restaurant_id, total_price, extra_info):
    user_id = users.user_id()
    sql = """
        INSERT INTO receipts (restaurant_id, user_id, price, additional_info, created_at) 
        VALUES (:restaurant_id, :user_id, :price, :additional_info, NOW())
        RETURNING id 
        """
    result = db.session.execute(sql, {"restaurant_id":restaurant_id, "user_id":user_id, "price":total_price, "additional_info":extra_info})
    receipt_id = (result.fetchone())[0]
    for item in order_info:
        dish_id = int(item)
        sql = "INSERT INTO receiptdishes (receipt_id, dish_id) VALUES (:receipt_id, :dish_id)"
        db.session.execute(sql, {"receipt_id":receipt_id, "dish_id":dish_id})
    db.session.commit()
    return receipt_id

def create_review(restaurant_id, review):
    user_id = users.user_id()
    sql = "INSERT INTO reviews (user_id, restaurant_id, review, visible, created_at) VALUES (:user_id, :restaurant_id, :review, TRUE, NOW())"
    db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id, "review":review})
    db.session.commit()

def best_reviews():
    sql ="""
        SELECT DISTINCT restaurants.name, restaurants.id
        FROM reviews, restaurants
        WHERE reviews.restaurant_id = restaurants.id AND restaurants.visible = TRUE
        """
    result = db.session.execute(sql)
    reviews = result.fetchall()
    return reviews

def restaurant_reviews(restaurant_id):
    sql ="""
        SELECT restaurants.name, reviews.id, reviews.review, reviews.created_at
        FROM reviews, restaurants
        WHERE reviews.restaurant_id = :restaurant_id 
        AND restaurants.id = :restaurant_id AND reviews.visible = TRUE
        """
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    reviews = result.fetchall()
    return reviews


    
