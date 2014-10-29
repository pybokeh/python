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

mdl_yr   = form.getvalue('mdl_yr')
fctry_cd = form.getvalue('fctry_cd')
mdl_nm   = form.getvalue('mdl_nm')
part_no  = form.getvalue('part_no')

sql = """
SELECT
features.MDL_YR as MDL_YR,
features.FCTRY_CD as FCTRY_CD,
features.MDL_NM as MDL_NM,
features.GRADE_SHORT as GRADE_SHORT,
features.SEATS_LEATHER as SEATS_LEATHER,
part.txtPart as PART_NO,
part.txtSupplier as SUPPLIER,
part.txtDest_CD as DEST_CD

FROM tblApplicationMasterVERT part

INNER JOIN FEATURES features on
part.txtTEMP_MTC_Model = features.MTO_MDL_CD
and part.txtMTC_Type = features.MTO_TYP_CD

WHERE
features.MDL_YR = '""" + mdl_yr + "' and features.FCTRY_CD = '" + fctry_cd + "' and features.MDL_NM = '" + \
mdl_nm + "' and txtPart like '" + part_no + "%' ORDER BY SUPPLIER limit 500"

cursor.execute(sql)

# Get column name of the resultset
column_name_list = [tuple[0] for tuple in cursor.description]

# Now create the response HTML page containing the resultset of the query
htmlbuilder.beginHTML("Audio Part LookUp Results")
htmlbuilder.createHtmlTable(column_name_list,cursor)
htmlbuilder.endHTML()
    
cursor.close()
