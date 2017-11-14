#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

mu, sigma = 100, 15
x = mu + sigma*np.random.randn(10000)

#xx = [100]*1000
xx = [1, 5, 6,  33, 55, 5, 23, 45 ,98, 65, 45, 1, 33, 44, 34, 98, 95]
x = np.array(xx)




print x

# the histogram of the data
n, bins, patches = plt.hist(x, 10, facecolor='green', alpha=0.75)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('file size')
plt.ylabel('count')
plt.title('Histogram of file size')
plt.axis([0, 50, 0, 17])
plt.grid(True)

plt.show()
