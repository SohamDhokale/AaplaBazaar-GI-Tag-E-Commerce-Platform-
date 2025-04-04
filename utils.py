import os
import logging
from datetime import datetime, timedelta
import random
import stripe

from twilio.rest import Client
from flask import url_for

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Stripe
stripe_key = os.environ.get('STRIPE_SECRET_KEY')
if stripe_key and stripe_key.startswith('pk_'):
    logging.error("ERROR: You provided a publishable key (pk_) instead of a secret key (sk_)")
    logging.error("Please update your STRIPE_SECRET_KEY environment variable with a secret key")
    # Don't set the api_key if it's a publishable key to avoid further issues
else:
    stripe.api_key = stripe_key
    logging.info(f"Stripe API key configured: {stripe.api_key is not None}")

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "your_twilio_sid")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "your_twilio_auth_token")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "+1234567890")

def send_sms_notification(to_phone_number, message):
    """
    Send SMS notification using Twilio
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # Adding country code for India if not present
        if not to_phone_number.startswith('+'):
            to_phone_number = '+91' + to_phone_number
            
        # Send the SMS
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        logging.info(f"Message sent with SID: {message.sid}")
        return True
    except Exception as e:
        logging.error(f"Failed to send SMS: {str(e)}")
        return False

def create_payment_session(products, total_amount, success_url, cancel_url):
    """
    Create a Stripe checkout session
    """
    # First check if we have a valid API key
    if not stripe.api_key or (stripe_key and stripe_key.startswith('pk_')):
        logging.error("Cannot create Stripe session: Invalid or missing secret key")
        return None
        
    try:
        # Convert to paisa (Stripe uses smallest currency unit)
        amount_in_paisa = int(total_amount * 100)
        
        logging.info(f"Creating Stripe checkout session for amount: {amount_in_paisa} paisa")
        logging.info(f"Success URL: {success_url}")
        logging.info(f"Cancel URL: {cancel_url}")
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'AaplaBazaar Order',
                        'description': f'Order total for {len(products)} items',
                    },
                    'unit_amount': amount_in_paisa,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        
        logging.info(f"Checkout session created successfully: {checkout_session.id}")
        return checkout_session
    except Exception as e:
        error_msg = str(e)
        if hasattr(e, 'user_message'):
            error_msg = e.user_message
        
        # Log detailed error information
        logging.error(f"Stripe session creation failed: {error_msg}")
        
        # Check for specific error types
        if "secret_key_required" in error_msg:
            logging.error("You need to use a secret key (sk_) for this operation, not a publishable key (pk_)")
        
        return None

def generate_order_tracking(order):
    """
    Generate mock tracking updates for the order
    Note: In a real application, this would be based on actual shipping data
    """
    current_time = datetime.utcnow()
    tracking_updates = []
    
    # Order received
    tracking_updates.append({
        'status': 'Order Received',
        'location': 'AaplaBazaar Warehouse',
        'timestamp': current_time,
        'description': 'Your order has been received and is being processed.'
    })
    
    # Processing
    processing_time = current_time + timedelta(hours=random.randint(2, 12))
    tracking_updates.append({
        'status': 'Processing',
        'location': 'AaplaBazaar Warehouse',
        'timestamp': processing_time,
        'description': 'Your order is being processed and packed.'
    })
    
    # Shipped
    shipping_time = processing_time + timedelta(hours=random.randint(12, 24))
    tracking_updates.append({
        'status': 'Shipped',
        'location': 'Mumbai Distribution Center',
        'timestamp': shipping_time,
        'description': 'Your order has been shipped and is on its way to you.'
    })
    
    # Out for Delivery (future event)
    delivery_time = shipping_time + timedelta(days=random.randint(1, 3))
    if delivery_time > datetime.utcnow():
        tracking_updates.append({
            'status': 'Out for Delivery',
            'location': f'Local Delivery Center - {order.shipping_city}',
            'timestamp': delivery_time,
            'description': 'Your order is out for delivery to your address.'
        })
    
    # Delivered (future event)
    delivered_time = delivery_time + timedelta(hours=random.randint(1, 8))
    if delivered_time > datetime.utcnow():
        tracking_updates.append({
            'status': 'Delivered',
            'location': order.shipping_city,
            'timestamp': delivered_time,
            'description': 'Your order has been delivered. Thank you for shopping with AaplaBazaar!'
        })
    
    return tracking_updates, delivered_time
