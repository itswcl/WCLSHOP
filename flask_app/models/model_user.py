from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User():
    def __init__(self):
        pass