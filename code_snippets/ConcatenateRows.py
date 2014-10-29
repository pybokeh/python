"""
INPUT (CSV file):
QIS_ID, PART_NUM
QIS1, PART1
QIS1, PART2
QIS2, PART3
QIS2, PART4
QIS2, PART5

OUTPUT (CSV file):
QIS_ID, PART_NUM
QIS1, 'PART1' 'PART2'
QIS2, 'PART3' 'PART4' 'PART5'
"""

input_file = open('/home/pybokeh/Desktop/sample.csv','r')

first_row = input_file.readline()

line_list = []
while input_file:
    line = input_file.readline().strip()
    if line == '':
        break
    line_data = line.split(",")
    line_list.append(line_data)

input_file.close()

# This creates a dictionary containing the key and its respective unique values
# http://stackoverflow.com/questions/5378231/python-list-to-dictionary-multiple-values-per-key
d = {}
for key, val in line_list:
    d.setdefault(key, []).append(val)


print first_row
# Concatenate the row values into a single column
for key, values in d.iteritems():
    print key + "," + str(values).replace(",","").replace("[","").replace("]","")

"""
# Uncomment this section if you want to create the CSV file
final_output = open('/home/pybokeh/Desktop/output.csv','w')
final_output.write(first_row)
for key, values in d.iteritems():
    final_output.write(key + "," + str(values).replace(",","").replace("[","").replace("]","") + '\n')

final_output.close()
"""
