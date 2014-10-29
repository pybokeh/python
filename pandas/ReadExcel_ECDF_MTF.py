# Must have module xlrd installed

import pandas as pandas
import numpy as np
import scikits.statsmodels.tools.tools as tools
import matplotlib.pyplot as plt

xls = pandas.ExcelFile('/home/pybokeh/Desktop/Civic_Blower.xls')
df = xls.parse('Claims')

fig = plt.figure()
plt.suptitle('HVAC Blower Motor Replaced\nMTF Histogram and Empirical CDF', fontsize=16)
plt.subplot(221)
n, bins, patches = plt.hist(df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='ELP')]['MILES_TO_FAIL'].values, 20, normed=False, cumulative=False, facecolor='red', alpha=1)
plt.grid(True)
plt.ylabel('Frequency', fontsize=8)
plt.xlabel('MTF Bins', fontsize=8)
plt.title('2008 ELP Civic', fontsize=12)

plt.subplot(222)
n, bins, patches = plt.hist(df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='HCM')]['MILES_TO_FAIL'].values, 20, normed=False, cumulative=False, facecolor='blue', alpha=1)
plt.grid(True)
plt.ylabel('Frequency', fontsize=8)
plt.xlabel('MTF Bins', fontsize=8)
plt.title('2008 HCM Civic', fontsize=12)

plt.subplot(223)
n, bins, patches = plt.hist(df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='SSS')]['MILES_TO_FAIL'].values, 15, normed=False, cumulative=False, facecolor='green', alpha=1)
plt.grid(True)
plt.ylabel('Frequency', fontsize=8)
plt.xlabel('MTF Bins', fontsize=8)
plt.title('2008 SSS Civic', fontsize=12)

plt.subplot(224)
dataELP = df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='ELP')]['MILES_TO_FAIL'].values
ecdf1 = tools.ECDF(dataELP)
x1 = np.linspace(min(dataELP), max(dataELP))
y1 = ecdf1(x1)

dataHCM = df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='HCM')]['MILES_TO_FAIL'].values
ecdf2 = tools.ECDF(dataHCM)
x2 = np.linspace(min(dataHCM), max(dataHCM))
y2 = ecdf2(x2)

dataSSS = df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='SSS')]['MILES_TO_FAIL'].values
ecdf3 = tools.ECDF(dataSSS)
x3 = np.linspace(min(dataSSS), max(dataSSS))
y3 = ecdf3(x3)

elp, hcm, sss = plt.step(x1,y1,'r-', x2, y2, 'b-', x3, y3, 'g-')
plt.grid(True)
plt.ylabel('ECDF', fontsize=8)
plt.xlabel('MTF', fontsize=8)
plt.title('Empirical CDF', fontsize=12)

plt.legend( (elp, hcm, sss), ('08M ELP', '08M HCM', '08M SSS'), 'best')
plt.show()

#fig.savefig(r'A:\DensoOBD\WarrantySummaries\79310 - Blower Motor\79310.png')
