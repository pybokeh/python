# Must have xlrd module installed for ExcelFile to work

import pandas as pandas
import matplotlib.pyplot as plt
import scikits.statsmodels.tools.tools as tools
import numpy as np
from matplotlib.ticker import MultipleLocator

pandas.set_printoptions(precision=6, max_columns=12)

# Open the Excel file
xls = pandas.ExcelFile('/home/pybokeh/Desktop/sample.xls')
# Parse the specific Excel sheet name
dfleft = xls.parse('Sheet1', index_col=0)
dfright = xls.parse('Sheet2', index_col=0)

print dfleft.to_string()
print dfleft.dtypes

print dfright.to_string()

dfjoined = dfleft.join(dfright)

print dfjoined.to_string()

#dfjoined.to_csv('/home/pybokeh/Desktop/sample.csv', header=True, index=True)
