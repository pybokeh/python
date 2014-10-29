from pandas import *
import matplotlib.pyplot as plt
import urllib2
from matplotlib.dates import date2num, MonthLocator, WeekdayLocator, DateFormatter
from datetime import date, datetime

# csv_file = urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=HMC&a=11&b=1&c=2011&d=0&e=1&f=2012&g=d&ignore=.csv')
df = read_csv('/home/pybokeh/Desktop/Key_Keyless_SymptomClass.csv', header=0)

# Print just the first 3 rows of data
print "Printing just the first 3 rows of data..."
print df[:3]
print "\n"

# Print just the last 3 rows of data
print "Printing just the last 3 rows of data..."
print df[-3:]
print "\n"

# Print all of the data
# print "Prining all of the data"
# print df.to_string()
# print "\n"

# Print the mean for each year
print "Printing the mean for each year..."
print df.groupby(['MODEL_YEAR'])['MILES_TO_FAIL'].mean()
print "\n"

# Print multiple groupbys
print "Printing means by multiple groups"
print df.groupby(['MODEL_YEAR','FACTORY_CODE','MODEL_NAME'])['MILES_TO_FAIL'].mean()
print "\n"

# Print the mean for a specific year
print "Printing the mean for just year=2008..."
print df[df['MODEL_YEAR']==2008]['MILES_TO_FAIL'].mean()
print "\n"

# Print the MTF values where YEAR=2009
print "Printing MTF where YEAR=2009"
print df[df['MODEL_YEAR']==2009]['MILES_TO_FAIL']

n, bins, patches = plt.hist(df[df['MODEL_YEAR']==2008]['MILES_TO_FAIL'].values, 10, normed=False, cumulative=False, facecolor='green', alpha=1)
n, bins, patches = plt.hist(df[df['MODEL_YEAR']==2009]['MILES_TO_FAIL'].values, 10, normed=False, cumulative=False, facecolor='red', alpha=1)
plt.show()
