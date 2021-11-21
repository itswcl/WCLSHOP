from flask_app import app
from flask_app.controllers import controller_inventory, controller_stripe, controller_admin

if __name__ == "__main__":
    app.run(debug=True)