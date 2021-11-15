from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

