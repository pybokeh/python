# OUTPUTS: 2 histograms by MTF and DTF

import pandas as pandas
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import scikits.statsmodels.tools.tools as tools
import numpy as np
from matplotlib.ticker import FormatStrFormatter, MultipleLocator

# Open the Excel file
xls = pandas.ExcelFile(r'D:\tomcat\webapps\DensoOBD\files\35400\08-12M HAM Door Jamb Switch.xls')
# Parse the specific Excel sheet name
df = xls.parse('Claims')

TL_2009_MTF = df[(df['MODEL_YEAR']==2009)
                 & (df['FACTORY_CODE']=='MAP')
                 & (df['MODEL_NAME']=='TL')
                 & (df['LOCATION']=='REAR')]['MILES_TO_FAIL'].values
TL_2009_DTF = df[(df['MODEL_YEAR']==2009)
                 & (df['FACTORY_CODE']=='MAP')
                 & (df['MODEL_NAME']=='TL')
                 & (df['LOCATION']=='REAR')]['DTF_MINZERO'].values


fig1 = plt.figure(1)
n, bins, patches = plt.hist(TL_2009_MTF, 15, normed=False, cumulative=False, facecolor='red', alpha=1)
ax = plt.gca()
ax.xaxis.set_ticks(bins, minor=False)
ax.xaxis.set_ticks(np.arange(0,84000,12000), minor=True)
plt.xticks(rotation=90)
major_tick_format = FormatStrFormatter('%d')
ax.xaxis.set_major_formatter(major_tick_format)
xtick_labels = ax.xaxis.get_ticklabels()
for label in xtick_labels:
    label.set_fontsize(8)
plt.xlabel("MTF")
plt.ylabel("Frequency")
plt.title("2009M TL Rear Door Jamb Switch MTF\n"+"Number of bins: " + str(len(bins)-1))
ax.xaxis.grid(which='major', linestyle='-', linewidth=1)
ax.yaxis.grid(which='major', linestyle='--')



fig2 = plt.figure(2)
n, bins, patches = plt.hist(TL_2009_DTF, 15, normed=False, cumulative=False, facecolor='red', alpha=1)
ax = plt.gca()
ax.xaxis.set_ticks(bins, minor=False)
plt.xticks(rotation=90)
major_tick_format = FormatStrFormatter('%d')
ax.xaxis.set_major_formatter(major_tick_format)
xtick_labels = ax.xaxis.get_ticklabels()
for label in xtick_labels:
    label.set_fontsize(8)
plt.xlabel("DTF")
plt.ylabel("Frequency")
plt.title("2009M TL Rear Door Jamb Switch DTF\n"+"Number of bins: " + str(len(bins)-1))
plt.grid(True)

plt.show()
