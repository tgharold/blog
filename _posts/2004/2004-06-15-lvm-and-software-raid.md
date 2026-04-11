---
layout: post
title: 'LVM and Software RAID'
date: '2004-06-15T11:18:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Links:

[Linux Logical Volume Manager (LVM) on Software RAID](http://www.aplawrence.com/Linux/lvm.html) - explains the benefits of using LVM, and also how to get LVM running on top of software RAID in RedHat 8.

[Google search for how to do software RAID and LVM](http://www.google.com/search?hl=en&lr=&ie=UTF-8&c2coff=1&q=%2Blvm+%2B%22software+raid%22+%2Blinux+%2Bgentoo&btnG=Search)

[The Software-RAID HOWTO](http://www.ibiblio.org/pub/Linux/docs/HOWTO/other-formats/html_single/Software-RAID-HOWTO.html) - Updated June 2004, so it's not an old outdated document.  Also see [the official URL](http://unthought.net/Software-RAID.HOWTO/).

[Gentoo Server Project Wiki](http://www.subverted.net/wakka/wakka.php?wakka=LogicalVolumes) 

[Notes on Building a Linux Storage Server](http://www.ethics-gradient.net/myth/storage.html)

[Gentoo Forums: How to do a gentoo install on a software RAID](http://forums.gentoo.org/viewtopic.php?t=8813&highlight=raid) - Thread was started back in July 2002, but there are posts as recently as June 2004.

Summary:

The "grub" boot loader needs a real physical partition to boot from (or possibly a RAID1 setup, RAID0 definitely doesn't work).  What some folks do is to create (2) identical physical partitions on the drives in the RAID array, and then periodically copy from the primary partition to the secondary partition.  (See [gentoo forum post](http://forums.gentoo.org/viewtopic.php?t=8813&postdays=0&postorder=asc&highlight=raid&start=25&sid=579dfce1c7aeed1ca3f0219970171233) or search for user "wrex".  Also look for posts by "hover" or "blake121666")  The copy command is as simple as "dd if=/dev/hda1 of=/dev/hdb1 bs=8192b".  You need to customize that to match your configuration (e.g. changing the source/dest partitions and the block size).  If I can puzzle it all out, I think I'm going to go with /boot on RAID1.  See section 7.3 of the [Software RAID HOWTO](http://unthought.net/Software-RAID.HOWTO/)

The "swap" partition should be mirrored.  Otherwise when the disk fails, existing applications with data in the swap partition of the failed drive will die a nasty death.  See section 2.3 of the [Software RAID HOWTO](http://unthought.net/Software-RAID.HOWTO/).

There's a special set of command that need to be done in "grub" if you want to be able to pull the primary disk and still have the system bootable.  (In case the primary disk would fail.)  This is all mentioned in the [gentoo forums thread about software RAID](http://forums.gentoo.org/viewtopic.php?t=8813&postdays=0&postorder=asc&highlight=raid&start=100), look for the post by "hover".  Alternatively, you can simply use a boot floppy and fixup the grub settings after the primary drive fails.

Replacing a failed disk in a software RAID1 array requires partitioning the drive by hand prior to rebuilding the array.  This is also mentioned in the [gentoo forums thread about software RAID](http://forums.gentoo.org/viewtopic.php?t=8813&postdays=0&postorder=asc&highlight=raid&start=100), look for the post by "hover". 

Searching around on my Gentoo 2004.0 Universal CD, I don't see the "mdadm" tools anywhere, but I do see "raidtools".
