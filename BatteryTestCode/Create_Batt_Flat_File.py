# This script only works if the input file in encoded in ANSI/ASCII text file.  It will not work if file is UTF-16
# If the input file is UTF-16, then use codecs module: codecs.open(myFile,mode='r',encoding='UTF-16')

import BatteryCodeTranslator
input_file = open("d:\\_python26\\_mycode\\tblBatteryClaims.txt",'r') # Open this file for read access only
output_file = open("d:\\_python26\\_mycode\\output.txt",'w') # Open/create this file for write access only

# Process just the 1st row since it contains the column names of the original input file
first_row = input_file.readline().strip()  # strip() removes any possible "white" spaces, carriage returns, or newlines
first_row = first_row.replace('"','')      # remove any double-quotes in the column names

# column_names_list is used later on in the while clause.  It is being used so that it doesn't matter where the columns
# are located in the input file.  This script is flexible!  The input file just needs to be an ASCII, CSV file.
column_names_list = first_row.split(",")

# Now grab the column names from the input file and concatenate them with the new battery attributes column names
column_names = first_row
column_names = column_names+",BATT_BIN_CODE,BATT_TEST_TYPE,SW_VERSION,BATT_TYPE,BATT_VOLTAGE,BATT_RESULT,"+\
               "BATT_RATING,BATT_CAPACITY,TEST_TEMP,TEST_MONTH,TEST_DAY,TEST_CODE_JDGMNT,SOC,BATT_CATEGORY"

# For debugging purposes, print out the column names to the console, otherwise comment it out
# print column_names

# Write the first row/column names to the output file:
output_file.write(column_names+"\n")

# Now process the rest of the rows which should only contain column values until you reach EOF "End Of File"          
while input_file:
    line = input_file.readline().strip()
    line = line.replace('"','')
    line_parts = line.split(",") # create a Python list of row data whose data elements are separated by a comma
    if line == "":   # If we reach EOF, then stop execution of this script
        break
    else:
        # Now grab the 3 attributes we need to apply business logic from the input file.
        # This script was designed to be flexible, so it doesn't matter where the 3 columns are located in the input file,  
        # as long as their column names are spelled exactly as agreed upon.  Otherwise, this script will not work correctly!
        OEM_CCA = line_parts[column_names_list.index("OEM_CCA")]     
        SERVICE_CCA = line_parts[column_names_list.index("SERVICE_CCA")]    
        BATT_TEST_CODE = line_parts[column_names_list.index("BATT_TEST_CD")]  

        # Create the 12 battery attributes that can be derived from the binary battery code via battery code translator      
        BATT_BIN_CODE = BatteryCodeTranslator.batt2bin(BATT_TEST_CODE)
        BATT_TEST_TYPE = BatteryCodeTranslator.getTestType(BATT_BIN_CODE)
        SW_VERSION = BatteryCodeTranslator.getVersion(BATT_BIN_CODE)
        BATT_TYPE = BatteryCodeTranslator.getType(BATT_BIN_CODE)
        BATT_VOLTAGE = str(BatteryCodeTranslator.getVoltage(BATT_BIN_CODE))
        BATT_RESULT = str(BatteryCodeTranslator.getResult(BATT_BIN_CODE))
        BATT_RATING = str(BatteryCodeTranslator.getRating(BATT_BIN_CODE))
        BATT_CAPACITY = str(BatteryCodeTranslator.getCapacity(BATT_BIN_CODE))
        TEST_TEMP = str(BatteryCodeTranslator.getTemp(BATT_BIN_CODE))
        TEST_MONTH = str(BatteryCodeTranslator.getMonth(BATT_BIN_CODE))
        TEST_DAY = str(BatteryCodeTranslator.getDay(BATT_BIN_CODE))
        SOC = BatteryCodeTranslator.getSOC(BATT_BIN_CODE,BatteryCodeTranslator.getVoltage(BATT_BIN_CODE))

        # If the battery rating obtained from the battery test code is equal to the OEM CCA or service CCA, then it is a good test code
        # Otherwise, it is a bad test code
        if BATT_RATING == OEM_CCA or BATT_RATING == SERVICE_CCA:
            TEST_CODE_JDGMNT = "Good Test Code"
        else:
            TEST_CODE_JDGMNT = "Bad Test Code"

        # The following is the logic for how the battery category gets assigned:
        BATT_CATEGORY = ""
        if BATT_RESULT == "Bad Cell - Replace":
            BATT_CATEGORY = "Suspect Damaged Battery"
        elif BATT_RESULT == "Bad Test Code":
            BATT_CATEGORY = "Bad Test Code"
        elif SOC == "Bad Test Code":
            BATT_CATEGORY = "Bad Test Code"            
        elif SOC == "Discharged" and BATT_RESULT != "Bad Cell - Replace" and TEST_CODE_JDGMNT == "Good Test Code":
            BATT_CATEGORY = "Discharged"
        elif SOC == "Discharged" and BATT_RESULT != "Bad Cell - Replace" and TEST_CODE_JDGMNT == "Bad Test Code":
            BATT_CATEGORY = "Bad Test Code"            
        elif SOC == "Charged" and BATT_RESULT != "Bad Cell - Replace" and TEST_CODE_JDGMNT == "Bad Test Code":
            BATT_CATEGORY = "Bad Test Code"
        elif SOC == "Charged" and BATT_RESULT != "Bad Cell - Replace" and TEST_CODE_JDGMNT == "Good Test Code":
            if BatteryCodeTranslator.getCapacity(BATT_BIN_CODE) < 0.85 * BatteryCodeTranslator.getRating(BATT_BIN_CODE):
                BATT_CATEGORY = "EOL"
            else:
                BATT_CATEGORY = "NTF"
        
        # Create a Python list containing the row data
        out_string = str(line_parts)
        
        # Since line_parts is a Python list containing strings, there will be brackets and single quotes.
        # Therefore, need to remove the left/right brackets and any single quotes or blank spaces.
        out_string = out_string.replace("[",'').replace("]",'').replace(" ",'').replace("'",'')

        # Now we are ready to concatenate the original input file row data with the newly created battery attributes
        out_string = out_string+","+BATT_BIN_CODE+","+BATT_TEST_TYPE+","+SW_VERSION+","+BATT_TYPE+","+BATT_VOLTAGE+","+BATT_RESULT+","+\
                     BATT_RATING+","+BATT_CAPACITY+","+TEST_TEMP+","+TEST_MONTH+","+TEST_DAY+","+TEST_CODE_JDGMNT+","+SOC+","+BATT_CATEGORY

        # Then write it to the output / flat file
        output_file.write(out_string+"\n")

        # For debugging purposes, print row data to the console, otherwise comment it out
        # print out_string

print "Flat file creation complete!"

input_file.close()
output_file.close()
