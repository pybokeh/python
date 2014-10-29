import cgi
import cgitb
import os
import Cookie
import htmlbuilder
cgitb.enable()

def check_membership():
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE']
        cookies = cookies.split('; ')
        for cookie in cookies:
           cookie = cookie.split('=')
           name = cookie[0]
           value = cookie[1]
           if name == "membership" :
               return int(value)
    else:
        return 0

val = check_membership()
htmlbuilder.beginHTML("Cookie")
if val == 0 :
    print "<B>You are not a member!</B>"
else :
    print "<B>You are a member!</B>"
htmlbuilder.endHTML()


