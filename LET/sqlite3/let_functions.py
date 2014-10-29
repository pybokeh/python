from bs4 import BeautifulSoup    #Used to process the XML formatted data
from datetime import datetime    #Used to calculate current times and increment dates
import time                        #Used to have a system wait command during closed SQL hours
import let_functions as lf    #Since many of the functions call others on this page I import itseld so all commands are available all the time
import os                        #Used to traverse directories
import pyodbc                    #Used to connect to the ODBC datasources to fetch and insert data
import sys                        #??
import re                        #Used to implement regular expressions in the code
import pdb                        #Used to kick off debugging in the applicaiton
import shutil                    #Used to move files
import sqlite3                   # Needed to access Sqlite3 database
import base64                    # Needed to de-fuzzy password
import tarfile

def getXmlFiles(dir):    
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------
    
    xml_file_list = []
    
    for path, subdirs, files in os.walk(dir):
        
        print('Digging in: ' + path)

        for i, name in enumerate(files):
            if name.endswith(".xml"):
                xml_file_list.append(os.path.join(path, name))

    return xml_file_list

    
def xml_load(module,files,date,conn):
    #-----------------------------------------------------------------------------------------------
    #xml_load([Module to Load],[Files To Check])
    #-----------------------------------------------------------------------------------------------
    
    #2012-05-02 Found some files in HMIN share that are empty and throw exceptions, added checking for non-empty files -JB-
    i = 1
    for file in files:        
        if module == 'lwc_angle' and os.path.getsize(file) > 0:
            load_lwc_angles(file, conn)
        elif module == 'fcm_angle' and os.path.getsize(file) > 0:
            load_fcm_angles(file, conn)        
        elif module == '12vb_check' and os.path.getsize(file) > 0:
            load_12vb_check(file, conn)
        elif module == 'tpms_id' and os.path.getsize(file) > 0:
            load_tpms_id(file, conn)
        elif module == 'fcm_serial' and os.path.getsize(file) > 0:
            load_fcm_serial(file, conn)
        # This print function prints real-time status of how many files were processed and also shows percent completed
        print("%.4f%% complete," % float((i*1.0000) / len(files)*100) + " file: " + str(i) + " of " + str(len(files)) + " | Time stamp:" + str(datetime.now()),"\r",end="")
        i = i + 1
    
    print("\n")

    return 

def hasTar(dir):
    """ Created this method and its companion method (extractTar) because HMIN IS has started to tar zip their LET XML files.
        Other plants may follow suit."""

    file_list = []
    tar_file = []

    for path, subdirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".xml") or file.endswith(".gz"):
                file_list.append(os.path.join(path, file))

    test = False
    for tar in file_list:
        if tar.endswith(".gz") == True:
            test = True
            print("Tar file found:", tar)
            tar_file.append(tar)
        
    if test == False:
        print("No tar file found")

    if tar_file.__len__() != 0:
        return tar_file, test
    else:
        return "No XML or tar files found", False

def extractTar(tar_file):
    """ This method extracts the tar zipped LET files to the tempdata folder using the tarfile module.
        The api doc for tarfile indicates that you can use the extractall() method, but I think there is a bug
        in which the path= flag does not work if the zipped file names include a path.
        As a workaround, I stripped the path from the file names by looping through members of the
        tar file, then execute the extract() method.
        Possible related bugs: http://bugs.python.org/issue10761 and http://bugs.python.org/issue12088"""

    tfile = tarfile.open(tar_file, 'r')
    tar_members = tfile.getmembers()
    for tar_member in tar_members:
        tar_member.name = os.path.basename(tar_member.name)  # Strip out the path and keep just the file name
        tfile.extract(tar_member, path="tempdata/")
    tfile.close()
    print("Finished extracting tar file")
    return

def load_tpms_id(file, conn):
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file),"lxml")
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look up the Destination
    #dest = fetch_market(vin)
    
    LET = conn.cursor()
    #Look through the file and find the TPMS_READ test Where the result was Pass
    process = soup.find("test",test="TPMS_READ",status="Pass")
    
    #Some judgements in ELP are a PASS, but really the sensor ID's are not inside
    #This is a value check to make sure that SENSID's are inside the process
    if not process == None and not (process.find(param=re.compile("SENSID.*")) == None) :
        #No need to format time, SQL will to that
        #time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
        time = process['testtime']
        #my = vin[9:10]
        #model = vin[3:5]
        #plant = vin[10:11] 

        for sensor in ["SENSID1","SENSID2","SENSID3","SENSID4"]:                    
            #Some LET tests record append on (FR,FL,RR,RL) to the SENSID# use regular expression to still resolve the ID
            ID = process.find(param=re.compile(sensor + ".*"))['val']
         
            #conn = sqlite3.connect(r'D:\webapps\tpms\server\db\tpms')
            #LET = conn.cursor()

            #Insert the values into the table, if there is a dup go ahead and continue
            try:
                LET.execute("insert into tpms_id(txtvin,txtvariable,txtvalue,dattime) values (?,?,?,?)",(vin,sensor,ID,time))
            except (sqlite3.IntegrityError):
                pass

            conn.commit()
    LET.close()
            
    return

