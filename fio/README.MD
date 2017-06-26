 Installing FIO Benchmark
====================

* From The Github Repo
```
https://github.com/axboe/fio
```

* Install package using YUM
 ```
sudo yum search fio
fio.x86_64 : Multithreaded IO generation tool
sudo yum install fio
```

Create a job config file "test.fio"
====================
```
[global]
ioengine=posixaio
rw=readwrite
size=1g
directory=/home/fio
thread=1

[trivial-readwrite-1g]
```
*sync/async

ioengine=sync (default)
ioengine=posixaio

*direct IO / buffered IO
direct=0 (default) # buffered IO
direct=1 #direct IO

* I/O pattern
rw=read # Seq read
rw=write # Seq write
rw=rand
rw=randread


Running FIO Benchmark
=========================

```
$ fio [options] [jobfile] ...

fio test.fio
```
