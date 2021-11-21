from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_inventory import Inventory

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shop/all")
def all_products():
    if not session:
        return render_template(
            "products_page.html",
            inventories = Inventory.sale_items(),
        )
    else:
        return render_template(
            "products_page.html",
            inventories = Inventory.sale_items(),
            session = session["uuid"]
        )

@app.route("/shop/<int:id>")
def one_product(id):
    inventory = Inventory.one_item({"id": id})
    # print (inventory.id)
    return render_template("detail_page.html", inventory = inventory)

@app.route("/shop/cart")
def cart_page():
    return render_template("cart_page.html")

@app.route("/shop/all/<category_name>/")
def category_products(category_name):
    return render_template("products_page.html", inventories = Inventory.category_items({"category_name": category_name}))

@app.route("/testimonial")
def testimonial():
    return render_template("test_page.html")

