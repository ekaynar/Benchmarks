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
