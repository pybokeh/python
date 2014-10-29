#  NOTE: xlrd module must be installed

import pandas as pandas
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

# Open the Excel file
xls = pandas.ExcelFile(r'\\mapfile01\aqg\mq\group\DOBD\Scorecard data\Jun - 2012 data\10M TL 42753.xls')
# Parse the specific Excel sheet name
df = xls.parse('Leak')

TL2009 = df[(df['MODEL_YEAR']==2009) & (df['MODEL_NAME']=='TL')]['MILES_TO_FAIL'].values
TL2010 = df[(df['MODEL_YEAR']==2010) & (df['MODEL_NAME']=='TL')]['MILES_TO_FAIL'].values
TL2011 = df[(df['MODEL_YEAR']==2011) & (df['MODEL_NAME']=='TL')]['MILES_TO_FAIL'].values

# Make a boxplot figure
fig1 = plt.figure(1, facecolor="white")
plt.subplot(1,1,1, axisbg='#cdc9c9')
ax = plt.gca()
ax.set_yticklabels(['2009 TL', '2010 TL', '2011 TL'])
plt.boxplot([TL2009, TL2010, TL2011], vert=0)
major_ticks = MultipleLocator(10000)
minor_ticks = MultipleLocator(1000)
ax.xaxis.set_major_locator(major_ticks)
ax.xaxis.set_minor_locator(minor_ticks)
ax.xaxis.grid(which='major', linestyle='-', linewidth=2)
ax.xaxis.grid(which='minor', linestyle='-.', linewidth=1)
plt.title("2009 TL TPMS Sensor Claims With Leak Contentions")
plt.xlabel("Miles To Fail")

plt.show()
