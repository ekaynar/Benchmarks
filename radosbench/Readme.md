Rados Bench comes with ceph-common package.
Make sure you have the latest version of to display IOPS, Average Bandwidth, Average IOPS ...etc

REGISTERING TO CDN
==============================
```
subscription-manager register
subscription-manager list --available
subscription-manager attach --pool=8a85f9815e3f19a8015e3fb6f1671f1c
subscription-manager repos --enable=rhel-7-server-rpms
yum update
```
ENABLING CEPH REPOSITORIES
==============================
```
subscription-manager repos --enable=rhel-7-server-rhceph-2-mon-rpms
subscription-manager repos --enable=rhel-7-server-rhceph-2-osd-rpms
subscription-manager repos --enable=rhel-7-server-rhceph-2-tools-rpms
```

Installation
==============================
```
yum install -y ceph-common
scp /etc/ceph/ceph.client.admin.keyring from ceph cluster
scp /etc/ceph/ceph.conf from ceph cluster
```
All the nodes - CONFIGURING NETWORK TIME PROTOCOL 
==============================
```
yum install -y ntp
systemctl enable ntpd
systemctl start ntpd
systemctl status ntpd
ntpq -p
```

Check
=====
```
ceph -s
````
