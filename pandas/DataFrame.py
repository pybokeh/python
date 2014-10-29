# Must have xlrd module installed for ExcelFile to work

import pandas as pandas
import matplotlib.pyplot as plt
import scikits.statsmodels.tools.tools as tools
import numpy as np

# Open the Excel file
xls = pandas.ExcelFile('/home/pybokeh/Desktop/35400_07-12M.xls')
# Parse the specific Excel sheet name
df = xls.parse('Claims')

pandas.set_printoptions(precision=6, max_columns=12)


# Print just the first 3 rows of data
print "Printing just the first 3 rows of data..."
print df[:3]
print "\n"

# Print just the last 3 rows of data
print "Printing just the last 3 rows of data..."
print df[-3:]
print "\n"

# Print all of the data
# print "Prining all of the data"
# print df.to_string()
# print "\n"

# Print the mean for each year
print "Printing the mean MTFs for each year..."
print df.groupby(['MODEL_YEAR'])['MILES_TO_FAIL'].mean()
print "\n"

data_09 = df[ df['MODEL_YEAR']==2009 ]
# Printing the mean of MTF for each factory and model name
print "Printing the mean of MTF for each factory and model name using groupby"
print data_09.groupby(['FACTORY_CODE','MODEL_NAME'])['MILES_TO_FAIL'].mean()
print "\n"

print "Printing the mean MTF by factory and model name using pivot table"
table = pandas.pivot_table(data_09, values='MILES_TO_FAIL', rows=['FACTORY_CODE','MODEL_NAME'], aggfunc=np.mean)
print table
print "\n"

# Printing the count for each factory and model name
print "Printing count by factory and model name"
print df.groupby(['MODEL_YEAR','FACTORY_CODE','MODEL_NAME'])['MILES_TO_FAIL'].count()
print "\n"

# Printing count by model year
print "Printing count by model year"
print df.groupby(['MODEL_YEAR'])['MILES_TO_FAIL'].count()
print "\n"

# Printing the Cumulative count by model year
print "Printing cumulative count by model year"
print df.groupby(['MODEL_YEAR'])['MILES_TO_FAIL'].count().cumsum()
print "\n"

print "Using the describe function for summary statistics"
print df['MILES_TO_FAIL'].describe()


print "Create user-defined column from concatenating values from different columns"
df['FAC_MODEL']=df['FACTORY_CODE'].map(str)+"-"+df['MODEL_NAME'].map(str)
print "Another user-defined column that is just a count of row values"
df['QTY'] = df.sum(axis=1)
print df[['FACTORY_CODE','MODEL_NAME','FAC_MODEL','QTY']].head()

print "Now sort the dataframe by QTY in descending order"
df.sort_index(by='QTY', ascending=False)
