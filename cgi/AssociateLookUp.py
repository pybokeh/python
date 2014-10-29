import cgi
import cgitb
import htmlbuilder
import sqlite3
cgitb.enable()

# Connect to the database
conn = sqlite3.connect(r"d:\tomcat\webapps\python\WEB-INF\db\HAM_DB")
cursor = conn.cursor()

# Get form variables and their values
form = cgi.FieldStorage()

# Check to see which input values are available, then process accordingly
if form.has_key('lastName'):
    lastName = form.getvalue('lastName')
    # The HR_ASSOCIATES table stores last names as upper case only
    lastName = lastName.upper()
    sql_QueryLastName = "select * from HR_ASSOCIATES where LAST_NAME_SRCH like '%" + lastName + "%'"
    cursor.execute(sql_QueryLastName)
else:
    value = form.getvalue('assocNo')
    # To use SQL prepared statement, we need to pass a tuple-so create a tuple now
    assocNo = (value,)
    sql_QueryAssocNo = "select * from HR_ASSOCIATES where EMPLID = ?"
    # Now that we have the sql and the tuple, we're ready to pass them to the excute method
    cursor.execute(sql_QueryAssocNo, assocNo)

# Get column name of the resultset
column_name_list = [tuple[0] for tuple in cursor.description]

# Now create the response HTML page containing the resultset of the query
htmlbuilder.beginHTML("HAM Associate Lookup")
htmlbuilder.createHtmlTable(column_name_list,cursor)
htmlbuilder.endHTML()
    
cursor.close()
