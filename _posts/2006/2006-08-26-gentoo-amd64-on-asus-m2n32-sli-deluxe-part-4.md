---
layout: post
title: 'Gentoo AMD64 on Asus M2N32-SLI Deluxe (part 4)'
date: '2006-08-26T00:04:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>This is a record of the kernel flags that I'm going to use for my AMD64 system. It's an Asus M2N32-SLI Deluxe (NVIDIA nForce 590 SLI MCP chipset) with an Athlon64 X2 4200+ chip along with 2GB of RAM. Hard drives are hooked up to the onboard SATA-II controller (NVIDIA nForce 590 SLI MCP chipset). Plus the motherboard has a pair of onboard gigabit ethernet NICs (Marvell 88E1116) and a Silicon Image Sil3132 SATA-II controller.  Other chips on the motherboard are the nVidia C51XE, nVidia MCP55PXE, AD1988B, and TSB43AB22A.

In addition, I'll have even more hard drives hooked up to a  HighPoint RocketRAID 2300 PCIe card.  There's also a 3Com 3C905B PCI ethernet card installed along with a pair of Intel PRO/1000 PCIe gigabit NICs.

<code># emerge mdadm
# emerge lvm2
# cd /usr/src/linux
# make menuconfig</code>

Linux Kernel v2.6.17-gentoo-r4 Configuration
<b>C</b>ode maturity level options
<b>G</b>eneral setup
<b>L</b>oadable module support
<b>P</b>rocessor type and features
--&gt; <b>P</b>rocessor family (changed to "AMD-Opteron/Athlon64")
--&gt; <b>P</b>reemption Model (No Forced Preemption (Server))
<b>P</b>ower management options (ACPI, APM)
<b>B</b>us options (PCI, etc.)
<b>E</b>xecutable file formats
<b>D</b>evice drivers
--&gt; ATA/ATAPI/MFM/RLL support
--&gt; --&gt; <b>g</b>eneric/default IDE chipset support (should already be ON)
--&gt; --&gt; --&gt; <b>A</b>TI IXP chipset IDE support (turn OFF)
--&gt; --&gt; --&gt; <b>I</b>ntel PIIXn chipsets support (turn OFF)
--&gt; --&gt; --&gt; <b>I</b>T821X IDE support  (turn OFF)
--&gt; <b>S</b>CSI device support
--&gt; --&gt; <b>S</b>CSI generic support (turn this ON)
--&gt; --&gt; <b>S</b>CSI low-level drivers
--&gt; --&gt; --&gt; <b>S</b>erial ATA (SATA) support (should already be ON)
--&gt; --&gt; --&gt; --&gt; <b>I</b>ntel PIIX/ICH SATA support (turn OFF)
--&gt; --&gt; --&gt; --&gt; <b>S</b>ilicon Image SATA support (turn OFF)
--&gt; --&gt; --&gt; --&gt; <b>S</b>ilicon Image 3124/3132 SATA support (turn ON as BUILT-IN)
--&gt; --&gt; --&gt; --&gt; <b>V</b>IA SATA support (turn OFF)
--&gt; M<b>u</b>lti-device support (should already be ON)
--&gt; --&gt; <b>R</b>AID support (turn it ON as BUILT-IN)
--&gt; --&gt; --&gt; <b>R</b>AID-1 mirroring mode (turn it ON as BUILT-IN)
--&gt; --&gt; --&gt; <b>R</b>AID-10 mirroring striping mode (turn it ON as BUILT-IN)
--&gt; --&gt; <b>D</b>evice mapper support (turn ON as BUILT-IN)
--&gt; N<b>e</b>tworking support
--&gt; --&gt; <b>E</b>thernet (1000Mbit)
--&gt; --&gt; --&gt; <b>I</b>ntel<b>.</b> PRO/1000 Gigabit Ethernet support (turn ON)
--&gt; --&gt; --&gt; <b>B</b>roadcom Tigon3 support (turn OFF)
--&gt; <b>C</b>haracter Devices
--&gt; --&gt; <b>I</b>ntel/AMD/VIA HW Random Number Generator (should be ON)
--&gt; --&gt; <b>I</b>ntel 440LX/BX/GX, I8xx and E7x05 chipset support (turn it OFF)
--&gt; <b>S</b>ound
--&gt; --&gt; <b>S</b>ound card support (turn OFF)
<b>F</b>ile systems
--&gt; N<b>e</b>twork File Systems
--&gt; --&gt; <b>S</b>MB file system support (turn ON as BUILT-IN)
--&gt; --&gt; <b>C</b>IFS support (turn ON as BUILT-IN)
<b>P</b>rofiling support
<b>K</b>ernel hacking
<b>S</b>ecurity options
<b>C</b>ryptographic options
--&gt; <b>C</b>ryptographic API (turn ON)
--&gt; --&gt; HM<b>A</b>C support (NEW) (turn ON as BUILT-IN)
--&gt; --&gt; (turn ON all other options as MODULE)
<b>L</b>ibrary routines

