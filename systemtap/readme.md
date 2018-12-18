# Installation and Setup
```
yum install -y systemtap systemtap-runtime
```

# Installing Required Kernel Information RPMs
Systemtap requires kernel packages for instrumentation. 

* kernel-debuginfo
* kernel-debuginfo-common
* kernel-devel

First find out the kernel version:

```
uname -r

```

Download and install the required RPMs
```
rpm -i kernel-debuginfo-common-x86_64-3.10.0-957.el7.x86_64.rpm
rpm -i kernel-debuginfo-3.10.0-957.el7.x86_64.rpm
rpm -i kernel-devel-3.10.0-957.el7.x86_64.rpm
debuginfo-install kernel-3.10.0-957.el7.x86_64
```

# Test the installation
```
stap -v -e 'probe vfs.read {printf("read performed\n"); exit()}'.
```

Output should look like:
```
[root@c04-h01-6048r ~]# stap -v -e 'probe vfs.read {printf("read performed\n"); exit()}'
Pass 1: parsed user script and 475 library scripts using 247796virt/45028res/3468shr/41848data kb, in 320usr/30sys/735real ms.
Pass 2: analyzed script: 1 probe, 1 function, 7 embeds, 0 globals using 412520virt/205068res/4868shr/206572data kb, in 1540usr/750sys/8150real ms.
Pass 3: using cached /root/.systemtap/cache/d5/stap_d52fff0ada67237c2e53ff02d00f763c_2763.c
Pass 4: using cached /root/.systemtap/cache/d5/stap_d52fff0ada67237c2e53ff02d00f763c_2763.ko
Pass 5: starting run.
read performed
Pass 5: run completed in 10usr/50sys/422real ms.
```

# Error during the run
Edit "UTS_VERSION" line in the followign file:
```
vim  /usr/src/kernels/3.10.0-957.el7.x86_64/include/generated/compile.h
```

```
/* This file is auto generated, version 1 */
/* SMP */
#define UTS_MACHINE "x86_64"
//#define UTS_VERSION "#1 SMP Thu Nov 8 23:39:32 UTC 2018"
#define UTS_VERSION "#1 SMP Thu Oct 4 20:48:51 UTC 2018"
#define LINUX_COMPILE_BY "mockbuild"
#define LINUX_COMPILE_HOST "kbuilder.bsys.centos.org"
#define LINUX_COMPILER "gcc version 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC) "
~
```

# Writing SystemTap scripts and building modules.


* To compile the script, run stap command as below.
```
stap -p4 -r $kenrelversion -m stap_example example.stp
```

# Attaching to running process
* Lets assume we want to track the function called "get_obj_iterate_cb" in the radosgw. There might be more than one 
First list the probe for the given function name with '-l' flag
```
stap -l 'process("<PROCESS NAME>").function("*"')| grep <FUNCTION_NAME>
```

```
[root@c04-h01-6048r ~]# stap -l 'process("/usr/bin/radosgw").function("*")'|grep get_obj_iterate_cb
process("/usr/bin/radosgw").function("_ZL19_get_obj_iterate_cbRK13RGWBucketInfoRK7rgw_objRK11rgw_raw_objlllbP11RGWObjStatePv")
process("/usr/bin/radosgw").function("_ZN8RGWRados18get_obj_iterate_cbEP12RGWObjectCtxP11RGWObjStateRK13RGWBucketInfoRK7rgw_objRK11rgw_raw_objlllbPv")
```

Here we are looking for "_ZN8RGWRados18get_obj_iterate_cbEP12RGWObjectCtxP11RGWObjStateRK13RGWBucketInfoRK7rgw_objRK11rgw_raw_objlllbPv"


Then we can start instrumenting 

```
stap -e 'probe process("/usr/bin/radosgw").function("_ZN8RGWRados18get_obj_iterate_cbEP12RGWObjectCtxP11RGWObjStateRK13RGWBucketInfoRK7rgw_objRK11rgw_raw_objlllbPv"){ <YOUR CODE> }'
```

For example lets print the stack back trace for current function:
```
stap -e 'probe process("/usr/bin/radosgw").function("_ZN8RGWRados18get_obj_iterate_cbEP12RGWObjectCtxP11RGWObjStateRK13RGWBucketInfoRK7rgw_objRK11rgw_raw_objlllbPv"){ print("\n"); print_ubacktrace(); print("************\n"); }'
```


