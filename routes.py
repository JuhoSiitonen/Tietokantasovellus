from app import app
from flask import render_template, request, redirect, session
import users
import restaurants
import admin

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
            return render_template("error.html", txt="Käyttäjätunnusta ei löydy", link="/", link_txt="Yritä uudelleen")
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
        if len(username) < 3 or len(password) < 3 or " " in username or " " in password:
            return render_template("error.html", 
            txt="Käyttäjätunnuksen ja salasanan pituus tulee olla vähintään 3 merkkiä", link="/register", link_txt="Yritä uudelleen")
        if password != password2:
            return render_template("error.html", txt="Salasanat eivät täsmää", link="/register", link_txt="Yritä uudelleen")
        if users.register(username,password):
            return render_template("front.html")
        else:
            return render_template("error.html", txt="Rekisteröinti ei onnistunut", link="/register", link_txt="Yritä uudelleen")

@app.route("/restaurants")
def restaurant():
    listing = restaurants.restaurant_list()
    return render_template("restaurants.html", listing=listing)

@app.route("/restaurants/<restaurant_id>")
def dishes(restaurant_id):
    listing = restaurants.dishes_list(restaurant_id)
    restaurant = restaurants.restaurant_name(restaurant_id)
    return render_template("dishes.html", listing=listing, restaurant=restaurant)

@app.route("/confirmation", methods=["POST"])
def confirmation():
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    dish = request.form.getlist("dish")
    orders = []
    total_price = 0
    for item in dish:
        order = restaurants.dish_name(item)
        orders.append(order)
        total_price += order[2]
    extra_info = request.form["message"]
    return render_template("confirmation.html", orders=orders, extra_info=extra_info, total_price=total_price)

@app.route("/receipt", methods=["POST"])
def receipt():
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    order_info = request.form.getlist("orders")
    restaurant_id = int(request.form["restaurant_id"])
    total_price = int(request.form["total_price"])
    extra_info = request.form["extra_info"]
    receipt = restaurants.create_receipt(order_info, restaurant_id, total_price, extra_info)
    return render_template("receipt.html", receipt=receipt)

@app.route("/receipts/<user_id>")
def receipt_archive(user_id):
    if int(user_id) != users.user_id():
        return render_template("error.html", txt="", link="/front", link_txt="Palaa etusivulle")
    receipts = users.user_receipts(user_id)
    if not receipts:
        return render_template("error.html", txt="Et ole tehnyt tilauksia", link="/front", link_txt="Takaisin etusivulle")
    return render_template("user_receipts.html", receipts=receipts)

@app.route("/receipt/<receipt_id>")
def inspect_receipt(receipt_id):
    receipt = users.inspect_receipt(receipt_id)
    if receipt.user_id != users.user_id():
        return render_template("error.html", txt="", link="/front", link_txt="Palaa etusivulle")
    receipt_dishes = users.receipt_dishes(receipt_id)
    return render_template("inspect_receipt.html", receipt_dishes=receipt_dishes, receipt=receipt)
    
@app.route("/review/<restaurant_id>", methods=["GET", "POST"])
def review(restaurant_id):
    if request.method == "GET":
         return render_template("review.html", restaurant_id=restaurant_id)
    if request.method == "POST":
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        #restaurant_id = (users.inspect_receipt(receipt_id)).restaurant_id
        stars = int(request.form["rating"])
        review = request.form["text_review"]
        restaurants.create_review(restaurant_id, review, stars)
        return render_template("error.html", txt="Palaute lähetetty", link="/front", link_txt="Takaisin etusivulle")

@app.route("/best_reviews")
def best_reviews():
    listing = restaurants.best_reviews()
    return render_template("best_reviews.html", reviews=listing)

@app.route("/best_reviews/<restaurant_id>")
def restaurant_reviews(restaurant_id):
    reviews = restaurants.restaurant_reviews(restaurant_id)
    return render_template("restaurant_reviews.html", reviews=reviews)

@app.route("/reviews/<user_id>")
def user_reviews(user_id):
    if int(user_id) != users.user_id():
        return render_template("error.html", txt="", link="/front", link_txt="Palaa etusivulle")
    reviews = users.user_reviews(user_id)
    if not reviews:
        return render_template("error.html", txt="Et ole tehnyt vielä yhtään arvostelua", link="/front", link_txt="Takaisin etusivulle")
    return render_template("user_reviews.html", reviews=reviews)

@app.route("/modify_review/<review_id>", methods=["GET", "POST"])
def modify_review(review_id):
    if request.method == "GET":
        if users.user_id() != users.check_review_id(review_id):
            return render_template("error.html", txt="", link="/front", link_txt="Palaa etusivulle")
        return render_template("modify_review.html", review_id=review_id)
    if request.method == "POST":
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        stars = int(request.form["rating"])
        review = request.form["text_review"]
        users.modify_review(review_id, review, stars)
        return render_template("error.html", txt="Palaute lähetetty", link="/front", link_txt="Takaisin etusivulle")   