def load_anc_serial(file, conn):
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the ASC_TRC_ABLTY test Where the result was Pass
    process = soup.find("test",test="ASC_TRC_ABLTY",status="Pass")
    
    #This is a check to make sure that HM_ASC_SERIAL is valid
    if not process == None and not (process.find(att=re.compile("HM_ASC_SERIAL")) == None) :
        #No need to format time, SQL will to that
        #time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
        time = process['testtime']
        my = vin[9:10]
        model = vin[3:5]
        plant = vin[10:11] 

        ID = process.find(att=re.compile("HM_ASC_SERIAL"))['val']
         
        conn = sqlite3.connect(r'd:\webapps\denso\server\db\denso')
        LET = conn.cursor()

        #Insert the values into the table, if there is a dup go ahead and continue
        try:
            LET.execute("insert into anc_serial(txtvin,txtvariable,txtvalue,dattime,txtmy,txtmodel,txtplant) values (?,?,?,?,?,?,?)",(vin,"ANC_SERIAL",ID,time,my,model,plant))
        except (sqlite3.IntegrityError):
            pass

        conn.commit()
        LET.close()
        conn.close()
            
    return

def load_lwc_angles(file, conn):
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the ASC_TRC_ABLTY test Where the result was Pass
    process = soup.find("test",test="LANEWATCH_CHECK",status="Pass")
    
    #This is a check to make sure that HM_ASC_SERIAL is valid
    if not process == None and not (process.find('test_attribute') == None):
        #No need to format time, SQL will to that
        #time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
        time = process['testtime']
        my = vin[9:10]
        model = vin[3:5]
        plant = vin[10:11] 

        pitch = process.find(param="Pitch_OFFSET")['val']
        roll  = process.find(param="Roll_OFFSET")['val']
        yaw   = process.find(param="Yaw_OFFSET")['val']
         
        conn = sqlite3.connect(r'd:\webapps\denso\server\db\denso')
        LET = conn.cursor()

        #Insert the values into the table, if there is a dup go ahead and continue
        try:
            LET.execute("insert into lane_watch(txtvin,pitch_offset,roll_offset,yaw_offset,dattime,txtmy,txtmodel,txtplant) values (?,?,?,?,?,?,?,?)",(vin,pitch,roll,yaw,time,my,model,plant))
        except (sqlite3.IntegrityError):
            pass

        conn.commit()
        LET.close()
        conn.close()
            
    return


def load_fcm_angles(file, conn):
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the ASC_TRC_ABLTY test Where the result was Pass
    process = soup.find("test",test="FCM_CHECK",status="Pass")
    
    #This is a check to make sure that HM_ASC_SERIAL is valid
    if not process == None and not (process.find('test_attribute') == None):
        #No need to format time, SQL will to that
        #time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
        time = process['testtime']
        my = vin[9:10]
        model = vin[3:5]
        plant = vin[10:11] 

        pitch = process.find(param="Pitch")['val']
        roll  = process.find(param="Roll")['val']
        yaw   = process.find(param="Yaw")['val']
         
        conn = sqlite3.connect(r'd:\webapps\denso\server\db\denso')
        LET = conn.cursor()

        #Insert the values into the table, if there is a dup go ahead and continue
        try:
            LET.execute("insert into fcm_camera(txtvin,pitch,roll,yaw,dattime,txtmy,txtmodel,txtplant) values (?,?,?,?,?,?,?,?)",(vin,pitch,roll,yaw,time,my,model,plant))
        except (sqlite3.IntegrityError):
            pass

        conn.commit()
        LET.close()
        conn.close()
            
    return

def load_12vb_check(file, conn):
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))

    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return

    #Set the VIN and its features
    vin = soup.unit_in_test['vin']
    features = getVinFeatures(vin)
    year         = features[0]
    factory      = features[1]
    model        = features[2]
    eng_cyl      = features[4]
    dest_cd      = features[8]    

    conn = sqlite3.connect(r'd:\webapps\denso\server\db\denso')
    LET = conn.cursor()    

    #Look through the file and find the HEV_BATT_VB tests Where the result was Pass
    tests = ["12VB_CHECK_01","12VB_CHECK_02","12VB_CHECK_03","12VB_CHECK_04","12VB_CHECK_05"]
    for iteration in tests:
        process = soup.find("test",test=iteration,status="Pass")

        #Pull in the Parameters of the test and store in the Parms table
        if not process == None and not (process.find('test_param') == None):
            testtime = process['testtime']
            params = process.find_all('test_param')

            for param in params:
                paramname = param.get('param', None)
                paramval  = param.get('val', None)
                paramunit = param.get('unit', None)

                try:
                    LET.execute("insert into vb_check_param(txtVIN,txtTest,txtparam,txtparamval,txtparamunit,dattime,mdl_yr,fctry_cd,mdl_nm,eng_cyl,dest_cd) values (?,?,?,?,?,?,?,?,?,?,?)",(vin,iteration,paramname,paramval,paramunit,testtime,year,factory,model,eng_cyl,dest_cd))
                except (sqlite3.IntegrityError):
                    pass
                conn.commit()

    LET.close()
    conn.close()                
    return


