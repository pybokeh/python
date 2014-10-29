# NOTE: This only works for Python 2.X
# Python program that creates a chart containing closing stock price vs date
# It grabs the source CSV file containing historical stock data directly from Yahoo's finance site
# This is just an example URL:
#   http://ichart.finance.yahoo.com/table.csv?s=HMC&a=0&b=1&c=2001&d=4&e=9&f=2011&g=d&ignore=.csv
# The parameters in the URL that are used to determine start and end date are as follows:
# a = start month where Jan = '0', Feb = '1, ... Dec = '11'
# b = start day
# c = start year
# d = end month
# e = end day
# f = end year
# NOTE: Since Yahoo's month number is one less than the usual (ie: Jan = '0', instead of '1'),
#       a function "yahoo_mth" was created to do the conversion.  Why did you do this Yahoo??
#
# Further references:
# http://matplotlib.sourceforge.net/examples/pylab_examples/date_demo2.html
# http://matplotlib.sourceforge.net/api/dates_api.html#matplotlib.dates.MonthLocator
# http://www.endlesslycurious.com/2011/05/06/graphing-real-data-with-matplotlib/

# from pylab import *   Do NOT do this, it combines matplotlib and numpy together, import them separately
#                       to avoid namespace conflicts and also a good idea to not import EVERYTHING
import matplotlib.pyplot as plt
from numpy import arange
import urllib2, os, sys
from datetime import date, datetime
from matplotlib.dates import date2num, MonthLocator, WeekdayLocator, DateFormatter
from urlparse import urlparse

# This is a function to convert your traditional month # to Yahoo's untraditional month number (Jan = 0, not 1 WTF!)
def yahoo_mth(mth):
    if mth == 1:
        return '0'
    elif mth == 2:
        return '1'
    elif mth == 3:
        return '2'
    elif mth == 4:
        return '3'
    elif mth == 5:
        return '4'
    elif mth == 6:
        return '5'
    elif mth == 7:
        return '6'
    elif mth == 8:
        return '7'
    elif mth == 9:
        return '8'
    elif mth == 10:
        return '9'
    elif mth == 11:
        return '10'
    elif mth == 12:
        return '11'
    else:
        return '??'

# Function that creates the string that represents the URL to Yahoo's stock data
def create_stock_data_url(stock_ticker, start_date, end_date):
    start_day   = start_date.day
    start_month = start_date.month
    start_year  = start_date.year
    end_day     = end_date.day
    end_month   = end_date.month
    end_year    = end_date.year

    url_begin  = 'http://ichart.finance.yahoo.com/table.csv?s='
    url_end = '&a=' + yahoo_mth(start_month) + '&b=' + str(start_day) + '&c=' + str(start_year) + '&d=' + \
              yahoo_mth(end_month)+'&e='+str(end_day)+'&f='+str(end_year)+'&g=d&ignore=.csv'

    return url_begin + stock_ticker + url_end

# Function used to get and store the stock data into a tuple
def get_chart_data_tuple(data_url):
    try:
        input_file = urllib2.urlopen(data_url)
    except:
        print 'Ticker symbol is not valid or URL page was no longer valid.'
        sys.exit()

    # Fetch first row which contains the column names        
    first_row = input_file.readline().strip()
    column_names_list = first_row.split(",")

    # Created indices that will help us get the closing date and closing price from the source data
    date_idx = column_names_list.index("Date")
    closing_price_idx = column_names_list.index("Adj Close")

    # Initialize a dictionary that will store the date and it's corresponding closing stock price
    stock_dict = {}

    # Process the rest of the CSV file...
    while input_file:
        row = input_file.readline().strip()
        row_data_list = row.split(",")
        if row == "":
            break
        else:
            # Get the date and convert to datetime, get the price, then add them to the dictionary
            closing_date = date2num( datetime.strptime(row_data_list[date_idx], '%Y-%m-%d'))
            closing_price = row_data_list[closing_price_idx]
            stock_dict[closing_date] = float(closing_price)
    # Close the file
    input_file.close()

    # Since we can't actually sort a dictionary, instead, create a list of tuples such as
    # [(key1, value1), (key2, value2), ... (key_n, value_n)] and sort it by key descending
    # I found this sort routine from a Google search, I don't like the syntax of this at all!
    stock_tuple_by_date = sorted(stock_dict.items(), key=lambda x: x[0])

    return stock_tuple_by_date

def create_img_save_loc(file_name, url_suffix):
    temp_loc = "d:\\yourfolder\\"+url_suffix.replace("/","\\")  # If on windows (sorry this is not an OS-agnostic Python script)
    slash_idx = temp_loc.rfind('\\')
    img_save_location = temp_loc[:slash_idx+1] + 'images\\'
    img_file_name = file_name
    return img_save_location + img_file_name

# Begin "MAIN" Python script
start_date = date(2009,1,1)
start_day   = start_date.day
start_month = start_date.month
start_year   = start_date.year
stock_ticker = 'HMC'

try:
    start_date = date(start_year,start_month,start_day)
except:
    print 'Start date is not valid.'
    sys.exit()
    
end_date = date.today()

yah_url = create_stock_data_url(stock_ticker, start_date, end_date)

# print yah_url   # Uncomment this line if you want to confirm the URL

# Now store the closing dates and their corresponding closing stock price into lists
data_tuple = get_chart_data_tuple(yah_url)
closing_dates = []
stock_prices  = []
for key,value in data_tuple:
    closing_dates.append(key)
    stock_prices.append(value)

# These will be used to set the min/max values on the y-axis
ymin = int(min(stock_prices))
ymax = int(max(stock_prices))

fig = plt.figure()
ax = plt.subplot(1,1,1)
month_interval = 3
months    = MonthLocator(bymonth=range(1,13),  bymonthday=1, interval=month_interval)
month    = MonthLocator(bymonth=range(1,13),  bymonthday=1, interval=1)
monthsFmt = DateFormatter("%b '%y")
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.xaxis.set_minor_locator(month)


plt.plot_date(closing_dates, stock_prices, '-', xdate=True)

# Get current axis and set x/yticklabel size
current_axis = plt.gca()
for xticklabels in current_axis.get_xticklabels():
    xticklabels.set_fontsize(8)

# Set the min/max value on the y-axis
ax.set_yticks(arange(ymin-2, ymax+2, 1))

# Get current y-axis instance and then set tick position (left|right), but 'both' don't work for some reason
yax = plt.gca().yaxis
yax.set_ticks_position('right')

# Set y-axis tick label size...
for yticklabels in current_axis.get_yticklabels():
    yticklabels.set_fontsize(8)

plt.title('Closing Stock Price for: ' + stock_ticker + ' from ' + str(start_date) + ' thru ' + str(end_date), fontsize=14)
plt.ylabel('Closing Stock Price')
plt.xlabel('Date in ' + str(month_interval) + '-month Invervals')
ax.xaxis.grid(True, 'minor')
ax.xaxis.grid(True, 'major', linestyle='-', linewidth=1)
ax.yaxis.grid(True, 'major')

# This will rotate the dates on the x axis if it gets too crowded
fig.autofmt_xdate()

fig.show()

# savefig(fileloc)  # Uncomment this to save the chart/figure
