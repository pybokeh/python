# Must have xlrd module installed for ExcelFile to work

import pandas as pandas
import matplotlib.pyplot as plt
import scikits.statsmodels.tools.tools as tools
import numpy as np
from matplotlib.ticker import MultipleLocator

# Open the Excel file
xls = pandas.ExcelFile('/home/pybokeh/Desktop/08-12M_125517.xls')
# Parse the specific Excel sheet name
df = xls.parse('Claims')

pandas.set_printoptions(precision=6, max_columns=12)


acc2008 = df[ (df['MODEL_YEAR']==2008)
              & (df['MODEL_NAME']=='ACCORD')
              & (df['ENGINE_CYLINDERS']==4)
            ].groupby(['RO_YR_MTH'])['VIN'].count()
acc2009 = df[ (df['MODEL_YEAR']==2009)
              & (df['MODEL_NAME']=='ACCORD')
              & (df['ENGINE_CYLINDERS']==4)
            ].groupby(['RO_YR_MTH'])['VIN'].count()
acc2010 = df[ (df['MODEL_YEAR']==2010)
              & (df['MODEL_NAME']=='ACCORD')
              & (df['ENGINE_CYLINDERS']==4)
            ].groupby(['RO_YR_MTH'])['VIN'].count()
acc2011 = df[ (df['MODEL_YEAR']==2011)
              & (df['MODEL_NAME']=='ACCORD')
              & (df['ENGINE_CYLINDERS']==4)
            ].groupby(['RO_YR_MTH'])['VIN'].count()

d = {'2008':pandas.Series(acc2008.values, index=acc2008.index),
     '2009':pandas.Series(acc2009.values, index=acc2009.index),
     '2010':pandas.Series(acc2010.values, index=acc2010.index),
     '2011':pandas.Series(acc2011.values, index=acc2011.index),
    }

data = pandas.DataFrame(d)


major_ticks = MultipleLocator(20)
minor_ticks = MultipleLocator(10)

xv = np.arange(0,len(data.index),1)
plt.bar(xv, data['2008'].values, width=0.25, color='red', label='2008')
plt.bar(xv+0.25, data['2009'].values, width=0.25, color='blue', label='2009')
plt.bar(xv+0.5, data['2010'].values, width=0.25, color='yellow', label='2010')
plt.bar(xv+0.75, data['2011'].values, width=0.25, color='green', label='2011')
plt.xticks(xv+0.5, data.index, rotation=90, size='small')
ax = plt.gca()
ax.yaxis.set_major_locator(major_ticks)
ax.yaxis.set_minor_locator(minor_ticks)
ax.yaxis.grid(which='major', linestyle='-', linewidth=2)
ax.yaxis.grid(which='minor', linestyle=':', linewidth=1)
xtick_labels = ax.get_xticklabels()
for label in xtick_labels:
    label.set_fontsize(7)
plt.title('08-11M Accord L4 125517 Warranty')
plt.ylabel('Claim Qty')
plt.xlabel('RO Month')
plt.legend(loc='best')

plt.show()
