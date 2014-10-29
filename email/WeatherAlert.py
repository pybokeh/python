import smtplib, time
from email.mime.text import MIMEText
from email.utils import COMMASPACE # This is a just a fancy way of doing: COMMASPACE = ", "
import urllib.request as request
import simplejson
from pprint import pprint  # Prettier printing of json data
from datetime import datetime

def emailWeatherAlert():
    json = request.urlopen('http://api.wunderground.com/api/your_api/alerts/q/OH/Dublin.json')
    parsed_json = simplejson.load(json)
    
    recipient = ['email@gmail.com']

    pwd = 'your_password'
    sender  = 'your_email@gmail.com'
    subject = '**** Wunderground Weather ALERT ****'

    top_border = "Weather ALERT from the Wunderground\n\n"+"Brought to you by the Raspberry Pi!\n"+\
    "*" * 45+"\n"
    bottom_border = "*" * 45+"\n\n"
    
    if parsed_json["alerts"]:
        email = ""
        for alert in parsed_json["alerts"]:
            date = alert["date"]
            description = alert["description"]
            expires = alert["expires"]
            message = alert["message"]
        
            email = email+top_border+"Date: "+date+"\n"+"Description: "+description+"\n"+"Expires: "\
            +expires+"\n"+bottom_border+"Message:\n"+message+"\n"
                
            msg = MIMEText(email)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = COMMASPACE.join(recipient) # COMMASPACE still works ok with just one recipient
            #msg['CC'] = COMMASPACE.join(recipient)
            #msg['BCC'] = COMMASPACE.join(recipient)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()

            try:
                server.login(sender,pwd)
            except smtplib.SMTPAuthenticationError: # Check for authentication error
                return "ERROR"

            try:
                server.sendmail(sender, recipient, msg.as_string())
            except smtplib.SMTPRecipientsRefused:   # Check if recipient's email was accepted by the server
                return "ERROR"
            server.quit()
    else:
        now = datetime.now()
        print("There are no alerts for this location at this time:",now.strftime("%Y-%m-%d %I:%M%p"))


while True:
    emailWeatherAlert()
    time.sleep(7200)
