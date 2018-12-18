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
