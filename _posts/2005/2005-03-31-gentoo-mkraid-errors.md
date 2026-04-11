---
layout: post
title: 'Gentoo mkraid errors'
date: '2005-03-31T10:08:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

So, I've created my /etc/raidtab file.  I've done the "<b>modprobe md</b>" and "<b>modprobe dm-mod</b>" commands.  I'm able to "<b>cat /proc/mdstat</b>" which shows that I have no personalities and no unused devices.  But, when I try to use the "<b>mkraid</b>" command, I get the following error:

```
# mkraid /dev/md0
cannot determine md version: no MD device file in /dev.
```

The fix (according to the wiki is):

```
cd /dev ; MAKEDEV md
```

The key resource to setting up Gentoo on a RAID:

[Gentoo Install on Software RAID](http://gentoo-wiki.com/HOWTO_Gentoo_Install_on_Software_RAID)

Now, they're not putting their swap file on a RAID1.  The reason that I put my swap in a RAID1 partition is that I don't want the system to crash if a drive dies (which it will, if you have 2 seperate, non-RAID swap partitions).  It's a question of whether you want a slightly higher level of stability, or if you want speed.

Other possible gotches:

1) (not confirmed) After you fdisk, you may want to reboot so make sure that the disks are no longer in use.  Otherwise you may get "bd_claim" errors when trying to setup the RAID array.

(still fighting with this a few hours later... going to start a new post)
