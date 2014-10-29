#from bs4 import BeautifulSoup
import os
import sys
import re
import parse_functions as pf
import pdb
import datetime as dt
import shutil
import sqlite3

#APPLICATION Requirements
#	3 Parameters are passed in [UPDATE or PATH] ([MODULE NAME]) ([PATH TO TRAVERSE])
#	
#	UPDATE 
#		parameter will ignore the other flags of [MODULE NAME] and [PATH TO TRAVERSE]
#
#	PATH
#		parameter requires both [MODULE NAME] and [PATH TO TRAVERSE]

invsyntx = "Invalid Syntax: parse ['update' or 'path'] (MODULE NAME) (PATH TO TRAVERSE)"

print "-----------------------"
print "| LET Update Database |"
print "-----------------------"
print ""

#Test the connections before proceeding
pf.test_connections()

#Output actions to be performed
if len(sys.argv)>1:
	if sys.argv[1] == "update":
		#Go ahead with a general update crawl
		action = "update"
		#sys.exit("UPDATE METHOD NOT IMPLEMENTED YET")
	elif sys.argv[1] == "path":
		#Specific data load chosen need to check following args to ensure valid
		#Function accepts two required parameters [Moduel Name] [Directory to traverse]
		if (len(sys.argv) == 4):
			module=sys.argv[2]
			dir=sys.argv[3]
			action = "path"
		else:
			sys.exit(invsyntx)
	else:
		sys.exit(invsyntx)
else:
	sys.exit(invsyntx)


#Perform a general update on the trackable modules
if action == "update":
    #Need to go fetch a list of updates to run
    #Select * from let_tests where date last ran < today -2 => Insert results into an array
    stopdt = dt.date.today() - dt.timedelta(days=2)
    conn = sqlite3.connect(r'd:\webapps\denso\server\db\denso')
    let = conn.cursor()
    #Find the date folders to copy locally to speed up
    lastrun = let.execute('SELECT datLastRun, txtFactory FROM let_tests WHERE datLastRun <\''+ str(stopdt) + '\' and flag = \'True\' GROUP BY datLastRun,txtFactory').fetchall()

    for row in lastrun:
        datLastRun = dt.datetime.strptime(row[0], "%Y-%m-%d").date()
        plant = row[1]
        while datLastRun < stopdt:
            base = let.execute('SELECT txtpath FROM let_paths WHERE txtplant = \''+ plant +'\'').fetchone()
            dir = base[0] + datLastRun.strftime("%Y") + '\\' + datLastRun.strftime("%Y%m") + '\\' + datLastRun.strftime("%Y%m%d") + '\\'
            #in order to speed up the data loading, we are going to copy the dir to the local dir tempdata while the update
            #is running, upon completion this will clear out this directory.

			#testing
            print "Date last run: " + str(datLastRun)
            print "Factory: " + plant
            print "Dir: " + dir

            #Need to ensure that the loacl path is present before deleteing
            if os.access("tempdata", os.F_OK):
                print "Removing tempdata directory..."
                shutil.rmtree("tempdata")
            #Need to ensure that the remote path is present before copying
            if os.access(dir, os.F_OK):
                print "Copying network data to tempdata for local processing..."
                shutil.copytree(dir,"tempdata")

            #Select Modules from the given date and plant that need to be executed
            result = let.execute('SELECT * FROM let_tests WHERE datLastRun =\''+ str(datLastRun) + '\' AND txtfactory = \''+ plant +'\'').fetchall()

            for test in result:
                txtModule  = test[0]
                txtDate = test[1]
                txtFactory = test[2]
                #Run the update module for that test until the date is today -2
                print ""
                print "----------------------------------------------------------"
                print "Loading: "+ txtModule
                print "From: " + txtFactory
                print "Date: " + txtDate
                print "----------------------------------------------------------"

                #Only traverse tempdata if the path is present
                if os.access("tempdata", os.F_OK):
                    files = pf.getXmlFiles("tempdata")
                    pf.xml_load(test[0],files,test[1])
                #If there is no data to traverse, alert the user. This is likely due to no production on that day
                else:
                    print "No files present to load"

                #Update the LET tracking file to show that the directory has been traversed.
                date_run = dt.datetime.strptime(test[1], "%Y-%m-%d").date()
                date_run = date_run + dt.timedelta(days=1)
                let.execute('UPDATE let_tests SET datLastRun = \''+ str(date_run) +'\' WHERE txtModule = \''+ txtModule + '\' AND txtFactory = \''+ txtFactory + '\'')
                conn.commit()  # When executing UPDATE or INSERT to a database, you must commit those changes in order for those changes to take affect

            datLastRun = datLastRun + dt.timedelta(days=1)
    conn.close()
    print "Finished updating LET database"


#Loading a specific path
elif action == "path":
    #Analyze the dir passed in from the command prompt

    pattern = re.compile("[2][0-9]{7}")
    date = pattern.search(dir)

    #Check to see if the directory is a specific date
    if date != None:
        #Only one date to load
        #Traverse the path given from the CLI
        print "Single date detected\nTraversing: " + dir
        files = pf.getXmlFiles(dir)
        clear = '\x08'*(len(dir)+1) 
        print clear + "COMPLETE                                   \n"

        #Collect the XML data desired
        print "Loading " + module + " from " + dir
        pf.xml_load(module,files,date)
        print "XML loaded"

    #If it is a range of dates we need to step through the dates to load
    else:
        files = pf.getXmlFiles(dir)
        pf.xml_load(module,files,date)

		#Need to step through the dirs
		#for folder in pf.date_dir(dir,[]):
		#	print "Single date detected\nTraversing: " + dir
		#	files = pf.getXmlFiles(folder)
		#	clear = '\x08'*(len(dir)+1) 
		#	print clear + "COMPLETE                                   \n"
		#	
		#	print "Loading " + module + " from " + folder
		#	pf.xml_load(module,folder,date)
			
			
# As of 2011 Here are known tracibility records that could be pulled from the LET Archive
# 	ABS_VSA_SERIAL_STORE
# 	AM_RADIO_ANT
# 	AUDIO_SERIAL_STORE		IMPLEMENTED 4/2012
# 	(NA_)BATTERY_SOC_CHECK	IMPLEMENTED 4/2012
# 	FI_SERIAL_STORE
# 	FM_RADIO_ANT
# 	MICU_SERIAL_STORE
# 	OPDS_SERIAL_STORE
# 	READ_AT_ECU_ID
# 	READ_FI_ECU_ID
# 	READ_VSA_ECU_ID
# 	SRS_SERIAL_STORE
# 	TPMS_SERIAL_STORE		IMPLEMENTED 4/2012
# 	EPS_SERIAL_STORE
# 	ESL_SERIAL_STORE
# 	PCU_SERIAL_STORE
# 	SMART_SERIAL_STORE
# 	AWD_SERIAL_STORE
			
			
			
			
			
			
			
			
			
			
			
			
			
			
