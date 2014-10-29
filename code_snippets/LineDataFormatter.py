# Open file that has the list of EDU numbers
input_file = open("C:\\_Python26\\_mycode\\ForTom\\EDU_Numbers.txt",'r')

# Create file that will contain partial SQL statements
output_file = open("C:\\_Python26\\_mycode\\ForTom\\output.txt",'w')

# Now read the 1st row / EDU number and strip out any possible blank/white spaces
first_row = input_file.readline().strip()

# Format the 1st row / EDU number and format it with SQL statements
first_row_formatted = "desc_text like '%" + first_row + "%'"

# Write to the output file
output_file.write(first_row_formatted + "\n")

# Now process the rest of the EDU numbers until you reach end of file (EOF)
while True:
    line = input_file.readline()
    if not line:  # If line is not a line, then you must've reached EOF
        break
    else:
        line = line.strip()
        line_formated = "or desc_text like '%" + line + "%'"
        output_file.write(line_formated + "\n")


input_file.close()
output_file.close()
