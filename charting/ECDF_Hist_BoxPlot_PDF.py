#  NOTE: xlrd module must be installed to open Excel 2003 or earlier,
#        openpyxl must be installed to open Excel version > Excel 2003
#        See http://pandas.pydata.org/pandas-docs/stable/io.html#excel-files
import pandas as pandas # Useful module for data analysis
import matplotlib.pyplot as plt # module for making charts
import numpy as np  # module for array or mathematical operations
import statsmodels.tools.tools as tools  # Used to obtain ECDF generator
from matplotlib.ticker import MultipleLocator # Used to generate chart tick values

##############################  Open the Excel file  ##############################
xls = pandas.ExcelFile(r'd:\_mycode\python\data\Book1.xlsx')
# Parse the specific Excel sheet name into a pandas data frame object
df = xls.parse('Sheet1')

#######  Then create a data frame for each model containing the dB values #########
TL     = df[(df['Model']=='UA') & (df['txtParam']=='FMRES1')]['txtParamval']
Acc4dr = df[(df['Model']=='CP') & (df['txtParam']=='FMRES1')]['txtParamval']
Acc2dr = df[(df['Model']=='CS') & (df['txtParam']=='FMRES1')]['txtParamval']

############################  Generate ECDF for each model  #######################
ecdf_TL = tools.ECDF(TL)
ecdf_Acc4dr = tools.ECDF(Acc4dr)
ecdf_Acc2dr = tools.ECDF(Acc2dr)

##############################  Begin charting ECDF  ##############################
fig1 = plt.figure(1)
x_TL = np.linspace(TL.min(), TL.max())
y_TL = ecdf_TL(x_TL)
plt.step(x_TL, y_TL, label='TL')
x_Acc4dr = np.linspace(Acc4dr.min(), Acc4dr.max())
y_Acc4dr = ecdf_Acc4dr(x_Acc4dr)
plt.step(x_Acc4dr, y_Acc4dr, label='Acc4dr')
x_Acc2dr = np.linspace(Acc2dr.min(), Acc2dr.max())
y_Acc2dr = ecdf_Acc2dr(x_Acc2dr)
plt.step(x_Acc2dr, y_Acc2dr, label='Acc2dr')
plt.legend(loc='best')
plt.title("Empirical Distribution Functions")

##############################  Begin plotting histogram  ###########################
fig2 = plt.figure(2)
n, bins, patches = plt.hist([TL, Acc4dr, Acc2dr], 30, normed=True, cumulative=False, label=('TL','Acc4dr','Acc2dr'))
plt.legend(loc='best')
plt.title("Histogram")

##############################  Begin plotting box plota  #############################
fig3 = plt.figure(3)
ax = plt.gca()
ax.set_yticklabels(['TL', 'Acc4dr', 'Acc2dr'])
plt.boxplot([TL,Acc4dr,Acc2dr], vert=0)
major_ticks = MultipleLocator(10)
minor_ticks = MultipleLocator(1)
ax.xaxis.set_major_locator(major_ticks)
ax.xaxis.set_minor_locator(minor_ticks)
ax.xaxis.grid(which='major', linestyle='-', linewidth=2)
ax.xaxis.grid(which='minor', linestyle='-.', linewidth=1)
plt.title("Box Plots")

#############################  Begin plotting of PDFs  ###########################
fig4 = plt.figure(4)
mu_TL, sigma_TL         = TL.mean(), TL.std()
mu_Acc4dr, sigma_Acc4dr = Acc4dr.mean(), Acc4dr.std()
mu_Acc2dr, sigma_Acc2dr = Acc2dr.mean(), Acc2dr.std()
plt.plot(x_TL, 1/(sigma_TL * np.sqrt(2 * np.pi)) * np.exp( - (x_TL - mu_TL)**2 / (2 * sigma_TL**2) ), label='TL', linewidth=2, color='r')
plt.plot(x_Acc4dr, 1/(sigma_Acc4dr * np.sqrt(2 * np.pi)) * np.exp( - (x_Acc4dr - mu_Acc4dr)**2 / (2 * sigma_Acc4dr**2) ), label='Acc4dr', linewidth=2, color='b')
plt.plot(x_Acc2dr, 1/(sigma_Acc2dr * np.sqrt(2 * np.pi)) * np.exp( - (x_Acc2dr - mu_Acc2dr)**2 / (2 * sigma_Acc2dr**2) ), label='Acc2dr', linewidth=2, color='g')
plt.legend(loc='best')
plt.title("Probability Distribution Functions")

############################  Show the figures  ###########################
fig1.show()
fig2.show()
fig3.show()
fig4.show()

###########################  Begin output of summary statistics  ##########################
#############################  to double-check the box plots  #############################
print "Summary statistics for TL:"
print TL.describe()
print "Summary statistics for Acc4dr:"
print Acc4dr.describe()
print "Summary statistics for Acc2dr:"
print Acc2dr.describe()
