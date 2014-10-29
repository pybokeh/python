from googlevoice import Voice
import sys
from bs4 import BeautifulSoup

voice=Voice() # Create a Voice object
voice.login()
voice.inbox() # Get recent unread messages
htmlsms=voice.inbox.html  # Parse the messages into a HTML file

msgitems = [] # accumulate message items here
#	Extract all conversations by searching for a DIV with an ID at top level.
tree = BeautifulSoup(htmlsms)			# parse HTML into tree
conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
for conversation in conversations :
    #	For each conversation, extract each row, which is one SMS message.
    rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
    for row in rows :							# for all rows
        #	For each row, which is one message, extract all the fields.
        msgitem = {"id" : conversation["id"]}		# tag this message with conversation ID
        spans = row.findAll("span",attrs={"class" : True}, recursive=False)
        for span in spans : # for all spans in row
            cl = span["class"][0].replace('gc-message-sms-', '')
            msgitem[cl] = (" ".join(span.findAll(text=True))).strip()	# put text in dict
        msgitems.append(msgitem)					# add msg dictionary to list

for msg in msgitems:
    if msg['from'] != 'Me:':
        print "from: " + msg['from']
        print "text: " + msg['text']
        print "time: " + msg['time']
        print "------------------------------------"
