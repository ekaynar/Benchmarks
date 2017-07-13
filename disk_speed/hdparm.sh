#!/bin/bash


file="hdparmRes"
date > $file
for i in `cat /proc/partitions | awk {'print $4'} |grep 1 |grep sd | tail -n +3`
do
 sudo hdparm -t --direct /dev/$i >> $file
wait
done


ave=$(cat $file | grep MB/sec | awk {'print $11'} | awk '{s+=$1} END {print "Average: " s/NR }')
#Max value
max=$(cat $file | grep MB/sec | awk {'print $11'} |sort -nr | head -1)
#Min value
min=$(cat $file | grep MB/sec | awk {'print $11'} |sort -nr | tail -1)

echo $ave >> $file
echo "Max: " $max >> $file
echo "Min: " $min >> $file

