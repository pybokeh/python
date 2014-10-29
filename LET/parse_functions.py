from bs4 import BeautifulSoup	#Used to process the XML formatted data
from datetime import datetime	#Used to calculate current times and increment dates
from decimal import *			#Used to perform calculations on % Complete
import time						#Used to have a system wait command during closed SQL hours
import parse_functions as pf	#Since many of the functions call others on this page I import itseld so all commands are available all the time
import os						#Used to traverse directories
import pyodbc					#Used to connect to the ODBC datasources to fetch and insert data
import sys						#??
import re						#Used to implement regular expressions in the code
import pdb						#Used to kick off debugging in the applicaiton
import shutil					#Used to move files
import tarfile                  #Used to extract tar files

def traverse(dir):	
	#-----------------------------------------------------------------------------------------------
	#
	#-----------------------------------------------------------------------------------------------
	
	tree = []
	
	for path, subdirs, files in os.walk(dir):
		
		print 'Digging in: ' + path

		for i, name in enumerate(files):
			#clear = '\x08'*40
			#print clear + str("%.8f" % round((Decimal(i) / Decimal(len(files))*100),8)) + "% Complete       ",
			if name.endswith(".xml"):
				tree.append(os.path.join(path, name))
	return tree

def date_dir(dir,dates):
	#-----------------------------------------------------------------------------------------------
	#
	#-----------------------------------------------------------------------------------------------
	
	pattern = re.compile("[0-9]{8}")
	for path, subdirs, files in os.walk(dir):
		for dir in subdirs:
			if pattern.match(dir) != None:
				dates.append(os.path.join(path,dir))
				print os.path.join(path,dir)
			else:
				dates = pf.date_dir(path + '\\' + dir,dates)
		return dates
	return dates
	
def xml_load(module,files,date):
	#-----------------------------------------------------------------------------------------------
	#xml_load([Module to Load],[Files To Check])
	#-----------------------------------------------------------------------------------------------
	
	#2012-05-02 Found some files in HMIN share that are empty and throw exceptions, added checking for non-empty files -JB-
	for i, file in enumerate(files):		
		if module == 'tpms_id' and os.path.getsize(file) > 0:
			load_tpms_id(file)
		elif module == 'batt_soc_orig' and os.path.getsize(file) > 0:
			load_batt_soc_orig(file)
		elif module == 'radio_serial' and os.path.getsize(file) > 0:
			load_radio_serial(file)
		elif module == 'ipu_cells' and os.path.getsize(file) > 0:
			load_IPU_cells(file)
		elif module == 'imid_serial' and os.path.getsize(file) > 0:
			load_iMID_serial(file)
		elif module == '12vb_check' and os.path.getsize(file) > 0:
			load_12vb_check(file)
		elif module == 'ant_db' and os.path.getsize(file)> 0:
			load_ant_db(file)
			#TEMP Command for a local process of Ant_DB data
			shutil.move(file,"D:\\2010_ANT_DB_DONE")
		clear = '\x08'*40  # This is hex respresentation of backspace character times 40
		print clear + str("%.8f" % round((Decimal(i) / Decimal(len(files))*100),8)) + "% Complete       ",
	
	clear = '\x08'*40
	print clear,
	return 1

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
        print "No tar file found"

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

def load_tpms_id(file):
	#-----------------------------------------------------------------------------------------------
	#
	#-----------------------------------------------------------------------------------------------
	
	#Open the file with Beautiful Soup
	soup = BeautifulSoup(open(file))
	
	#2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
	if soup.findAll('unit_in_test') == []: return
	
	#Set the VIN
	vin = soup.unit_in_test['vin']
	
	#Look up the Destination
	dest = fetch_market(vin)
	
	#Look through the file and find the TPMS_READ test Where the result was Pass
	process = soup.find("test",test="TPMS_READ",status="Pass")
	
	#Some judgements in ELP are a PASS, but really the sensor ID's are not inside
	#This is a value check to make sure that SENSID's are inside the process
	if not process == None and not (process.find(param=re.compile("SENSID.*")) == None) :
		#No need to format time, SQL will to that
		#time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
		time = process['testtime']
		my = vin[9:10]
		model = vin[3:5]
		plant = vin[10:11] 
		for sensor in iter(["SENSID1","SENSID2","SENSID3","SENSID4"]):					
			#Some LET tests record append on (FR,FL,RR,RL) to the SENSID# use regular expression to still resolve the ID
			ID = process.find(param=re.compile(sensor + ".*"))['val']
			
			LET = connect('LET')
			#Insert the values into the table, if there is a dup go ahead and continue
			try:
				LET.execute("insert into tpms_id(txtvin,txtvariable,txtvalue,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?)",vin,sensor,ID,time,my,model,plant,dest)
			except (pyodbc.IntegrityError):
				pass
			LET.close()
			
	return

