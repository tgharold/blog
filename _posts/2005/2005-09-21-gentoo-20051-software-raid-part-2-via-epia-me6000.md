---
layout: post
title: 'Gentoo 2005.1 Software RAID (part 2) VIA EPIA ME6000'
date: '2005-09-21T12:44:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Time to [configure the Gentoo kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7).  I'm configuring this for my VIA EPIA ME6000 motherboard.  (Notice that I'm now including the LVM2 components as part of my base installation.)

<code># emerge mdadm
# emerge lvm2
# cd /usr/src/linux
# make menuconfig</code>

Linux Kernel v2.6.11 Configuration
(C)ode maturity level options
(G)eneral setup
--&gt; (C)onfigure standard kernel features for small systems (turn ON)
--&gt; --&gt; (O)ptimize for size (turn ON)
(L)oadable module support
(P)rocessor type and features
--&gt; (P)rocessor family (changed to "CyrixIII/VIA-C3")
--&gt; (S)ymetric multi-processing support (turned this one OFF)
--&gt; M(a)chine Check Exception (turned this OFF)
(P)ower management options (ACPI, APM)
(B)us options (PCI, PCMCIA, EISA&lt; MCA, ISA)
(E)xecutable file formats
(D)evice drivers
--&gt; (P)arallel port support (turned OFF)
--&gt; (A)TA/ATAPI/MFM/RLL support 
--&gt; --&gt; (V)IA82CXXX chipset support (turned ON)
--&gt; M(u)lti-device support (turn it ON)
--&gt; --&gt; (R)AID support (turn it ON as BUILT-IN)
--&gt; --&gt; --&gt; (R)AID-1 mirroring mode (turn it ON as BUILT-IN)
--&gt; --&gt; (D)evice mapper support (set to MODULE, per section 13 of LVM2 guide)
--&gt; N(e)tworking support 
--&gt; --&gt; (E)thernet (10 or 100Mbit)
--&gt; --&gt; --&gt; (R)ealTek RTL-8139 PCI Fast Ethernet (turn it OFF)
--&gt; --&gt; --&gt; (V)IA Rhine support (turn it ON)
--&gt; --&gt; --&gt; --&gt; (U)se MMIO instead of PIO (turn it ON)

--&gt; (C)haracter Devices
--&gt; --&gt; (I)ntel/AMD/VIA HW Random Number Generator (turn ON as BUILT-IN)
--&gt; --&gt; (I)ntel 440LX/BX/GX, I8xx and E7x05 chipset support (turn it OFF)
--&gt; --&gt; (V)IA chipset support (turn ON)
--&gt; (S)ound
--&gt; --&gt; (S)ound card support (turn OFF)
(F)ile systems
--&gt; N(e)twork File Systems
--&gt; --&gt; (S)MB file system support (turn ON as BUILT-IN)
--&gt; --&gt; (C)IFS support (turn ON as BUILT-IN)
(P)rofiling support
(K)ernel hacking
(S)ecurity options
(C)ryptographic options
--&gt; (C)ryptographic API (turn ON)
--&gt; --&gt; HM(A)C support (NEW) (turn ON as BUILT-IN)
--&gt; --&gt; (turn ON all other options as MODULE)
(L)ibrary routines

Exit and save your configuration. Then build the kernel (the following command is for 2.6 kernels). Expect the compile to take about an hour.

<code># make &amp;&amp; make modules_install</code>
