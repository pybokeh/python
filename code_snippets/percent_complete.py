import os

file_list = []

for path, dir, files in os.walk('/usr/lib/python2.7'):
    for file in files:
        file_list.append(os.path.join(path,file))

print "Total number of files in the file list is: " + str(len(file_list))

i = 1
for file in file_list:
    # print "\r%.1f%% complete" % round((Decimal(i) / Decimal(len(file_list))*100),1),
    print "\r%.1f%% complete," % float((i*1.0) / len(file_list)*100), "file: " + str(i), "of " + str(len(file_list)),
    i = i + 1

# output should look like: '100.0000000% complete, file: 8042 of 8042

# For Python 3:
print('\r'+your_string,end='')
