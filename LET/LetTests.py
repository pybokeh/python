from bs4 import BeautifulSoup                         # Module to parse XML files
import pyodbc                                         # Module to connect to ODBC data sources
import base64                                         # Module to decode my password
import os                                             # Module to work with the computer's OS properties
from datetime import datetime                         # Module to work with date/datetime objects
import datetime as dt                                 # Module to perform date calculations
import re                                             # Module to access regex functions
import shutil
import tarfile
import time

def getVehBuildDate(txtVIN):
    """Method that returns the vehicle production date"""

    # Get password and "de-fuzzy" it
    pw_file = open(r'D:\webapps\_server\pyodbc\cmq.txt', 'r')
    pw = base64.b64decode(pw_file.read())
    userid = 'rb10'
    pw_file.close()

    cnxn_string = 'DSN=CMQ_PROD;UID=' + userid + ';PWD=' + pw
    
    cnxn = pyodbc.connect(cnxn_string)

    cursor = cnxn.cursor()

    sql = """
SELECT
date(AF_CAL.CAL_DT) as AFOFFDT

FROM CMQ.V_FACT_VHCL_PRDN_SLS PROD

INNER JOIN CMQ.V_DIM_DATE AF_CAL
ON PROD.AF_ON_DT_SK = AF_CAL.CAL_DT_SK

WHERE
PROD.VIN_NO = ?"""

    cursor.execute(sql, txtVIN)
    cnxn.commit()

    resultset = cursor.fetchone()

    afoffdt = resultset[0]

    cursor.close()

    return str(afoffdt)

def getLetDrive(txtVIN):
    """Method that returns the base LET drive path"""
    MAP_DRIVE = "\\\\naslet01p\\mapdata\\"
    ELP_DRIVE = "\\\\naslet01p\\elpdata\\"
    HMA_DRIVE = "\\\\hma1nas1\\let_xml\\"
    HMI_DRIVE = "\\\\hminnas\\Hmin_nas_galc_let\\Hmin\\Let\\result_xml\\"

    factory_code = txtVIN[10:11]

    if factory_code == 'A':
        return MAP_DRIVE
    elif factory_code == 'L':
        return ELP_DRIVE
    elif factory_code == 'B':
        return HMA_DRIVE
    elif factory_code == 'E':
        return HMI_DRIVE
    else:
        return 'N/A'


def getVinFeatures(txtVIN):
    # Do not get data from Core MQ server between 9pm and 7am
    while datetime.now().hour > 18 and datetime.now().hour < 07:
        print "Can not run during Core MQ's nightly job.  So I am sleeping now..."
        time.sleep(3600) #Time is in seconds, sleep for one hour each time

    # Get password and "de-fuzzy" it
    pw_file = open(r'D:\webapps\_server\pyodbc\cmq.txt', 'r')
    pw = base64.b64decode(pw_file.read())
    userid = 'rb10'
    pw_file.close()

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
        print "There was an error in your SQL"

    resultset = cursor.fetchone()

    # Close connections
    cursor.close()
    cnxn.close()
    
    return resultset

def hasTar(dir):
    """ Created this method and its companion method (extractTar) because HMIN IS has started to tar zip their LET XML files.
        Other plants may follow suit."""

    file_list = []
    tar_file = ''

    for path, subdirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".xml") or file.endswith(".xmls.tar.gz"):
                file_list.append(os.path.join(path, file))

    test = False
    for tar in file_list:
        if tar.endswith("tar.gz") == True:
            test = True
            print "Tar file found:", tar
            tar_file = tar
        
    if test == False:
        print "Tar file was not found"

    if tar_file != '':
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
    print "Finished extracting tar file"
    return

