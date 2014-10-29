# http://www.dzone.com/snippets/how-send-im-jabber-message
import sys,xmpp

# Google Talk constants
FROM_GMAIL_ID = "your_email@gmail.com"
GMAIL_PASS = "your_pwd"
GTALK_SERVER = "talk.google.com"
TO_GMAIL_ID = "your_friends@gmail.com"

jid=xmpp.protocol.JID(FROM_GMAIL_ID)
cl=xmpp.Client(jid.getDomain(),debug=[])
if not cl.connect((GTALK_SERVER,5222)):
    raise IOError('Can not connect to server.')
if not cl.auth(jid.getNode(),GMAIL_PASS):
    raise IOError('Can not auth with server.')

cl.send( xmpp.Message( TO_GMAIL_ID ,"Hello World!" ) )
cl.disconnect()
