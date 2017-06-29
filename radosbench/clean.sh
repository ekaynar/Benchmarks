#!/bin/bash

#usage
#
#
#./clean k m
#./clean 3way

rm -rf /var/lib/pbench-agent/pbench-user-benchmark* && \
rados bench -p default.rgw.buckets.data 30 write --no-cleanup && \
pbench-user-benchmark "./rados_bench.sh -k $1 -m $2" && \
mv /var/lib/pbench-agent/pbench-user-benchmark* /var/www/html/pub/rados.$1.$2 

