#!/bin/bash
#
#
#clients=("localhost")
clients=("gprfc033" "gprfc034" "gprfc035")
pathWrite="/root/radosWriteRes"
pathRead="/root/radosReadRes"
summary="summary"

function write_obj {
echo "Running Rados Write"
for i in ${clients[@]}
do
ssh $i "rados bench -p default.rgw.buckets.data $run_time write -t $thread -b $b_size --run_name $i --no-cleanup" &
done
wait
}

function read_obj {
echo "Running Rados Read"
for i in ${clients[@]}
do
ssh $i "rados bench -p default.rgw.buckets.data $run_time seq -t $thread --run_name $i" &
done
wait
}

function read (){
echo "Running Read"
for i in 1
do
        read_obj
done >> $1
}
function write (){
echo "Running Write"
for i in 1
do
        write_obj
done >> $1
}

function parsing {
cat $1 |grep "Average IOPS" | awk '{print $3}' |awk '{ sum += $1 } END { if (NR > 0) print "Average IOPS " sum / NR }'
cat $1 |grep "Average IOPS" | awk '{print $3}' |awk '{ sum += $1 } END { if (NR > 0) print "SUM IOPS " sum }'
cat $1 |grep "Max latency*" | awk '{print $3}' |sort -g -r | head -1 | awk '{print "Max Latency " $1}'
cat $1 |grep "Bandwidth (MB/sec)" | awk '{print $3}' |awk '{ sum += $1 } END { if (NR > 0) print "Average Bandwidth " sum / NR }'
cat $1 |grep "Bandwidth (MB/sec)" | awk '{print $3}' |awk '{ sum += $1 } END { if (NR > 0) print "Agg Bandwidth " sum }'
}

while getopts o:k:m:t:p:b: OPTION
do
 case "${OPTION}" in
 o) o=${OPTARG};;
 k) k=${OPTARG};;
 m) m=${OPTARG};;
 t) run_time=${OPTARG};;
 p) thread=${OPTARG};;
 b) b_size=${OPTARG};;
 esac
done

if [[ "$o" == "write" ]] ;then
	filename=$pathWrite/radosBench.$k.$m
	date > $filename
	write $filename &&
	sleep 3
	parsing $filename
	res=$(parsing $filename)
	echo $res >> $filename
	echo "Results for RadosWriteBench $k,$m ,time:$run_time" >> $pathWrite/$summary
	echo $res >> $pathWrite/$summary
else	
	filename=$pathRead/radosBench.$k.$m
        date > $filename
        read $filename &&
	sleep 3
	parsing $filename 
	res=$(parsing $filename) 
	echo $res >> $filename
	echo "Results for RadosReadBench $k,$m ,time:$run_time" >> $pathRead/$summary
	echo $res >> $pathRead/$summary
fi

