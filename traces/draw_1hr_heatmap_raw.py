#!/usr/bin/python

import re
import glob
import os
import string
import argparse
import sys
import getopt
import random
from collections import deque
import subprocess
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import math

fnt_sz = 14
inpf = open("histogram_file.csv", "r")
inpf_content = inpf.readlines()
hrly_accesses = []
cntr = 0
for line in inpf_content:
	line_split = line.split("\n")[0]#.replace("[","")#.replace("]","")
	tmp = (line_split.replace("[", "")).replace("]","")
	tmp_split = tmp.split(",")
	new_list = [float(key) for key in tmp_split]	
	hrly_accesses.append(new_list)
	cntr += 1

print len(hrly_accesses)
print hrly_accesses[23]
#exit(0)
external = []
for i in xrange(len(hrly_accesses[0])):
        internal = []
        for element in hrly_accesses:
		print i, element
                internal.append(element[i])
        external.append(internal)

hrly_accesses = external
data_1000 = np.array(hrly_accesses)


fig, ax = plt.subplots(1)
gran = 1
data_range = 24 * gran
heatmap = ax.pcolor(data_1000, cmap=plt.cm.Reds, norm=LogNorm())
#fig.colorbar(heatmap)
cbar = fig.colorbar(heatmap)#.yticks(fontsize = fnt_sz)#, fontsize = fnt_sz)
cbar.ax.tick_params(labelsize=fnt_sz)
ax.set_xticks([x for x in range(0,data_range,24)])
ax.set_yticks([x for x in range(0,data_range,24)])
#plt.title('Bytes read heat-map')
plt.xlabel('First access time (in hours)', fontsize=fnt_sz)
plt.ylabel('Time (in hours)', fontsize=fnt_sz)
plt.xticks(fontsize = fnt_sz)
plt.yticks(fontsize = fnt_sz)
plt.savefig('new_FB_1hr_heatmap_byte_raw.pdf', format='pdf', dpi=1000)
plt.show()


inpf = open("raw_hr_heatmap_data.txt", "r")
inpf_content = inpf.readlines()
hrly_accesses = []
cntr = 0
for line in inpf_content:
        line_split = line.split("\n")[0]#.replace("[","")#.replace("]","")
        tmp = (line_split.replace("[", "")).replace("]","")
        tmp_split = tmp.split(",")
        new_list = [float(key) for key in tmp_split]
        hrly_accesses.append(new_list)
        cntr += 1

external = []
for i in xrange(len(hrly_accesses[0])):
        internal = []
        for element in hrly_accesses:
                internal.append(element[i])
        external.append(internal)

hrly_accesses = external
data_1000 = np.array(hrly_accesses)


fig, ax = plt.subplots(1)
gran = 1
data_range = 24 * gran
heatmap = ax.pcolor(data_1000, cmap=plt.cm.Reds, norm=LogNorm())
#fig.colorbar(heatmap)
cbar = fig.colorbar(heatmap)#.yticks(fontsize = fnt_sz)#, fontsize = fnt_sz)
cbar.ax.tick_params(labelsize=fnt_sz)
ax.set_xticks([x for x in range(0,data_range,24)])
ax.set_yticks([x for x in range(0,data_range,24)])
#plt.title('Accesses heatmap')
plt.xlabel('First access time (in hours)', fontsize = fnt_sz)
plt.ylabel('Time (in hours)', fontsize = fnt_sz)
ax.annotate('Total number of bytes read: 1097 TB', xy=(120, 1), xycoords='figure pixels', fontsize=14)
plt.xticks(fontsize = fnt_sz)
plt.yticks(fontsize = fnt_sz)
plt.savefig('new_FB_1hr_heatmap_access_raw.pdf', format='pdf', dpi=1000)
plt.show()




exit(0)