def getXmlFiles(vin, base, afoffdt):    
    """Method that returns a list containing XML files for that specific VIN.
    Since the VIN may not always get its LET data read on the day it is built,
    it will search 3 days' worth of LET data beginning with the VIN's build date.
    As a consequence of this, the method may not return the XML files if the VIN
    was built just before a long shutdown.  This method should work 90% of the time.
    You can manually set the afoffdt/start date when this method returns no XML files."""

    print "VIN:", vin
    print "Vehicle AF On date:", afoffdt

    # To take advantage of built-in date functions, need to convert the string afoffdt into an actual date object
    actual_date = datetime.strptime(afoffdt, '%Y-%m-%d').date() # Parse the afoffdt into a date object
    stop_date = actual_date + dt.timedelta(days=2)

    xml_file_list = []
    final_file_list = []

    while actual_date < stop_date:
        strDate = str(actual_date) # Convert date into a string so I can substring it below
        print "LET date: ", strDate

        # Concatenate base LET drive path with the year, year-month, and year-month-day
        dir = base + strDate[:4] + '\\' + strDate[:4]+strDate[5:7] + '\\' + strDate[:4]+strDate[5:7]+strDate[-2:] + '\\'

        # Utilize os.walk() method to search inside a directory - it is awesome!
        for path, subdirs, files in os.walk(dir):
            print 'Digging in: ' + path

            for name in files:
                if name.endswith(".xml") and vin in name: # Get only XML files for that VIN
                    print "Adding XML file:", os.path.join(path,name)
                    xml_file_list.append(os.path.join(path, name)) # then add them to the xml list (full path+filename)
                elif name.endswith(".xmls.tar.gz"):
                    xml_file_list.append(os.path.join(path, name))

        tar_file, test = hasTar(dir)
        if test == True:
            print "Creating tempdata folder if it does not already exist"
            if not os.path.exists("tempdata"):
                os.makedirs("tempdata")

            print "Extracting tar file into tempdata folder:", tar_file
            extractTar(tar_file)
        else:
            pass

        actual_date = actual_date + dt.timedelta(days=1)  # Increment the date or else you'll have an infinite loop!

    for path, subdirs, files in os.walk("tempdata"):
        print 'Digging in: ' + path

        for name in files:
            if name.endswith(".xml") and vin in name: # Get only XML files for that VIN
                print "Adding XML file:", os.path.join(path, name)
                final_file_list.append(os.path.join(path, name))

    # if tar file was found, then replace xml_file_list with the list containing uzipped files
    if test == True:
        xml_file_list = list(final_file_list) # Now make xml_file_list contain a copy of final_file_list
                                                  # because that is what this method needs to return.
                                                  # xml_file_list = final_file_list is NOT the right way to copy a list!

    return xml_file_list

def print_tpms_id(file):
    """Prints the TPMS sensor IDs"""
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the TPMS_READ test Where the result was Pass
    process = soup.find("test",test="TPMS_READ",status="Pass")
    
    #Some judgements in ELP are a PASS, but really the sensor ID's are not inside
    #This is a value check to make sure that SENSID's are inside the process
    if not process == None and not (process.find(param=re.compile("SENSID.*")) == None) :
        #No need to format time, SQL will to that
        #time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
        time = process['testtime']

        print "TPMS Sensor IDs:"
        for sensor in ["SENSID1","SENSID2","SENSID3","SENSID4"]:                    
            #Some LET tests record append on (FR,FL,RR,RL) to the SENSID# use regular expression to still resolve the ID
            ID = process.find(param=re.compile(sensor + ".*"))['val']
            
            print vin, sensor, ID, time

    return


def print_12vb_check(file):
    """Prints all the 12vb_Check parameters"""
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))

    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return

    #Set the VIN
    vin = soup.unit_in_test['vin']

    #Look through the file and find the HEV_BATT_VB tests Where the result was Pass
    tests = ["12VB_CHECK_01","12VB_CHECK_02","12VB_CHECK_03","12VB_CHECK_04","12VB_CHECK_05"]
    for iteration in tests:
        process = soup.find("test",test=iteration,status="Pass")

        #Pull in the Parameters of the test and store in the Parms table
        if not process == None and not (process.find('test_param') == None):
            testtime = process['testtime']
            params = process.find_all('test_param')

            if params.__len__() == 0 or params == None:
                print "No 12VB tests found"

            features     = getVinFeatures(vin)
            year         = features[0]
            factory      = features[1]
            model        = features[2]
            eng_cyl      = features[4]
            dest_cd      = features[8]

            for param in params:
                paramname = param.get('param', None)
                paramval  = param.get('val', None)
                paramunit = param.get('unit', None)

                print "VIN:", vin, "datTime:", testtime, "param:", paramname, "value:", paramval, "unit:", paramunit, "year:", year, "factory:", factory, "model:", model, "eng cyl:", eng_cyl, "dest:", dest_cd


