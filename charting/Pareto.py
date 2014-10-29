# Must have xlrd module installed for ExcelFile to work

import pandas as pandas
import matplotlib.pyplot as plt
import scikits.statsmodels.tools.tools as tools
import numpy as np
from matplotlib.ticker import MultipleLocator

# Open the Excel file
xls = pandas.ExcelFile(r'D:\tomcat\webapps\DensoOBD\files\35400\08-12M HAM Door Jamb Switch.xls')
# Parse the specific Excel sheet name
df = xls.parse('Claims')

pandas.set_printoptions(precision=6, max_columns=12)

data = df[(df['MODEL_YEAR']==2009)
        & (df['FACTORY_CODE']=='ELP')
        & (df['MODEL_NAME']=='CRV')]

counts = data.groupby(['RO_DEALER_STATE'])['VIN'].count()

qty = counts.values
state = counts.index

# zip the qty and state lists together so we can sort it by qty
data_list_numeric = zip(qty, state)
data_list_numeric.sort()
data_list_numeric.reverse()

xlabels = []
yvalues = []
for y,x in data_list_numeric:
        yvalues.append(y)
        xlabels.append(x)

xvalues = np.arange(0, len(yvalues), 1)

ax = plt.gca()
major_ticks = MultipleLocator(5)
minor_ticks = MultipleLocator(1)
ax.yaxis.set_major_locator(major_ticks)
ax.yaxis.set_minor_locator(minor_ticks)
plt.bar(xvalues, yvalues)
plt.xticks(xvalues+0.5, xlabels, rotation=90)
ax.yaxis.grid(which='major', linestyle='-', linewidth=2)
xtick_labels = ax.get_xticklabels()
for label in xtick_labels:
    label.set_fontsize(10)
plt.title("2009 ELP CRV Door Jamb Switch Replaced Qty by Dealer State")
plt.xlabel("Dealer State")
plt.ylabel("Qty")
plt.show()

