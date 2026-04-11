---
layout: post
title: 'Gentoo Install: "emerge grub" or "emerge lilo" fails to mount /boot'
date: '2004-06-16T15:26:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Sometimes "emerge grub" or "emerge lilo" fails with the following error and you are attempting to mount "/boot" on a software RAID1 partition:
```
*
* Cannot automatically mount your /boot partition.
* Your boot partition has to be mounted rw before the installation
* can continue. lilo needs to install important files there.
*

!!! ERROR: sys-boot/lilo-22.5.8-r1 failed.
!!! Function mount-boot_mount_boot_partition, Line 53, Exitcode 0
!!! Please mount your /boot partition manually!

!!! FAILED preinst: 1
```

(The error messages will be pretty much identical for both "lilo" and "grub".)

The problem was, for me at least, that prior to doing the chroot into the new environment, I had failed to mkdir and mount the /boot partition.  ([See the start of step 2 in my install notes](/blog/2004-06-15-gentoo-install-2-via-epia-me6000/).)

Here's the quick-n-easy way that I fixed the problem.  I had to temporarily exit out of the chroot'd environment, back to the livecd bootup environment, mount the partition, and then chroot back.
```
livecd / # exit
livecd / # mkdir /mnt/gentoo/boot
livecd / # mount /dev/md0 /mnt/gentoo/boot
livecd / # cat /proc/mounts
livecd gentoo # chroot /mnt/gentoo /bin/bash
livecd / # env-update
livecd / # source /etc/profile

(now copy your kernel into /boot again from /usr/src/linux-2.6.6)

livecd / # emerge lilo
(or if you're using grub...)
livecd / # emerge grub
```

Update: While this set of instructions did properly fixup the /boot partition with "grub", it really didn't treat the root cause of the entire mess.  (See [Troubleshooting Software RAID](/blog/2004-06-17-troubleshooting-software-raid-boot-problems/).)

The root-cause was that back when I did the first part of the install, not only did I fail to mount the /mnt/gentoo and /mnt/gentoo/boot folders properly, but I then mounted them out-of-order when I did catch the error.  That causes all sorts of problems down the road, yet the install process will look like it's going off without a hitch (until you reboot).

Links:

[www.gentoo.pl](http://www.gentoo.pl/?id=forum&id_watek=1669&posty=1) - This page might've had the answer, but unfortunately it was written in polish.
