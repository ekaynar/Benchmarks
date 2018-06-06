# Installation of Ceph-linode Cluster with Ceph-ansible from ISO
## Get the latest version of ansible (Make sure the ansible version is > 2.4)
  * Download iso file
  ```
  mkdir /root/staging_area/
  cd /root/staging_area
  wget http://download-node-02.eng.bos.redhat.com/composes/auto/ceph-3.0-rhel-7/latest-RHCEPH-3-RHEL-7/compose/OSD/x86_64/iso/RHCEPH-3.0-RHEL-7-20180604.ci.0-x86_64-dvd.iso
  ```
 * Mount the iso file for Ceph
 ```
 mkdir /mnt/rhcs3.0
 mount /root/staging_area/RHCEPH-3.0-RHEL-7-20180604.ci.0-x86_64-dvd.iso /mnt/rhcs3.0/
 ```
 * Edit /etc/yum.repos.d/rhcs.repo
 ```
[ceph-MON]
name=ceph-MON
baseurl=file:///mnt/rhcs3.0/MON
gpgcheck=0
enabled=1

[ceph-OSD]
name=ceph-OSD
baseurl=file:///mnt/rhcs3.0/OSD
gpgcheck=0
enabled=1

[ceph-TOOLS]
name=ceph-TOOLS
baseurl=file:///mnt/rhcs3.0/Tools
gpgcheck=0
enabled=1
 
 ```
 
 * Edit /etc/yum.repos.d/rhel-extras.repo
 ```
 [Server]
name=Server
baseurl=http://download-node-02.eng.bos.redhat.com/rel-eng/RHEL-7.5-Update-1.1/compose/Server/x86_64/os/
enabled=1
gpgcheck=0
#skip_if_unavailable=1

[Server-Optional]
name=Server-Optional
baseurl=http://download-node-02.eng.bos.redhat.com/rel-eng/RHEL-7.5-Update-1.1/compose/Server-optional/x86_64/os/
enabled=1
gpgcheck=0
#skip_if_unavailable=1

[Server-Extras]
name=Server-Extras
baseurl=http://pulp.dist.prod.ext.phx2.redhat.com/content/dist/rhel/server/7/7Server/x86_64/extras/os
enabled=1
gpgcheck=0
#skip_if_unavailable=1
 
 ```
* Install ceph-ansible
```
yum clean all
yum install -y ceph-ansible

```

# Get "ceph-linode" from github
```
git clone https://github.com/batrick/ceph-linode
```

# Setup a virtualenv with linode-python
```
yum install python-virtualenv -y
cd ceph-linode
virtualenv linode-env && source linode-env/bin/activate && pip install linode-python
```

# Ceph-Ansible Configuration
* Define number of nodes and their role. "plan" defines the node type. "plan:1" is for "Nanode 1GB"
```
cp cluster.json.sample cluster.json
```
* Edit cluster.json
```
[
  {
    "count": 3,
    "prefix": "mon",
    "plan": 1,
    "group": "mons"
  },
  {
    "count": 3,
    "prefix": "osd",
    "plan": 1,
    "root_size": 4096,
    "group": "osds"
  },
  {
    "count": 1,
    "prefix": "mds",
    "plan": 1,
    "group": "mdss"
  },
  {
    "count": 1,
    "prefix": "rgw",
    "plan": 1,
    "group": "rgws"
  },
  {
    "count": 1,
    "prefix": "mgr",
    "plan": 1,
    "group": "mgrs"
  },
  {
    "count": 1,
    "prefix": "client",
    "plan": 1,
    "group": "clients"
  }
]

```

* Navigate to the Ceph Ansible group_vars directory
```
cd /usr/share/ceph-ansible/group_vars/
```

* Edit all.yml (cp all.yml.sample all.yml)
```
---
dummy:
fetch_directory: /ceph-ansible-keys
ceph_rhcs_iso_install: true
ceph_origin: repository
ceph_repository: rhcs
ceph_rhcs_version: 3
valid_ceph_repository_type:
  - iso
ceph_rhcs_iso_path: /root/staging_area/RHCEPH-3.0-RHEL-7-20180604.ci.0-x86_64-dvd.iso
monitor_interface: eth0
journal_size: 5120 # OSD journal size in MB
public_network: 192.168.128.0/17
radosgw_civetweb_port: 8080
radosgw_address: 192.168.128.0/17
osd_objectstore: filestore
ceph_conf_overrides:
  mon:
    mon_allow_pool_delete: true
  ```
 * Edit osds.yml (cp osds.yml.sample osds.yml)
```
---
dummy:
osd_scenario: non-collocated
devices: [ '/dev/sdc','/dev/sdd','/dev/sde','/dev/sdf','/dev/sdaa', '/dev/sdh', '/dev/sdi', '/dev/sdj', '/dev/sdk', '/dev/sdl', '/dev/sdm' ,'/dev/sdn','/dev/sdo', '/dev/sdp', '/dev/sdq', '/dev/sdr', '/dev/sds', '/dev/sdt', '/dev/sdu', '/dev/sdv', '/dev/sdw', '/dev/sdx', '/dev/sdy', '/dev/sdz']
dedicated_devices: ['/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1', '/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1','/dev/nvme0n1']
----
dummy:
osd_scenario: collocated
devices:
  - /dev/sdc

```

# Disable filewall
* Edit: /root/ceph-linode/launch.sh
* Add Line: "ansible -m shell -a "systemctl stop firewalld; systemctl disable firewalld" 
```
function main {
    if [ "$NUKE" -gt 0 ]; then
        time python2 "$(dirname "$0")/linode-nuke.py"
    fi
    if [ "$NUKE" -gt 0 -o ! -f ansible_inventory ]; then
        time python2 "$(dirname "$0")/linode-launch.py"
        ansible -m shell -a "systemctl stop firewalld; systemctl disable firewalld" all
    fi
    # wait for Linodes to finish booting
    time python2 "$(dirname "$0")/linode-wait.py"
```

# Disable gpg Signature Checks
```
sed -i 's/gpgcheck=1/gpgcheck=0/g' /usr/share/ceph-ansible/roles/ceph-common/templates/redhat_storage_repo.j2
```

# Deploying a Ceph Cluster
```
cd ceph-linode
export LINODE_API_KEY=<your_key>
./launch.sh --ceph-ansible /usr/share/ceph-ansible/
```

# Destroying a Ceph Cluster
```
cd ceph-linode
python linode-destroy.py
```

# Inventory file for nodes
```/root/ceph-linode/ansible_inventory```
