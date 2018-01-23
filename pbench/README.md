How to Install PBench with Ansible
=====================================
# Adding Repos :

 For all the nodes: 
---------------------
* Add repo for the Pbench benchmark and tool packages from CORP (For Fedora, CentOS, and RHEL users only)

CORP : https://copr.fedorainfracloud.org/coprs/ndokos/pbench/

```
wget -O /etc/yum.repos.d/_copr_ndokos-pbench.repo https://copr.fedorainfracloud.org/coprs/ndokos/pbench/repo/epel-7/ndokos-pbench-epel-7.repo
```
* Download and install the EPEL rpm 
```
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -i epel-release-latest-7.noarch.rpm 
```
# Installation with Ansible
For master node
-----------------------
* Install ansible on the master machine
* Configure `/etc/ansible/hosts` file

```
[pbench_agents]
gprfs033
gprfs034

[pbench_webserver]
gprfs033
```
* Add master's public key to all agent nodes

* Edit internal-host file (remove master from internal-host files)
```
gprfs034
gprfs035
```

* Run the ansible playbook
```
ansible-playbook -v pbench_ins.yml 
```


NOTES:
===================================
Before you do anything else, you need to source the file /etc/profile.d/pbench-agent.sh.
remove master from internal-host files

Viewing pbench graphs and data
=================================
* Local configurations for webserver
```
ln -sf /opt/pbench-web-server/html/static /var/www/html
```
* Browse to
```
http://localhost/pub
```
# More info
https://github.com/distributed-system-analysis/pbench

