from flask_app import app
from flask import redirect, request, render_template, session
import stripe

from flask_app.models.model_inventory import Inventory
# This is a sample test API key. Sign in to see examples pre-filled with your key.
stripe.api_key = 'sk_test_51J6cbdH6XBwBmUIZcdaYXRymcIZk2Dh16ZSUbYweWpF5diTkOwgrCdWvQpIpy0Ye8UIelUDVyEqqKdTDT6FF0ybH00LCsrFYFD'

# YOUR_DOMAIN = 'http://18.189.49.147/'
YOUR_DOMAIN = 'http://localhost:5000'
# YOUR_DOMAIN = 'http://solewcl.com/'

@app.route('/create-checkout-session/', methods=['POST'])
def create_checkout_session():
    session["id"] = request.form["id"]
    name = Inventory.one_item({"id": session["id"]}).name
    image = Inventory.one_item({"id": session["id"]}).picture + "?."
    price = Inventory.one_item({"id": session["id"]}).price

    try:
        checkout_session = stripe.checkout.Session.create(
            # method 1 base on the price id which create before hand
            # line_items=[
            #     {
            #         # Provide the exact Price ID (e.g. pr_1234) of the product you want to sell
            #         'price': price.id,
            #         'quantity': 1,
            #     },
            # ],
            # method 2 base on given data from web page
            line_items=[
                {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': name,
                    'images' : [image]
                    },
                    'unit_amount': price,
                },
                'quantity': 1,
                }
            ],

            payment_method_types=[
                'card',
            ],

            shipping_address_collection= {
                "allowed_countries": ["US", "CA"],
            },

            shipping_options=[
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {
                        'amount': 0,
                        'currency': 'usd',
                        },
                        'display_name': 'Free shipping',
                    }
                },
            ],

            mode='payment',
            success_url=YOUR_DOMAIN + "/shop/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=YOUR_DOMAIN + "/shop/all",
        )

    except Exception as e:
        return str(e)

    # print(request.form["id"])
    return redirect(checkout_session.url, code=303)

@app.route('/shop/success')
def order_success():
    session_stripe = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    # print(session_stripe)
    customer = stripe.Customer.retrieve(session_stripe.customer)
    print(customer)
    Inventory.update_availability({"id": session["id"]})

    return render_template("success.html", customer = customer)