import Cookie
# Build the beginning part of the HTML page
def beginHTML(title):
    member = Cookie.SimpleCookie()
    member["membership"] = 1
    member["membership"]["expires"] = 60*60*24*14
    print member
    print "Content-Type: text/html\n\n"
    print """
<HTML>
<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
<META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">
<head><title>%s</title></head>
<body>""" % title

# Build HTML table  (2 parts to this function: 1st part prints the column names, 2nd part prints the actual resultset
def createHtmlTable(column_name_list, resultset):
    num_columns = len(column_name_list)
    print "<table border=\"4\">"
    print "<tr>"
    for column_name in column_name_list:
        print "<th align=\"center\">" + column_name + "</th>"
    print "</tr>"
    print "<tr>"
    for row in resultset:
        for i in range(num_columns):
            print "<td align=\"center\">" + str(row[i]) + "</td>"
            i = i + 1
        print "</tr>"
    print "</table>"

# Build/finish the HTML page
def endHTML():
    print """
</body>
</HTML>"""
