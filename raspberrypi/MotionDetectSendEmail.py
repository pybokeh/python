# This script allows the raspberry pi to detect motion and then sends an email
# Works with Python 3

from Crypto.Cipher import AES
import smtplib
import RPi.GPIO as GPIO
import time
import base64
import os
import codecs # This is needed to convert a string with single backslashes to byte string

def decrypt_with_key(key, encryptedString):
    """ Method to decrypt message using a decryptionn key passed in as a parameter """
    
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).decode('utf-8').rstrip(PADDING)
    try:
        cipher = AES.new(key)
        decoded = DecodeAES(cipher, encryptedString)
        return decoded
    except:
        print("Error in decoding the secret message")

# Get the decryption key
key_file = open('/home/pi/venv/motion/src/key','r')
# Read the decryption key properly adn strip out newline character
key = codecs.escape_decode(key_file.read().strip())[0]
key_file.close()

# Open the file containing the encrypted password
efile = open('/home/pi/venv/motion/src/pwd','r')
emessage = efile.read()
efile.close()

GMAIL_USER = 'pybokeh@gmail.com'
GMAIL_PASS = decrypt_with_key(key, emessage)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email(recipient, subject, text):
    smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + recipient + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + subject + '\n'
    msg = header + '\n' + text + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, recipient, msg)
    smtpserver.close()

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN)

while True:
    input_state = GPIO.input(18)
    if input_state == True:
        print('Motion Detected')
        time.sleep(2)
        send_email('justdanielnow@gmail.com', '### ALERT! ###', 'Motion detected at the house!')
