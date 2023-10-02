import random
import string
from django.conf import settings
from twilio.rest import Client  # Import the Twilio Client if using Twilio

def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_phone(phone_number, otp):
    account_sid = 'AC23d2597c23476ed2a12747a9b47a0a1e'  # Replace with your Twilio account SID
    auth_token = '410b75750b5fa0b19a9ddcf623ed406c'  # Replace with your Twilio auth token
    twilio_phone_number = '+18062305450'  # Replace with your Twilio phone number

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Ваш код: {otp}',
        from_=twilio_phone_number,
        to=phone_number
    )