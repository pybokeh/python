import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib.ticker import FormatStrFormatter, MultipleLocator

# function pcc creates the process control chart
# arguments: data = data array, ucl = upper control limit, lcl = lower control limit, xinterval = x-axis interval size
def pcc(data, avg, ucl, lcl, xinterval):
    upper_control_limit = ucl
    lower_control_limit = lcl
    data_mean = avg

    count = len(data)
    xvalues = np.arange(1,count+1,1)

    UCL=[]
    counter = 0
    while counter < count:
        UCL.append(upper_control_limit)
        counter = counter + 1

    LCL=[]
    counter = 0
    while counter < count:
        LCL.append(lower_control_limit)
        counter = counter + 1

    mean=[]
    counter = 0
    while counter < count:
        mean.append(data_mean)
        counter = counter + 1

    fig = plt.figure(facecolor="white")
    ax = plt.subplot(1,1,1, axisbg='#cdc9c9')

    # Add plots and set axis properties
    plt.plot(xvalues, data,'o-', label='data', color='black')
    plt.plot(xvalues, mean,'-', label='mean', color='black', linewidth=4)
    plt.plot(xvalues, UCL,'--', color='red', linewidth=2)
    plt.plot(xvalues, LCL,'--', color='green', linewidth=2)
    plt.grid(True)
    plt.xticks(xvalues)
    xax = plt.gca().xaxis
    plt.xlim(1,count)
    #plt.ylim(np.min(data)-1, np.max(data)+1)
    plt.ylim(-10, 10)
    major_ticks = MultipleLocator(int(xinterval))
    ax.xaxis.set_major_locator(major_ticks)

    # Add text / legend
    plt.text(count+0.1, upper_control_limit, 'UCL', color='red', fontsize=15)
    plt.text(count+0.1, lower_control_limit, 'LCL',color='green', fontsize=15)
    plt.text(count+0.1, data_mean, 'mean='+'%0.4f'%(data_mean,),color='black', fontsize=15)
    plt.legend(bbox_to_anchor=(1.01, 0.8), loc=2, borderaxespad=0.)
    plt.ylabel("% Nonconforming", fontsize=15)
    plt.title("Standardized Control Chart", fontsize=24)
    plt.show()

if __name__ == "__main__":
    df = pandas.read_csv(r'D:\_mycode\python\charting\sample_data\battery.csv', names=['sample_size','num_defects'])
    sample_size = df['sample_size'].values.astype(float)
    num_defects = df['num_defects'].values.astype(float)
    Pi = num_defects / sample_size
    Pavg = Pi.mean()
    Zi = (Pi-Pavg)/np.sqrt(Pavg*(1-Pavg)/sample_size)

    UCL = 3
    LCL = -3
    pcc(Zi,Pavg,UCL,LCL,xinterval=1)
