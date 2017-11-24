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
buckets=1000
workers=36
objects=8000
rgw_list=("node-1" "node-2" "node-3")
size="(64)KB"

function edit_write {
	key=$(ssh $rgw 'radosgw-admin user info --uid=johndoe | grep secret_key' | tail -1 | awk '{print $2}' | sed 's/"//g')
	sed  -i "s/password=.*;/password=$key;/g" write.xml &&
	command="s/type=\"prepare\" workers=\".*\" config/type=\"prepare\" workers=\"$workers\" config/g"
	sed  -i "$command" write.xml
	command="s/containers=r(1,.*)\"/containers=r(1,$buckets)\"/g"
	sed  -i "$command" write.xml
	command="s/containers=r(1,.*);obj/containers=r(1,$buckets);obj/g"
	sed  -i "$command" write.xml
	command="s/objects=r(1,.*);s/objects=r(1,$objects);s/g"
        sed  -i "$command" write.xml
	command="s/sizes=c.*\"/sizes=c$size\"/g"
	sed  -i "$command" write.xml
	
}

function edit_read {
        key=$(ssh $rgw 'radosgw-admin user info --uid=johndoe | grep secret_key' | tail -1 | awk '{print $2}' | sed 's/"//g')
        sed  -i "s/password=.*;/password=$key;/g" read.xml
V#        command="s/type=\"prepare\" workers=\".*\" config/type=\"prepare\" workers=\"$workers\" config/g"
#        sed  -i "$command" write.xml
#        command="s/containers=r(1,.*)\"/containers=r(1,$buckets)\"/g"
#        sed  -i "$command" write.xml
#        command="s/containers=r(1,.*);obj/containers=r(1,$buckets);obj/g"
#        sed  -i "$command" write.xml
#        command="s/sizes=c.*\"/sizes=c$size\"/g"
#        sed  -i "$command" write.xml
#

}



function stop_rgw {
	ansible -m shell -a 'systemctl stop ceph-radosgw@rgw.`hostname -s`.service' all
}

function start_rgw {
        ansible -m shell -a 'systemctl start ceph-radosgw@rgw.`hostname -s`.service' all
}

function pool() {
	./pool_mng.sh -r $1 -k $2 -m $3 -d $4 -i $5 -o $6 -f $7 &&
	echo "done"
}

function create_user {

	ssh $rgw 'radosgw-admin user create --uid=johndoe --display-name="John Doe" --email=john@example.com' &&
	ssh $rgw 'radosgw-admin subuser create --uid=johndoe --subuser=johndoe:swift --access=full' 

}

function main {  
	echo "Stopping RGWs" &&
	stop_rgw &&
	echo "Removing and Recreating Pools" &&
	pool $1 $2 $3 $4 $5 $6 $7 &&
	sleep 120
	echo "Starting RGWs" &&
	start_rgw &&
	echo "Creating User" &&
	create_user &&
	edit_write &&
	echo "done"	
}

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

function pbench {
	rm -rf /var/lib/pbench-agent/pbench-user-benchmark* && \
	pbench-user-benchmark "./cos.sh $1" &&
	mv /var/lib/pbench-agent/pbench-user-benchmark* /var/www/html/pub/$2
	

}
main $1 $2 $3 $4 $5 $6 $7 &&
pbench $8 $9
#run1 $8
#ain $1 $2 $3 $4 $5 $6 $7
#edit_write

