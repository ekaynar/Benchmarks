#!/bin/bash
path="/mnt/raid0/traces/twosigma/perdayfiles/upload"
fname=$1
workerIP=("0.0.0.0"  "10.13.67.13")
workers=$2
lines="$(wc $1 | awk '{print $1}')" &&
splitSize=$((lines / workers))

echo "SPpliting Files"
split -l $splitSize $fname part
i=0
for entry in "."/part*
do
    
   files[$i]="$entry"        
    (( i++ ))
done

echo ${files[1]}


echo "Copying Files"
for i in  $(seq 0 $workers)
do
   echo ${workerIP[$i]}
	scp -r ${files[$i]} root@${workerIP[$i]}:$path/${files[$i]}
done

for i in  $(seq 0 $workers)
do
	ssh  root@${workerIP[$i]} "$path/upload.py $path/${files[$i]}" &

done

wait

