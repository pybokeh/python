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


ELP_CRV_2009 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='ELP') & (df['MODEL_NAME']=='CRV')]['MILES_TO_FAIL'].values
HDM_CRV_2009 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='HDM') & (df['MODEL_NAME']=='CRV')]['MILES_TO_FAIL'].values
TL_2009 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='MAP') & (df['MODEL_NAME']=='TL')]['MILES_TO_FAIL'].values
RDX_2009 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='MAP') & (df['MODEL_NAME']=='RDX')]['MILES_TO_FAIL'].values
ELP_CIV_2009 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='ELP') & (df['MODEL_NAME']=='CIVIC')]['MILES_TO_FAIL'].values
ELE_2009 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='ELP') & (df['MODEL_NAME']=='ELEMENT')]['MILES_TO_FAIL'].values
ACC_2009 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='MAP') & (df['MODEL_NAME']=='ACCORD')]['MILES_TO_FAIL'].values

dfCRV_09 = df[(df['MODEL_YEAR']==2009) & (df['FACTORY_CODE']=='ELP') & (df['MODEL_NAME']=='CRV')]['MILES_TO_FAIL']


# Make a boxplot figure
fig1 = plt.figure(1)
current_axis = plt.gca()
current_axis.set_yticklabels(['ELP CRV','HDM CRV', 'TL', 'RDX', 'CIVIC', 'ELEMENT','ACCORD'])
data = [ELP_CRV_2009, HDM_CRV_2009, TL_2009, RDX_2009, ELP_CIV_2009, ELE_2009, ACC_2009]
plt.boxplot(data, vert=0)
plt.grid(True)
plt.title("2009 Door Jamb Switch Failures")
plt.xlabel("Miles To Fail")

# Make a histogram figure
fig2 = plt.figure(2)
plt.subplot(2,1,1)
n, bins, patches = plt.hist(TL_2009, 15, normed=False, cumulative=False, facecolor='red', alpha=1)
plt.xlabel("MTF")
plt.ylabel("Frequency")
plt.title("TL MTF Histogram")
plt.grid(True)

plt.subplot(2,1,2)
n, bins, patches = plt.hist(ELP_CRV_2009, 20, normed=False, cumulative=False, facecolor='red', alpha=1)
plt.xlabel("MTF")
plt.ylabel("Frequency")
plt.title("ELP CRV MTF Histogram")
plt.grid(True)

# Make a ECDF figure
fig3 = plt.figure(3)
ecdf = tools.ECDF(ELP_CRV_2009)
x = np.linspace(min(ELP_CRV_2009), max(ELP_CRV_2009))
y = ecdf(x)
plt.step(x,y,'r-')
plt.grid(True)

# Make text figure.  Reference: http://matplotlib.sourceforge.net/users/text_props.html
fig4 = plt.figure(4)
ax = fig4.add_axes([0,0,1,1]) # This sets up axis dimensions of 1 x 1
ax.text(0.05, 0.65, str('2009M ELP CRV:\n'+str(dfCRV_09.describe())), color='black', transform=ax.transAxes)
ax.set_axis_off()

plt.show()
