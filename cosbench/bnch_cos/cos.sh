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
rgw="node-1"
buckets=9
workers=30
objects=256
rgw_list=("node-1" "node-2" "node-3")
size="(4)MB"

cosPath=/root/0.5.2
function run1 {
	f_name=$1
	OUTPUT=$(sh $cosPath/cli.sh submit $f_name) &&
	jobId=$(echo $OUTPUT |awk '{print $4}') &&
#	echo "$cosPath/archive/$jobId-rep.144.obj.4m/$jobId-rep.144.obj.4m.csv"
	exist=1
	while [ $exist -eq 1 ];do
	if grep "completed" $cosPath/archive/$jobId-tesing/$jobId-tesing.csv > /dev/null
	then
		exist=0
	fi
	sleep 5
	done
}

run1 $1
#ain $1 $2 $3 $4 $5 $6 $7
#edit_write