def load_radio_serial(file):
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------

    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))

    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return

    #Set the VIN
    vin = soup.unit_in_test['vin']

    #Look up the Destination
    dest = fetch_market(vin)

    processes = soup.findAll("test",test=re.compile("AUDIO_SERIAL_STORE|AUDIO_TRC_ABLTY"),status="Pass")

    if processes == None or processes == []:
        return

    for process in processes:
        if not process == None and not (process.find(att='SUPPLIER_AUDIO_SERIAL') == None):
            #No need to format time, SQL will to that
            #time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
            time = process['testtime']
            my = vin[9:10]
            model = vin[3:5]
            plant = vin[10:11] 

            ID = process.find(att='SUPPLIER_AUDIO_SERIAL')['val']

            LET = connect('LET')
            #Insert the values into the table, if there is a dup go ahead and continue
            try:
                LET.execute("insert into radio_serial(txtvin,txtvariable,txtvalue,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?)",vin,'AUDIO_SERIAL',ID,time,my,model,plant,dest)
            except (pyodbc.IntegrityError):
                pass	
            LET.close()

    return

def load_batt_soc_orig(file):
	#-----------------------------------------------------------------------------------------------
	#
	#-----------------------------------------------------------------------------------------------
	
	#Open the file with Beautiful Soup
	soup = BeautifulSoup(open(file))
	
	#2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
	if soup.findAll('unit_in_test') == []: return
	
	#Set the VIN
	vin = soup.unit_in_test['vin']
	
	#Look up the Destination
	dest = fetch_market(vin)
	my = vin[9:10]
	model = vin[3:5]
	plant = vin[10:11] 
		
	#Look through the file and find the AUDIO_SERIAL_STORE test Where the result was Pass
	process = soup.find("test",test=re.compile(".*BATTERY_SOC.*"),status="Pass")
	
	if not process == None and not (process.find(param=re.compile('(?!MIN).*SOC')) == None) :
		#No need to format time, SQL will to that
		#time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
		time = process['testtime']
		
		soc = process.find(param=re.compile('(?!MIN).*SOC'))['val']
		minsoc = process.find(param=re.compile('(?!MIN).*SOC'))['lolimit']
		
		LET = connect('LET')
		#Insert the values into the table, if there is a dup go ahead and continue
		try:
			LET.execute("insert into battery_soc(txtvin,txtvariable,txtvalue,txtmin,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?,?)",vin,'Calculated SOC',soc,minsoc,time,my,model,plant,dest)
		except (pyodbc.IntegrityError):
			pass	
		LET.close()
		
	return

def load_IPU_cells(file):
    #-----------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------

    #Open the file with Beautiful Soup
    soup = BeautifulSoup(open(file))

    #2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []: return

    #Set the VIN
    vin = soup.unit_in_test['vin'].strip() #IPU Cell data (before VIN install) has leading chars in the string 2012-05-24

    if vin == '' or vin == None: # Found out HMIN's XML file can have an empty VIN
        return

    my = vin[9:10]
    model = vin[3:5]
    plant = vin[10:11]

    #Look up the Destination
    dest = fetch_market(vin)

    #Look through the file and find the HEV_BATT_VB tests Where the result was Pass
    tests = ["HEV_BATT_VB_01","HEV_BATT_VB_02","HEV_BATT_VB_03","IPU_BATT_VOLTAGE"]
    for iteration in tests:
        process = soup.find("test",test=iteration,status="Pass")

        #Pull in the attributes of the test
        if not process == None and not (process.find(param=re.compile("VBC.*")) == None) :
	
            testtime = process['testtime']

            #Set the number of iterations for the number of Cells recorded
            cells = process.find_all(att=re.compile("VBC.*"))

            for cell in cells:
                cellname = cell['att']
                cellv    = cell['val']

                #Insert the values into the table, if there is a dup go ahead and continue
                try:
                    connect('LET').execute("insert into ipu_cells_attr(txtVIN,txtTest,txtAttr,txtValue,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?,?)",vin,iteration,cellname,cellv,testtime,my,model,plant,dest)
                except (pyodbc.IntegrityError):
                    pass
        #Pull in the Parameters of the test and store in the Parms table
        if not process == None and not (process.find('test_param') == None):
	
            testtime = process['testtime']

            params = process.find_all('test_param')

            for param in params:
                paramname = param.get('param', None)
                paramval  = param.get('val', None)
                paramunit = param.get('unit', None)
				#paramhi   = param.get('hilimit', None)
				#paramlo   = param.get('lolimit', None)

                LET = connect('LET')
                try:
                    LET.execute("insert into ipu_cells_param(txtVIN,txtTest,txtparam,txtparamval,txtparamunit,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?,?,?)",vin,iteration,paramname,paramval,paramunit,testtime,my,model,plant,dest)
                except (pyodbc.IntegrityError):
                    pass
                LET.close()

        #time.sleep(0.35)		
    return

