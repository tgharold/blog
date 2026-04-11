---
layout: post
title: 'Gentoo Install 1 (VIA EPIA ME6000)'
date: '2004-06-15T12:39:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Going to rebuild my VIA EPIA Gentoo linux server.  While the [current setup](/blog/2004-04-27-gentoo-epia-install-part-1/) was fine, I've decided that I want to switch to use a pair of matched 5400rpm drives and [software RAID1](/blog/2004-06-15-lvm-and-software-raid/).  The configuration is identical to the [old drive configuration](/blog/2004-04-27-via-epia-gentoo-build/), except that I'm now using a pair of 300GB 5400rpm Maxtor drives.  The power draw seems to be well within the limits of the tiny power-supply in the Morex Venus 668 case.

I'm going to skip some of the [initial information about my setup](/blog/2004-04-27-gentoo-epia-install-part-1/) as all of that really hasn't changed.  Shared video memory is still only 32MB instead of the default 128MB, and I've turned off all of the ports and devices that I'm not going to use (leaving only ethernet, firewire and USB ports active).  I'm still using the Gentoo 2004.0 Universal CD as my bootstrap system.

Start by booting up the Gentoo Universal CD, as soon as you see the "<b>boot:</b>" prompt, enter the following command (which hopefully fixes the shutdown/lockup issue I had at the end of the last install):
<pre>boot: gentoo nohotplug</pre>

The LiveCD will then boot up, now load the md and dm-mod modules.  Prior to loading these two modules, "/proc/mdstat" will not exist:
<pre># modprobe md
# modprobe dm-mod</pre>

It's possible that your ethernet card on the VIA EPIA ME6000 will not be detected.  To fix this, you'll need to load the via-rhine module by hand, and then reconfigure your network adapters.
<pre># modprobe via-rhine
# net-setup eth0
# ifconfig</pre>

Create partitions using fdisk.  I want a 64MB /boot partition, a 2048MB swap partition, a 2048MB root partition, and the rest set aside for LVM.  Also see the [gentoo install documentation](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=4) section on preparing the disks.
<pre># ls /dev/hd*
# fdisk /dev/hda

Command: n
Command action: p
Partition number: 1
First cylinder: 1
Last cylinder: +64M
Command: a
Partition number: 1
Command: t
Hex code: fd

Command: n
Command action: p
Partition number: 2
First cylinder: [enter]
Last cylinder: +2048M
Command: t
Partition number: 2
Hex code: fd

Command: n
Command action: p
Partition number: 3
First cylinder: [enter]
Last cylinder: +2048M
Command: t
Partition number: 3
Hex code: fd

Command: n
Command action: p
First cylinder: [enter]
Last cylinder: [enter]
Command: t
Partition number: 4
Hex code: fd

Command: p</pre>

Verify your configuration.  My system had (4) primary partitions, with the first partition marked as active ('*' under the "Boot" column).  Now, write the partition table to disk (<b>be sure everything is correct</b>).
<pre>Command: w
#</pre>

Repeat the above for the 2nd disk in the array (/dev/hdc in my case).

Create your "/etc/raidtab" configuration file (I used "<b>nano -w /etc/raidtab</b>", but other text editors will work).
<pre># this config is for mirroring /dev/hda with /dev/hdc
# /boot (RAID1)
raiddev                 /dev/md0
raid-level              1
nr-raid-disks           2
nr-spare-disks          0
chunk-size              32
persistent-superblock   1
device                  /dev/hda1
raid-disk               0
device                  /dev/hdc1
raid-disk               1 

# *swap* (RAID1)
raiddev                 /dev/md1
raid-level              1
nr-raid-disks           2
nr-spare-disks          0
chunk-size              8
persistent-superblock   1
device                  /dev/hda2
raid-disk               0
device                  /dev/hdc2
raid-disk               1 

# / (RAID1)
raiddev                 /dev/md2
raid-level              1
nr-raid-disks           2
nr-spare-disks          0
chunk-size              32
persistent-superblock   1
device                  /dev/hda3
raid-disk               0
device                  /dev/hdc3
raid-disk               1 

# LVM (RAID1)
raiddev                 /dev/md3
raid-level              1
nr-raid-disks           2
nr-spare-disks          0
chunk-size              16
persistent-superblock   1
device                  /dev/hda4
raid-disk               0
device                  /dev/hdc4
raid-disk               1 

# end of /etc/raidtab</pre>

Create the raid set(s).
<pre># mkraid /dev/md0
# mkraid /dev/md1
# mkraid /dev/md2
# mkraid /dev/md3</pre>

If you get the error message: "raid_disks + spare_disks != nr_disks" when attempting to create any of your RAID sets, go back and verify your "/etc/raidtab" file as well as verifying your disk partitions.  The RAID sets will build in the background and you should periodically monitor their progress using "<b>cat /proc/mdstat</b>".  Another possibility is that you have set the "chunk-size" setting to be too small or too large (e.g. "chunk-size 4" did not work for me, but "chunk size 8" worked fine).  

Since it's going to take 150 minutes to prep that last RAID volume, I'm going to [pick this up again later](/blog/2004-06-15-gentoo-install-1-via-epia-me6000/).  Data rate according to "<b>cat /proc/mdstat</b>" is around 30MB/sec, which is about what I'd expect for a 5400rpm PATA drive.
