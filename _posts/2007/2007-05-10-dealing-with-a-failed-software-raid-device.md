---
layout: post
title: 'Dealing with a failed Software RAID device'
date: '2007-05-10T08:03:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


As part of my server setup, I like to make sure that plans are working as expected...  which means intentionally breaking things like RAID sets.

In this particular case I have a triple-active RAID1 mirror set on the first 3 disks in the system (/dev/sda, /dev/sdb, /dev/sdc).  In this RAID1 set, all 3 disks are active, with no hot-spare.  I prefer this over a (2) active (1) hot-spare setup because it allows for up to 2 disks to fail before you lose data.  And if I'm already dedicating a hot-spare spindle solely for the use of the RAID1 set, I may as well get to use it.  The output of /proc/mdstat looks similar to (note that none of the slices are tagged with a "(S)").:

<code>md2 : active raid1 sdc2[2] sdb2[1] sda2[0]
      7911936 blocks [3/3] [UUU]</code>

Each disk has quite a few md devices associated with it.  In this particular case I have /dev/md0 up through /dev/md5 created.  Probably one of the few downsides to SoftwareRAID is that you end up with quite a few md devices to keep track of.  But such is the price for just about the ultimate flexibility.

GRUB Note: In a mirrored setup, you must make sure to install GRUB to the MBR (master boot record) on all of the mirror disks.  Some Linux distros don't do this on their own and you'll have to do it yourself.  Otherwise, when the first disk in the mirror set fails, you'll find you're left with an unbootable system.  This is also why I like to make copies of the MBR for each disk in the system (# dd if=/dev/sda of=dd-sda-mbr-date.img bs=512 count=1).

So, after <b>making very good backups</b>, I decided it was time to test whether I could pull a disk and survive.  To make sure that I had taken care of the GRUB issue, I shutdown the server and pulled the primary drive in the RAID set.

<code># cat /proc/mdstat
md2 : active raid1 sdc2[2] sdb2[1]
      7911936 blocks [3/3] [_UU]</code>

Ah good, mdadm is *not* happy here (as expected).  It knows that one of the disks has failed in the array.  So let's shutdown and replace the failed drive with a blank one.  In this case, I used a spare drive that I had laying around that had been previously wiped.  (Or, with care, you could zero out the drive that you pulled.)

I recomend using "sfdisk" in dump mode to configure the new drive.  So if your failed drive is "sda" and one of the good ones is "sdb", you could use:

      # sfdisk -d /dev/sdb | sfdisk /dev/sda

After which, you can use the "mdadm" command to add the new slices to the existing RAID arrays.

      # mdadm --add /dev/mdX /dev/sdYZ 

Last, don't forget to install GRUB to the MBR on the new disk.
