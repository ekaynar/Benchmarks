
import sys
import numpy as np
import operator
import pandas as pd
from collections import deque
from lru import LRU
import ConfigParser
import lfucache.lfu_cache as LFU
import logging
import datetime
##############################################################
## GLobal Variables
#-----------------------------
key=[]
trace=[]
osize=[]
dict={}
accessCount=0

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
log_file = config.get('My Section', 'log_file')
logging.basicConfig(filename=log_file,level=logging.DEBUG)


## Parsing the input file
## Get object ID,size and calculate footprint of
## input data for calculating the cache size, 
#----------------------------------------------

#{"remote-addr":"127.0.0.1","user-principal":"-","date":"2018-02-02T16:51:07.004Z","method":"GET","url":"https://celfs.cfsrs1rs92.dft.twosigma.com:10012/celfs/locatecel/dcat?cel=0_26833&pid=1091&path=3","http-version":"1.1","status":"200","content-length":"244","user-agent":"CelFS/20171212.2 Java (app=com.twosigma.simulator.PrefsSimRun,module=ts_pithos_sys_core,pid=967,realm=CB.TWOSIGMA.COM)","request-time":"1","cache-hit":"CacheHit","cache-time":"1","cache-reason":"ok","cache-hit-local-chunks":"1","cache-hit-non-local-chunks":"-","cache-hit-local-bytes":"810","cache-hit-non-local-bytes":"-","cache-timing":"cipherGet=-90376,firstChunkRead=55,followingChunks=1,decrypt=0","response-time":"0.53596","pid":"28851","keyserver-details":"keyUseCounter=0,keyserversKnown=0,keyserverShuffleCount=0,keyserverUrl=,knownStorageInstances=1521,keySizeKnown=-1,wasHotCache=1"}
#"remote-addr":"127.0.0.1","user-principal":"-","date":"2018-02-02T16:51:07.004Z","method":"GET","url":"http://cfssch1rs9.dft.twosigma.com:10010/celfs/read/vwx_EU_30/4799/4799/metadata/data/EU.dir.xml?offset=0&length=254","http-version":"1.1","status":"200","content-length":"244","user-agent":"CelFS/20171212.2 Java (app=com.twosigma.simulator.PrefsSimRun,module=ts_pithos_sys_core,pid=967,realm=CB.TWOSIGMA.COM)","request-time":"1","cache-hit":"CacheHit","cache-time":"1","cache-reason":"ok","cache-hit-local-chunks":"1","cache-hit-non-local-chunks":"-","cache-hit-local-bytes":"810","cache-hit-non-local-bytes":"-","cache-timing":"cipherGet=-90376,firstChunkRead=55,followingChunks=1,decrypt=0","response-time":"0.53596","pid":"28851","keyserver-details":"keyUseCounter=0,keyserversKnown=0,keyserverShuffleCount=0,keyserverUrl=,knownStorageInstances=1521,keySizeKnown=-1,wasHotCache=1"

def parse(fname):
        fd = open(fname, 'r')
        data=0
	fp=0
	accessCount=0
	for line in fd:
                value = line.split(",")
		if ((value[3].split(":")[1].replace("\"","") == "GET") and ("read" in value[4])) :
			url = value[4].split("http://")[1].replace("\"","")
			offset = url.split("?")[1].split("&")[0].split("=")[1]
			lenght = url.split("?")[1].split("&")[1].split("=")[1]
			accessCount += 1
 			trace.append(url)
			if url not in dict:
				dict[url]= lenght
				fp+=int(lenght)	    
        fd.close()
	now = datetime.datetime.now()
	logging.info(str(now)[:19]+ "	Footprint " + str(fp))

## FIFO eviction policy
#-----------------------------
def fifo(size):
	hitCounter=missCounter=0
        #Size in GB
        size = spaceLeft= int(size)*1024*1024*1024
	hashmap={}
	fifo=deque()
	for key in trace:
		if key in hashmap:
			hitCounter+=int(dict[key])
		else:
			missCounter+=int(dict[key])
			if (int(dict[key]) <= spaceLeft):
				fifo.append(key)
				hashmap[key]=dict[key]
                                spaceLeft -= int(dict[key])	
			else:
				while(dict[key] > spaceLeft):
					id=fifo.popleft()
					spaceLeft+=hashmap[id]
					del hashmap[id]
				hashmap[key]=dict[key]
				fifo.append(key)
                                spaceLeft -= int(dict[key])

	print "Hit_Counter:"+str(hitCounter)+",Miss_Counter:"+str(missCounter)
	print "Miss_Ratio:"+ str(float(missCounter)/ float(hitCounter+missCounter))
	logging.info( str(now)[:19]+"	Hit_Counter:"+str(hitCounter)+",Miss_Counter:"+str(missCounter))	
        logging.info( str(now)[:19]+"	Miss_Ratio:"+ str(float(missCounter)/ float(hitCounter+missCounter)))	


