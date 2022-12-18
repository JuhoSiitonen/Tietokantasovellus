from flask import render_template, request, redirect, abort
from app import app
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
        error_txt = "Käyttäjätunnusta ei löydy"
        link_txt = "Yritä uudelleen"
        if users.login(username, password):
            return render_template("front.html")
        return render_template("error.html", txt=error_txt, link="/", link_txt=link_txt)
    return render_template("front.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="GET":
        return render_template("register.html")
    if request.method =="POST":
        link = "/register"
        link_txt = "Yritä uudelleen"
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if not users.check_text_input(username,3,20) or not users.check_text_input(password,3,20):
            error_txt = "Käyttäjätunnuksen ja salasanan pituus tulee olla vähintään 3 merkkiä " \
                "ja maksimissaan 20 merkkiä"
            return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
        if password != password2:
            error_txt = "Salasanat eivät täsmää"
            return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
        if users.register(username,password):
            return render_template("front.html")
        return render_template(
            "error.html", txt="Rekisteröinti ei onnistunut", link=link, link_txt=link_txt
            )

# Next four functions render the pages when clicking "Ravintolat lähelläsi"
# from the frontpage.

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
    if not dish:
        error_txt = "Et ole valinnut mitään tilattavaksi."
        link = "/front"
        link_txt = "Palaa etusivulle"
        return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
    orders = []
    total_price = 0
    for item in dish:
        order = restaurants.dish_name(item)
        orders.append(order)
        total_price += order[2]
    extra_info = request.form["message"]
    if len(extra_info) > 500:
        error_txt = "Erikoistiedoissa voi olla enintään 500 merkkiä"
        link = "/front"
        link_txt = "Palaa etusivulle"
        return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
    return render_template(
        "confirmation.html", orders=orders, extra_info=extra_info, total_price=total_price
        )

@app.route("/receipt", methods=["POST"])
def receipt():
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    order_info = request.form.getlist("orders")
    restaurant_id = int(request.form["restaurant_id"])
    extra_info = request.form["extra_info"]
    receipt = restaurants.create_receipt(order_info, restaurant_id, extra_info)
    return render_template("receipt.html", receipt=receipt)

# Receipt archive function renders the page "Omat tilaukseni" and inspec_receipt
# renders the page for viewing a specific order chosen from receipt_archive page

@app.route("/receipts/<user_id>")
def receipt_archive(user_id):
    link = "/front"
    link_txt = "Palaa etusivulle"
    if int(user_id) != users.user_id():
        return render_template("error.html", txt="", link=link, link_txt=link_txt)
    receipts = users.user_receipts(user_id)
    if not receipts:
        error_txt = "Et ole tehnyt tilauksia"
        return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
    return render_template("user_receipts.html", receipts=receipts)

@app.route("/receipt/<receipt_id>")
def inspect_receipt(receipt_id):
    receipt = users.inspect_receipt(receipt_id)
    if receipt.user_id != users.user_id():
        return render_template("error.html", txt="", link="/front", link_txt="Palaa etusivulle")
    receipt_dishes = users.receipt_dishes(receipt_id)
    return render_template("inspect_receipt.html", receipt_dishes=receipt_dishes, receipt=receipt)

# Review function renders the review page which is accessed after order confirmation
# or separately from the frontpage, modifying reviews is its own page

@app.route("/review/<restaurant_id>", methods=["GET", "POST"])
def review(restaurant_id):
    if request.method == "GET":
        return render_template("review.html", restaurant_id=restaurant_id)
    if request.method == "POST":
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        link = "/front"
        link_txt = "Takaisin etusivulle"
        stars = int(request.form["rating"])
        if stars < 1 or stars > 5:
            error_txt = "Soo soo, älä manipuloi keskiarvoja"
            return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
        review = request.form["text_review"]
        if not users.check_text_input(review, 0, 500):
            error_txt = "Voit lähettää maksimissaan 500 merkin sanallisen palautteen"
            return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
        restaurants.create_review(restaurant_id, review, stars)
        return render_template("error.html", txt="Palaute lähetetty", link=link, link_txt=link_txt)

# Best reviews function renders the page accessed by clicking "Parhaiten arvostellut ravintolat"
# on the frontpage and restaurant_reviews shows user the reviews for a chosen restaurant

@app.route("/best_reviews")
def best_reviews():
    listing = restaurants.best_reviews()
    return render_template("best_reviews.html", reviews=listing)

@app.route("/best_reviews/<restaurant_id>")
def restaurant_reviews(restaurant_id):
    reviews = restaurants.restaurant_reviews(restaurant_id)
    return render_template("restaurant_reviews.html", reviews=reviews)

# user_reviews function renders the page accessed by clicking "Omat arvosteluni" in the
# frontpage, and modify reviews lets user modify chosen review from user_reviews page.

@app.route("/reviews/<user_id>")
def user_reviews(user_id):
    link = "/front"
    link_txt = "Palaa etusivulle"
    if int(user_id) != users.user_id():
        return render_template("error.html", txt="", link=link, link_txt=link_txt)
    reviews = users.user_reviews(user_id)
    if not reviews:
        error_txt = "Et ole tehnyt vielä yhtään arvostelua"
        return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
    return render_template("user_reviews.html", reviews=reviews)

@app.route("/modify_review/<review_id>", methods=["GET", "POST"])
def modify_review(review_id):
    link = "/front"
    link_txt = "Palaa etusivulle"
    if request.method == "GET":
        if users.user_id() != users.check_review_id(review_id):
            return render_template("error.html", txt="", link=link, link_txt=link_txt)
        return render_template("modify_review.html", review_id=review_id)
    if request.method == "POST":
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        stars = int(request.form["rating"])
        if stars < 1 or stars > 5:
            error_txt = "Soo soo, älä manipuloi keskiarvoja"
            return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
        review = request.form["text_review"]
        if not users.check_text_input(review, 0, 500):
            error_txt = "Voit lähettää maksimissaan 500 merkin sanallisen palautteen"
            return render_template("error.html", txt=error_txt,link=link, link_txt=link_txt)
        users.modify_review(review_id, review, stars)
        return render_template("error.html", txt="Palaute lähetetty", link=link, link_txt=link_txt)

# Find and result functions for page "Ravintolahaku"

@app.route("/find_restaurant")
def find_restaurant():
    return render_template("find_restaurant.html")

@app.route("/result")
def result():
    description = request.args["description"]
    if not users.check_text_input(description, 3, 20):
        error_txt = "Voit käyttää hakusanakentässä 3-20 merkkiä"
        link = "/find_restaurant"
        link_txt = "Yritä uudelleen"
        return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)
    results = restaurants.find_restaurants(description)
    if results:
        return render_template("result.html", results=results)
    return render_template(
        "error.html", txt="Hakusanoillasi ei löytynyt ravintoloita", link="/front",
        link_txt="Takaisin etusivulle"
        )

