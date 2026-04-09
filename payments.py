import stripe
from config import STRIPE_SECRET, DOMAIN

stripe.api_key = STRIPE_SECRET


def create_payment_link(user_id, product, amount):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product,
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"{DOMAIN}/success",
        cancel_url=f"{DOMAIN}/cancel",
        metadata={
            "tg_id": user_id,
            "product": product
        }
    )

    return session.url