def load_12vb_check(file):
	#-----------------------------------------------------------------------------------------------
	#
	#-----------------------------------------------------------------------------------------------
	
	#Open the file with Beautiful Soup
	soup = BeautifulSoup(open(file))
	
	#2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
	if soup.findAll('unit_in_test') == []: return
	
	#Set the VIN
	vin = soup.unit_in_test['vin']
	my = vin[9:10]
	model = vin[3:5]
	plant = vin[10:11]

	#Look up the Destination
	dest = fetch_market(vin)
	
	#Look through the file and find the HEV_BATT_VB tests Where the result was Pass
	tests = ["12VB_CHECK_01","12VB_CHECK_02","12VB_CHECK_03","12VB_CHECK_04","12VB_CHECK_05"]
	for iteration in tests:
		process = soup.find("test",test=iteration,status="Pass")
		
		#Pull in the attributes of the test
		if not process == None and not (process.find('test_attribute') == None) :
			
			testtime = process['testtime']
			
			#Fetch all the test attrs
			attrs = process.find_all('test_attribute')
			
			for attr in attrs:
				attribute  = attr['att']
				attrval    = attr['val']
				
				#Insert the values into the table, if there is a dup go ahead and continue
				try:
					connect('LET').execute("insert into 12vb_check_attr(txtVIN,txtTest,txtAttr,txtValue,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?,?)",vin,iteration,attribute,attrval,testtime,my,model,plant,dest)
				except (pyodbc.IntegrityError):
					pass
		#Pull in the Parameters of the test and store in the Parms table
		if not process == None and not (process.find('test_param') == None):
			params = process.find_all('test_param')

			for param in params:
				paramname = param.get('param', None)
				paramval  = param.get('val', None)
				paramunit = param.get('unit', None)
				#paramhi   = param.get('hilimit', None)
				#paramlo   = param.get('lolimit', None)
				
				LET = connect('LET')
				try:
					LET.execute("insert into 12vb_check_param(txtVIN,txtTest,txtparam,txtparamval,txtparamunit,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?,?,?)",vin,iteration,paramname,paramval,paramunit,testtime,my,model,plant,dest)
				except (pyodbc.IntegrityError):
					pass
				LET.close()
		#time.sleep(0.35)		
	return

def load_ant_db (file):
	#-----------------------------------------------------------------------------------------------
	#
	#-----------------------------------------------------------------------------------------------
	
	#Open the file with Beautiful Soup
	soup = BeautifulSoup(open(file))
	
	#2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
	if soup.findAll('unit_in_test') == []: return
	
	#Set the VIN
	vin = soup.unit_in_test['vin']
	my = vin[9:10]
	model = vin[3:5]
	plant = vin[10:11]

	#Look up the Destination
	dest = fetch_market(vin)
	
	#pdb.set_trace()
	
	#Look through the file and find the Reception tests where the result was Pass
	tests = ["FM_RADIO_ANT","AM_RADIO_ANT"]
	for iteration in tests:
		process = soup.find("test",test=iteration,status="Pass")
		
		#Pull in the attributes of the test
		if not process == None and not (process.find('test_attribute') == None) :
			
			testtime = process['testtime']
			
			#Fetch all the test attrs
			attrs = process.find_all('test_attribute')
			
			for attr in attrs:
				attribute  = attr['att']
				attrval    = attr['val']
				
				#Insert the values into the table, if there is a dup go ahead and continue
				try:
					connect('LET').execute("insert into ant_db_attr(txtVIN,txtTest,txtAttr,txtValue,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?,?)",vin,iteration,attribute,attrval,testtime,my,model,plant,dest)
				except (pyodbc.IntegrityError):
					pass
		#Pull in the Parameters of the test and store in the Parms table
		if not process == None and not (process.find('test_param') == None):
			params = process.find_all('test_param')

			for param in params:
				paramname = param.get('param', None)
				paramval  = param.get('val', None)
				paramunit = param.get('unit', None)
				paramhi   = param.get('hilimit', None)
				paramlo   = param.get('lolimit', None)
				
				LET = connect('LET')				
				try:
					LET.execute("insert into ant_db_param(txtVIN,txtTest,txtparam,txtparamval,txtparamunit,paramhi,paramlo,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?,?,?,?,?)",vin,iteration,paramname,paramval,paramunit,paramhi,paramlo,testtime,my,model,plant,dest)
				except (pyodbc.IntegrityError):
					pass
				LET.close()
				
		#time.sleep(0.1)		
	return

