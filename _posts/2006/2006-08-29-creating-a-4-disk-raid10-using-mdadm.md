---
layout: post
title: 'Creating a 4-disk RAID10 using mdadm'
date: '2006-08-29T13:25:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Since I can't seem to find instructions on how to do this (yet)...

I'm going to create a 4-disk RAID10 array using Linux Software RAID and mdadm.  The old way is to create individual RAID1 volumes and then stripe a RAID0 volume over the RAID1 arrays.  That requires creating extra /dev/mdN nodes which can be confusing to the admin that follows you.

1) Create the /dev/mdN node for the new RAID10 array.  In my case, I already have /dev/md0 to /dev/md4 so I'm going to create /dev/md5 (note that "5" appears twice in the command).

```
# mknod /dev/md5 b 9 5
```

2) Use fdisk on the (4) drives, create a single primary partition of type "fd" (Linux raid autodetect).  Note that I have *nothing* on these brand new drives, so I don't care if it wipes out data.

3) Create the mdadm RAID set using 4 devices and a level of RAID10.

```
# mdadm --create /dev/md5 -v --raid-devices=4 --chunk=32 --level=raid10 /dev/sdc1 /dev/sdd1 /dev/sde1 /dev/sdf1
```

Which will result in the following output:

```
mdadm: layout defaults to n1
mdadm: size set to 732571904K
mdadm: array /dev/md5 started.

# cat /proc/mdstat

Personalities : [raid1] [raid10] 
md5 : active raid10 sdf1[3] sde1[2] sdd1[1] sdc1[0]
      1465143808 blocks 32K chunks 2 near-copies [4/4] [UUUU]
      [&gt;....................]  resync =  0.2% (3058848/1465143808) finish=159.3min speed=152942K/sec
```

As you can see, we get around 150MB/s from the RAID10 array.  The regular RAID1 arrays only have about 75MB/s throughput (same as a single 750GB drive).

A final note.  My mdadm.conf file is completely empty on this system.  That works well for simple systems, but you'll want to create a configuration file in more complex setups.

<b>Updates:</b>

Most of the arrays that I've built have been based on 7200 RPM SATA drives.  For small arrays (4 disks w/ a hot spare), often you can find enough ports on the motherboard.  For larger arrays, you'll need to look for PCIe SATA controllers.  I've used Promise and 3ware SATA RAID cards.  Basically any card that allows the SATA drives to be seen and is supported directly in the Linux kernel are good bets (going forward we're going to switch to Areca at work).
