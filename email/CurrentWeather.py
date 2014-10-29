import smtplib, time, codecs, crypto
from email.mime.text import MIMEText
from email.utils import COMMASPACE # This is a just a fancy way of doing: COMMASPACE = ", "
import urllib.request as request
import simplejson
from datetime import datetime

def emailCurrentWeather():
    json = request.urlopen('http://api.wunderground.com/api/your_key/conditions/q/OH/Dublin.json')
    parsed_json = simplejson.load(json)
    
    recipient = ['email@gmail.com']

    key = codecs.escape_decode(open('/home/pi/tmp/key','r').read().strip())[0]
    pw = open('/home/pi/tmp/pw','r').read().strip()
    pwd = crypto.decrypt_with_key(key, pw)
    sender  = 'your_email'
    subject = 'Current Weather Conditions'

    top_border = "Current weather conditions from the Wunderground\n\n"+"Brought to you by the Raspberry Pi!\n"+\
    "*" * 45+"\n"
    bottom_border = "*" * 45+"\n\n"
    
    if parsed_json['current_observation']:
        city = parsed_json['current_observation']['display_location']['city']
        state = parsed_json['current_observation']['display_location']['state']
        current_temp = parsed_json['current_observation']['temperature_string']
        feels_like = parsed_json['current_observation']['feelslike_string']
        as_of = parsed_json['current_observation']['observation_time']
        rel_humidity = parsed_json['current_observation']['relative_humidity']
        weather = parsed_json['current_observation']['weather']
        forecast_url = parsed_json['current_observation']['forecast_url']
        
        email = top_border+as_of+"\n"+"City/State: "+city+", "+state+"\n"+bottom_border+ \
        "Current temp: "+current_temp+"\n"+"Feels like: "+feels_like+"\n"+"Rel. humidity: "+rel_humidity+"\n"+ \
        "Weather condition: "+weather+"\n"+"Forecast URL: "+forecast_url
        
        subject = subject+": "+current_temp
                
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
        print("Current weather conditions are not available at this time:",now.strftime("%Y-%m-%d %I:%M%p"))
