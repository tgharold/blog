---
layout: post
title: 'Gentoo Install 6 (Grub, System Tools, Finalizing the Install)'
date: '2004-06-16T23:25:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


([previous post about configuring the kernel and setting up the filesystem](/blog/2004-06-16-gentoo-install-5-manual-kernel-configuration/))

Picking up with [9.b. Default: Using GRUB](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=9#doc_chap2) in the handbook.  (Also see my [older post about configuring grub](/blog/2004-04-28-gentoo-epia-install-part-6/).)  Also take a look at the end of the thread [](http://forums.gentoo.org/viewtopic.php?t=8813&amp;postdays=0&amp;postorder=asc&amp;highlight=raid&amp;start=100) on the gentoo forums (look for user "havoc") where it discusses how to setup grub on both the primary and secondary drives ([see the original article](http://lists.us.dell.com/pipermail/linux-poweredge/2003-July/014331.html)).  Now is also a good time to pull up the [official Software RAID HOWTO](http://unthought.net/Software-RAID.HOWTO/) and review that as well (especially section 7.3).
<pre># grub --no-floppy
grub&gt; find /grub/stage1
(hd0,0)
(hd1,0)
grub&gt; root (hd0,0)
grub&gt; setup (hd0)
grub&gt; device (hd0) /dev/hdc
grub&gt; root (hd0,0)       
grub&gt; setup (hd0)
grub&gt; quit</pre>

The above is a little tricky to follow.  The first "root" and "setup" commands specify that grub should boot from the first partition on hd0 (which is /dev/hda in my config) and "setup" installs the MBR record to the drive.

Then we pull a switch on grub with the "device" command, telling it to pretend that /dev/hdc (the secondary drive in the RAID array) is now hd0.  The second set of "root/setup" commands then write the MBR out to the 2nd drive in the array.  If I undstand everything correctly, this means that in the case of the primary drive dying, the RAID array will still be able to boot off of the secondary drive.  (I don't believe that you would need to move it to the primary cable.)

Now edit/create your config file for grub, "<b>nano -w /boot/grub/grub.conf"</b>".  You'll need to know the name of your kernel file that you compiled and copied to /boot earlier.  Here's what mine looks like (booting from the first partition on the first drive):
<pre>default 0
timeout 30
title=Gentoo Linux 2.6.6 (June 16 2004)
root (hd0,0)
kernel /kernel-2.6.6-gentoo root=/dev/md2</pre>

Refer to the handbook, [Installing Necessary System Tools](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=10), for the next few commands (I mostly used the defaults, but this is a cut-n-paste from my [previous install](/blog/2004-04-28-gentoo-epia-install-part-6/)).
<pre># emerge syslog-ng
# rc-update add syslog-ng default
# emerge dcron
# rc-update add dcron default
# crontab /etc/crontab</pre>

Then refer to [Finalizing your Gentoo Installation](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=11).
<pre># passwd
# useradd john -m -G users,wheel,audio -s /bin/bash
# passwd john</pre>

Note: Now you need to unmount everything that you can (including LVM), possibly shutdown the RAID as well prior to reboot.
<pre>livecd gentoo # exit
livecd / # cd /
livecd / # cat /proc/mounts

(unmount all of your mounted partitions, including the LVM mounts)
livecd / # umount ... (insert list of mounted file systems)

livecd / # vgchange -an vgmirror
livecd / # raidstop -a /dev/md0
livecd / # raidstop -a /dev/md3
livecd / # reboot</pre>

If all goes well, the system should shutdown and then restart from the software RAID.  

My system locked up during shutdown on or after "Stopping USB and PCI hotplugging".  Which probably means there was a boot option that I should've entered way back when I booted off the LiveCD (actually it means I didn't properly specify the "nohotplug" option at the "boot:" prompt on the LiveCD).
