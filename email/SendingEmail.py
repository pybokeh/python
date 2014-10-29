import smtplib
from email.mime.text import MIMEText
from email.utils import COMMASPACE # This is a just a fancy way of doing: COMMASPACE = ", "

def sendEmail():
    recipient = ['email@gmail.com','email2@gmail.com']

    pwd = 'your password'
    sender  = 'pyfeeds@gmail.com'
    subject = '**** ALERT ****'
    message = "ATTENTION: Someone has entered the home"

    msg = MIMEText(message)
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
