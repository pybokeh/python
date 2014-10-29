import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

sample = np.random.normal(49.74, 1.1, 1000)
ecdf = sm.distributions.ECDF(sample)
x = np.linspace(min(sample), max(sample))
y = ecdf(x)
plt.step(x, y)
plt.title("Empirical CDF", weight="bold")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)

plt.show()
