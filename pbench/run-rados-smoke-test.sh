#!/bin/bash
rm -rf /var/lib/pbench-agent/pbench-user-benchmark* 
pbench-user-benchmark 'rados bench -p rbd 60 write' > /tmp/radosbench.log  && \
mv /tmp/radosbench.log /var/lib/pbench-agent/pbench-user-benchmark*/ && \
mv /var/lib/pbench-agent/pbench-user-benchmark* /var/www/html/pub/ && \
chmod -R a+r /var/www/html/pub && \
chown -R apache:apache /var/www/html/pub

