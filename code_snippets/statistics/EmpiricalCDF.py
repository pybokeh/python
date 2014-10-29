import numpy as np
from scikits.statsmodels.tools.tools import ECDF
import matplotlib.pyplot as plt

sample = np.random.uniform(0,1,50)
sample2 = np.random.normal(0,0.5,1000)
ecdf = ECDF(sample)
ecdf2 = ECDF(sample2)
x = np.linspace(min(sample),max(sample))
x2 = np.linspace(min(sample),max(sample2))
y = ecdf(x)
y2 = ecdf2(x2)
#plt.step(x,y)
plt.step(x2,y2)
plt.show()
