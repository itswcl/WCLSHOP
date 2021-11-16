from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_inventory import Inventory

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shop/all")
def all_products():
    return render_template("products_page.html", inventories = Inventory.all_items())

@app.route("/shop/<int:id>")
def one_product(id):
    return render_template("detail_page.html", inventory = Inventory.one_item({"id": id}))

@app.route("/shop/cart")
def cart_page():
    return render_template("cart_page.html")
# @app.route("/shop/<string:category_name>")
# def products(category_name):
#     Inventory.all_items()
#     return render_template("products_page.html")

# @app.route("/shop/testimonial")
# def testimonial():
#     return render_template("testimonial.html")

