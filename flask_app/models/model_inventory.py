from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

class Inventory():
    db = "wcl_shop_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.size = data["size"]
        self.price = data["price"]
        self.picture = data["picture"]
        self.availability = data["availability"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.category_id = data["category_id"]

    # CRUD create read update delete

    # Create item from frontend
    @classmethod
    def add_item(cls, data):
        query = '''
                INSERT INTO inventories
                (name, size, price, picture, availability, category_id)
                VALUES
                (%(name)s, %(size)s, %(price)s, %(picture)s, %(availability)s, %(category_id)s, )
                '''
        return connectToMySQL(cls.db).query_db(query, data)


    # READ ALL items
    @classmethod
    def all_items(cls):
        query = "SELECT * FROM inventories"

        results = connectToMySQL(cls.db).query_db(query)

        inventories = []
        for row in results:
            inventories.append(cls(row))

        return inventories


    # READ One
    @classmethod
    def one_item(cls, data):
        query = "SELECT * FROM inventories WHERE id = %(id)s"

        results = connectToMySQL(cls.db).query_db(query, data)

        if results:
            return Inventory(results[0])


    # READ by category
    @classmethod
    def category_items(cls, data):
        query = '''SELECT * FROM inventories
                LEFT JOIN categories
                ON inventories.category_id = categories.id
                WHERE categories.category_name LIKE %(category_name)s
                AND availability = 1
                '''

        results = connectToMySQL(cls.db).query_db(query, data)

        inventories = []
        for row in results:
            inventories.append(cls(row))
        return inventories


    # READ by availability
    @classmethod
    def sale_items(cls):
        query = '''
                SELECT * FROM inventories
                WHERE availability = 1
                '''
        results = connectToMySQL(cls.db).query_db(query)

        inventories = []
        for row in results:
            inventories.append(cls(row))

        return inventories


    # Update availability from 1 to 0 if check out
    @classmethod
    def update_availability(cls, data):
        query = '''
                UPDATE inventories
                SET availability = 0, updated_at = NOW()
                WHERE id = %(id)s
                '''
        return connectToMySQL(cls.db).query_db(query, data)


    # Delete the item in DB from frontend
    @classmethod
    def delete_item(cls, data):
        query = '''DELETE FROM inventories
                WHERE id = %(id)s'''
        return connectToMySQL(cls.db).query_db(query, data)