@app.route("/find_restaurant")
def find_restaurant():
    return render_template("find_restaurant.html")

@app.route("/result")
def result():
    description = request.args["description"]
    results = restaurants.find_restaurants(description)
    if results:
        return render_template("result.html", results=results)
    return render_template("error.html", txt="Hakusanoillasi ei löytynyt ravintoloita", link="/front", link_txt="Takaisin etusivulle")

@app.route("/reviewable")
def review_restaurant():
    user_id = users.user_id()
    listing = users.reviewable_restaurants(user_id)
    if listing:
        return render_template("reviewable.html", listing=listing)
    return render_template("error.html", txt="Et voi arvioida ravintoloita, koska et ole vielä tilannut mistään", 
    link="/front", link_txt="Takaisin etusivulle")

@app.route("/admin_tools")
def admin_tools():
    if users.is_admin():
        return render_template("admin_tools.html")
    else:
        return render_template("error.html", txt="Jotain meni pieleen", link="/front", link_txt="Takaisin etusivulle")

@app.route("/add/<element_to_add>", methods=["GET", "POST"])
def add(element_to_add):
    if request.method == "GET":
        if element_to_add == "restaurant":
            return render_template("add.html", element="1")
        elif element_to_add == "dish":
            return render_template("add.html", element="2")
        elif element_to_add == "admin":
            return render_template("add.html", element="3")

    if request.method == "POST":

        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        
        if element_to_add == "restaurant":
            restaurant_name = request.form["restaurant_name"]
            restaurant_address = request.form["restaurant_address"]
            description = request.form["description"]
            if admin.add_restaurant(restaurant_name, restaurant_address, description):
                return render_template("error.html", txt="Ravintolan lisäys onnistui!", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
            return render_template("error.html", txt="Ravintolan lisäys ei onnistunut", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
        
        elif element_to_add == "dish":
            restaurant_name = request.form["restaurant_name"]
            dish_name = request.form["dish_name"]
            price = int(request.form["price"])
            restaurant_id = restaurants.get_restaurant_id(restaurant_name)[0]
            if admin.add_dish(restaurant_id, dish_name, price):
                return render_template("error.html", txt="Annoksen lisäys onnistui!", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
            return render_template("error.html", txt="Annoksen lisäys ei onnistunut", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
        
        elif element_to_add == "admin":
            user_name = request.form["user_name"]
            if admin.add_admin(user_name):
                return render_template("error.html", txt="Ylläpitäjän lisäys onnistui!", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
            return render_template("error.html", txt="Ylläpitäjän lisäys ei onnistunut", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")

@app.route("/delete/<element_to_delete>", methods=["GET", "POST"])
def delete(element_to_delete):
    if request.method == "GET":
        if element_to_delete == "user":
            return render_template("delete.html", element="1")
        elif element_to_delete == "restaurant":
            return render_template("delete.html", element="2")
        elif element_to_delete == "dish":
            return render_template("delete.html", element="3")
        elif element_to_delete == "review":
            return render_template("delete.html", element="4")

    if request.method == "POST":
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)

        if element_to_delete == "user":
            username = request.form["username"]
            user_id = admin.get_user_id(username)
            if user_id != 0:
                admin.delete_user(user_id)
                return render_template("error.html", txt="Käyttäjän poistaminen onnistui", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
            return render_template("error.html", txt="Käyttäjän poistaminen ei onnistunut", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
        
        elif element_to_delete == "restaurant":
            restaurant_name = request.form["restaurant_name"]
            restaurant_id = restaurants.get_restaurant_id(restaurant_name)[0]
            if restaurant_id != 0:
                admin.delete_restaurant(restaurant_id)
                return render_template("error.html", txt="Ravintolan poistaminen onnistui", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
            return render_template("error.html", txt="Ravintolan poistaminen ei onnistunut", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
        
        elif element_to_delete == "dish":
            restaurant_name = request.form["restaurant_name"]
            restaurant_id = restaurants.get_restaurant_id(restaurant_name)[0]
            dish_name = request.form["dish_name"]
            dish_id = restaurants.get_dish_id(restaurant_id, dish_name)[0]
            if restaurant_id != 0 and dish_id != 0:
                admin.delete_dish(dish_id)
                return render_template("error.html", txt="Annoksen poistaminen onnistui", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
            return render_template("error.html", txt="Annoksen poistaminen ei onnistunut", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
        
        elif element_to_delete == "review":
            review_id = request.form["review_id"]
            if admin.delete_reviews(review_id):
                return render_template("error.html", txt="Arvion poistaminen onnistui", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")
            return render_template("error.html", txt="Arvion poistaminen ei onnistunut", link="/admin_tools", link_txt="Palaa ylläpitäjän työkaluihin")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


