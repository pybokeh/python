import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 100, 15
x = mu + sigma*np.random.randn(10000)

# n - represents the counts in each bin
# bins - are the x values that respresents the width of the bins
# patches - are the 2 points (x, y) coordinates that represents the bottom left
#           corner of the bin and the top left corner of the bin, see diagram below:
#
#       |           * (x2, y2)
#       |           |
#       |           |
#       |           |
#       |           |
#       |           |
#       |           |
#       * (x1, y1)

# normed = if set to True, means the area of the histogram will equal to 1
# alpha - allows you to control how transparent the histogram will be (1=opaque, 0=transparent)
n, bins, patches = plt.hist(x, 50, normed=True, cumulative=True, facecolor='green', alpha=1)

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('A Histogram')
plt.axis([bins.min(), bins.max(), n.min(), n.max()])
plt.grid(True)
plt.show()