def print_fcm_serial(file):
    """Prints the serial number of the FCM control unit"""

    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the TPMS_READ test Where the result was Pass
    process = soup.find("test",test="FCM_TRC_ABLTY",status="Pass")

    print "Scanning for FCM serial number in file:", file

    if process == None:
        print "No FCM serial number found"
    
    if not process == None and not (process.find(att='SUPPLIER_FCM_SERIAL') == None):
        fcm_serial = process.find(att='SUPPLIER_FCM_SERIAL')['val']
        print "FCM_Serial:", fcm_serial, "\n"


def print_fcm_check(file):
    """Prints all the parameter values in the FCM_CHECK test"""

    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    features     = getVinFeatures(vin)
    year         = features[0]
    factory      = features[1]
    model        = features[2]
    eng_cyl      = features[4]
    dest_cd      = features[8]

    #Look through the file and find the FCM_CHECK test Where the result was Pass
    process = soup.find("test",test="FCM_CHECK")

    print "Scanning for FCM_Check parameters in file:", file

    if process == None:
        print "No FCM_Check found\n"
        return
    elif process != None and process['status'] =='Pass':
        time = process['testtime']
        print "Status:", process['status']
        params = process.find_all('test_param')

        print "Printing FCM check parameters..."
        for param in params:
            paramname = param['param']
            paramval  = param['val']
            paramunit = param.get('unit', None) # A parameter may not have a 'Unit' attribute, so need to use the dict.get() method

            print "datTime:", time, "param:", paramname, "value:", paramval, "unit:", paramunit

        print "\n"
        return
    else:
        time = process['testtime']
        print "Status:", process['status']
        params = process.find_all('test_param')

        print "Printing FCM check parameters..."

        for param in params:
            paramname = param['param']
            paramval  = param['val']
            paramunit = param.get('unit', None) # A parameter may not have a 'Unit' attribute, so need to use the dict.get() method

            print "datTime:", time, "param:", paramname, "value:", paramval, "unit:", paramunit

        codes = process.find_all('fault_code')
        if codes == []:
            print "No fault codes found"

        for code in codes:
            fault_code = code['faultcode']
            fault_desc = code['shortdesc']

            print "LET test date-time:", time
            print "Fault Code:", fault_code
            print "Fault short description:", fault_desc, "\n"
        return


def print_fcm_angles(file):
    """Prints the FCM camera angles"""
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the FCM_CHECK test
    process = soup.find("test",test="FCM_CHECK")

    print "Scanning for FCM angles in file:", file

    if process == None:
        print "No FCM CHECK angles found\n"
        return
    elif process != None and process['status'] =='Pass':
        time = process['testtime']
        pitch = process.find(param="Pitch")['val']
        roll  = process.find(param="Roll")['val']
        yaw   = process.find(param="Yaw")['val']

        print "Status:", process['status']
        print "LET test date-time:", time
        print "pitch:", pitch
        print "roll:", roll
        print "yaw:", yaw, "\n"
        return
    else:
        print "No camera angles recorded - error occurred"
        print "Status:", process['status']

        time = process['testtime']
        codes = process.find_all('fault_code')

        if codes == []:
            print "No fault codes found"

        for code in codes:
            fault_code = code['faultcode']
            fault_desc = code['shortdesc']

            print "LET test date-time:", time
            print "Fault Code:", fault_code
            print "Fault short description:", fault_desc, "\n"

        return

