import os
import os.path
import time
from sys import exit

input_path = raw_input("Enter path: ")

# Check to see if user entered the last backslash
if input_path[len(input_path)-1] != '\\':
    input_path = input_path + '\\'

if os.path.isdir(input_path):
    pass
else:
    print "You did not enter a valid directory, exiting now..."
    time.sleep(1)
    exit()

output_flag = raw_input("Do you want to export to a text file?(y/n): ")
if output_flag == "y" or output_flag == "Y":
    outfile_name = raw_input("Enter file name: ")
    outfile = open(outfile_name,'w')
    dir_contents = os.listdir(input_path)
    for item in dir_contents:
        if os.path.isfile(input_path + item):
            outfile.write(item+"\n")
    print "Your file was created at this location: " + os.getcwd()
    outfile.close()

elif output_flag == "n" or output_flag == "N":
    dir_contents = os.listdir(input_path)
    for item in dir_contents:
        if os.path.isfile(input_path + item):
            print item

else:
    pass