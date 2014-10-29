# NOTE: This only works for Python 2.X
# Python program that creates a chart containing closing stock price vs date
# It grabs the source CSV file containing historical stock data directly from Yahoo's finance site
# This is just an example URL:
#   http://ichart.finance.yahoo.com/table.csv?s=HMC&a=0&b=1&c=2001&d=4&e=9&f=2011&g=d&ignore=.csv
# The parameters in the URL that are used to determine start and end date are as follows:
# a = start month where Jan = '0', Feb = '1, ... Dec = '11'
# b = start day
# c = start year
# d = end month where Jan = '0', Feb = '1, ... Dec = '11'
# e = end day
# f = end year
# NOTE: Yahoo's month number is one less than the conventional month number.
#
# Further references:
# http://matplotlib.sourceforge.net/examples/pylab_examples/date_demo2.html
# http://matplotlib.sourceforge.net/api/dates_api.html#matplotlib.dates.MonthLocator
# http://www.endlesslycurious.com/2011/05/06/graphing-real-data-with-matplotlib/

import tkFileDialog
import matplotlib.pyplot as plt
import urllib2, os, sys
from numpy import arange
from matplotlib.dates import date2num, MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
from urlparse import urlparse
from Tkinter import *
import ttk
from datetime import date, datetime

class StockTickerCharter(Frame):
    """
    A GUI class that charts a stock ticker symbol over the user defined time period.
    """
    
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()

        self.lblticker = Label(self.frame, text="Choose or type stock ticker:")
        self.lblticker.grid(row=0, column=0)

        ticker_list = ('AMZN-Amazon','CSCO-Cisco','GOOG-Google','HMC-Honda','INTC-Intel','MSFT-Microsoft','TM-Toyota','WMT-Walmart')

        self.strticker = StringVar()
        self.ticker = ttk.Combobox(self.frame, textvariable=self.strticker, value=ticker_list)
        self.ticker.grid(row=0, column=1, columnspan=6)

        self.lblStartDate = Label(self.frame, text="Start Date(yyyy-mm-dd):")
        self.lblStartDate.grid(row=1, column=0)

        self.strStartYear = StringVar()
        self.StartYear = Entry(self.frame, textvariable=self.strStartYear, width=4, borderwidth=2)
        self.StartYear.grid(row=1, column=1)

        self.lblHyphen1 = Label(self.frame, text="-", width=1)
        self.lblHyphen1.grid(row=1, column=2)

        self.strStartMonth = StringVar()
        self.StartMonth = Entry(self.frame, textvariable=self.strStartMonth, width=2, borderwidth=2)
        self.StartMonth.grid(row=1, column=3)

        self.lblHyphen2 = Label(self.frame, text="-", width=1)
        self.lblHyphen2.grid(row=1, column=4)

        self.strStartDay = StringVar()
        self.StartDay = Entry(self.frame, textvariable=self.strStartDay, width=2, borderwidth=2)
        self.StartDay.grid(row=1, column=5)

        self.lblEndDate = Label(self.frame, text="End Date(yyyy-mm-dd):")
        self.lblEndDate.grid(row=2, column=0)

        self.strEndYear = StringVar()
        self.EndYear = Entry(self.frame, textvariable=self.strEndYear, width=4, borderwidth=2)
        self.EndYear.grid(row=2, column=1)

        self.lblHyphen3 = Label(self.frame, text="-", width=1)
        self.lblHyphen3.grid(row=2, column=2)

        self.strEndMonth = StringVar()
        self.EndMonth = Entry(self.frame, textvariable=self.strEndMonth, width=2, borderwidth=2)
        self.EndMonth.grid(row=2, column=3)

        self.lblHyphen4 = Label(self.frame, text="-", width=1)
        self.lblHyphen4.grid(row=2, column=4)

        self.strEndDay = StringVar()
        self.EndDay = Entry(self.frame, textvariable=self.strEndDay, width=2, borderwidth=2)
        self.EndDay.grid(row=2, column=5)

        self.lblMonthInterval = Label(self.frame, text="Month interval size:")
        self.lblMonthInterval.grid(row=3, column=0)

        self.strMonthInterval = StringVar()
        self.MonthInterval = Entry(self.frame, textvariable=self.strMonthInterval, width=3, borderwidth=2)
        self.strMonthInterval.set('3')
        self.MonthInterval.grid(row=3, column=1)

        self.lblYinterval = Label(self.frame, text="Y interval size")
        self.lblYinterval.grid(row=4, column=0)

        self.strYinterval = StringVar()
        self.Yinterval = Entry(self.frame, textvariable=self.strYinterval, width=3, borderwidth=2)
        self.strYinterval.set('1')
        self.Yinterval.grid(row=4, column=1)
             
        self.btnSubmit = Button(self.frame, text="Submit", fg="red", command=self.main)
        self.btnSubmit.grid(row=5, column=0)

        self.btnClear = Button(self.frame, text="Clear", command=self.clearURL)
        self.btnClear.grid(row=5, column=1)

        self.strURL = StringVar()
        self.txtURL = Entry(self.frame, textvariable=self.strURL, fg="black", width=60)
        self.txtURL.grid(row=6, column=0, columnspan=6)

        self.ticker.focus_set()

    # Function used to get and store the stock data into a tuple
    def get_chart_data_tuple(self, data_url):
        # http_proxy enironment variable needs to be created first = http://username:password@proxyserver:proxyport
        proxy = urllib2.ProxyHandler()
        auth = urllib2.HTTPBasicAuthHandler()
        opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        
        input_file = urllib2.urlopen(data_url)

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


    def clearURL(self):
        """
        Clears the data URL and the ticker text field and let the ticker text field receive focus
        """
        self.strURL.set('')
        self.strticker.set('')
        self.ticker.focus_set()


    def main(self):
        """
        Given the ticker symbol, start date, and end date, it will attempt to create the chart
        """
        try:
            start_date  = date(int(self.strStartYear.get()), int(self.strStartMonth.get()), int(self.strStartDay.get()))
            end_date    = date(int(self.strEndYear.get()), int(self.strEndMonth.get()), int(self.strEndDay.get()))
        except:
            self.strURL.set("One or more date inputs are wrong")
            print "One or more date inputs are wrong"
            
        start_day   = start_date.day
        start_month = start_date.month - 1  # Yahoo's month number is one less than the conventional month number
        start_year  = start_date.year
        end_day     = end_date.day
        end_month   = end_date.month - 1    # Yahoo's month number is one less than the conventional month number
        end_year    = end_date.year

        url_begin  = 'http://ichart.finance.yahoo.com/table.csv?s='
        url_end = '&a=' + str(start_month) + '&b=' + str(start_day) + '&c=' + str(start_year) + '&d=' + \
              str(end_month)+'&e='+str(end_day)+'&f='+str(end_year)+'&g=d&ignore=.csv'


        if self.strticker.get().find('-'):
            tickerlist = self.strticker.get().split('-')
            ticker_symbol = tickerlist[0].upper()
        else:
            ticker_symbol = self.strticker.get().upper()

        yahoo_url = url_begin + ticker_symbol + url_end

        self.strURL.set( yahoo_url )

        # Now store the closing dates and their corresponding closing stock price into lists
        try:
            data_tuple = self.get_chart_data_tuple(yahoo_url)
        except:
            print "Ticker Symbol is not valid or finance.yahoo.com site is down."
            self.strURL.set('Ticker Symbol is not valid or finance.yahoo.com site is down.')
            
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
        
        # Get the month interval size from the GUI
        month_interval = int(self.strMonthInterval.get())
        
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

        # Get the Y-axis interval size from the GUI
        major_ticks = MultipleLocator(int(self.strYinterval.get()))
        ax.yaxis.set_major_locator(major_ticks)

        # Get current y-axis instance and then set tick position (left|right), but 'both' don't work for some reason
        yax = plt.gca().yaxis
        yax.set_ticks_position('right')

        # Set y-axis tick label size...
        for yticklabels in current_axis.get_yticklabels():
            yticklabels.set_fontsize(8)

        plt.title('Closing Stock Price for: ' + self.strticker.get().upper() + ' from ' + str(start_date) + ' thru ' + str(end_date), fontsize=14)
        plt.ylabel('Closing Stock Price')
        plt.xlabel('Date in ' + str(month_interval) + '-month Invervals')
        ax.xaxis.grid(True, 'minor')
        ax.xaxis.grid(True, 'major', linestyle='-', linewidth=1)
        ax.yaxis.grid(True, 'major')

        # Rotate the x-axis ticks to 90 degrees
        plt.xticks(rotation=90)

        plt.show()

        # savefig(fileloc)  # Uncomment this to save the chart/figure        


if __name__ == "__main__":
    root = Tk()
    root.title("Stock Ticker Charter")
    root.update()
    app = StockTickerCharter(root)
    root.mainloop()
