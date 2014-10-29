from pandas import *
import matplotlib.pyplot as plt
import urllib2
from matplotlib.dates import date2num, MonthLocator, WeekdayLocator, DateFormatter
from datetime import date, datetime

csv_file = urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=HMC&a=11&b=1&c=2011&d=0&e=1&f=2012&g=d&ignore=.csv')
df = read_csv('/home/pybokeh/Desktop/MTF.csv', header=0)

# Print the data frame in a user-friendly output
print df.to_string()

# Print the mean for each year
print "Printing the mean for each year..."
print df.groupby(['YEAR']).mean()
print "\n"

# Print the mean for a specific year
print "Printing the mean for just year=2000..."
print df[df['YEAR']==2000].mean()
print "\n"

print "Describing YEAR column..."
print df['YEAR'].describe()


"""
n, bins, patches = plt.hist(df['MTF'], 20, normed=False, cumulative=False, facecolor='green', alpha=1)
plt.show()
"""
