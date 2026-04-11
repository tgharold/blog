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


<div style="clear:both;"></div>Time to [configure the Gentoo kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7).  I'm configuring this for my Celeron motherboard.

Note the use of "emerge lvm2" since I'm using LVM2 on this system during the initial installation.

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
--&gt; (P)rocessor family (changed to "Pentium-III...")
--&gt; (S)ymetric multi-processing support (turned this one OFF)
--&gt; M(a)chine Check Exception (turned this OFF)
(P)ower management options (ACPI, APM)
(B)us options (PCI, PCMCIA, EISA&lt; MCA, ISA)
(E)xecutable file formats
(D)evice drivers
--&gt; (A)TA/ATAPI/MFM/RLL support
--&gt; --&gt; (P)ROMISE PDC202{46|62|65|67} support (turn ON)
--&gt; N(e)tworking support
--&gt; --&gt; N(e)twork device support (should already be BUILT-IN)
--&gt; --&gt; --&gt; (E)thernet (10 or 100Mbit)
--&gt; --&gt; --&gt; --&gt; (T)ulip family network device support
--&gt; --&gt; --&gt; --&gt; --&gt; "(T)ulip" family network device support (turn ON as BUILT-IN)
--&gt; --&gt; --&gt; --&gt; --&gt; --&gt; (D)ECchip Tulip (dc2114x) PCI support (turn ON as BUILT-IN)
--&gt; --&gt; --&gt; --&gt; --&gt; --&gt; --&gt; (I left the sub-options alone)
--&gt; --&gt; --&gt; --&gt; (E)ISA, VLB, PCI and on board controllers (turn OFF)
--&gt; (P)arallel port support (turned OFF)
--&gt; M(u)lti-device support (turn it ON)
--&gt; --&gt; (R)AID support (turn it ON as BUILT-IN)
--&gt; --&gt; --&gt; (R)AID-1 mirroring mode (turn it ON as BUILT-IN)
--&gt; --&gt; (D)evice mapper support (set to MODULE, per section 13 of LVM2 guide)
--&gt; (C)haracter Devices
--&gt; --&gt; (I)ntel/AMD/VIA HW Random Number Generator (turn ON as BUILT-IN)
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

<code># make &amp;&amp; make modules_install</code><div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SoftwareRAID.shtml">SoftwareRAID</a>
		<div class="Byline">
			posted by Thomas at 
			[23:31](http://www.tgharold.com/techblog/2005/09/gentoo-20051-software-raid-part-2.shtml)

		</div>