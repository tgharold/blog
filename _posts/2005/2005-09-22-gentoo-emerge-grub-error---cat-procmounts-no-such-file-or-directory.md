---
layout: post
title: 'Gentoo: emerge grub error - cat: /proc/mounts: No such file or directory'
date: '2005-09-22T20:49:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


During my initial Gentoo installation, I ran into the following issue after trying to "emerge grub".

```
...
>>> Completed installing grub-0.96-r2 into /var/tmp/portage/grub-0.96-r2/image/

>>> Merging sys-boot/grub-0.96-r2 to /
cat: /proc/mounts: No such file or directory
cat: /proc/mounts: No such file or directory
 * 
 * Cannot automatically mount your /boot partition.
 * Your boot partition has to be mounted rw before the installation
 * can continue. grub needs to install important files there.
 * 

!!! ERROR: sys-boot/grub-0.96-r2 failed.
!!! Function mount-boot_mount_boot_partition, Line 51, Exitcode 0
!!! Please mount your /boot partition manually!
!!! If you need support, post the topmost build error, NOT this status message.

!!! FAILED preinst: 1
livecd linux # grub
bash: grub: command not found
```

[This thread over at Short-Media](http://www.short-media.com/forum/archive/index.php/t-15576.html) has exactly this error listed.  However, that thread went nowhere and the user was redirected to search over at the Gentoo.org forums.

[emerge grub fails (Jun 2004)](http://forums.gentoo.org/viewtopic.php?t=187073)
['emerge grub' fails (Jun 2004)](http://forums.gentoo.org/viewtopic.php?t=183830)
[Grub wont compile. (Apr 2004)](http://forums.gentoo.org/viewtopic.php?t=165555)

Most posters indicate that you must run the following command prior to entering the chroot environment.  

```
mount -t proc /proc /mnt/gentoo/proc 
```

However, I can look back at my session logs and see that I already ran that particular command before entering the chroot.  Oh, wait... no I did not run that particular command. (This is where using a terminal program like SecureCRT comes in handy.)  This command should have been run just prior to entering the chroot environment.  ([See chapter 6 of the installation handbook.](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=6))

The fix should be as simple as:

```
livecd linux # cat /proc/mounts
cat: /proc/mounts: No such file or directory
livecd linux # exit
exit
livecd gentoo # mount -t proc none /mnt/gentoo/proc
livecd gentoo # chroot /mnt/gentoo /bin/bash
livecd / # env-update
>>> Regenerating /etc/ld.so.cache...
livecd / # source /etc/profile
livecd / # emerge grub
```
