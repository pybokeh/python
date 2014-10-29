# OUTPUTS: 2 histograms by DTF and DTF

import pandas as pandas
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import scikits.statsmodels.tools.tools as tools
import numpy as np
from matplotlib.ticker import FormatStrFormatter, MultipleLocator

# Open the Excel file
xls = pandas.ExcelFile(r'\\mapfile01\aqg\mq\group\Chassis\MTitus27368\89Ki_BP_Project\MeetsTriggerNoActivity\TL Keyless Battery.xls')
# Parse the specific Excel sheet name
TL_2009 = xls.parse('Claims')
TL_2008 = xls.parse('Claims 2008')


pandas.set_printoptions(precision=6, max_columns=12)

DTF2008 = TL_2008['DTF_MINZERO'].values
DTF2009 = TL_2009['DTF_MINZERO'].values

print "2008 TL Summary Statistics:\n" + TL_2008['DTF_MINZERO'].describe().to_string()+'\n'
print "2009 TL Summary Statistics:\n" + TL_2009['DTF_MINZERO'].describe().to_string()



# Make a histogram
fig1 = plt.figure(1)
n, bins, patches = plt.hist(DTF2008, 10, normed=False, cumulative=False, facecolor='red', alpha=1)
ax = plt.gca()
#ax.xaxis.set_ticks(bins, minor=False)
plt.xticks(rotation=90)
major_tick_format = FormatStrFormatter('%d')
ax.xaxis.set_major_formatter(major_tick_format)
xtick_labels = ax.xaxis.get_ticklabels()
for label in xtick_labels:
    label.set_fontsize(8)
plt.xlabel("DTF")
plt.ylabel("Frequency")
plt.title("2008M TL Keyless Remote Battery DTF Histogram\n"+"Number of bins: " + str(len(bins)-1))
ax.yaxis.grid(which='major', linestyle='--')


# Make a histogram
fig2 = plt.figure(2)
n, bins, patches = plt.hist(DTF2009, 20, normed=False, cumulative=False, facecolor='red', alpha=1)
ax = plt.gca()
#ax.xaxis.set_ticks(bins, minor=False)
plt.xticks(rotation=90)
major_tick_format = FormatStrFormatter('%d')
ax.xaxis.set_major_formatter(major_tick_format)
xtick_labels = ax.xaxis.get_ticklabels()
for label in xtick_labels:
    label.set_fontsize(8)
plt.xlabel("DTF")
plt.ylabel("Frequency")
plt.title("2009M TL Keyless Remote Battery DTF Histogram\n"+"Number of bins: " + str(len(bins)-1))
plt.grid(True)



# Make a ECDF figure
fig3 = plt.figure(3)
ecdf2008 = tools.ECDF(DTF2008)
x2008 = np.linspace(min(DTF2008), max(DTF2008))
y2008 = ecdf2008(x2008)

ecdf2009 = tools.ECDF(DTF2009)
x2009 = np.linspace(min(DTF2009), max(DTF2009))
y2009 = ecdf2009(x2009)

plt.step(x2008,y2008,'r-', x2009, y2009, 'b-')
plt.grid(True)
plt.legend(['2008','2009'], loc='best')
plt.title('Empirical CDF vs DTF')
plt.ylabel('% of Failures')
plt.xlabel('Days To Fail')


data = [DTF2008, DTF2009]

# Make a boxplot figure
fig4 = plt.figure(4)
ax = plt.gca()
ax.set_yticklabels(['2008 TL', '2009 TL'])
box_dict = plt.boxplot(data, vert=0)
major_ticks = MultipleLocator(90)
minor_ticks = MultipleLocator(30)
plt.xticks(np.arange(0,1600,1), rotation=90)
ax.xaxis.set_major_locator(major_ticks)
ax.xaxis.set_minor_locator(minor_ticks)
ax.xaxis.grid(which='major', linestyle='-', linewidth=1)
ax.xaxis.grid(which='minor', linestyle=':', linewidth=1)
xtick_labels = ax.xaxis.get_ticklabels()
for label in xtick_labels:
    label.set_fontsize(8)
plt.title("2008-9 TL Keyless Battery Replacements\nBox Plot")
plt.xlabel("Days To Fail")

plt.show()
