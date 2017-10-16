#!/usr/bin/python
import getopt
import sys
import commands


##cat pgdump| sed -n '8,1607p' |awk '{print $16}' >> primary_2
array=[]

def get_osd_info():
	sizes= commands.getstatusoutput("""df -h |awk '{print $3 "\t" $6}' |grep osd | awk '{print $1}'""")
        disks=commands.getstatusoutput("""df -h |grep osd |awk '{print $1}' | cut -d "/" -f3 |cut -d "1" -f1""")
        osds= commands.getstatusoutput("""df -h |awk '{print $3 "\t" $6}' |grep osd | cut -d "-" -f2""")
        osd_list=osds[1].split("\n")
        disk_list=disks[1].split("\n")
        size_list=sizes[1].split("\n")
	return osd_list, disk_list, size_list
def read_traces(inputfile):
 	osd_list, disk_list, size_list=get_osd_info()	
	for i in range(36):
		array.append(0)
        fd = open(inputfile, 'r')
	for line in fd:
		array[int(line)]=array[int(line)]+1
	fd.close()
	count=0
	print "size \t disks \t primary_osd \t op_out_bytes \t op_r "#(Client Read operations)"
	for i in range(36):
		if str(i) in osd_list:
			status,op_out_bytes=commands.getstatusoutput("""ceph --admin-daemon /var/run/ceph/ceph-osd.%s.asok perf dump |grep 'op_out_bytes'""" % str(i))
			status,op_r=commands.getstatusoutput("""ceph --admin-daemon /var/run/ceph/ceph-osd.%s.asok perf dump |grep '"op_r":' |tail -1""" % str(i))
			op_bytes= op_out_bytes.split(":")
			op_bytes= op_bytes[1].replace(",","")
			op_reads= op_r.split(":")
			op_reads= op_reads[1].replace(",","")
			print size_list[count],"\t",disk_list[count],"\t", array[i],"\t",op_bytes[1], "\t", op_reads[1]
			count=count+1
		
def reset_counter():
	osd_list, disk_list, size_list=	get_osd_info()
	for i in osd_list:
		status,op_out_bytes=commands.getstatusoutput("""ceph --admin-daemon /var/run/ceph/ceph-osd.%s.asok perf reset all"""%str(i))

def main(argv):
	inputfile = ''
   	try:
      		opts, args = getopt.getopt(argv,"hr=i:")
   	except getopt.GetoptError:
      		print 'test.py -i <inputfile>'
      		sys.exit(2)
   	for opt, arg in opts:
		if opt == '-h':
         		print 'stat.py -i <inputfile> '
         		print 'stat.py -r  '
	         	sys.exit()
      		elif opt == '-r':
		 	print 'reset perf counters'
			reset_counter() 	
		elif opt in '-i':
         		inputfile = arg
			print 'Run statistics'
			read_traces(inputfile)
if __name__ == "__main__":
	
        #read_traces(sys.argv[1:])
        main(sys.argv[1:])

