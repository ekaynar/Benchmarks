
import sys
import numpy as np
import operator
import pandas as pd
from lru import LRU
import ConfigParser
import logging
import tarfile
import datetime
from os import listdir
from os.path import isfile,join
import os
##############################################################

##Configurations
#
oFile="fridgeLogs"
path="/mnt/raid0/traces/twosigma/perdayfiles"
logFilePath="home/tsfridgeprod/log-snapshot/cache.log1"
tarFileName="fridgeLogs.tar.gz"

## Check file is a good file or not
#
def isGoodFile(vmDir,tFile,fd):
	for line in tFile:
		line=line.replace("\n","")
		# Remove below line
#		line="{"+line+"}"
		lineDict=eval(line)
		fullUrl = lineDict['url']
		if fullUrl == '/':
			# Not a good File	
			break
		elif lineDict['cache-reason'] != "ok":
			break 
		else:
			if lineDict['method'] == "GET" and "read" in lineDict['url']:
				fd.write(vmDir+','+line+"\n")


# Extract cache-log files
def getCacheLogFile(path):
	fd=open(oFile,"w")
	for vmDir in listdir(path):
		try:
			tDir= tarfile.open( join(join(path,vmDir),"logs.tar.gz"),'r:gz')
			for tFile in  tDir:
				if tFile.name == logFilePath:
					lFile = tDir.extractfile(tFile)
					isGoodFile(vmDir,lFile,fd)
														

		except:
			continue

	fd.close()



def archieveCacheLogFile(output_filename,source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


if __name__ == "__main__":

	getCacheLogFile(path)
	archieveCacheLogFile(tarFileName,oFile)
	
