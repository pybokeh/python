#  NOTE: xlrd module must be installed

import pandas as pandas
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import scikits.statsmodels.tools.tools as tools
import numpy as np

# Open the Excel file
xls = pandas.ExcelFile('/home/pybokeh/Desktop/35400_07-12M.xls')
# Parse the specific Excel sheet name
df = xls.parse('Claims')

CRV_09 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='ELP') & (df['MODEL_NAME']=='CRV')]['MILES_TO_FAIL'].values
TL_09 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='MAP') & (df['MODEL_NAME']=='TL')]['MILES_TO_FAIL'].values

fig1 = plt.figure(1)
current_axis = plt.gca()
current_axis.set_yticklabels(['CRV'])
plt.boxplot(CRV_09, vert=0)
plt.grid(True)
plt.xlabel("MTF", fontsize=8)
plt.title("Boxplot", fontsize=12)


fig2 = plt.figure(2)
n, bins, patches = plt.hist(CRV_09, 120, normed=False, cumulative=False, facecolor='red', alpha=1)
plt.xlabel("MTF", fontsize=8)
plt.ylabel("Frequency", fontsize=8)
plt.title("ELP CRV MTF Histogram", fontsize=10)
plt.grid(True)


plt.show()
