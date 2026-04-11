---
layout: post
title: 'Gentoo: eth0 does not exist'
date: '2005-10-20T14:17:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


So, oops.  When I built my Celeron box, I didn't include the driver for my Netgear FA310TX Rev-D1 in the kernel build.  The Universal CD automatically detects the network card properly, now I just need to get it configured into my kernel build (using "make menuconfig").  The Universal CD (2005.1) detected and configured it using the Tulip driver (Lite-On 82c168).

So I know it works, I just don't have it right and proper.  My original build for this kernel is:

[Gentoo 2005.1 Software RAID (part 2) Celeron CPU](/blog/2005-09-22-gentoo-20051-software-raid-part-2-celeron-cpu/)

During that build, I didn't touch network devices at all. It had automatically selected the RealTek network device driver under the EISA option. 

```
# cd /usr/src/linux
# make menuconfig
```

(D)evice drivers
--> N(e)tworking support
--> --> N(e)twork device support (should already be BUILT-IN)
--> --> --> (E)thernet (10 or 100Mbit)
--> --> --> --> (T)ulip family network device support
--> --> --> --> --> "(T)ulip" family network device support (turn ON as BUILT-IN)
--> --> --> --> --> --> (D)ECchip Tulip (dc2114x) PCI support (turn ON as BUILT-IN)
--> --> --> --> --> --> --> (I left the sub-options alone)
--> --> --> --> (E)ISA, VLB, PCI and on board controllers (turn OFF)

Now, make sure that /boot is mounted, then compile your new kernel.

```
# make &amp;&amp; make modules_install
# cp arch/i386/boot/bzImage /boot/kernel-2.6.12-Oct2005
# cp System.map /boot/System.map-2.6.12-Oct2005
# cp .config /boot/config-2.6.12-Oct2005
# nano -w /boot/grub/grub.conf
```

Contents of my grub.conf file:

```
# Which listing to boot as default. 0 is the first, 1 the second etc.
default 0
timeout 30

# Oct 2005 recompile kernel to add Netgear FA310TX rev D1
title=Gentoo Linux 2.6.12 (Oct 20 2005)
root (hd0,0)
kernel /kernel-2.6.12-Oct2005 root=/dev/md2

# Sep 2005 installation (software RAID, no LVM2)
title=Gentoo Linux 2.6.12 (Sep 22 2005)
root (hd0,0)
kernel /kernel-2.6.12-Sep2005 root=/dev/md2
```

Not technically difficult, if you can find out what device driver to  use.  Which, is why I try to document as much of this stuff as possible.
