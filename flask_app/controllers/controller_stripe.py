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
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (e.g. pr_1234) of the product you want to sell
                    'price': "price_id",
                    'quantity': 1,
                },
            ],

            payment_method_types=[
                'card',
            ],

            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)