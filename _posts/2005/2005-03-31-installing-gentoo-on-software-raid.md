---
layout: post
title: 'Installing Gentoo on Software RAID'
date: '2005-03-31T15:48:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>I'm currently fighting with this again.  Apparently, there have been some changes between the 2004.0 CD and the 2005.0 CD (mostly related to the 2.6 kernal and the DevFS vs UDev systems).

First off, some tips-n-tricks:

1) <b>ifconfig</b> - find out the IP address of the box
2) <b>passwd</b> - change the root password to something you know
3) [Starting the SSH daemon](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=2) - The command is: <b>/etc/init.d/sshd start</b>

Now I'll be able to use SecureCRT and have an easier time of copy-n-paste.  (Pick 'keyboard interactive' and 'ssh2' under options when setting up the connection in SecureCRT.)

Links:

[Gentoo 2004.3 Software RAID Install HOWTO](http://forums.gentoo.org/viewtopic.php?t=257374&amp;highlight=mknod+dev+md0)
[Gentoo.org - x86 tips and tricks (including software RAID)](http://www.gentoo.org/doc/en/gentoo-x86-tipsntricks.xml)
[The Linux Documentation Project: Software RAID](http://www.tldp.org/HOWTO/Software-RAID-HOWTO.html)
[An older gentoo.org thread on software raid](http://forums.gentoo.org/viewtopic.php?p=46458#46458)

Now... to show you what I did and where it breaks.  I have (2) IDE disks, attached as /dev/hda and /dev/hdc.  I plan on mirroring them, and have already created /dev/hda1 (128MB for /boot), /dev/hda2 (2GB for swap), /dev/hda3 (2GB for root), and /dev/hda4 (rest of disk for LVM).  All partitions are flagged as type 'fd' (linux raid auto).

<code># modprobe md
# ls /dev/md*
ls: /dev/md*: No such file or directory
# for i in 0 1 2 3; do mknod /dev/md$i b 9 $i; done 
# ls /dev/md*
/dev/md0  /dev/md1  /dev/md2  /dev/md3
# nano -w /etc/mdadm.conf</code>

Contents of my mdadm.conf file:

<code>DEVICE /dev/hda1 /dev/hda2 /dev/hda3 /dev/hda4
DEVICE /dev/hdc1 /dev/hdc2 /dev/hdc3 /dev/hdc4

ARRAY /dev/md0 devices=/dev/hda1,/dev/hdc1
ARRAY /dev/md1 devices=/dev/hda2,/dev/hdc2
ARRAY /dev/md2 devices=/dev/hda3,/dev/hdc3
ARRAY /dev/md3 devices=/dev/hda4,/dev/hdc4 </code>

Pretty generic... now to create the raid.  This is where we hit our first issue:

<code># modprobe raid1
# mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/hda1 /dev/hdc1 
mdadm: /dev/hda1 appears to contain an ext2fs file system
    size=72192K  mtime=Wed Mar 30 16:46:07 2005
mdadm: /dev/hdc1 appears to contain an ext2fs file system
    size=72192K  mtime=Wed Mar 30 16:46:07 2005
Continue creating array? y
mdadm: ADD_NEW_DISK for /dev/hda1 failed: Device or resource busy
# </code>

Here are the problems:

1) Even though I have a 128MB partition for /boot, it is still showing 64MB from a previous partitioning scheme.

2) mdadm: ADD_NEW_DISK for /dev/hda1 failed: Device or resource busy

So... take a look at my partition list:

<code>livecd root # fdisk -l 

Disk /dev/hda: 76.8 GB, 76869918720 bytes
16 heads, 63 sectors/track, 148945 cylinders
Units = cylinders of 1008 * 512 = 516096 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/hda1   *           1         249      125464+  fd  Linux raid autodetect
/dev/hda2             250        4218     2000376   fd  Linux raid autodetect
/dev/hda3            4219        8187     2000376   fd  Linux raid autodetect
/dev/hda4            8188      148945    70942032   fd  Linux raid autodetect

Disk /dev/hdc: 76.8 GB, 76869918720 bytes
16 heads, 63 sectors/track, 148945 cylinders
Units = cylinders of 1008 * 512 = 516096 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/hdc1   *           1         249      125464+  fd  Linux raid autodetect
/dev/hdc2             250        4218     2000376   fd  Linux raid autodetect
/dev/hdc3            4219        8187     2000376   fd  Linux raid autodetect
/dev/hdc4            8188      148945    70942032   fd  Linux raid autodetect
livecd root # </code>

All of which looks right and proper.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SoftwareRAID.shtml">SoftwareRAID</a>
		<div class="Byline">
			posted by Thomas at 
			[15:48](http://www.tgharold.com/techblog/2005/03/installing-gentoo-on-software-raid.shtml)

		</div>