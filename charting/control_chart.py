import matplotlib.pyplot as plt
import numpy
from matplotlib.ticker import FormatStrFormatter, MultipleLocator


# data = data array, ucl = upper control limit, lcl = lower control limit, xinterval = x-axis interval size
def pcc(data, ucl, lcl, xinterval):
    upper_control_limit = ucl
    lower_control_limit = lcl
    data_mean = numpy.mean(data)

    count = len(data)
    xvalues = numpy.arange(1,count+1,1)

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

    fig = plt.figure()
    ax = plt.subplot(1,1,1)

    # Add and set up plots
    plt.plot(xvalues, data,'o-', label='data', color='black')
    plt.plot(xvalues, mean,'-', label='mean', color='black', linewidth=4)
    plt.plot(xvalues, UCL,'--', color='red', linewidth=2)
    plt.plot(xvalues, LCL,'--', color='green', linewidth=2)
    plt.grid(True)
    plt.xticks(xvalues)
    xax = plt.gca().xaxis
    plt.xlim(1,count)
    plt.ylim(numpy.min(data)-5, numpy.max(data)+5)
    major_ticks = MultipleLocator(int(xinterval))
    ax.xaxis.set_major_locator(major_ticks)

    # Add text / legend
    plt.text(count+0.1, upper_control_limit-0.5, 'UCL', color='red', fontsize=15)
    plt.text(count+0.1, lower_control_limit-0.5, 'LCL',color='green', fontsize=15)
    plt.text(count+0.1, data_mean-0.5, 'mean='+'%0.2f'%(data_mean,),color='black', fontsize=15)
    plt.legend(bbox_to_anchor=(1.01, 0.8), loc=2, borderaxespad=0.)
    plt.ylabel("Torque Value", fontsize=15)
    plt.title("Process Control Chart Example", fontsize=24)
    plt.show()

if __name__ == "__main__":
    data = numpy.random.normal(55,5.5,1000)
    mean = numpy.mean(data)
    std  = numpy.std(data)

    UCL = mean + 3 * std
    LCL = mean - 3 * std
    pcc(data,UCL,LCL,xinterval=100)
