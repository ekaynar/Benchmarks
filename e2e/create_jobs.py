#!/usr/bin/python
import getopt
import sys
import getopt
import random
import subprocess
import operator
import hashlib
dict={}
f_size=512
thread=72

f_name="files"
f_job_name="jobs"

def create_files(argv):
	fd = open(sys.argv[1], 'r')
	out = open(f_name, 'w')
	out2 = open(f_job_name, 'w')
	filename=0
	jcount=0
	#hash={
	sume=0
	bucket=0
        for line in fd:
                value = line.split(" ")
		key=value[2]
		length =value[2].split("length=")[1].replace("\n","")
		if key not in dict:
			dict[key]=filename
			sume+=int(length)
			#files = "sort128G "+"inputPath"+str(bucket)+" "+"file"+str(filename)+" "+str(length) +" \n"
			files = "sort128G "+"file"+str(filename)+" "+str(length) +" \n"
			out.write(files)
			filename+=1
		#req = "sort128G "+"inputPath"+str(bucket)+" file"+str(dict[key]) +" "+"job"+str(jcount)+" "+str(1)+" \n"
		req = "sort128G "+"file"+str(dict[key]) +" "+"job"+str(jcount)+" "+str(1)+" \n"
		out2.write(req)
		jcount+=1
		
		if filename%625 ==0:
			bucket+=1
	#	print files
		
			
	print len(dict)
	print filename
	print sume
        fd.close()
        out.close()
        out2.close()



if __name__ == "__main__":
	create_files(sys.argv[1:])