def load_iMID_serial (file):
	#-----------------------------------------------------------------------------------------------
	#
	#-----------------------------------------------------------------------------------------------
	
	#Open the file with Beautiful Soup
	soup = BeautifulSoup(open(file))

	#2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
	if soup.findAll('unit_in_test') == []: return
	
	#Set the VIN
	vin = soup.unit_in_test['vin']
	my = vin[9:10]
	model = vin[3:5]
	plant = vin[10:11]

	#Look up the Destination
	dest = fetch_market(vin)
	
	#Look through the file and find the HEV_BATT_VB tests Where the result was Pass
	tests = ["I_MID_TRC_ABLTY"]
	for iteration in tests:
		
		process = soup.find("test",test=iteration,status="Pass")
		
		if not process == None and not (process.find(att=re.compile('HM_I_MID_SERIAL')) == None):
			
			time = process['testtime']
			
			himid = process.find(att=re.compile('HM_I_MID_SERIAL'))['val']
			simid = process.find(att=re.compile('SUPPLIER_I_MID_SERIAL'))['val']
			
			LET = connect('LET')
			#Insert the values into the table, if there is a dup go ahead and continue
			try:
				LET.execute("insert into imid_serial(txtVIN,txtTest,dattime,hm_imid_serial,sup_imid_serial,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?,?)",vin,'I_MID_TRC_ABLTY',time,himid,simid,my,model,plant,dest)
			except (pyodbc.IntegrityError):
				pass
			LET.close()
	return

def load_fcw_serial(file):
    # Open file with Beautiful Soup
    soup = BeautifulSoup(open(file))

    # 2012-05-02 Found some files in HMIN share that are malformed and throw exceptions, this should work around this -JB-
    if soup.findAll('unit_in_test') == []:
        return

    # Set the VIN
    vin = soup.unit_in_test['vin']

    # Look up the Destination
    dest = fetch_market(vin)

    # Look through the file and find the "FCM_TRC_ABLTY" test Where the result was Pass
    process = soup.find("test",test=re.compile("FCM_TRC_ABLTY"),status="Pass")

    # Need to validate that the process does not have a fault code
    if not process == None and not (process.find(att='SUPPLIER_FCM_SERIAL') == None):
        #No need to format time, SQL will to that
		#time = datetime.strptime(process['testtime'],"%Y-%m-%dT%H:%M:%S")
        time = process['testtime']
        my = vin[9:10]
        model = vin[3:5]
        plant = vin[10:11]

        ID = process.find(att='SUPPLIER_FCM_SERIAL')['val']

        LET = connect('LET')

        # Insert the values into the table, if there is a dup go ahead and continue
        try:
            LET.execute("insert into fcw_serial(txtvin,txtvariable,txtvalue,dattime,txtmy,txtmodel,txtplant,txtdest) values (?,?,?,?,?,?,?,?)",vin,'FCW_SERIAL',ID,time,my,model,plant,dest)
        except(pyodbc.IntegrityError):
            pass
    
    return

	
def fetch_market(vin):
    #-----------------------------------------------------------------------------------------------
    #This function will return the destination market, if none found it will return and empty string
    #-----------------------------------------------------------------------------------------------

    #Check to make sure it is not between Midnight and 7:00AM (These are CLOSED times for SQL)
    while datetime.now().hour > 00 and datetime.now().hour < 07:
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

def connect(database):
	#-----------------------------------------------------------------------------------------------
	#	Connects to specified DSN database and returns a cursor to that database
	#-----------------------------------------------------------------------------------------------
	
	cnxn = pyodbc.connect('DSN='+database)
	cursor = cnxn.cursor()
	return cursor

def test_odbc(database):
	#-----------------------------------------------------------------------------------------------
	#   Tests connection to the specified database, the name passed is the ODBC name in Windows
	#-----------------------------------------------------------------------------------------------
	
	try: pyodbc.connect('DSN='+database)
	except:
		return 0
	return 1
	
def test_connections():
	#-----------------------------------------------------------------------------------------------
	#   Check to make sure that the user has correct connection rights to the needed databases to
	#   run the application
	#-----------------------------------------------------------------------------------------------
	
	print "Testing connection to MySQL LET: ",
	print "",
	#Need to test availability of the LET Database
	if (pf.test_odbc("LET") == 1):
		print "OK"
	else:
		print "FAILED"
		sys.exit("Could not connect to LET database")
	print ""
	print "Testing connection to SQL: ",
	print "",
	#Need to test availability of the SQL Warranty database
	if (pf.test_odbc("mmp-sqlp-warranty") == 1):
		print "OK"
	else:
		print "FAILED"
		sys.exit("Could not connect to SQL database")
	print ""
