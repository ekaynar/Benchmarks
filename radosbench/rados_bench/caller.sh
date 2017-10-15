#!/bin/bash

#usage
#
#
#./clean k m
#./clean 3way

#usage

#inputs from auto.sh script
k=$1
m=$2
run_time=$3
thread=$4
b_size=$5

dram_ips=("node-1" "node-2" "node-3" "gprfc033" "gprfc034" "gprfc035")
clients=("gprfc033" "gprfc034" "gprfc035")

len=${#clients[@]}


function clean_ceph {
echo "Clean Dram of the Ceph and Clients"
for i in ${dram_ips[@]};
do
  ssh root@$i 'sync; echo 3 > /proc/sys/vm/drop_caches'
done
}


function cleanup {
echo "Cleaning Buckets"
for i in ${clients[@]}
do
rados -p default.rgw.buckets.data --run_name $i cleanup &&
echo "clean"
done
}

function single_run {
#echo "-k $k -m $m -t $run_time -p $thread -o $o_size -b $b_size"
rm -rf /var/lib/pbench-agent/pbench-user-benchmark*
clean_ceph &&
pbench-user-benchmark "./radosbench.sh -o write -k $k -m $m -t $run_time -p $thread -b $b_size" && \
mv /var/lib/pbench-agent/pbench-user-benchmark* /var/www/html/pub/radosWrite.$1.$2 && \
echo "Data Writen into the pool" && \
clean_ceph &&
sleep 5

pbench-user-benchmark "./radosbench.sh -o read -k $k -m $m -t $run_time -p $thread  -b $b_size" && \
mv /var/lib/pbench-agent/pbench-user-benchmark* /var/www/html/pub/radosRead.$1.$2 && \
cleanup
}

single_run 