# Review function for review page accessed from the frontpage

@app.route("/reviewable")
def review_restaurant():
    user_id = users.user_id()
    listing = users.reviewable_restaurants(user_id)
    error_txt = "Et voi arvioida ravintoloita, koska et ole vielä tilannut mistään"
    link = "/front"
    link_txt = "Palaa etusivulle"
    if listing:
        return render_template("reviewable.html", listing=listing)
    return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)

# Admin tools function renders a second navigation page with admin tools

@app.route("/admin_tools")
def admin_tools():
    if users.is_admin():
        return render_template("admin_tools.html")
    error_txt = "Jotain meni pieleen"
    link = "/front"
    link_txt = "Palaa etusivulle"
    return render_template("error.html", txt=error_txt, link=link, link_txt=link_txt)

# Two functions for all the adding tools and deletion tools in admin tools page
# One add and one delete page used with these functions, and dynamically rendered according
# to user selection with functions below the view function

@app.route("/add/<element_to_add>", methods=["GET", "POST"])
def add(element_to_add):
    if request.method == "GET":
        if element_to_add == "restaurant":
            return render_template("add.html", element="1")
        if element_to_add == "dish":
            return render_template("add.html", element="2")
        if element_to_add == "admin":
            return render_template("add.html", element="3")

    if request.method == "POST":
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        if element_to_add == "restaurant":
            return add_restaurant()
        if element_to_add == "dish":
            return add_dish()
        if element_to_add == "admin":
            return add_admin()

def add_restaurant():
    restaurant_name = request.form["restaurant_name"]
    restaurant_address = request.form["restaurant_address"]
    description = request.form["description"]
    link = "/admin_tools"
    link_txt ="Palaa ylläpitäjän työkaluihin"
    name_error = "Ravintolan nimi voi olla 3-30 merkkiä pitkä"
    address_error = "Ravintolan osoite voi olla 3-60 merkkiä pitkä"
    desc_error = "Ravintolan kuvaus voi olla maksimissaan 1000 merkkiä"
    add_success = "Ravintolan lisäys onnistui!"
    add_failure = "Ravintolan lisäys ei onnistunut"
    if not users.check_text_input(restaurant_name, 3, 30):
        return render_template("error.html", txt=name_error, link=link, link_txt=link_txt)
    if not users.check_text_input(restaurant_address, 3, 60):
        return render_template("error.html", txt=address_error, link=link, link_txt=link_txt)
    if len(description) > 1000:
        return render_template("error.html", txt=desc_error, link=link, link_txt=link_txt)
    if admin.add_restaurant(restaurant_name, restaurant_address, description):
        return render_template("error.html", txt=add_success, link=link, link_txt=link_txt)
    return render_template("error.html", txt=add_failure, link=link, link_txt=link_txt)

