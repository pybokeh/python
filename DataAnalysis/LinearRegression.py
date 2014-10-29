import numpy as np
import matplotlib.pyplot as plt

N = 100
start = 0
end = 1

A = np.random.rand()
B = np.random.rand()

x = np.linspace(start, end, N)
print x

y = A * x + B
print "Printing y...\n"
print y


print "Printing y+=...\n"
y = y + np.random.randn(N)/50
print y

p = np.polyfit(x, y, 1)

plt.figure()

plt.plot(x, y, 'o', label='Measured data; A=%.2f, B=%.2f' % (A,B))
plt.plot(x, np.polyval(p, x), '-', label='Linear regression; A=%.2f, B=%.2f' % tuple(p))
plt.legend(loc='best')
plt.show()
