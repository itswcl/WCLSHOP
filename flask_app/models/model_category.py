from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Category:
    db = "wcl_shop_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.category_name = data["category_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # CRUD
    # Read 1 by id
    @classmethod
    def one_category(cls, data):
        query = "SELECT * FROM categories WHERE id = %(id)s"

        results = connectToMySQL(cls.db).query_db(query, data)

        if results:
            return Category(results[0])