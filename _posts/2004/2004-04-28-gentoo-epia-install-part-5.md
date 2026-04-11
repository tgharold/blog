---
layout: post
title: 'Gentoo EPIA Install (part 5)'
date: '2004-04-28T20:20:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


([previous entry](/blog/2004-04-27-gentoo-epia-install-part-4/))

Well, that took somewhere around 2 hours to import and build the kernel from the development-sources package.    Now I need to [configure the kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7) (per chapter 7c of the handbook).  There are also notes over at [epiawiki.org](http://www.epiawiki.org/wiki/tiki-index.php?page=EpiaTheEpiaKernel) and [building a small MP3 server](http://www.ath0.com/meta/prose/mp3-server/part3.html) about configuring that I'll need to investigate (specifically looking at [their copy of the make config file](http://www.ath0.com/meta/prose/mp3-server/m10000-kernel-config-meta) which goes in "/usr/src/linux/.config").

I'm going with the manual option, so "cd /usr/src/linux" then "make menuconfig".  Anywhere I say "turn ON" means to use the "Y" key to turn an option on as built-in, I'll specifically say MODULE if I loaded the option as a module.

	Linux Kernel v2.6.3 Configuration
	(C)ode maturity level options
	(G)eneral setup
	(L)oadable module support
	(P)rocessor type and features
	--> (P)rocessor family (changed to "CyrixIII/VIA-C3")
	--> (S)ymetric multi-processing support (turned this one OFF)
	--> M(a)chine Check Exception (turned this OFF)
	(P)ower management options (ACPI, APM)
	(B)us options (PCI, PCMCIA, EISA< MCA, ISA)
	(E)xecutable file formats
	(D)evice drivers
	--> (P)arallel port support (turned mine OFF)
	--> (A)TA/ATAPI/MFM/RLL support (turned ON the VIA82CXXX chipset support as built-in)
	--> M(u)lti-device support (turn it ON, set Device mapper support to MODULE, [per section 13 of LVM2 guide](http://www.gentoo.org/doc/en/lvm2.xml))
	--> N(e)tworking support (look under Ethernet 10/100Mbit, turn OFF the RealTek RTL-8139 option, turn ON the VIA Rhine option, also turn ON the MMIO instead of PIO option)
	--> (C)haracter Devices (under the AGP support section, I turned OFF the Intel 440... support option and turned ON the VIA chipset support option, turn ON the Intel/AMD/VIA HW RNG support, )
	--> (I)2C support (turn this option ON, then see the rest of this list, heavily reliant on [building an MP3 server](http://www.ath0.com/meta/prose/mp3-server/part3.html) for thse options)
	-->--> (I)2C device interface (turned ON, epiawiki says to turn on, MP3 server article leaves it off)
	-->--> (I)2C Algorithms (turn ON bit-banging)
	-->--> (I)2C Hardware Bus (turn ON the VIA 82C586B support... this is the old "VIA" option, not sure how to decide between that one and the 82C596/82C686/823x, a.k.a. VIAPRO option though so I flipped a coin)
	-->--> (I)2C Hardware Sensors Chip (turn ON the VIA686A option)
	-->--> (I)2C Core debugging messages (left alone)
	-->--> (I)2C Bus debugging messages (left alone)
	-->--> (I)2C Chip debugging messages (left alone)
	--> M(u)ltimedia devices (left this alone since I'm not interested in using the video-out features)
	(F)ile systems
	--> (D)OS/FAT/NT Filesystems (turned ON the built-in NTFS filesystem, including debugging/write support)
	--> You may also need to turn on "/dev file system support (OBSOLETE)" under (P)seudo filesystems, also turn on "Automatically mount at boot".
	(P)rofiling support
	(K)ernel hacking
	(S)ecurity options
	(C)ryptographic options (turned ON, then turned ON the HMAC, everything else as MODULE)
	(L)ibrary routines

Hit "Exit" when done and save your new kernel configuration.  Use "make &amp;&amp; make modules_install" to build the kernel, then follow the instructions to install the kernel (last part of chapter 7c).  I should also go back and do a genkernel (section 7d) and compare it to what I picked.  The kernel took under an hour to compile.  The last few commands of section 7c:

	# cp arch/i386/boot/bzImage /boot/kernel-2.6.3-gentoo
	# cp System.map /boot/System.map-2.6.3-gentoo
	# cp .config /boot/config-2.6.3-gentoo

([next entry](/blog/2004-04-29-gentoo-epia-install-part-6/))
