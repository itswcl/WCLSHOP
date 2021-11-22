from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

from flask import flash
import re

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Admin:
    db = "wcl_shop_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # admin resgistration
    @classmethod
    def create_admin(self, data):
        query = "INSERT INTO admins (email, password) VALUE (%(email)s,%(password)s);"
        return connectToMySQL(self.db).query_db(query, data)


    # find admin by email
    @classmethod
    def by_email(self,data):
        query = "SELECT * FROM admins WHERE email = %(email)s;"

        results = connectToMySQL(self.db).query_db(query, data)

        if len(results) == 0:
            return False

        return Admin(results[0])



    # find admin by id
    @classmethod
    def by_id(self,data):
        query = "SELECT * FROM admins WHERE id = %(id)s"

        results = connectToMySQL(self.db).query_db(query, data)

        if len(results) == 0:
            return False

        return Admin(results[0])


    # log in validation
    @staticmethod
    def login_validation(post_data):
        admin = Admin.by_email({"email": post_data["email"]})

        if not admin:
            flash("no admin in the record")
            return False

        if not bcrypt.check_password_hash(admin.password, post_data["password"]):
            flash("wrong password")
            return False

        return True


    @staticmethod
    def in_valid(post_data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # if len(post_data["first_name"]) < 2:
        #     flash("invalid first name")
        #     is_valid = False

        # if len(post_data["last_name"]) < 2:
        #     flash("invalid last name")
        #     is_valid = False

        if not EMAIL_REGEX.match(post_data["email"]):
            flash("invalid email")
            is_valid = False
        else:
            admin = Admin.by_email({"email": post_data["email"]})
            if admin:
                flash("Try another email")
                is_valid = False

        if len(post_data["password"]) < 8:
            flash("invalid password")
            is_valid = False
        elif post_data["password"].isalpha():
            flash("at least 1 number required in password")
            is_valid = False
        elif not any(letter.isupper() for letter in post_data["password"]):
            flash("at least 1 uppercase required in password")
            is_valid = False

        if post_data["password"] != post_data["confirm_password"]:
            flash("password not match")
            is_valid = False

        return is_valid