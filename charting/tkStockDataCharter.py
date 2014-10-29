# This is a Python program that creates a chart containing closing stock prices vs date
# There is a version I made where it gets the stock data directly from yahoo, but at work
#    our stupid firewall blocks my Python code from getting that data.
#
# So I created this version where you have to first download the stock data to your computer
#    then this script does the rest (processes the data and charts it).  In this version,
#    I've made a GUI using Tkinter to make it easier to find/load the input file.
#    In previous version, it was strictly through the console.
#
# Further references:
# http://matplotlib.sourceforge.net/examples/pylab_examples/date_demo2.html
# http://matplotlib.sourceforge.net/api/dates_api.html#matplotlib.dates.MonthLocator
# http://www.endlesslycurious.com/2011/05/06/graphing-real-data-with-matplotlib/

# from pylab import *   Do NOT do this anymore! It combines matplotlib and numpy together, import
#                       them separately to avoid namespace conflicts and also a good idea to
#                       not import EVERYTHING.

import tkFileDialog
import os, sys
import matplotlib.pyplot as plt
from Tkinter import *
from numpy import arange
from datetime import date, datetime
from matplotlib.dates import date2num, MonthLocator, WeekdayLocator, DateFormatter

class StockDataCharter(Frame):
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.frame.pack()

        self.label_open = Label(self.frame, text="Choose input file:")
        self.label_open.grid(row=0, columnspan=2)
        
        self.button_open = Button(self.frame, text='OPEN', fg="red", command=self.processInputFile)
        self.button_open.grid(row=1)

        self.button_close = Button(self.frame, text='CLOSE', fg="black", command=root.destroy)
        self.button_close.grid(row=1, column=1)

        self.strView = StringVar()  # this is used to update the label in real time
        self.label_filename = Label(self.frame, textvariable=self.strView, fg="black")
        self.label_filename.grid(row=2, columnspan=2)

    def processInputFile(self):
        file_opt = {}
        # file_opt['filetypes']=[('all files','.*'), ('text files', '.txt'), ('csv files','.csv')]
        file_opt['filetypes']=[('csv files','.csv')]
        file_opt['parent'] = root

        filename = tkFileDialog.askopenfilename(**file_opt)
        if filename:
            print filename  # print for debugging purposes
            self.strView.set(filename)

        # Open the data input file
        input_file = open(filename,'r')

        # Fetch first row which contains the column names
        first_row = input_file.readline().strip()
        column_names_list = first_row.split(",")

        # find the closing date and its corresponding closing price
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
                
        # Close the input data file
        input_file.close()

        # Since we can't actually sort a dictionary, instead, create a list of tuples such as
        # [(key1, value1), (key2, value2), ... (key_n, value_n)] and sort it by key descending
        # I found this sort routine from a Google search, I don't like the syntax of this at all!
        data_tuple = sorted(stock_dict.items(), key=lambda x: x[0])
        
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

        plt.title('Closing Stock Price', fontsize=14)
        plt.ylabel('Closing Stock Price')
        plt.xlabel('Date in ' + str(month_interval) + '-month Invervals')
        ax.xaxis.grid(True, 'minor')
        ax.xaxis.grid(True, 'major', linestyle='-', linewidth=1)
        ax.yaxis.grid(True, 'major')

        # This will rotate the dates on the x axis if it gets too crowded
        fig.autofmt_xdate()

        fig.show()

        # savefig(fileloc)  # Uncomment this to save the chart/figure

        
root = Tk()
root.title("Tk")

root.update()

# Begin code to center the window
w = root.winfo_width()
h = root.winfo_height()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = (sw/2) - (w/2)
y = (sh/2) - (h/2)
# root.geometry('%dx%d+%d+%d' % (w,h,x,y,)) use this if you made window with specific width and height
root.geometry('+%d+%d' % (x,y))

app = StockDataCharter(root)

root.mainloop()
