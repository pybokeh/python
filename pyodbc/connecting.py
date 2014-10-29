import pyodbc as pyodbc
cnxn = pyodbc.connect('DSN=CMQ_PROD;UID=myUserID;PWD=myPassword')
cursor = cnxn.cursor()
cursor.execute("SELECT MDL_YR, FCTRY_CD, MDL_NM FROM CMQ.V_DIM_MTO_FEATURE_PIVOT WHERE MDL_YR = 2012")
row = cursor.fetchone()
if row:
   print row