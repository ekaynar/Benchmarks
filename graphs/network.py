import numpy as np
import matplotlib.pyplot as plt
import time
import sys

for arg in sys.argv:
	print arg

data = np.genfromtxt(arg, delimiter=',', skip_header=4, names=['x', 'y', 'z','k'])

y_ticks = [1000,2000,3000,4000,5000, 6000, 7000,8000]

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.grid(True)
ax1.yaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1.5)
ax1.set_axisbelow(True)
ax1.plot(data['x'], data['y'], color='b',linewidth=3, label='3way-RX')
ax1.plot(data['x'], data['z'], color='#663399', linewidth=3,label='3way-TX')
ax1.plot(data['x'], data['k'], color='#FFA500', linewidth=3,label='3way-lo-tx')
plt.ylim([0,8000])
plt.tick_params(axis='both', which='major', labelsize=18)
plt.tick_params(axis='both', which='minor', labelsize=18)
plt.ylabel('Network (Mbits/sec)',  fontsize=20)
plt.xlabel('Time',  fontsize=20)
leg=plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0., fontsize=19)
#leg=plt.legend(loc=4, fontsize=18)


# set the linewidth of each legend object
for legobj in leg.legendHandles:
    legobj.set_linewidth(8.0)

#plt.legend()
#labels[1] =  time.gmtime(float(labels[6]))
ax1.set_xticklabels(["","1","2","3","4","5","6"])


plt.show()