def print_fcm_clear(file):
    """Prints any available FCM fault codes"""
    
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the FCM_CLEAR test Where the result was Pass
    process = soup.find("test",test="FCM_CLEAR")

    print "Scanning for FCM fault codes in file:", file

    if process == None:
        print "No FCM fault codes found\n"
    
    #This is a check to make sure that the test existed in the fist place
    if not process == None:
        time = process['testtime']

        codes = process.find_all('fault_code')

        if codes == []:
            print "No fault codes found"

        for code in codes:
            fault_code = code['faultcode']
            fault_desc = code['shortdesc']

            print "LET test date-time:", time
            print "LET XML file:", file
            print "Fault Code:", fault_code
            print "Fault short description:", fault_desc, "\n"


def print_lwc_angles(file):
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
        time = process['testtime']

        pitch = process.find(param="Pitch_OFFSET")['val']
        roll  = process.find(param="Roll_OFFSET")['val']
        yaw   = process.find(param="Yaw_OFFSET")['val']
        
        print "LET test date-time:", time
        print "LET XML file:", file
        print "pitch:", pitch
        print "roll:", roll
        print "yaw:", yaw, "\n"


def print_acc_radar_angles(file):
    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    features     = getVinFeatures(vin)
    year         = features[0]
    factory      = features[1]
    model        = features[2]
    eng_cyl      = features[4]
    dest_cd      = features[8]

    #print "VIN:", vin, "YEAR:", year, "FACTORY:", factory, "MODEL:", model, "ENG CYL:", eng_cyl, "DEST CD:", dest_cd

    #Look through the file and find the ACC-related tests where the result was Pass
    acc_serial = soup.find("test", test="ACC_TRC_ABLTY", status="Pass")
    acc_fixture_aim = soup.find("test",test="ACC_FIXTURE_AIM",status="Pass")
    acc_check = soup.find("test",test="ACC_CHECK",status="Pass")

    if not acc_serial == None and not(acc_serial.find('test_attribute') == None):
        acc_serial_testtime = acc_serial['testtime']
        acc_serial_no = acc_serial.find("test_attribute", att="SUPPLIER_ACC_SERIAL")['val']

        print "\n"
        print "ACC serial #:", acc_serial_no, "test time:", acc_serial_testtime
    
    if not acc_fixture_aim == None and not (acc_fixture_aim.find('test_param') == None):
        acc_fixture_aim_testtime = acc_fixture_aim['testtime']
        vert_aim = acc_fixture_aim.find("test_param", param="Final Radar Deg")['val']

        print "\n"
        print "Final vertical aim (deg):", vert_aim, "test time:", acc_fixture_aim_testtime

    if not acc_check == None and not (acc_check.find('test_param') == None):
        acc_check_testtime = acc_check['testtime']
        horizontal_aim = acc_check.find("test_param", param="Adj Radar Deg")['val']

        print "\n"
        print "Final horizontal aim (deg):", horizontal_aim, "test time:", acc_check_testtime


def print_bsi_serial(file):
    """Prints the serial number of the blind spot indicator unit"""

    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))
    
    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return
    
    #Set the VIN
    vin = soup.unit_in_test['vin']
    
    #Look through the file and find the BSI_TRC_ABLTY test Where the result was Pass
    process = soup.find("test",test="BSI_TRC_ABLTY",status="Pass")
    
    if not process == None and not (process.find(att='SUPPLIER_BSI_SERIAL') == None):
        bsi_serial = process.find(att='SUPPLIER_BSI_SERIAL')['val']
        time = process['testtime']

        print "LET test date-time:", time
        print "LET XML file:", file
        print "BSI Serial:", bsi_serial, "\n"

def print_audio_serial(file):
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------

    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))

    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return

    #Set the VIN
    vin = soup.unit_in_test['vin']

    processes = soup.findAll("test",test=re.compile("AUDIO_SERIAL_STORE|AUDIO_TRC_ABLTY"),status="Pass")

    print "Scanning for audio serial in file:", file

    if processes == None or processes == []:
        print "No audio unit serial # found"

    for process in processes:
        if process.find(att='SUPPLIER_AUDIO_SERIAL') != None:
            time = process['testtime']
            ID = process.find(att='SUPPLIER_AUDIO_SERIAL')['val']
            print "Audio serial #:", ID
            print "testtime:", time
