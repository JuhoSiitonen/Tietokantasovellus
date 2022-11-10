from app import app
from flask import render_template, request, redirect
import users
import restaurants

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/front", methods=["GET","POST"])
def front():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return render_template("front.html")
        else:
            return render_template("error.html", txt="Käyttäjätunnusta ei löydy", link="/")
    else:
        return render_template("front.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="GET":
        return render_template("register.html")
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", txt="Salasanat eivät täsmää", link="/register")
        if users.register(username,password):
            return render_template("front.html")
        else:
            return render_template("error.html", txt="Rekisteröinti ei onnistunut", link="/register")

@app.route("/restaurants", methods=["GET","POST"])
def restaurant():
    if request.method =="GET":
        list = restaurants.restaurant_list()
        return render_template("restaurants.html", listing=list)

@app.route("/restaurants/<restaurant_id>")
def dishes(restaurant_id):
    list = restaurants.dishes_list(restaurant_id)
    restaurant = restaurants.restaurant_name(restaurant_id)
    return render_template("dishes.html", listing=list, restaurant=restaurant)

@app.route("/confirmation", methods=["POST"])
def confirmation():
    dish = request.form["dish"]
    orders = restaurants.dish_name(dish)
    extra_info = request.form["message"]
    return render_template("confirmation.html", orders=orders, extra_info=extra_info)

@app.route("/receipt", methods=["POST"])
def receipt():
    restaurants.create_receipt()
    return render_template("receipt.html")

@app.route("/receipts/<user_id>")
def receipt_archive(user_id):
    receipts = users.user_receipts(user_id)
    if not receipts:
        return render_template("error.html", txt="Et ole tehnyt tilauksia", link="/front")
    return render_template("user_receipt.html", receipts=receipts)

@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
         return render_template("review.html")
    if request.method == "POST":
        review = request.form["text_review"]
        user_id = users.user_id()
        return render_template("review.html")

@app.route("/best_reviews", methods=["GET"])
def best_reviews():
    if request.method == "GET":
        list = restaurants.best_reviews()
        return render_template("best_reviews.html", reviews=list)

@app.route("/best_reviews/<restaurant_id>", methods=["POST"])
def restaurant_reviews(restaurant_id):
    reviews = restaurants.restaurant_reviews(restaurant_id)
    return render_template("restaurant_reviews.html", reviews=reviews)

@app.route("/reviews/<user_id>")
def user_reviews(user_id):
    reviews = users.user_reviews(user_id)
    if not reviews:
        return render_template("error.html", txt="Et ole tehnyt vielä yhtään arvostelua", link="/front")
    return render_template("user_reviews.html", reviews=reviews)

@app.route("/modify_review/<review_id>")
def modify_review(review_id):
    pass

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