def lru(size):
	hitCounter=missCounter=0
	#Size in GB
 	size = spaceLeft= int(size)*1024*1024*1024
        hashmap={}
	cache = LRU(size)
	for key in trace:
		if key in hashmap:
			hitCounter+=int(dict[key])
			cache[key]=dict[key]
		else:
			missCounter +=int(dict[key])
			# Miss no Eviction
			if (int(dict[key]) <= spaceLeft):
				cache[key]=dict[key]
				hashmap[key]=dict[key]
				spaceLeft -= int(dict[key])
			else:
			# Miss - Cache Eviction	
				while(dict[key] > spaceLeft):
					id = cache.peek_last_item()[0]	
				 	spaceLeft+=int(hashmap[id])
                                        del cache[id]
					del hashmap[id]
				hashmap[key]=dict[key]
                                cache[key]=dict[key]
                                spaceLeft -= int(dict[key])
        now = datetime.datetime.now()
	print "Hit_Counter:"+str(hitCounter)+",Miss_Counter:"+str(missCounter)
	print "Miss_Ratio:"+ str(float(missCounter)/ float(hitCounter+missCounter))
	logging.info( str(now)[:19]+"	Hit_Counter:"+str(hitCounter)+",Miss_Counter:"+str(missCounter) )	
        logging.info( str(now)[:19]+"	Miss_Ratio:"+ str(float(missCounter)/float(hitCounter+missCounter)) )	

def lfu(ratio,output_file,data):
	hit=miss=0
        size = avail = float(data * ratio)/100
        hashmap={}
        avail=int(avail)
	cache = LFU.Cache()
	for i in range(len(key)):
                if key[i] in hashmap:
			if(i>14915099):
				hit+=int(osize[i])
			cache.access(key[i])
		else:
			if(i>14915099):
				miss+=int(osize[i])
			if (int(osize[i]) <= avail):
                        	cache.insert(key[i],"a")
                                hashmap[key[i]]=int(osize[i])
                                avail -= int(osize[i])
			else:
				while(int(osize[i]) > avail):
					id = cache.get_lfu()[0]
					avail+=int(hashmap[id])
					cache.delete_lfu()
					del hashmap[id]
	 			hashmap[key[i]]=osize[i]
				cache.insert(key[i],"a")
				avail -= int(osize[i])
        fd = open("lfu.res","a")
        fd.write(str(hit)+","+str(miss)+"\n")
        fd.close()
        logging.info("Hit Ratio:"+str(hit))
        logging.info("Miss Ratio:"+str(miss))
        print hit, "," , miss


if __name__ == "__main__":

## Load the configuration filec
#------------------------------
	input_file = config.get('My Section', 'input_file')	
	cache_size= config.get('My Section', 'cache_size').split(",")
	cache_type = config.get('My Section', 'cache_type')

	print input_file, cache_size, cache_type

## Parsing the Input File
	logging.info('**************************')
	now = datetime.datetime.now()
	logging.info(str(now)[:19]+'	Parsing File:' + str(input_file))
	parse(input_file)	
	for i in cache_size:
		if cache_type =="lru":
			now = datetime.datetime.now()
			logging.info(str(now)[:19]+ '	Eviction Policy: LRU '+ 'Cache Size: '+str(i)+" GB" )
			lru(i)	

		elif cache_type =="fifo":
			now = datetime.datetime.now()
                	logging.info(str(now)[:19]+ '   Eviction Policy: FIFO '+ 'Cache Size: '+str(i)+" GB" )
                	fifo(i)
## Running Single Level Cache
#	if cache_type == "fifo":
#		logging.info('Eviction Policy: FIFO' )
#		for i in xrange(1,size_ratio+1):
#			fifo(i, output_file,data)
#	if cache_type =="lru":
#		logging.info('Eviction Policy: LRU' )
#		for i in xrange(1,size_ratio+1):
#		liste=[0.2,0.3,0.4]
		
#		for i in liste:
#			lru(i, output_file,data)
		
#	elif cache_type =="lfu":
#               logging.info('Eviction Policy: LFU' )
#                for i in xrange(1,size_ratio+1):
#                        lfu(i, output_file,data)
		
   	#test(sys.argv[1:])
