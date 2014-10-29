from numpy import *
from matplotlib.ticker import FuncFormatter
import pylab as p

# I'm used to  the ln notation for the natural log
from numpy import log as ln

# Paramters
beta = 5.2
eta = 12

# Genrate 10 numbers following a Weibull distribution
x = eta *random.weibull(beta, size=10)
F = 1 - exp( -(x/eta)**beta )

# Estimate Weibull parameters
lnX = ln(x)
lnF = ln( -ln(1-F) )
a, b = polyfit(lnF, lnX, 1)
beta0 = 1/a
eta0  = exp(b)

# ideal line
F0 = array([1e-3, 1-1e-3])
x0 = eta0 * (-ln(1-F0))**(1/beta0)
lnF0 = ln(-ln(1-F0))


# Weibull plot
p.figure()
ax = p.subplot(111)
# This adds the data points onto the chart
p.semilogx(x, lnF, "bs")
# This adds the ideal line to the chart
p.plot(x0, lnF0, 'r-', label="beta= %5G\neta = %.5G" % (beta0, eta0) )
p.grid()
p.xlabel('x')
p.ylabel('Cumulative Distribution Function')
p.legend(loc='lower right')

# ticks
def weibull_CDF(y, pos):
    return "%G %%" % (100*(1-exp(-exp(y))))

formatter = FuncFormatter(weibull_CDF)
ax.yaxis.set_major_formatter(formatter)

yt_F = array([ 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5,
           0.6, 0.7, 0.8, 0.9, 0.95, 0.99])
yt_lnF = ln( -ln(1-yt_F))
p.yticks(yt_lnF)