Now we can compile and copy the kernel to the /boot partition.

<code># make &amp;&amp; make modules_install
# ls -l /boot
# ls -l arch/x86_64/boot
# df
# cp arch/x86_64/boot/bzImage /boot/kernel-2.6.17-25Aug2006-2300
# cp System.map /boot/System.map-2.6.17-25Aug2006-2300
# cp .config /boot/config-2.6.17-25Aug2006-2300
# ls -l /boot</code>

Next is [Chapter 8, Configuring your System](http://www.gentoo.org/doc/en/handbook/handbook-amd64.xml?part=1&amp;chap=8).

<code>(chroot) livecd linux # nano -w /etc/fstab</code>

My fstab (there are lines not shown):

<pre>/dev/md0                /boot           ext2            noauto,noatime  1 2        
/dev/md1                /               ext3            noatime         0 1        
/dev/md3                none            swap            sw              0 0        
/dev/cdroms/cdrom0      /mnt/cdrom      iso9660         noauto,ro       0 0
#/dev/fd0               /mnt/floppy     auto            noauto          0 0

/dev/vgmirror/home      /home                   ext3    noatime         0 3        
/dev/vgmirror/tmp       /tmp                    ext2    noatime         0 3 
/dev/vgmirror/vartmp    /var/tmp                ext2    noatime         0 3
/dev/vgmirror/log1      /var/log                ext3    noatime         0 3
/dev/vgmirror/portage   /usr/portage            ext3    noatime         0 3

/dev/vgmirror/svn       /var/svn                ext3    noatime         0 4        
/dev/vgmirror/backupsys /backup/system          ext3    noatime         0 4</pre>

Now for some final clean-up work:

<code>(chroot) livecd linux # nano -w /etc/conf.d/hostname
(chroot) livecd linux # nano -w /etc/conf.d/net
config_eth7=( "192.168.142.100 netmask 255.255.255.0" ) 
routes_eth7=( "default gw 192.168.142.1" )
(chroot) livecd linux # cd /etc/init.d
(chroot) livecd init.d # ln -s net.lo net.eth7
(chroot) livecd init.d # rc-update add net.eth7 default
 * net.eth7 added to runlevel default
 * rc-update complete.
(chroot) livecd init.d # cat /etc/resolv.conf
(verify your DNS servers if you specified a static IP)
(chroot) livecd init.d # nano -w /etc/conf.d/clock
CLOCK_SYSTOHC="yes"
(chroot) livecd init.d # passwd
(set your root password to something you will remember)
(chroot) livecd init.d # passwd
New UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
(chroot) livecd init.d #
# emerge syslog-ng
# rc-update add syslog-ng default
# emerge dcron
# rc-update add dcron default
# crontab /etc/crontab
# /usr/bin/ssh-keygen -t dsa -b 2048 -f /etc/ssh/ssh_host_dsa_key -N ""
(the key may take a a minute to generate)
# chmod 600 /etc/ssh/ssh_host_dsa_key
# chmod 644 /etc/ssh/ssh_host_dsa_key.pub
# rc-update add sshd default</code>

Now it's time for grub.

<code>(chroot) livecd init.d # emerge grub
(chroot) livecd init.d # ls -l /boot
total 3468
-rw-r--r--  1 root root 1090703 Aug 26 00:35 System.map-2.6.17-25Aug2006-2300
lrwxrwxrwx  1 root root       1 Aug 25 18:09 boot -&gt; .
-rw-r--r--  1 root root   28714 Aug 26 00:35 config-2.6.17-25Aug2006-2300
drwxr-xr-x  2 root root    1024 Aug 26 01:03 grub
-rw-r--r--  1 root root 2397504 Aug 26 00:35 kernel-2.6.17-25Aug2006-2300
drwx------  2 root root   12288 Aug 25 16:46 lost+found
(chroot) livecd init.d # nano -w /boot/grub/grub.conf
# Which listing to boot as default. 0 is the first, 1 the second etc.
default 0
timeout 30

# Aug 2006 Base Installation (software RAID, LVM2)                     
title=Gentoo Linux 2.6.17 (Aug 25 2006) BASE INSTALL
root (hd0,0)
kernel /kernel-2.6.17-25Aug2006-2300 root=/dev/md1         

# Aug 2006 Base Installation (software RAID, LVM2) - NOAPIC
title=Gentoo Linux 2.6.17 (Aug 25 2006) BASE NOAPIC 
root (hd0,0)
kernel /kernel-2.6.17-25Aug2006-2300 root=/dev/md1 noapic
(chroot) livecd init.d # grub --no-floppy
grub&gt; find /grub/stage1
(hd0,0)
(hd1,0)
grub&gt; root (hd0,0)
grub&gt; setup (hd0)
grub&gt; device (hd0) /dev/sdb
grub&gt; root (hd0,0)
grub&gt; setup (hd0)
grub&gt; quit</code>

Time to exit the chroot, unmount everything, and try a reboot.

<code>livecd / # cat /proc/mounts
rootfs / rootfs rw 0 0
tmpfs / tmpfs rw 0 0
/dev/hda /mnt/cdrom iso9660 ro 0 0
/dev/loop/0 /mnt/livecd squashfs ro 0 0
proc /proc proc rw,nodiratime 0 0
sysfs /sys sysfs rw 0 0
udev /dev tmpfs rw,nosuid 0 0
devpts /dev/pts devpts rw 0 0
tmpfs /mnt/livecd/lib64/firmware tmpfs rw 0 0
tmpfs /mnt/livecd/usr/portage tmpfs rw 0 0
usbfs /proc/bus/usb usbfs rw 0 0
/dev/md1 /mnt/gentoo ext3 rw,data=ordered 0 0
/dev/md0 /mnt/gentoo/boot ext2 rw,nogrpid 0 0
/dev/vgmirror/tmp /mnt/gentoo/tmp ext2 rw,nogrpid 0 0
/dev/vgmirror/vartmp /mnt/gentoo/var/tmp ext2 rw,nogrpid 0 0
/dev/vgmirror/home /mnt/gentoo/home ext3 rw,data=ordered 0 0
/dev/vgmirror/portage /mnt/gentoo/usr/portage ext3 rw,data=ordered 0 0
/dev/vgmirror/log1 /mnt/gentoo/var/log ext3 rw,data=ordered 0 0
/dev/vgmirror/svn /mnt/gentoo/var/svn ext3 rw,data=ordered 0 0
/dev/vgmirror/backupsys /mnt/gentoo/backup/system ext3 rw,data=ordered 0 0
none /mnt/gentoo/proc proc rw,nodiratime 0 0
udev /mnt/gentoo/dev tmpfs rw,nosuid 0 0
livecd / # unmount /mnt/gentoo/backup/system /mnt/gentoo/var/svn /mnt/gentoo/var/log /mnt/gentoo/usr/portage
-bash: unmount: command not found
livecd / # umount /mnt/gentoo/backup/system /mnt/gentoo/var/svn /mnt/gentoo/var/log /mnt/gentoo/usr/portage 
livecd / # umount /mnt/gentoo/home /mnt/gentoo/var/tmp /mnt/gentoo/tmp
livecd / # umount /mnt/gentoo/boot /mnt/gentoo/dev /mnt/gentoo/proc /mnt/gentoo
livecd / # reboot</code>

Remove the LiveCD and cross your fingers.  Success!<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>
		<div class="Byline">
			posted by Thomas at 
			[00:04](http://www.tgharold.com/techblog/2006/08/gentoo-amd64-on-asus-m2n32-sli-deluxe_26.shtml)

		</div>