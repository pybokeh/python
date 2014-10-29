# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# http://osdir.com/ml/python.matplotlib.general/2005-10/msg00029.html

import pandas
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

xls = pandas.ExcelFile(r"D:\_mycode\python\data\geographical\50_States_To_Lon_Lat.xls")
df = xls.parse("Lon_Lat", index_col=0)

map = Basemap(projection='cyl',llcrnrlon=-180,llcrnrlat=10, urcrnrlon=-40, urcrnrlat=75)

# draw coastlines, country boundaries, fill continents.
map.drawcoastlines()
map.drawcountries(linewidth=1.5)
map.drawstates(linewidth=1, color='gray')
map.fillcontinents(color = 'white')

# draw the edge of the map projection region (the projection limb)
map.drawmapboundary()

# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0, 360, 10))
map.drawparallels(np.arange(-90, 90, 10))

lon = df['LON'][:10].values
lat = df['LAT'][:10].values

x, y = map(lon, lat)

fig1 = plt.figure(1)
fig1.set_size_inches(9,11)
plt.plot(x, y, 'ro', markersize=3)

plt.show()


