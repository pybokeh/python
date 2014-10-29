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

from pylab import *
import urllib2, os, cgi, sys
from datetime import date, datetime
from matplotlib.dates import date2num, MonthLocator, DateFormatter
from matplotlib.ticker import MultipleLocator
from urlparse import urlparse

# Begin function declarations #####################################################
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

# Creates Yahoo's URL to the historical stock data stored in CSV format
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

# Saves historical stock data into a Python list containing tuples
def get_chart_data_tuple(data_url):
    # Check to see if the URL containing the ticker's historical stock data is valid...
    try:
        input_file = urllib2.urlopen(data_url)
    except:
        print 'Content-type: text/html\n\n' + '<h3>Ticker symbol is not valid.  Hit the back button to correct.</h3>'
        sys.exit()

    # Read the 1st row of the CSV file.  It contains the column names...    
    first_row = input_file.readline().strip()
    column_names_list = first_row.split(",")

    # Get the column number of the data and closing price...
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
    # [(key1, value1), (key2, value2), ... (key_n, value_n)] and sort it by key ascending
    stock_tuple_by_date = sorted(stock_dict.items(), key=lambda x: x[0])

    return stock_tuple_by_date

# Creates the location where the chart image will be saved at
def create_img_save_loc(file_name, url_suffix):
    temp_loc = "d:\\tomcat\\webapps"+url_suffix.replace("/","\\")
    slash_idx = temp_loc.rfind('\\')
    img_save_location = temp_loc[:slash_idx+1] + 'images\\'
    img_file_name = file_name
    return img_save_location + img_file_name

# End function declarations ###############################################################

# Get the form data...start date, ticker symbol, x-axis month interval size, and y-axis interval size
form = cgi.FieldStorage()
startmth = int(form["startmth"].value)
startday = int(form["startday"].value)
startyr = int(form["startyear"].value)
stock_ticker = form["ticker"].value.upper()

# If user entered the ticker symbol using the drop-down box, we just want the ticker symbol
if stock_ticker.find('-'):
    stock_ticker = stock_ticker.split('-')[0]

month_interval = int(form["xinterval"].value)
yinterval = int(form["yinterval"].value)

# Check if the start date is valid...
try:
    start_date = date(startyr,startmth,startday)
except:
    print 'Content-type: text/html\n\n' + '<h3>Start date is not valid.  Hit the back button to correct.</h3>'
    sys.exit()
    
end_date = date.today()

# Get Yahoo's URL to the historical stock data...
yah_url = create_stock_data_url(stock_ticker, start_date, end_date)

# Now store the dates and their corresponding closing stock price into lists
data_tuple = get_chart_data_tuple(yah_url)
closing_dates = []
stock_prices  = []
for key,value in data_tuple:
    closing_dates.append(key)
    stock_prices.append(value)

# These will be used to set the min/max values on the y-axis
ymin = int(min(stock_prices))
ymax = int(max(stock_prices))

# Prepare the chart, enable x-axis to diplay major and minor tick marks...
fig = figure()
ax = subplot(1,1,1)
months = MonthLocator(bymonth=range(1,13),  bymonthday=1, interval=month_interval)
month  = MonthLocator(bymonth=range(1,13),  bymonthday=1, interval=1)
monthsFmt = DateFormatter("%b '%y")  # ex. 'May '08
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.xaxis.set_minor_locator(month)

# Plot the chart, add title, labels, etc.
plot_date(closing_dates, stock_prices, '-', xdate=True)

# Get current axis and set xaxis tick label size
current_axis = gca()
for xticklabels in current_axis.get_xticklabels():
    xticklabels.set_fontsize(8)

# Set the min/max value on the y-axis
ax.set_yticks(arange(ymin-2, ymax+2, 1))

# Get the Y-axis interval size from the GUI
major_ticks = MultipleLocator(yinterval)
ax.yaxis.set_major_locator(major_ticks)

# Get current y-axis instance and then set tick position (left|right), but 'both' don't work for some reason
yax = gca().yaxis
yax.set_ticks_position('right')

# Set y-axis tick label size...
for yticklabels in current_axis.get_yticklabels():
    yticklabels.set_fontsize(8)

title('Closing Stock Price for: ' + stock_ticker + ' from ' + str(start_date) + ' thru ' + str(end_date), fontsize=12)
ylabel('Closing Stock Price')
xlabel('Date in ' + str(month_interval) + '-month Invervals')
ax.xaxis.grid(True, 'minor')
ax.xaxis.grid(True, 'major', linestyle='-', linewidth=1)
ax.yaxis.grid(True, 'major')

# This will rotate the dates on the x axis if it gets too crowded
fig.autofmt_xdate()

# Get the request URL so that we can use it to save the chart image in the correct location...
http_referer = os.environ['HTTP_REFERER']
url_parser = urlparse(http_referer)
url_suffix = url_parser.path
fileloc = create_img_save_loc('chart1.png', url_suffix)
savefig(fileloc, facecolor='w', edgecolor='w')

# Send user to original page, then refresh the page with new chart
print 'Content-type: text/html\n\n' + '<meta http-equiv="REFRESH" content="0;url=' + http_referer + '">'
