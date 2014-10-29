import os
import sys
import let_functions as lf
import shutil
import sqlite3
import datetime as dt

class LET(object):
    def __init__(self, db_path_name):
        """Get the database path and name"""
        self.db_path_name = db_path_name

    def getConnection(self):
        """Method that connects to the database specified by the __init__() method"""
        try:
            self.conn = sqlite3.connect(self.db_path_name)
            print("Successfully connected to the database.")
        except:
            print("Failed to connect to the database.  Please check the path to the database.")
            sys.exit()
        
    def close(self):
        """Closes the database connection."""
        try:
            print("Closing connection...")
            self.conn.close()
            print("Successfully closed connection to the database.")
        except:
            print("Failed to close connection to the database.")

    def processLetFiles(self):
        """Gets the XML files then invokes the insertLetData() method"""
        stopdt = dt.date.today() - dt.timedelta(days=2)

        sql = """
        SELECT
        datLastRun,
        txtFactory
        
        FROM let_tests
        
        WHERE datLastRun < \'""" + str(stopdt) + "'" + " and flag = \'True\' GROUP BY datLastRun,txtFactory"
        
        self.cursor = self.conn.cursor()
        print("Executing SQL:\n"+sql)
        resultset = self.cursor.execute(sql).fetchall()
        
        for row in resultset:
            self.datLastRun = dt.datetime.strptime(row[0], "%Y-%m-%d").date()
            self.plant = row[1]
            while self.datLastRun < stopdt:
                base = self.cursor.execute('SELECT txtpath FROM let_paths WHERE txtplant = \''+ self.plant +'\'').fetchone()
                dir = base[0] + self.datLastRun.strftime("%Y") + '\\' + self.datLastRun.strftime("%Y%m") + '\\' + self.datLastRun.strftime("%Y%m%d") + '\\'
                #in order to speed up the data loading, we are going to copy the dir to the local dir tempdata while the update
                #is running, upon completion this will clear out this directory.

			    #testing
                print("Date last run: " + str(self.datLastRun))
                print("Factory: " + self.plant)
                print("Dir: " + dir)

                #Need to ensure that the loacl path is present before deleteing
                if os.access("tempdata", os.F_OK):
                    print("Removing tempdata directory...")
                    shutil.rmtree("tempdata")
                #Need to ensure that the remote path is present before copying
                if os.access(dir, os.F_OK):
                    print("Copying network data to tempdata folder for local processing...")
                    shutil.copytree(dir,"tempdata")

                # Because HMIN IS has started to tar zip their XML files, added this logic to handle tar files
                tar_file, test = lf.hasTar(dir)

                if test == True:
                    for file in tar_file:
                        print("Extracting tar file:", file)
                        lf.extractTar(file)
                else:
                    pass

                self.insertLetData(self.datLastRun, self.plant)

                self.datLastRun = self.datLastRun + dt.timedelta(days=1)

        return

    def insertLetData(self, date, plant):
        """Inserts the LET records into the sqlite3 database."""
        result = self.cursor.execute('SELECT * FROM let_tests WHERE datLastRun =\''+ str(date) + '\' AND txtfactory = \''+ plant +'\'').fetchall()

        for test in result:
            txtModule  = test[0]
            txtDate = test[1]
            txtFactory = test[2]
            #Run the update module for that test until the date is today -2
            print()
            print("----------------------------------------------------------")
            print("Loading: "+ txtModule)
            print("From: " + txtFactory)
            print("Date: " + txtDate)
            print("----------------------------------------------------------")

            #Only traverse tempdata if the path is present
            if os.access("tempdata", os.F_OK):
                files = lf.getXmlFiles("tempdata")
                lf.xml_load(test[0],files,test[1], self.conn)
            #If there is no data to traverse, alert the user. This is likely due to no production on that day
            else:
                print("No files present to load")

            #Update the LET tracking file to show that the directory has been traversed.
            date_run = dt.datetime.strptime(test[1], "%Y-%m-%d").date()
            date_run = date_run + dt.timedelta(days=1)
            self.cursor.execute('UPDATE let_tests SET datLastRun = \''+ str(date_run) +'\' WHERE txtModule = \''+ txtModule + '\' AND txtFactory = \''+ txtFactory + '\'')
            self.conn.commit()  # UPDATE or INSERT to a database requires that you commit those changes in order for those changes to take affect

        return
