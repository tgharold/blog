---
layout: post
title: 'Gentoo 2005.0 on Gigabyte GA-6VA7+ (part 2)'
date: '2005-03-31T09:43:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

Okay, tossed the new 2005.0 boot CD in, and I'm booting it up.  Just trying a standard default boot for the moment (not trying to use the "nohotplug" option yet).

Load the RAID modules, and verify some things:

<code># modprobe md
# modprobe dm-mod
# ifconfig         { verifies that the ethernet card is working }
# ls -l /dev/hd*</code>

Now, use <b>fdisk</b> to blow away and setup partitions.  (Note: You will lose all data on these disks when you perform this step.)  Use the 'w' command to confirm the destruction of all partitions when you're finished.

Setup the new partitions:

<code># fdisk /dev/hda

Command: n
Command action: p
Partition number: 1
First cylinder: 1
Last cylinder: +128M
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

Command: p

Command: w</code>

This gives me a 128MB boot area, a 2GB swap area, a 2GB root area, with the rest of the disk set aside for my LVM partitions.  Repeat the above commands to configure the 2nd disk in the same fashion.  Note that I'm using a different partition type then that shown in [chapter 4.c](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=4).  The 'fd' partition type is what I need to use since all 4 partitions on hda/hdc are going to be put into a software RAID1 set.

The 3rd disk is a single primary partition with the '8E' (LVM) type.  (Need to verify this, but I'm pretty sure that's correct.)

Create your "/etc/raidtab" configuration file (I used "<b>nano -w /etc/raidtab</b>", but other text editors will work).

<code># this config is for mirroring /dev/hda with /dev/hdc
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

# end of /etc/raidtab</code>

Create the raid set(s).

<code># mkraid /dev/md0
# mkraid /dev/md1
# mkraid /dev/md2
# mkraid /dev/md3</code>

If you get the error message: "raid_disks + spare_disks != nr_disks" when attempting to create any of your RAID sets, go back and verify your "/etc/raidtab" file as well as verifying your disk partitions. The RAID sets will build in the background and you should periodically monitor their progress using "<b>cat /proc/mdstat</b>". Another possibility is that you have set the "chunk-size" setting to be too small or too large (e.g. "chunk-size 4" did not work for me, but "chunk size 8" worked fine).

Building the raid sets may take a while, so once again, I'll come back to this point in a few hours.

Update:  <b>mkraid is tossing errors</b> (see my next post)<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gigabyte-GA-6VA7%2B.shtml">Gigabyte-GA-6VA7+</a>
		<div class="Byline">
			posted by Thomas at 
			[09:43](http://www.tgharold.com/techblog/2005/03/gentoo-20050-on-gigabyte-ga-6va7-part_31.shtml)

		</div>