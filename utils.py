import os
import logging
from datetime import datetime, timedelta
import random

from twilio.rest import Client
from flask import url_for

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

def send_sms_notification(to_phone_number, message):
    """
    Send SMS notification using Twilio
    
    Note: With trial accounts, you can only send messages to verified numbers.
    If using a trial account, verify the phone numbers at:
    https://www.twilio.com/console/phone-numbers/verified
    """
    # Check if Twilio credentials are properly configured
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]) or \
       TWILIO_ACCOUNT_SID == "your_twilio_sid":
        logging.warning("Twilio is not properly configured. SMS notification skipped.")
        return False
    
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
        # If the error is due to unverified number in trial account, log a more helpful message
        if "unverified" in str(e).lower():
            logging.error(f"Failed to send SMS: The number {to_phone_number} is not verified. "
                         f"With trial accounts, you must verify numbers at "
                         f"https://www.twilio.com/console/phone-numbers/verified")
        else:
            logging.error(f"Failed to send SMS: {str(e)}")
        return False



def generate_order_tracking(order):

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
