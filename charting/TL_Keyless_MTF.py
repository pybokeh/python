# OUTPUTS: 2 histograms by MTF and DTF

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

MTF2008 = TL_2008['MILES_TO_FAIL'].values
MTF2009 = TL_2009['MILES_TO_FAIL'].values

print "2008 TL Summary Statistics:\n" + TL_2008['MILES_TO_FAIL'].describe().to_string()+'\n'
print "2009 TL Summary Statistics:\n" + TL_2009['MILES_TO_FAIL'].describe().to_string()



# Make a histogram
fig1 = plt.figure(1)
n, bins, patches = plt.hist(MTF2008, 10, normed=False, cumulative=False, facecolor='red', alpha=1)
ax = plt.gca()
ax.xaxis.set_ticks(bins, minor=False)
#ax.xaxis.set_ticks(np.arange(0,84000,12000), minor=True)
plt.xticks(rotation=90)
major_tick_format = FormatStrFormatter('%d')
ax.xaxis.set_major_formatter(major_tick_format)
xtick_labels = ax.xaxis.get_ticklabels()
for label in xtick_labels:
    label.set_fontsize(8)
plt.xlabel("MTF")
plt.ylabel("Frequency")
plt.title("2008M TL Keyless Remote Battery\n"+"Number of bins: " + str(len(bins)-1))
ax.yaxis.grid(which='major', linestyle='--')


# Make a histogram
fig2 = plt.figure(2)
n, bins, patches = plt.hist(MTF2009, 15, normed=False, cumulative=False, facecolor='red', alpha=1)
ax = plt.gca()
ax.xaxis.set_ticks(bins, minor=False)
plt.xticks(rotation=90)
major_tick_format = FormatStrFormatter('%d')
ax.xaxis.set_major_formatter(major_tick_format)
xtick_labels = ax.xaxis.get_ticklabels()
for label in xtick_labels:
    label.set_fontsize(8)
plt.xlabel("MTF")
plt.ylabel("Frequency")
plt.title("2009M TL Keyless Remote Battery\n"+"Number of bins: " + str(len(bins)-1))
plt.grid(True)



# Make a ECDF figure
fig3 = plt.figure(3)
ecdf2008 = tools.ECDF(MTF2008)
x2008 = np.linspace(min(MTF2008), max(MTF2008))
y2008 = ecdf2008(x2008)

ecdf2009 = tools.ECDF(MTF2009)
x2009 = np.linspace(min(MTF2009), max(MTF2009))
y2009 = ecdf2009(x2009)

plt.step(x2008,y2008,'r-', x2009, y2009, 'b-')
plt.grid(True)
plt.legend(['2008','2009'], loc='best')
plt.title('Empirical CDF vs MTF')
plt.ylabel('% of Failures')
plt.xlabel('MTF')


data = [MTF2008, MTF2009]

# Make a boxplot figure
fig4 = plt.figure(4)
ax = plt.gca()
ax.set_yticklabels(['2008 TL', '2009 TL'])
box_dict = plt.boxplot(data, vert=0)
major_ticks = MultipleLocator(10000)
minor_ticks = MultipleLocator(1000)
ax.xaxis.set_major_locator(major_ticks)
ax.xaxis.set_minor_locator(minor_ticks)
ax.xaxis.grid(which='major', linestyle='-', linewidth=1)
ax.xaxis.grid(which='minor', linestyle=':', linewidth=1)
plt.title("2008-9 TL Keyless Battery Replacements\nBox Plot")
plt.xlabel("Miles To Fail")

plt.show()
