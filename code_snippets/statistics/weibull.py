import matplotlib.pyplot as plt
import numpy as np

def weib(x, scale, beta):
    return (beta / scale) * (x / scale)**(beta - 1) * np.exp(-(x / scale)**beta)

x = np.arange(1,100.)/50.
print weib(x, 1., 5.)
print weib(1., 1., 5.)
count, bins, ignored = plt.hist(np.random.weibull(5., 1000))
scale = count.max()/weib(x, 1., 5.).max()
print count.max()
print scale
plt.plot(x, weib(x,1.,5.)*scale)


plt.grid()
plt.show()