def fetch_market(vin):
	#-----------------------------------------------------------------------------------------------
	#This function will return the destination market, if none found it will return and empty string
	#-----------------------------------------------------------------------------------------------
	
	#Check to make sure it is not between Midnight and 7:00AM (These are CLOSED times for SQL)
	while datetime.now().hour > 0 and datetime.now().hour < 7:
		time.sleep(3600) #Time is in seconds, sleep for one hour each time
		
	where = ("WHERE " + 
					" VIN_MANU_CODE = '" + vin[0:2] + "' AND " + 
					" VIN_CAR_TYPE = '" + vin[2:3] + "' AND " + 
					" VIN_MODEL_TYPE = '" + vin[3:5] + "' AND " + 
					" VIN_TRANS_TYPE = '" + vin[5:6] + "' AND " + 
					" VIN_NO_DOORS = '" + vin[6:7] + "' AND " + 
					" VIN_GRADE = '" + vin[7:8] + "' AND " + 
					" VIN_CHECK_NO = '" + vin[8:9] + "' AND " + 
					" VIN_MODEL_YR = '" + vin[9:10] + "' AND " + 
					" VIN_FACTORY = '" + vin[10:11] + "' AND " + 
					" VIN_SERIAL_NO = " + str(int(vin[11:17])))		
	
	WAR = connect('mmp-sqlp-warranty')
	#Run a lookup in SQL to check the destination market
	dest = WAR.execute("SELECT VEHICLE_DESTN_CODE FROM WAR.WRSAL1 " + where).fetchone()
	if dest == None:
		dest = ""
	else:
		dest = dest[0]
	WAR.close()
	
	return dest



def getVinFeatures(txtVIN):
    # Do not get data from Core MQ server between 9pm and 7am
    while datetime.now().hour > 20 or datetime.now().hour < 6:
        print("Can not run during Core MQ's nightly job.  So I am sleeping now...\n")
        time.sleep(3600) #Time is in seconds, sleep for one hour each time

    # Get password and "de-fuzzy" it
    #pw_file = open(r'D:\webapps\_server\pyodbc\cmq.txt', 'r')
    pw = base64.b64decode('I2RraW0wNyM=').decode('ascii')
    userid = 'rb10'
    #pw_file.close()

    cnxn_string = 'DSN=CMQ_PROD;UID=' + userid + ';PWD=' + pw

    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()

    sql = """
SELECT
FEATURES.MDL_YR,
FEATURES.FCTRY_CD,
FEATURES.MDL_NM,
FEATURES."DOORS",
FEATURES."ENGINE CYLINDERS",
FEATURES."TRANSMISSION",
FEATURES."GRADE SHORT",
FEATURES."GRADE LONG",
FEATURES.DEST_CD

FROM CMQ.V_FACT_VHCL_PRDN_SLS PROD

INNER JOIN CMQ.V_DIM_MTO_FEATURE_PIVOT FEATURES
ON PROD.MTO_SK = FEATURES.MTO_SK

WHERE
PROD.VIN_NO = ?
"""

    try:
        cursor.execute(sql, txtVIN)
    except:
        print("There was an error in your SQL")

    resultset = cursor.fetchone()

    # Close connections
    cursor.close()
    cnxn.close()
    
    return resultset

def load_fcm_serial(file, conn):
    """Obtains the serial number of the FCM control unit"""

    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file), "lxml")
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the TPMS_READ test Where the result was Pass
    process = soup.find("test",test="FCM_TRC_ABLTY",status="Pass")

    LET = conn.cursor()    

    if not process == None and not (process.find(att='SUPPLIER_FCM_SERIAL') == None):
        fcm_serial = process.find(att='SUPPLIER_FCM_SERIAL')['val']
        time = process['testtime']
        try:
            LET.execute("insert into fcm_serial(txtVIN,txtSerial,datTime) values (?,?,?)",(vin,fcm_serial,time))
        except (sqlite3.IntegrityError):
            pass
        conn.commit()

    LET.close()
    return
