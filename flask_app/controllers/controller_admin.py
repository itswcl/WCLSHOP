from flask import render_template, request, redirect,session

from flask_app import app
from flask_app.models.model_admin import Admin
from flask_app.models.model_inventory import Inventory
from flask_app.models.model_category import Category


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# -------------------- Display Route --------------------------- #
# register page for admin, no need for most of time only for new admin
# @app.route("/register")
# def form_admin():
#     return render_template("register_admin.html") if need register switch below


# display the admin on dashboard page
@app.route("/admin")
def dashboard():
    if not "uuid" in session:
        return redirect("/")

    admin = Admin.by_id({"id": session["uuid"]})
    inventories = Inventory.all_items()
    categories = {}

    for inventory in inventories:
        categories[inventory.category_id] = Category.one_category({"id": inventory.category_id})

    return render_template(
        "admin_dashboard.html",
        admin = admin,
        inventories = inventories,
        categories = categories
    )


# display log in page
@app.route("/login")
def index_admin():

    return render_template("login_page.html")


# --------------------- Action Route --------------------------- #
# register admin - only action route below if new admin join
# @app.route("/register_admin", methods=["POST"])
# def form_user_create():
#     if not Admin.in_valid(request.form):
#         return redirect ("/register")

#     if "uuid" in session:
#         return redirect("/")

#     new_user = {
#         **request.form,
#         # bcrypt the pass word for the user
#         "password": bcrypt.generate_password_hash(request.form["password"])
#     }

#     # save to session while creating the new user
#     session["uuid"] = Admin.create_admin(new_user)
#     return redirect("/")


# admin log in
@app.route("/login", methods=["POST"])
def form_user_login():
    if not Admin.login_validation(request.form):
        return redirect("/login")

    admin = Admin.by_email({"email": request.form["email"]})
    session["uuid"] = admin.id

    return redirect("/admin")


# admin log out
# log out = clean out session
@app.route("/logout")
def log_out():
    session.clear()
    return redirect("/")