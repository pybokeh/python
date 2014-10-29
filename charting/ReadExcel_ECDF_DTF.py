# Must have module xlrd installed

import pandas as pandas
import numpy as np
import scikits.statsmodels.tools.tools as tools
import matplotlib.pyplot as plt

xls = pandas.ExcelFile('/home/pybokeh/Desktop/Civic_Blower.xls')
df = xls.parse('Claims')


ELP_2008 = df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='ELP') & (df['MODEL_NAME']=='CIVIC')]['DAYS_TO_FAIL_MINZERO'].values
HCM_2008 = df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='HCM') & (df['MODEL_NAME']=='CIVIC')]['DAYS_TO_FAIL_MINZERO'].values
SSS_2008 = df[(df['MODEL_YEAR']==2008) & (df['FACTORY_CODE']=='SSS') & (df['MODEL_NAME']=='CIVIC')]['DAYS_TO_FAIL_MINZERO'].values


ecdf1 = tools.ECDF(ELP_2008)
x1 = np.linspace(min(ELP_2008), max(ELP_2008))
y1 = ecdf1(x1)

ecdf2 = tools.ECDF(HCM_2008)
x2 = np.linspace(min(HCM_2008), max(HCM_2008))
y2 = ecdf2(x2)

ecdf3 = tools.ECDF(SSS_2008)
x3 = np.linspace(min(SSS_2008), max(SSS_2008))
y3 = ecdf3(x3)

fig1 = plt.figure(1)
elp, hcm, sss = plt.step(x1,y1,'r-', x2, y2, 'b-', x3, y3, 'g-')
plt.grid(True)
plt.ylabel('ECDF', fontsize=8)
plt.xlabel('DTF', fontsize=8)
plt.title('Empirical CDF', fontsize=10)

plt.legend( (elp, hcm, sss), ('2008M ELP', '2008M HCM', '2008M SSS'), 'best')


fig2 = plt.figure(2)
data = [ELP_2008, HCM_2008, SSS_2008]
n, bins, patches = plt.hist(data, 15, normed=True, cumulative=False, alpha=1, label=['ELP','HCM','SSS'])
plt.grid(True)
plt.legend(loc='best')

plt.show()