def add_dish():
    restaurant_name = request.form["restaurant_name"]
    dish_name = request.form["dish_name"]
    price = request.form["price"]
    link = "/admin_tools"
    link_txt = "Palaa ylläpitäjän työkaluihin"
    name_error = "Ravintolan nimi voi olla 3-30 merkkiä pitkä"
    dish_error = "Annoksen nimi voi olla 3-30 merkkiä pitkä"
    price_error = "Hinnan tulee olla kokonaisluku joka on 1-9 merkkiä pitkä"
    add_success = "Annoksen lisäys onnistui!"
    add_failure = "Annoksen lisäys ei onnistunut"
    if not users.check_text_input(restaurant_name, 3, 30):
        return render_template("error.html", txt=name_error, link=link, link_txt=link_txt)
    if not users.check_text_input(dish_name, 3, 30):
        return render_template("error.html", txt=dish_error, link=link, link_txt=link_txt)
    if not users.check_text_input(price, 1, 9, True):
        return render_template("error.html", txt=price_error, link=link, link_txt=link_txt)
    price = int(price)
    restaurant_id = restaurants.get_restaurant_id(restaurant_name)[0]
    if admin.add_dish(restaurant_id, dish_name, price):
        return render_template("error.html", txt=add_success, link=link, link_txt=link_txt)
    return render_template("error.html", txt=add_failure, link=link, link_txt=link_txt)

def add_admin():
    user_name = request.form["user_name"]
    link = "/admin_tools"
    link_txt = "Palaa ylläpitäjän työkaluihin"
    name_error = "Käyttäjänimi voi olla 3-20 merkkiä pitkä"
    success = "Ylläpitäjän lisäys onnistui!"
    failure ="Ylläpitäjän lisäys ei onnistunut"
    if not users.check_text_input(user_name, 3, 20):
        return render_template("error.html", txt=name_error, link=link, link_txt=link_txt)
    if admin.add_admin(user_name):
        return render_template("error.html", txt=success, link=link, link_txt=link_txt)
    return render_template("error.html", txt=failure, link=link, link_txt=link_txt)

@app.route("/delete/<element_to_delete>", methods=["GET", "POST"])
def delete(element_to_delete):
    if request.method == "GET":
        if element_to_delete == "user":
            return render_template("delete.html", element="1")
        if element_to_delete == "restaurant":
            return render_template("delete.html", element="2")
        if element_to_delete == "dish":
            return render_template("delete.html", element="3")
        if element_to_delete == "review":
            return render_template("delete.html", element="4")

    if request.method == "POST":
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        if element_to_delete == "user":
            return delete_user()
        if element_to_delete == "restaurant":
            return delete_restaurant()
        if element_to_delete == "dish":
            return delete_dish()
        if element_to_delete == "review":
            return delete_review()

def delete_user():
    link = "/admin_tools"
    link_txt = "Palaa ylläpitäjän työkaluihin"
    success = "Käyttäjän poistaminen onnistui"
    failure = "Käyttäjän poistaminen ei onnistunut"
    username = request.form["username"]
    user_id = admin.get_user_id(username)
    if user_id != 0:
        admin.delete_user(user_id)
        return render_template("error.html", txt=success, link=link, link_txt=link_txt)
    return render_template("error.html", txt=failure, link=link, link_txt=link_txt)

def delete_restaurant():
    link = "/admin_tools"
    link_txt = "Palaa ylläpitäjän työkaluihin"
    success = "Ravintolan poistaminen onnistui"
    failure = "Ravintolan poistaminen ei onnistunut"
    restaurant_name = request.form["restaurant_name"]
    restaurant_id = restaurants.get_restaurant_id(restaurant_name)[0]
    if restaurant_id != 0:
        admin.delete_restaurant(restaurant_id)
        return render_template("error.html", txt=success, link=link, link_txt=link_txt)
    return render_template("error.html", txt=failure, link=link, link_txt=link_txt)

def delete_dish():
    link = "/admin_tools"
    link_txt = "Palaa ylläpitäjän työkaluihin"
    success = "Annoksen poistaminen onnistui"
    failure = "Annoksen poistaminen ei onnistunut"
    restaurant_name = request.form["restaurant_name"]
    restaurant_id = restaurants.get_restaurant_id(restaurant_name)[0]
    dish_name = request.form["dish_name"]
    dish_id = restaurants.get_dish_id(restaurant_id, dish_name)[0]
    if restaurant_id != 0 and dish_id != 0:
        admin.delete_dish(dish_id)
        return render_template("error.html", txt=success, link=link, link_txt=link_txt)
    return render_template("error.html", txt=failure, link=link, link_txt=link_txt)

def delete_review():
    link = "/admin_tools"
    link_txt = "Palaa ylläpitäjän työkaluihin"
    success = "Arvion poistaminen onnistui"
    failure = "Arvion poistaminen ei onnistunut"
    review_id = request.form["review_id"]
    if admin.delete_reviews(review_id):
        return render_template("error.html", txt=success, link=link, link_txt=link_txt)
    return render_template("error.html", txt=failure, link=link, link_txt=link_txt)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
