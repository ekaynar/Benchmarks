## COSBENCH INSTALLATION

# Download COSBench
* Obtain installation package from [github(Releases)](https://github.com/intel-cloud/cosbench/releases) and place it at COSBench package under the /home directory on the controller node.

```
unzip 0.4.2.c4.zip
cd 0.4.2.c4
chmod +x *.sh
```

# Installation
* Install dependencies
```
sudo yum install -y java-1.8.0-openjdk
sudo yum install nc
```

# Single Node 
* Start COSBench Drivers
```
./start-driver.sh
```

* Start COSBench Controller
```
./start-controller.sh
```

* Start COSBench controller and COSBench driver 
```
./start-all.sh
```


# Multinode
* Don't touch the driver.conf file on nodes.
* Run the following command on each node (client node)

```
./start-driver.sh 
```
* Then edit the controller config file on the master node
```
[controller]
drivers = 2
log_level = INFO
log_file = log/system.log
archive_dir = archive

[driver1]
name = driver1
url = http://127.0.0.1:18088/driver

[driver2]
name=driver2
url=http://gprfc078:18088/driver
```
* run the controller from master node
```
./start-controller.sh 
```
# Reset Multinode Cluster
* run from controller node

* Stop drivers and controller
```
cd 0.4.2.c4/
./stop-controller.sh
cd -
for i in `cat client`; do ssh root@$i 'cd /root/0.4.2.c4/; sh stop-driver.sh' ; done
```

* Start drivers and controller
```
cd -
for i in `cat client`; do ssh root@$i 'cd /root/0.4.2.c4/; sh start-driver.sh' ;done
cd 0.4.2.c4/
./start-controller.sh
```
# Visulization
```
<IP_adress_of_Controller>:19088/controller/index.html
```

# Hints
* If you restart Controller, previos workload will not show up on the webpage. CLick the botton to load previoous workload by clicking **unload archived workloads** botton.

* .csv files for each work is stored in **archive** folder (/root/0.4.2.c4/archive)

* Pbench will not work with COSBench properly. COSbench is setting the system clock and mess up the Pbench's time synchronization. You can find more info about the issue on here: https://github.com/intel-cloud/cosbench/issues/340
To solve the issue, I downloaded COSBench source code and remove the line in **cosbench/dev/cosbench-driver-web/src/com/intel/cosbench/driver/handler/PingHandler.java** . Then I build the code with eclipse SDK and it worked fine.



