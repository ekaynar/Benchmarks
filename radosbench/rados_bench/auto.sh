#!/bin/bash


for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r rep -k 0 -m 0 -d 1024 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 3 way.$i 1800 18 2M

echo "Finish"

done

for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r rep -k 0 -m 0 -d 1024 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 3 way.$i 1800 18 4M

echo "Finish"

done

for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r rep -k 0 -m 0 -d 1024 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 3 way.$i 1800 18 8M

echo "Finish"

done

for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r rep -k 0 -m 0 -d 1024 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 3 way.$i 1800 18 16M

echo "Finish"

done

for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r ec -k 3 -m 2 -d 512 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 3 2.$i 1800 18 4M

echo "Finish"

done


for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r ec -k 3 -m 2 -d 512 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 3 2.$i 1800 18 8M

echo "Finish"

done

for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r ec -k 3 -m 2 -d 512 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 3 2.$i 1800 18 16M

echo "Finish"

done

for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r ec -k 6 -m 3 -d 512 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 6 3.$i 1800 18 4M

echo "Finish"

done

for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r ec -k 6 -m 3 -d 512 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 6 3.$i 1800 18 8M

echo "Finish"

done


for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r ec -k 6 -m 3 -d 512 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 6 3.$i 1800 18 16M

echo "Finish"

done


for i in {1..1}
do
echo "Creating Pool 3 way"
 ./pool_mng.sh -r ec -k 10 -m 4 -d 256 -i 32 -o 32 -f 0
echo "Pool is created" &&
sleep 200 &&
ceph -s &&
ceph osd dump | grep 'erasure' &&
ceph osd dump | grep 'repliated' &&
echo "Pool is created"
echo "Running $i"
./caller.sh 10 4.$i 1800 18 4M

echo "Finish"

done
















