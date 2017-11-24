#!/bin/bash

./workload.sh rep 0 0 1024 32 32 0 write.xml 3rep.write64K.36w && \
./workload.sh ec 6 3 512 32 32 0 write.xml ec63.write64K.36w && \

echo "done"
