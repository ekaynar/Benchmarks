#!/bin/bash
#
#
#Usage
#rados bench -p <pool_name> <seconds> <write|seq|rand>


## Configurations
run_time=30
ceph_ips=("gprfs033" "gprfs034" "gprfs035" "gprfs036")
rgw_ip="gprfc085"
path="/root/radosBenchRes"


function clean_ceph {
echo "Clean Ceph Dram"
for i in ${ceph_ips[@]}; 
do
    ssh root@$i 'sync; echo 3 > /proc/sys/vm/drop_caches'

done
}

function clean_rgw {
echo "Clean RGW Dram"
ssh root@$rgw_ip 'sync; echo 3 > /proc/sys/vm/drop_caches'
}

function create_obj {
echo "Creating the Objects"
rados bench -p default.rgw.buckets.data $run_time write --no-cleanup 
}

function seq_read {
echo "Running Seq Read"
rados bench -p default.rgw.buckets.data $run_time seq
}


function clean_up {
echo "Clean UP"
rados -p default.rgw.buckets.data cleanup
}

function parsing () {

cat $1 |grep "Average IOPS" | awk '{print $3}' |awk '{ sum += $1 } END { if (NR > 0) print "Average IOPS " sum / NR }'
cat $1 |grep "Max latency(s)" | awk '{print $3}' |sort -g -r | head -1 | awk '{print "Max Latency " $1}'

}

function run (){
create_obj &&
sleep 3
echo "Running Seq Read"
for i in {1..5}
do
	echo $i
	clean_rgw &&
	clean_ceph &&
    	seq_read 
done >> $1
clean_up
}


while getopts k:m: OPTION
do
 case "${OPTION}" in
 k) k=${OPTARG};;
 m) m=${OPTARG};;
 esac
done

filename=$path/radosBench.$k.$m
echo $filename
date > $filename
run $filename &&
parsing $filename 
parsing $filename >> $filename

exit 1

