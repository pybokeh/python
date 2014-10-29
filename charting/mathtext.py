# Reference: http://matplotlib.sourceforge.net/users/mathtext.html
# Zi = (Pi-Pavg)/sqr( Pavg*(1-Pavg)/ni )
# Pi = Di / Ni
# Ni = sample size
# Di = number of nonconforming units

import matplotlib.pyplot as plt

fig = plt.figure(1)
ax = fig.add_axes([0,0,1,1])

ax.text(0.5,0.5,r'$\mathtt{Z_i = \frac{\^p_i-p}{\sqrt{\frac{p(1-p)}{n_i}}}}$', fontsize=20)

plt.show()
