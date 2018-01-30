# Installation of CEPH with Ceph-ansible from ISO
## Download iso file and Key
```
 wget http://perf1.lab.bos.redhat.com/jharriga/SLdec2017_recovery/redhat-build.txt
 wget http://perf1.lab.bos.redhat.com/jharriga/SLdec2017_recovery/RHCEPH-3.0-RHEL-7-20171031.ci.0-x86_64-dvd.iso
 rpm --import redhat-build.txt
```
## Get the latest version of ansible (Make sure the ansible version is > 2.4)
```
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo rpm -i epel-release-latest-7.noarch.rpm 
```
## SETTING DNS NAME RESOLUTION
```
hostname -s
```
## CONFIGURING NETWORK TIME PROTOCOL
```yum install -y ntp
systemctl enable ntpd
systemctl start ntpd
systemctl status ntpd
ntpq -p
```
## List Delete Iptables Firewall Rules
```
iptables -F
iptables -L
```
## ENABLING PASSWORD-LESS SSH  - (Master Node Only)
```
ssh-keygen
ssh-copy-id node1 (repeat for all slave nodes)
```

## Installing Ceph-ansible 
```
yum install -y ceph-ansible
```
* Edit /etc/ansible/hosts
```
[mgrs]
ceph1

[mons]
mon1
mon2
mon3

[osds]
ceph1
ceph2
ceph3
ceph4

[rgws]
rgw1 radosgw_address=10.16.70.111
rgw2 radosgw_address=10.16.70.112
rgw3 radosgw_address=10.16.70.113
```
* Ensure that Ansible can reach the Ceph hosts
```
ansible all -m ping
```
* Create a directory under the home directory so Ansible can write the keys:
```
cd ~
mkdir ceph-ansible-keys
```

* Navigate to the Ceph Ansible group_vars directory
```
cd /root/ceph-ansible/group_vars/
```

* Edit all.yml (cp all.yml.sample all.yml)
```
dummy:
fetch_directory: fetch/
ceph_origin: repository
ceph_repository: rhcs
ceph_repository_type: iso
ceph_stable_rh_storage_iso_path: /root/RHCEPH-3.0-RHEL-7-20171031.ci.0-x86_64-dvd.iso
generate_fsid: true
cephx: true
monitor_interface: enp4s0f0
monitor_address_block:  172.16.0.0/16
journal_size: 5120 # OSD journal size in MB
public_network: 172.16.0.0/16
cluster_network: 172.17.0.0/16 #"{{ public_network }}"
radosgw_civetweb_port: 8080
ceph_conf_overrides:
   mon:
      mon allow pool delete: true
```

* Edit osds.yml (cp osds.yml.sample osds.yml)
```
dummy:
osd_scenario: non-collocated
devices: [ '/dev/sdc','/dev/sdd','/dev/sde','/dev/sdf','/dev/sdaa', '/dev/sdh', '/dev/sdi', '/dev/sdj', '/dev/sdk', '/dev/sdl', '/dev/sdm' ,'/dev/sdn','/dev/sdo', '/dev/sdp', '/dev/sdq', '/dev/sdr', '/dev/sds', '/dev/sdt', '/dev/sdu', '/dev/sdv', '/dev/sdw', '/dev/sdx', '/dev/sdy', '/dev/sdz']
dedicated_devices: ['/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1','/dev/nvme1n1']
```

* Deploying a Ceph Cluster
```
cd /root/ceph-ansible
ansible-playbook site.yml
```

* Purging Ceph Cluster
```
cd /root/ceph-ansible
ansible-playbook purge-cluster.yml
```

## BlueStore installation
* The number of osds per nodes was limited by aio-max-nr. By default its set to 65536 in RHEL 7.4. 
We should increase aio-max-nr for bluestore 
```
ansible -m shell -a "cat /proc/sys/fs/aio-nr" osds
ansible -m shell -a "echo 131072 > /proc/sys/fs/aio-max-nr" osds
```
if you want to make 1M
```
ansible -m shell -a "echo 1048576 > /proc/sys/fs/aio-max-nr" osds
```

Helpuful link:
 - https://access.redhat.com/solutions/2756421
 - http://lists.ceph.com/pipermail/ceph-users-ceph.com/2017-August/020408.html



* Edit all.yml (cp all.yml.sample all.yml)
```
dummy:
fetch_directory: fetch/
ceph_origin: repository
ceph_repository: rhcs
ceph_repository_type: iso
ceph_rhcs_iso_path: /root/RHCEPH-3.0-RHEL-7-20171031.ci.0-x86_64-dvd.iso # "{{ ceph_stable_rh_storage_iso_path | default('') }}"
generate_fsid: true
cephx: true
monitor_interface: enp130s0f0
monitor_address_block:  172.16.0.0/16
journal_size: 5120 # OSD journal size in MB
public_network: 172.16.0.0/16
cluster_network: 172.17.0.0/16 #"{{ public_network }}"
osd_objectstore: bluestore
radosgw_civetweb_port: 8080
radosgw_interface: enp130s0f0
ceph_conf_overrides:
   mon:
      mon allow pool delete: true
```
* Edit osds.yml (cp osds.yml.sample osds.yml)
```
---
dummy:
osd_scenario: non-collocated
devices: [ '/dev/sdc','/dev/sdd','/dev/sde','/dev/sdf','/dev/sdaa', '/dev/sdh', '/dev/sdi', '/dev/sdj', '/dev/sdk', '/dev/sdl', '/dev/sdm' ,'/dev/sdn','/dev/sdo', '/dev/sdp', '/dev/sdq', '/dev/sdr', '/dev/sds', '/dev/sdt', '/dev/sdu', '/dev/sdv', '/dev/sdw', '/dev/sdx', '/dev/sdy', '/dev/sdz']
dedicated_devices: ['/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1']
```


