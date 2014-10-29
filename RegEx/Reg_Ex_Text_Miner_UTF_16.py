# This script only works if the input file is ANSI/ASCII text.  It will not work if it is UTF-16
# If the input file is UTF-16, then use codecs module: codecs.open(myFile,mode='r',encoding='UTF-16')

import re   # import the regular expressions package
import codecs

# Enter the regular expression pattern here:
pattern = re.compile("[tT][oO][nN][eE][rR]")

input_file = codecs.open("d:\\_python26\\_mycode\\regex\\InputFile.txt",mode='r',encoding="UTF-16") # Open this file for read access only
output_file = open("d:\\_python26\\_mycode\\regex\\output.txt",'w') # Open/create this file for write access only

first_row = input_file.readline().strip().encode("ASCII","replace")  # strip() removes any possible "white" spaces, carriage returns, or newlines

# Get the number of commas in the the header row so that when we read in the data which may include text fields that
# can contain commas, we don't accidentally create too many columns when doing the split() method below
num_commas = first_row.count(",")

column_name = first_row+",\"MiningResult\""

output_file.write(column_name+"\n")

column_names_list = first_row.split(",")

while input_file:
    # strip() removes any possible "white" spaces, carriage returns, or newlines at the beginning or end of the input line
    line = input_file.readline().strip().encode("ASCII","replace")
    
    if line == "":   # If we reach EOF, then stop the while loop
        break
 
    else:
        # Now create a Python list containing the data elements separated by a comma.  num_commas ensures that we have
        # same number of columns as the header row
        row_data = line.split(",",num_commas)

        search_column = row_data[column_names_list.index("\"IncidentDescription\"")]

        out_string = str(row_data)
        
        # Since row_data/out_string is a Python list containing strings, there will be brackets and single quotes.
        # Therefore, need to remove the left/right brackets, any single quotes or back slashes.
        out_string = out_string.replace("[",'').replace("]",'').replace("'",'').replace("\\",'')
        
        # str() adds a space between the comma and double quote
        # which can cause problems when importing into certain applications (, ") -> (,")
        out_string = out_string.replace(", \"",",\"")
        
        # test to see if the search column has the pattern we're looking for
        test = pattern.search(search_column)

        if test:
            output_file.write(out_string+",\"Match found\""+"\n")
        else:
            output_file.write(out_string+",\"\""+"\n")

print "Text miner has completed its process."
input_file.close()
output_file.close()
