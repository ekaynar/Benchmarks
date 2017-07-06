## COSBENCH INSTALLATION

# Download CosBench
* Obtain installation package from github(Releases) and place it at COSBench package under
the /home directory on the controller node.

```
unzip 0.4.2.c4.zip
cd 0.4.2.c4
chmod +x *.sh
```
# Installation
* Install Java
```
sudo yum install -y java-1.8.0-openjdk
```

* install nc
```
 sudo yum install nc
```

* Run Drivers
```
./start-driver.sh
```

* Run Controller
```
./start-controller.sh
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

# Visulization
```
<IP_adress_of_Controller>:19088/controller/index.html
```
