import pandas as pd
from pandas import DataFrame
from datetime import date

df = DataFrame(
        {'VIN':['VIN1','VIN1','VIN2','VIN3'], 
         'RO_DATE':[date(2013,1,3),date(2013,1,1),date(2013,2,1),date(2013,4,10)],
         'MODEL_NAME':['ACCORD','ACCORD','CIVIC','RDX'],
         'int':[2,1,3,3]
        }
     )

# Print original dataframe
print df

# Now group the original dataframe by 'VIN'
grouped = df.groupby(df['VIN'])

# Sort the grouped dataframe by 'RO_DATE' and then drop duplicates, take_last=False means keep the 1st record
print grouped.sort_index(by='RO_DATE').drop_duplicates(['VIN'], take_last=False)
