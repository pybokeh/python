#from bs4 import BeautifulSoup
import os
import sys
import re
import parse_functions as pf
import pdb
import datetime as dt
import shutil
import tarfile

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
    let = pf.connect('LET')
    #Find the date folders to copy locally to speed up
    dates2cp = let.execute('SELECT datLastRun, txtFactory FROM let_tests WHERE datLastRun <\''+ str(stopdt) + '\' and Flag = \'True\' GROUP BY datLastRun,txtFactory').fetchall()

    for date in dates2cp:
        while date[0] < stopdt:
            base = let.execute('SELECT txtpath FROM let_paths WHERE txtplant = \''+ date [1] +'\'').fetchone()
            dir = base[0] + date[0].strftime("%Y") + '\\' + date[0].strftime("%Y%m") + '\\' + date[0].strftime("%Y%m%d") + '\\'
            #in order to speed up the data loading, we are going to copy the dir to the local dir tempdata while the update
            #is running, upon completion this will clear out this directory.

            #testing
            print "Data Last Run: " + str(date[0])
            print "Factory: " + str(date[1])
            print "Dir: " + dir

            #Need to ensure that the loacl path is present before deleteing
            if os.access("tempdata", os.F_OK):
                print "Removing tempdata directory..."
                shutil.rmtree("tempdata")
            #Need to ensure that the remote path is present before copying
            if os.access(dir, os.F_OK):
                print "Copying netowrk data to tempdata for local processing..."
                shutil.copytree(dir,"tempdata")

            # Because HMIN IS has started to tar zip their XML files, added this logic to handle tar files
            tar_file, test = pf.hasTar(dir)

            if test == True:
                print "Extracting tar file:", tar_file
                pf.extractTar(tar_file)
            else:
                pass

            #Select Modules from the given date and plant that need run
            result = let.execute('SELECT * FROM let_tests WHERE datLastRun =\''+ str(date[0]) + '\' and Flag = \'True\' AND txtfactory = \''+ date [1] +'\' order by datLastRun').fetchall()

            for test in result:
                #Run the update module for that test until the date is today -2
                print ""
                print "----------------------------------------------------------"
                print "Loading: "+ test[0] 
                print "From: " + test[2]
                print "Date: " + str(test[1])
                print "----------------------------------------------------------"

                #while test[1] < stopdt:
                #Need to create the files array that we will load
                #base = let.execute('SELECT txtpath FROM let_paths WHERE txtplant = \''+ test [2] +'\'').fetchone()
                #Format is BASE\YYYY\YYYYMM\YYYYMMDD\ then traverse
                #dir = base[0] + test[1].strftime("%Y") + '\\' + test[1].strftime("%Y%m") + '\\' + test[1].strftime("%Y%m%d") + '\\'

                #Only traverse tempdata if the path is present
                if os.access("tempdata", os.F_OK):
                    files = pf.traverse("tempdata")
                    pf.xml_load(test[0],files,test[1])
                #If there is no data to traverse, alert the user. This is likely due to no production on that day
                else:
                    print "No files present to load"

                #Update the LET tracking file to show that the directory has been traversed.
                test[1] = test[1] + dt.timedelta(days=1)
                let.execute('UPDATE let_tests SET datLastRun = \''+ str(test[1]) +'\' WHERE txtModule = \''+ test[0] + '\' AND txtFactory = \''+ test[2] + '\'')

            date[0] = date[0]+ dt.timedelta(days=1)
    None


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
		files = pf.traverse(dir)
		clear = '\x08'*(len(dir)+1) 
		print clear + "COMPLETE                                   \n"
		
		#Collect the XML data desired
		print "Loading " + module + " from " + dir
		pf.xml_load(module,files,date)
		print "XML loaded"
		
	#If it is a range of dates we need to step through the dates to load
	else:
		files = pf.traverse(dir)
		pf.xml_load(module,files,date)
		
		
		#Need to step through the dirs
		#for folder in pf.date_dir(dir,[]):
		#	print "Single date detected\nTraversing: " + dir
		#	files = pf.traverse(folder)
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
