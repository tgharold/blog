---
layout: post
title: 'Gentoo Install 5 (Manual Kernel Configuration)'
date: '2004-06-16T10:37:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>([previous post - building the kernel](/2004/06/gentoo-install-4-installing-kernel.shtml))

Note: This is for a VIA EPIA ME6000 motherboard being used as a headless server.  All of the multimedia and graphic options are disabled.  (See my [previous install](/techblog/2004/04/gentoo-epia-install-part-5.shtml).)  If this is your first install, you should probably use the "genkernel" method rather then manual configuration.  The [Gentoo docs explain configuring the kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7#doc_chap3).  They recommend being familiar with the "<b>cat /proc/pci</b>" and "<b>lsmod</b>" commands which is something I missed on my [previous install](/2004/04/gentoo-epia-install-part-5.shtml).
<pre># cd /usr/src/linux
# make menuconfig</pre>

Anywhere in the following list where I say "turn ON" means to use the "Y" key to turn an option on as built-in, I'll specifically say MODULE if I loaded the option as a module.

<b>Linux Kernel v2.6.6 Configuration</b>
(C)ode maturity level options
(G)eneral setup
--&gt; (C)onfigure standard kernel features for small systems (<b>turn ON</b>)
--&gt; --&gt; (O)ptimize for size (<b>turn ON</b>)
(L)oadable module support
(P)rocessor type and features
--&gt; (P)rocessor family (<b>changed to "CyrixIII/VIA-C3"</b>)
--&gt; (S)ymetric multi-processing support (<b>turned this one OFF</b>)
--&gt; M(a)chine Check Exception (<b>turned this OFF</b>)
(P)ower management options (ACPI, APM)
(B)us options (PCI, PCMCIA, EISA&lt; MCA, ISA)
(E)xecutable file formats
(D)evice drivers
--&gt; (P)arallel port support (<b>turned OFF</b>)
--&gt; (A)TA/ATAPI/MFM/RLL support (<b>turned ON the VIA82CXXX chipset support as BUILT-IN</b>)
--&gt; M(u)lti-device support (<b>turn it ON</b>)
--&gt; --&gt; (R)AID support (<b>turn it ON as BUILT-IN</b>)
--&gt; --&gt; --&gt; (R)AID-1 mirroring mode (<b>turn it ON as BUILT-IN</b>)
--&gt; --&gt; (D)evice mapper support (<b>set to MODULE</b>, [per section 13 of LVM2 guide](http://www.gentoo.org/doc/en/lvm2.xml))
--&gt; N(e)tworking support
--&gt; --&gt; N(e)twork device support, (E)thernet 10/100Mbit
--&gt; --&gt; --&gt; (R)ealTek RTL-8139 PCI (<b>turn OFF</b>)
--&gt; --&gt; --&gt; (V)IA Rhine (<b>turn ON as BUILT-IN</b>)
--&gt; --&gt; --&gt; --&gt; (U)se MMIO instead of PIO (<b>turn ON</b>)
--&gt; (C)haracter Devices 
--&gt; --&gt; (I)ntel/AMD/VIA HW Random Number Generator (<b>turn ON as BUILT-IN</b>)
--&gt; --&gt; /(d)ev/agpgart AGP Support
--&gt; --&gt; --&gt; (I)ntel 440LX/BX/GX I8xx E7x05 (<b>turn OFF</b>)
--&gt; --&gt; --&gt; (V)IA chipset support (<b>turn ON as BUILT-IN</b>)
--&gt; (I)2C support (<b>turn ON</b>, heavily reliant on [building an MP3 server](http://www.ath0.com/meta/prose/mp3-server/part3.html) for these options)
--&gt; --&gt; (I)2C device interface (<b>turned ON as BUILT-IN</b>, epiawiki says "on", MP3 server article says "off")
--&gt; --&gt; (I)2C Algorithms 
--&gt; --&gt; --&gt; (I)2C bit-banging interface (<b>turn ON as BUILT-IN</b>)
--&gt; --&gt; (I)2C Hardware Bus support
--&gt; --&gt; --&gt; (V)IA 82C586B support (<b>turn on as BUILT-IN</b>)
--&gt; --&gt; (I)2C Hardware Sensors Chip 
--&gt; --&gt; --&gt; (V)IA686A (<b>turn on as BUILT-IN</b>)
--&gt; (S)ound
--&gt; --&gt; (S)ound card support (<b>turn OFF</b>)
(F)ile systems
--&gt; (P)seudo filesystems
--&gt; --&gt; /(d)ev file system support OBSOLETE (<b>turn ON</b>)
--&gt; --&gt; --&gt; (A)utomatically mount at boot (<b>turn ON</b>)
(P)rofiling support
(K)ernel hacking
(S)ecurity options
(C)ryptographic options 
--&gt; (C)ryptographic API (<b>turn ON</b>)
--&gt; --&gt; (H)MAC support (<b>turn ON</b>)
--&gt; --&gt; (<b>turn ON the others as MODULE</b>)
(L)ibrary routines

Exit and save your configuration.  Then build the kernel (the following is for 2.6 kernels).  Expect the compile to take about an hour.
<pre>make &amp;&amp; make modules_install</pre>

Now you need to install your kernel into the boot partition.  Change the "2.6.6-gentoo" portion of the filenames to whatever you want.
<pre># cp arch/i386/boot/bzImage /boot/kernel-2.6.6-gentoo
# cp System.map /boot/System.map-2.6.6-gentoo
# cp .config /boot/config-2.6.6-gentoo</pre>

Next is [7.e. Installing Separate Kernel Modules](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7#kernel_modules), which is where we specify which modules from above that we configured as "MODULE" instead of "BUILT-IN" get loaded at bootup.  Use the command "<b>nano -w /etc/modules.autoload.d/kernel-2.6</b>" to edit your config file.  Here is what mine looked like (yours will probably be different).
<pre># autoloads the following modules at boot time
#LVM2 (logical volume manager)
dm-mod

#ethernet
#mii (not needed?)
#via-rhine (compiled as built-in)</pre>

I also need to emerge in LVM2 support as well as the "raidtools" package (per [Gentoo x86 Installation Tips &amp; Tricks](http://www.gentoo.org/doc/en/gentoo-x86-tipsntricks.xml#software-raid)).
<pre># modules-update
# emerge lvm2
# emerge raidtools</pre>

Time to edit the "/etc/fstab" table (see [8.a. Filesystem Information](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=8) and also refer back to [my mount commands from earlier](/techblog/2004/06/gentoo-install-2-via-epia-me6000.shtml)).  Here's my "/etc/fstab" file:
<pre>/dev/md0 /boot ext2 noauto,noatime 1 2
/dev/md2 / ext3 natime 0 1
/dev/md1 none swap sw 0 0
/dev/cdroms/cdrom0 /mnt/cdrom auto noauto,user 0 0

/dev/vgmirror/opt /opt ext3 noatime 0 3
/dev/vgmirror/usr /usr ext3 noatime 0 3
/dev/vgmirror/var /var ext3 noatime 0 3
/dev/vgmirror/home /home ext3 noatime 0 0
/dev/vgmirror/tmp /tmp ext2 noatime 0 3
/dev/vgmirror/vartmp /var/tmp ext2 noatime 0 3

none /proc proc defaults 0 0
none /dev/shm tmpfs defaults 0 0</pre>

Change your hostname, domainname, and the default run level.
<pre># echo yourhostname &gt; /etc/hostname
# echo yourdnsname &gt; /etc/dnsdomainname
# rc-update add domainname default
# nano -w /etc/conf.d/net
(either use iface_eth0="dhcp" or configure your IP and gateway)
# rc-update add net.eth0 default
# cat /etc/resolv.conf
(verify your DNS servers if you specified a static IP)
# nano -w /etc/rc.conf
(change CLOCK="UTC" to CLOCK="local")</pre>

Onward to [chapter 9, configuring the bootloader](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=9).  Here's where I ran into trouble; ["emerge grub" or "emerge lilo" failed with "cannot automatically mount your /boot partition"](/techblog/2004/06/gentoo-install-emerge-grub-or-emerge.shtml).
<pre># emerge grub</pre>

([continued in my next post](/techblog/2004/06/gentoo-install-6-grub-system-tools.shtml))<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VIAEPIA.shtml">VIAEPIA</a>
		<div class="Byline">
			posted by Thomas at 
			[10:37](http://www.tgharold.com/techblog/2004/06/gentoo-install-5-manual-kernel.shtml)

		</div>