from pandas import *
import matplotlib.pyplot as plt
import urllib2
from matplotlib.dates import date2num, MonthLocator, WeekdayLocator, DateFormatter
from datetime import date, datetime

# csv_file = urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?s=HMC&a=11&b=1&c=2011&d=0&e=1&f=2012&g=d&ignore=.csv')
df = read_csv('/home/pybokeh/Desktop/Key_Keyless_SymptomClass.csv', header=0)

n, bins, patches = plt.hist(df[df['MODEL_YEAR']==2008]['MILES_TO_FAIL'].values, 10, normed=False, cumulative=False, facecolor='green', alpha=1)
n, bins, patches = plt.hist(df[df['MODEL_YEAR']==2009]['MILES_TO_FAIL'].values, 10, normed=False, cumulative=False, facecolor='red', alpha=1)
plt.show()
