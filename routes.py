from app import app
from flask import render_template, request, redirect
import users
import restaurants

# Mikään osio ei vielä sisällä käyttäjän syötteen tarkastelua esim liian pitkälle merkkijonolle
# Tämä moduuli tulisi varmaan jakaa useampaan eri moduuliin.. 

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
        if password != password2:
            return render_template("error.html", txt="Salasanat eivät täsmää", link="/register", link_txt="Yritä uudelleen")
        if users.register(username,password):
            return render_template("front.html")
        else:
            return render_template("error.html", txt="Rekisteröinti ei onnistunut", link="/register", link_txt="Yritä uudelleen")

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

# Olisiko muuta tapaa kantaa käyttäjän tilaustietoa mukana, jolloin ei tulisi niin monta POST
# metodin ja hidden inputtien käyttöä HTML pohjassa?? Esimerkiksi luokka? 

@app.route("/confirmation", methods=["POST"])
def confirmation():
    dish = request.form.getlist("dish")
    orders =[]
    total_price = 0
    for item in dish:
        order = restaurants.dish_name(item)
        orders.append(order)
        total_price += order[2]
    extra_info = request.form["message"]
    return render_template("confirmation.html", orders=orders, extra_info=extra_info, total_price=total_price)

@app.route("/receipt", methods=["POST"])
def receipt():
    order_info = request.form.getlist("orders")
    restaurant_id = int(request.form["restaurant_id"])
    total_price = int(request.form["total_price"])
    extra_info = request.form["extra_info"]
    receipt = restaurants.create_receipt(order_info, restaurant_id, total_price, extra_info)
    return render_template("receipt.html", receipt=receipt)

@app.route("/receipts/<user_id>")
def receipt_archive(user_id):
    if int(user_id) != users.user_id():
        return render_template("error.html", txt="", link="/front")
    receipts = users.user_receipts(user_id)
    if not receipts:
        return render_template("error.html", txt="Et ole tehnyt tilauksia", link="/front", link_txt="Takaisin etusivulle")
    return render_template("user_receipts.html", receipts=receipts)

@app.route("/receipt/<receipt_id>")
def inspect_receipt(receipt_id):
    receipt = users.inspect_receipt(receipt_id)
    receipt_dishes = users.receipt_dishes(receipt_id)
    return render_template("inspect_receipt.html", receipt_dishes=receipt_dishes, receipt=receipt)
    
@app.route("/review/<receipt_id>", methods=["GET", "POST"])
def review(receipt_id):
    if request.method == "GET":
         return render_template("review.html", receipt_id=receipt_id)
    if request.method == "POST":
        restaurant_id = (users.inspect_receipt(receipt_id)).restaurant_id
        review = request.form["text_review"]
        restaurants.create_review(restaurant_id, review)
        return render_template("error.html", txt="Palaute lähetetty", link="/front", link_txt="Takaisin etusivulle")

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
        return render_template("error.html", txt="Et ole tehnyt vielä yhtään arvostelua", link="/front", link_txt="Takaisin etusivulle")
    return render_template("user_reviews.html", reviews=reviews)

@app.route("/modify_review/<review_id>")
def modify_review(review_id):
    pass

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


