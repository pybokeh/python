# This script allows the raspberry pi to detect motion and then sends a SMS using Twilio
# Works with Python 3

import RPi.GPIO as GPIO
import time
from twilio.rest import TwilioRestClient

def send_sms(msg, to):
    sid = "your_sid"
    auth_token = "your_auth_token"
    twilio_number = "your_twilio_number"

    client = TwilioRestClient(sid, auth_token)

    message = client.messages.create(body=msg,
                                     from_=twilio_number,
                                     to=to,
                                     )

msg = "####  MOTION DETECTED  ####"
to = "number_to_send_sms_to"

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN)

while True:
    input_state = GPIO.input(18)
    if input_state == True:
        print('Motion Detected')
        time.sleep(2)
        send_sms(msg, to)
