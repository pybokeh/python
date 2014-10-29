# Basic plotting using matplotlib
# Shows how to create subplots and adding x/y axis and tick marks
# Also shows how you can set tick label size/rotation

from pylab import *


xstart = -4
xend   =  4
x = arange(-4,xend+1,1)
y = x ** 2
y2 = x

fig = figure()
ax1 = subplot(2,1,1)
# Get current axis
current_axis = gca()
for label in current_axis.get_xticklabels() + current_axis.get_yticklabels():
    label.set_fontsize(10)

plot(x,y)
axhline(color='gray')
axvline(color='gray')
xticks(x, rotation=0)
yticks(arange(min(y)-2,max(y)+2,1))
title('y=x^2', fontsize=20)
xlabel('X', rotation=0)
ylabel('Y', rotation=0)
axis('scaled')
grid()

ax2 = subplot(2,1,2)
plot(x,y2)
axhline(color='gray')
axvline(color='gray')
xticks(x)
yticks(arange(min(y2)-2,max(y2)+2,1))
xlabel('X', rotation=0)
ylabel('Y', rotation=0)
grid()
axis('scaled')
show()


"""
# Subplotting 2x2 Plots Example
fig = figure()
subplot(2,1,1)
title('Upper Half')
subplot(2,2,3)
title('Bottom Left')
subplot(2,2,4)
title('Bottom Right')
show()"""
