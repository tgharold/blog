---
layout: post
title: 'Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 4)'
date: '2005-04-20T20:43:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

(previous step)

Time to [configure the kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7).

<code># emerge lvm2
# emerge mdadm
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
--&gt; (P)arallel port support (turned OFF)
--&gt; (A)TA/ATAPI/MFM/RLL support (turned ON the PDC20262 chipset support as BUILT-IN)
--&gt; M(u)lti-device support (turn it ON)
--&gt; --&gt; (R)AID support (turn it ON as BUILT-IN)
--&gt; --&gt; --&gt; (R)AID-1 mirroring mode (turn it ON as BUILT-IN)
--&gt; --&gt; (D)evice mapper support (set to MODULE, per section 13 of LVM2 guide)
--&gt; (C)haracter Devices
--&gt; --&gt; (I)ntel/AMD/VIA HW Random Number Generator (turn ON as BUILT-IN)
--&gt; (S)ound
--&gt; --&gt; (S)ound card support (turn OFF)
(F)ile systems
(P)rofiling support
(K)ernel hacking
(S)ecurity options
(C)ryptographic options
(L)ibrary routines

Exit and save your configuration. Then build the kernel (the following is for 2.6 kernels). Expect the compile to take about an hour.

<code># make &amp;&amp; make modules_install</code>

Now you need to install your kernel into the boot partition. Change the "2.6.6-gentoo" portion of the filenames to whatever you want.

<code># cp arch/i386/boot/bzImage /boot/kernel-2.6.11-gentoo-Apr20
# cp System.map /boot/System.map-2.6.11-gentoo-Apr20
# cp .config /boot/config-2.6.11-gentoo-Apr20</code>

Now we need to configure LVM to auto-load.

<code># nano -w /etc/modules.autoload.d/kernel-2.6</code>

Here is what my autoload file looks like:

<code># /etc/modules.autoload.d/kernel-2.6:  kernel modules to load when system boots.
# $Header: /home/cvsroot/gentoo-src/rc-scripts/etc/modules.autoload.d/kernel-2.6,v 1.1 2003/07/16 18:13:45 azarah Exp $
#
# Note that this file is for 2.6 kernels.
#
# Add the names of modules that you'd like to load when the system
# starts into this file, one per line.  Comments begin with # and
# are ignored.  Read man modules.autoload for additional details.

# For example:
# 3c59x

dm-mod</code>

Now, edit the /etc/fstab file:

<code># /etc/fstab: static file system information.
# $Header: /home/cvsroot/gentoo-src/rc-scripts/etc/fstab,v 1.14 2003/10/13 20:03:38 azarah Exp $
#
# noatime turns off atimes for increased performance (atimes normally aren't
# needed; notail increases performance of ReiserFS (at the expense of storage
# efficiency).  It's safe to drop the noatime options if you want and to
# switch between notail and tail freely.

# &lt;fs&gt;                  &lt;mountpoint&gt;    &lt;type&gt;          &lt;opts&gt;                  &lt;dump/pass&gt;

# NOTE: If your BOOT partition is ReiserFS, add the notail option to opts.
/dev/md0                /boot           ext2            noauto,noatime          1 2
/dev/md1                /               ext3            noatime                 0 1
/dev/md2                none            swap            sw                      0 0
/dev/cdroms/cdrom0      /mnt/cdrom      auto            noauto,ro,user          0 0
#/dev/fd0               /mnt/floppy     auto            noauto                  0 0

/dev/vgmirror/opt       /opt            ext3            noatime                 0 3        
/dev/vgmirror/usr       /usr            ext3            noatime                 0 3
/dev/vgmirror/var       /var            ext3            noatime                 0 3
/dev/vgmirror/home      /home           ext3            noatime                 0 3
/dev/vgmirror/tmp       /tmp            ext2            noatime                 0 3
/dev/vgmirror/vartmp    /var/tmp        ext2            noatime                 0 3        

# NOTE: The next line is critical for boot!
none                    /proc           proc            defaults                0 0

# glibc 2.2 and above expects tmpfs to be mounted at /dev/shm for
# POSIX shared memory (shm_open, shm_unlink).
# (tmpfs is a dynamically expandable/shrinkable ramdisk, and will
#  use almost no memory if not populated with files)
# Adding the following line to /etc/fstab should take care of this:

none                    /dev/shm        tmpfs           defaults                0 0</code>

Now, some misc stuff:

<code># echo yourhostname &gt; /etc/hostname
# echo yourdnsname &gt; /etc/dnsdomainname
# rc-update add domainname default
# nano -w /etc/conf.d/net
(either use iface_eth0="dhcp" or configure your IP and gateway)
# rc-update add net.eth0 default
# cat /etc/resolv.conf
(verify your DNS servers if you specified a static IP)
# nano -w /etc/rc.conf
(change CLOCK="UTC" to CLOCK="local")
# passwod
(set your root password to something you will remember)

# useradd -m -G users,wheel,audio -s /bin/bash john
# passwd john

(add a user called 'john' and set a password)</code>

(next step)
