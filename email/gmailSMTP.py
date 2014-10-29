import cgi
import smtplib
from email.mime.text import MIMEText

# Get user input from the browser form
form      = cgi.FieldStorage()
sender    = form.getvalue('sender')
pwd       = form.getvalue('password')
recipient = form.getvalue('recipient')
subject   = form.getvalue('subject')
message   = form.getvalue('message')


msg = MIMEText(message)
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = recipient

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()

try:
    server.login(sender,pwd)
except smtplib.SMTPAuthenticationError:               # Check for authentication error
    print "Content-Type: text/html\n\n"
    print """
<html>
<h3>Error: Please check your email and password.</h3>
</html>"""
    
try:
    server.sendmail(sender,recipient,msg.as_string())
    print "Content-Type: text/html\n\n"
    print """
<html>
<h3>Your email was successfully sent.</h3>
</html>"""
except smtplib.SMTPRecipientsRefused:                # Check if recipient's email was accepted by the server
    print "Content-Type: text/html\n\n"
    print """
<html>
<h3>Error: the recipient's email was not accepted.  Please check the spelling.</h3>
</html>"""
    
server.quit()
