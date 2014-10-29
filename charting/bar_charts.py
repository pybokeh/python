import matplotlib.pyplot as plt
import numpy as np
import urllib2


# http_proxy enironment variable needs to be created first = http://username:password@proxyserver:proxyport
proxy = urllib2.ProxyHandler()
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

# Grab the source CSV file directly from the US census website
input_file = urllib2.urlopen('http://www.census.gov/popest/data/national/totals/2011/files/NST_EST2011_ALLDATA.csv')

first_row = input_file.readline().strip()
column_names_list = first_row.split(",")

col_value      = column_names_list.index("CENSUS2010POP")
col_name       = column_names_list.index("NAME")
is_state_col   = column_names_list.index("STATE")

pop_dict = {}

while input_file:
    row = input_file.readline().strip()
    row_data_list = row.split(",")
    if row == "":
        break
    else:
        if row_data_list[is_state_col] == '0':
            pass
        else:
            value          = int(row_data_list[col_value])/1e6
            name           = row_data_list[col_name]
            pop_dict[name] = value 
    
input_file.close()

# Since we can't actually sort a dictionary, instead, create a list of tuples such as...
# [(key1, value1), (key2, value2), ... (key_n, value_n)] and sort it by value desc
pop_tuple_by_value = sorted(pop_dict.items(), key=lambda x: x[1], reverse=True)

"""
print "Creating a list of tuples, sorted by key ascending..."
pop_tuple_by_key = sorted(pop_dict.items(), key=lambda x: x[0])
print pop_tuple_by_key"""


# Now store the state names and their respective population values in separate lists
state_name = []
state_pop  = []

for key,value in pop_tuple_by_value:
    state_name.append(key)
    state_pop.append(value)


# But we just want the top 10 states
top10_state_name = []
top10_state_pop  = []

for i in range(10):
    top10_state_name.append(state_name[i])
    top10_state_pop.append(state_pop[i])

# For horizontal bar chart, if you want longer bars to be shown at top, need to reverse the lists
top10_state_name.reverse()
top10_state_pop.reverse()

# horizontal bar chart
fig = plt.figure(1)
plt.barh(range(len(top10_state_name)), top10_state_pop, align='center')
#xlim(0,int(max(cens2000pop_data)+2))
plt.xlim(0,int(max(top10_state_pop)+2))
plt.xticks(np.arange(int(max(top10_state_pop)+2)), rotation=90, size='small')
plt.yticks(np.arange(len(top10_state_name)), top10_state_name)
plt.title('Top 10 US States By Population')
plt.xlabel("Population in Millions")
plt.ylabel("State Name")
plt.axis('auto')
plt.grid(True)
plt.show()


"""
# vertical bar chart
figure(1)
bar(range(len(top10_state_name)), top10_state_pop, align='center')
#xlim(0,int(max(cens2000pop_data)+2))
ylim(0,int(max(top10_state_pop)+2))
yticks(arange(int(max(top10_state_pop)+2)))
xticks(arange(len(top10_state_name)), top10_state_name)
title('Top 10 US States By Population')
xlabel("State Name")
ylabel("Population in Millions")
#axis('auto')
grid()"""


