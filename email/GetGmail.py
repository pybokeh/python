import cgi
import imaplib
service = imaplib.IMAP4_SSL('imap.gmail.com',993)

# Get user input from the browser form
form      = cgi.FieldStorage()
email     = form.getvalue('email')
pwd       = form.getvalue('password')
sentSince = form.getvalue('date')

try:
   service.login(email,pwd)
except:               # Check for authentication error
   print "Content-Type: text/html\n\n"
   print """
<html>
<h3>Error: Please check your email and password.</h3>
</html>"""

status,count = service.select('inbox')
query = '(ALL SENTSINCE %s)' % sentSince
retcode,messages = service.search(None,query)
print "Content-Type: text/plain\n\n"

if retcode == 'OK':
   for message in messages[0].split(' '):
       # Create a 2 dimensional list containing email message and email sender
       (ret, mesginfo) = service.fetch(message, '(BODY[HEADER.FIELDS (FROM)] BODY[TEXT])')
       if ret == 'OK':
           print 50*'+','BEGIN GMAIL',50*'+','\n'
           print mesginfo[1][1]                   # Print who the sender was
           print mesginfo[0][1]                   # Print the message body

service.close()
service.logout()
