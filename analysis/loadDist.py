import sys
import numpy as np
import ConfigParser
import logging
from uhashring import HashRing
from clandestined import Cluster
from clandestined import RendezvousHash
##############################################################
## GLobal Variables
#-----------------------------
global hr
trace=[]

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
log_file = config.get('My Section', 'log_file')
logging.basicConfig(filename=log_file,level=logging.DEBUG)

def parser(filename):
	fd =  open(filename, 'r')
	for line in fd:
		value = line.split(" ")
		url = value[2]
		trace.append(url)

def setUp(hashType,nodeNum):
	# node config
	nodes={}
	if (hashType == "consistent"):
		for i in range(int(nodeNum)):
			sname='server'+str(i)
			nodes[str(i)]={'hostname':sname, 'weight': 1}
		
	elif (hashType == "rendezvous"):
		for i in range(int(nodeNum)):
			sname='server'+str(i)
			nodes[str(i)]={'name':sname }
	return nodes

def rendezvousHashing(trace,nodeNum):
	nodes=setUp("rendezvous",nodeNum)
	hr = RendezvousHash(nodes.keys(),seed=1337)
	servers=np.zeros(len(nodes))
	for each in trace:
		index=int(hr.find_node(each))-1
		servers[index]+=1
	print "rendezvousHashing"
	print servers

def consistentHashing(trace,nodeNum):
	nodes=setUp("consistent",nodeNum)
	# create a new consistent hash ring with the nodes
	hr = HashRing(nodes,vnodes=200)
	servers=np.zeros(len(nodes))
	for each in trace:
		index=int(hr.get_node(each))-1
		servers[index]+=1
	print "consistentHashing"
	print servers



if __name__ == "__main__":

## Load the configuration filec
#------------------------------
	input_file = config.get('My Section', 'input_file')	
#	distType = config.get('My Section', 'dist_type')

	
## Parsing the Input File
	logging.info('**************************')
	now = datetime.datetime.now()
	logging.info(str(now)[:19]+'	Parsing File:' + str(input_file))
	parser(input_file)	
	nodeNum=6
	consistentHashing(trace,nodeNum)
	rendezvousHashing(trace,nodeNum)


