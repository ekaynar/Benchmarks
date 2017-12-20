#!/usr/bin/python
import getopt
import sys
import subprocess
from subprocess import call
import random
import hashlib
from multiprocessing.dummy import Pool as ThreadPool 
import collections
import os
import time
import os.path
dict={}

f_name="files"
f_job_name="jobs"
filenames=[]
sizes=[]

def swift(file,lenght):
#	print file
	with open(file, 'wb') as fout:
        	fout.write(os.urandom(int(lenght)))
#	command= "swift -A http://localhost:80/auth/1.0 -U hadoop:swift -K rLSuhyfNbWZBWRFzXMhqzgHIssyaKa01aEPUKTgh upload sort128G "+ file
#	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
#	process.wait()
	time.sleep(2)
	os.remove(file)
def product_helper(args):
	return swift(*args)

def calculateParallel(key,size):
	pool = ThreadPool(100)
	job_args = [(item_a, size[i]) for i, item_a in enumerate(key)]
	results = pool.map(product_helper,job_args)
	

def upload(argv):
	fd = open(sys.argv[1], 'r')
	filename=1
	jcount=1
	#hash={}
	count =1
  
        for line in fd:
                value = line.split(" ")
		if line not in dict:
			dict[value[1]]=value[2].replace('\n','')
			filenames.append(value[1])
			sizes.append(dict[value[1]])
#			print value[1],value[2]
		if count ==1000:
			break;
		count+=1
        fd.close()
	
	calculateParallel(filenames,sizes)

if __name__ == "__main__":
	upload(sys.argv[1:])

