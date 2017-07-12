Rados Bench comes with ceph-common package.
Make sure you have the latest version of to display IOPS, Average Bandwidth, Average IOPS ...etc

subscription-manager repos --enable=rhel-7-server-rhceph-2-mon-rpms
subscription-manager repos --enable=rhel-7-server-rhceph-2-osd-rpms

yum --showduplicates list ceph-common
