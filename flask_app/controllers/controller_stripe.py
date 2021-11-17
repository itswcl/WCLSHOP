from flask_app import app
import os
from flask import Flask, redirect, request

import stripe

from flask_app.models.model_inventory import Inventory
# This is a sample test API key. Sign in to see examples pre-filled with your key.
stripe.api_key = 'sk_test_51J6cbdH6XBwBmUIZcdaYXRymcIZk2Dh16ZSUbYweWpF5diTkOwgrCdWvQpIpy0Ye8UIelUDVyEqqKdTDT6FF0ybH00LCsrFYFD'

YOUR_DOMAIN = 'http://localhost:5000'

@app.route('/create-checkout-session/', methods=['POST'])
def create_checkout_session():

    # item = stripe.Product.create(
    #     name = request.form["name"]
    # )

    # item.images.append(request.form["image"])
    # print(item)

    # price = stripe.Price.create(
    #     unit_amount = request.form["price"],
    #     currency = "usd",
    #     product = item["id"]
    # )

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
                    'name': request.form["name"],
                    'images' : [request.form["image"]]
                    },
                    'unit_amount': request.form["price"],
                },
                'quantity': 1,
            }
            ],

            payment_method_types=[
                'card',
            ],

            mode='payment',
            success_url=YOUR_DOMAIN + "/success.html",
            cancel_url=YOUR_DOMAIN + "/shop/all",
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)