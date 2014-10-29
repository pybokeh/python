from scipy.stats import pearsonr
from scipy.stats import linregress
from matplotlib import pyplot as plt
import numpy as np

sat = np.array([595,520,715,405,680,490,565])
gpa = np.array([3.4,3.2,3.9,2.3,3.9,2.5,3.5])

fig1 = plt.figure(1)
ax = plt.subplot(1,1,1)

pearson = pearsonr(sat, gpa)

plt.scatter(sat,gpa, label="data")

# Get linear regression parameters
slope, intercept, r_value, p_value, std_err = linregress(sat, gpa)

# Format the chart
plt.xlabel("SAT Scores")
plt.ylabel("GPA")
plt.title("Scatter Plot with Linear Regression Fit\nY=a*X + b\na=%0.4f, b=%0.4f" % (slope, intercept))
plt.grid()

# Create linear regression x values
x_lr = sat

# Create linear regression y values: Y = slope*X + intercept
y_lr = slope * x_lr + intercept

print "Pearson correlation coefficient: ", pearson[0]
print "Fit x-values: ", str(x_lr)
print "Fit y-values: ", str(y_lr)
print "Fit slope: ",slope
print "Fit intercept: ", intercept
plt.plot(x_lr, y_lr, label="fit")
plt.legend()

plt.show()



