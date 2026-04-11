---
layout: post
title: 'Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 5)'
date: '2005-04-20T23:39:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

(previous step)

Time to [install the bootloader](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=10).  I plan on using GRUB:

<code># emerge grub</code>

Now to configure GRUB (refer to my [old post about GRUB](/techblog/2004/06/gentoo-install-6-grub-system-tools.shtml) for a more in-depth explanation of what I'm telling GRUB to do here).

<code># grub --no-floppy
grub&gt; find /grub/stage1
(hd0,0)
(hd1,0)
grub&gt; root (hd0,0)
grub&gt; setup (hd0)
grub&gt; device (hd0) /dev/hdc
grub&gt; root (hd0,0)       
grub&gt; setup (hd0)
grub&gt; quit
#</code>

Now, edit your config file for grub:

<code># nano -w /boot/grub/grub.conf</code>

Here is what mine looks like.  Yours may be different, depending on how you configured things (and remember that I'm using Software RAID).

<code># cat /boot/grub/grub.conf
default 0
timeout 30
title=Gentoo Linux 2.6.11 (April 20 2005)
root (hd0,0)
kernel /kernel-2.6.11-gentoo-Apr20 root=/dev/md2
#</code>

Now I install various system tools (see the handbook):

<code># emerge syslog-ng
# rc-update add syslog-ng default
# emerge dcron
# rc-update add dcron default
# crontab /etc/crontab</code>

Note: Now you need to unmount everything that you can (including LVM), possibly shutdown the RAID as well prior to reboot.

<code>livecd gentoo # exit
livecd / # cd /
livecd / # cat /proc/mounts

(unmount all of your mounted partitions, including the LVM mounts)

livecd / # umount ... (insert list of mounted file systems)

livecd / # vgchange -an vgmirror
livecd / # reboot</code>

Pull the CD-ROM at this point, otherwise the LiveCD will probably boot.

(next step)
