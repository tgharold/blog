---
layout: post
title: 'Gentoo 2005.1 Software RAID (part 2) Celeron CPU'
date: '2005-09-22T23:31:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Time to [configure the Gentoo kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&chap=7).  I'm configuring this for my Celeron motherboard.

Note the use of "emerge lvm2" since I'm using LVM2 on this system during the initial installation.

```
# emerge mdadm
# emerge lvm2
# cd /usr/src/linux
# make menuconfig
```

Linux Kernel v2.6.11 Configuration
(C)ode maturity level options
(G)eneral setup
--> (C)onfigure standard kernel features for small systems (turn ON)
--> --> (O)ptimize for size (turn ON)
(L)oadable module support
(P)rocessor type and features
--> (P)rocessor family (changed to "Pentium-III...")
--> (S)ymetric multi-processing support (turned this one OFF)
--> M(a)chine Check Exception (turned this OFF)
(P)ower management options (ACPI, APM)
(B)us options (PCI, PCMCIA, EISA< MCA, ISA)
(E)xecutable file formats
(D)evice drivers
--> (A)TA/ATAPI/MFM/RLL support
--> --> (P)ROMISE PDC202{46|62|65|67} support (turn ON)
--> N(e)tworking support
--> --> N(e)twork device support (should already be BUILT-IN)
--> --> --> (E)thernet (10 or 100Mbit)
--> --> --> --> (T)ulip family network device support
--> --> --> --> --> "(T)ulip" family network device support (turn ON as BUILT-IN)
--> --> --> --> --> --> (D)ECchip Tulip (dc2114x) PCI support (turn ON as BUILT-IN)
--> --> --> --> --> --> --> (I left the sub-options alone)
--> --> --> --> (E)ISA, VLB, PCI and on board controllers (turn OFF)
--> (P)arallel port support (turned OFF)
--> M(u)lti-device support (turn it ON)
--> --> (R)AID support (turn it ON as BUILT-IN)
--> --> --> (R)AID-1 mirroring mode (turn it ON as BUILT-IN)
--> --> (D)evice mapper support (set to MODULE, per section 13 of LVM2 guide)
--> (C)haracter Devices
--> --> (I)ntel/AMD/VIA HW Random Number Generator (turn ON as BUILT-IN)
--> (S)ound
--> --> (S)ound card support (turn OFF)
(F)ile systems
--> N(e)twork File Systems
--> --> (S)MB file system support (turn ON as BUILT-IN)
--> --> (C)IFS support (turn ON as BUILT-IN)
(P)rofiling support
(K)ernel hacking
(S)ecurity options
(C)ryptographic options
--> (C)ryptographic API (turn ON)
--> --> HM(A)C support (NEW) (turn ON as BUILT-IN)
--> --> (turn ON all other options as MODULE)
(L)ibrary routines

Exit and save your configuration. Then build the kernel (the following command is for 2.6 kernels). Expect the compile to take about an hour.

```
# make && make modules_install
```
