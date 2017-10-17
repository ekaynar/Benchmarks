#!/bin/bash

clients=("gprfs017" "gprfs018" "gprfs019")

function reset_counter {
for i in ${clients[@]}
do
	ssh $i "python stat.py -r" &
done
wait
}

function stats {
for i in ${clients[@]}
do
        echo $i &&
	ssh $i "python stat.py -s" 
done
wait
}

while [[ $# -gt 0 ]]
do
key="$1"
case $key in
-r|--reset)
    echo "Reset Counters"
    reset_counter
    shift # past argument
    shift # past value
    ;;
-s|--stat)
    echo "Running Stats"
    stats
    shift # past argument
    shift # past value
    ;;
esac
done



