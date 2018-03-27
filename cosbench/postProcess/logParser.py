#!/usr/bin/python
from datetime import datetime
import argparse
import collections
import datetime
from collections import OrderedDict
def printRunSummary(out,fname):
	print "RUN SUMMARY"
	print "-----------"
	out.write("RUN SUMMARY\n")
	out.write( "-----------\n")
	fd=open(fname,"r")
 	for line in fd:
		if ("COSbench jobID" in line):
			if("Started" in line):
				jobID = line.split("is:")[1].split("-")[0].replace(" " ,"")
				jobStart = line.split("COSbench")[0].replace(" " ,"")
				jobStart = jobStart[:-1]
				print "COSbench jobID:" , jobID
				print "RUN START TIME:" , jobStart
				out.write("COSbench jobID: "+ jobID+"\n")
				out.write("RUN START TIME: " + jobStart+"\n")
			if ("Completed" in line):
				jobEnd = line.split("COSbench")[0].replace(" " ,"")
				jobEnd = jobEnd[:-1]
				print "RUN END TIME:" , jobEnd
				out.write("RUN END TIME: " + jobEnd+"\n")
	d1 = datetime.datetime.strptime(jobStart, '%Y/%m/%d:%H:%M:%S')
	d2 = datetime.datetime.strptime(jobEnd, '%Y/%m/%d:%H:%M:%S')
	diff = int((d2 - d1).total_seconds() )
	print "TOTAL RUN DURATION", str(diff), "seconds"
	out.write("TOTAL RUN DURATION "+str(diff)+" seconds")
	fd.close()

def printPerStage(out,dict,ceph):
	print "\nPER stage information:"
	print "----------------------"
        out.write("\n\nPER stage information:\n")
	out.write("------------------------\n")
	startFD=0
	endFD=1	
	for key in dict:
        	print "STAGE NAME: "+ key
                out.write("STAGE NAME: "+key+"\n")
		print ceph[startFD]
                out.write(ceph[startFD]+"\n")

		print "START Time :" , dict[key][0]
                out.write("START Time :" + dict[key][0]+"\n")
	
                print "FAILURE Time :" , dict[key][1]
                out.write("FAILURE Time :" + dict[key][1]+"\n")

                print "RECOVERY Time :" , dict[key][2]
                out.write("RECOVERY Time :" + dict[key][2]+"\n")
                
		print "END Time :" , dict[key][3]
                out.write("END Time :" + dict[key][3]+"\n")

		print ceph[endFD]
                out.write(ceph[endFD])
                out.write("\n\n")
		print "\n"

		startFD+=1
		endFD+=1

def collectPerStage(out,fname):
	cephStat=[]
	fd=open(fname,"r")
	stageStart=stageEnd=recStart=0
	ceph = ""
	dict=OrderedDict()
	for line in fd:
                if ("START:" in line) and ("Cleanup" not in line):
			stageStart = line.split("START:")[0].replace(" " ,"")
                       	stageStart = stageStart[:-1]
			stageName = line.split("START:")[1].split("-")[0]
			if stageName not in dict.keys():
				dict[stageName]=[stageStart]
				
		elif("FAILURE:" in line):
			recStart = line.split("FAILURE:")[0].replace(" " ,"")
                       	recStart = recStart[:-1]
			dict[stageName].append(recStart)
		elif("RECOVERY:" in line):
			recStart = line.split("RECOVERY:")[0].replace(" " ,"")
                       	recStart = recStart[:-1]
			dict[stageName].append(recStart)
		elif ("END:" in line) and ("Cleanup" not in line):
			stageEnd = line.split("END:")[0].replace(" " ,"")
                       	stageEnd = stageEnd[:-1]
			dict[stageName].append(stageEnd)
		elif ("%RAW USED") in line:
			nextline = fd.next().replace("\n","").split(" ")
		 	nextline = filter(None, nextline)	
			ceph = "ceph df = %RAW USED " + nextline[len(nextline)-1]
		elif ("%USED") in line:
			nextline = fd.next().replace("\n","").split(" ")
		 	nextline = filter(None, nextline)	
			ceph += " and buckets.data "  + nextline[len(nextline)-1]
			cephStat.append(ceph)
	fd.close()
	return dict,cephStat

def GetJobID(fname):
	fd=open(fname,"r")
 	for line in fd:
		if ("COSbench jobID" in line):
			if("Started" in line):
				jobID = line.split("is:")[1].split("-")[0].replace(" " ,"")
				fd.close()
				return jobID
	return None

if __name__ == "__main__":
      	parser = argparse.ArgumentParser(description='Simulate a cache')
        parser.add_argument('-d','--archieve', help='Archieve Directory for Workload Logs', required=True)
        arguments = vars(parser.parse_args())
	
	param=arguments['archieve']
	jobID = GetJobID(param)
	if jobID == None :
		print "There is no job"
		exit(0)	

	output=jobID+"-summary"
	out=open(output,"w")

	printRunSummary(out,param)
	dict,ceph = collectPerStage(out,param)
	printPerStage(out,dict,ceph)
	out.close()
