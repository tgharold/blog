---
layout: post
title: 'Gentoo emerge sync errors during installation'
date: '2005-09-18T12:50:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


So, I'm trying to install Gentoo 2005.1 on Software RAID and LVM2.  Everything seems to work up until I do my initial "emerge --sync".

<code>livecd / # emerge --sync
...
app-benchmarks/bashmark/
app-benchmarks/bashmark/files/
app-benchmarks/httperf/
app-benchmarks/httperf/files/
app-benchmarks/iozone/
app-benchmarks/iozone/files/
app-benchmarks/jmeter/
app-benchmarks/ltp/
app-benchmarks/nbench/
         986 100%    0.00kB/s    0:00:00
app-accessibility/java-access-bridge/ChangeLog
        2947 100%    0.00kB/s    0:00:00
app-accessibility/java-access-bridge/Manifest
         568 100%    0.00kB/s    0:00:00
app-accessibility/java-access-bridge/files/digest-java-access-bridge-1.4.5-r1
          77 100%    0.00kB/s    0:00:00
app-accessibility/java-access-bridge/java-access-bridge-1.4.5-r1.ebuild
        1250 100%    0.00kB/s    0:00:00
app-accessibility/java-access-bridge/java-access-bridge-1.4.5.ebuild
        1902 100%    0.00kB/s    0:00:00
app-accessibility/mbrola/ChangeLog
        3274 100%    0.00kB/s    0:00:00
app-accessibility/mbrola/Manifest
         616 100%    0.00kB/s    0:00:00
mkstemp "/usr/portage/app-accessibility/mbrola/files/.digest-mbrola-3.0.1h-r1.S11U8n" failed: Input/output error
         236 100%    0.00kB/s    0:00:00
mkstemp "/usr/portage/app-accessibility/mbrola/files/.digest-mbrola-3.0.1h-r3.C8lndQ" failed: Read-only file system
...</code>

Plan A:

Exit out of the chroot'd environment, umount the filesystem in question (/dev/vgmirror/usr).  I ran fsck against it and found numerous errors, so I just went and re-formatted.  Then re-mounted everything and started over with Chapter 5 (extraction of stages and onward).

Same issues

Plan B:

Don't use LVM2 during the initial installation.  My guess is that there's something not quite right on the 2005.1 boot CD for Gentoo.  So far it seems to be working, at least I'm hoping that I can get a system up and running before trying to get LVM2 up and running.

Plan C:

Use smaller disks.  I did some more digging and the Gigabyte motherboard almost certainly does not support 48bit LBA drives (larger then 136GB).  In fact, the Promise FastTrak66 card certainly does not but I was misled by the fact that DBaN (drive wipe software) showed me the full 160GB of the disks.  I'm running some tests now to see whether DBaN will pickup this sort of issue if you run it in verify mode.

I have (3) 120GB disks on order and will be dropping them into this system when they arrive.  That will take care of the issue and still allow me to put this older hardware into use.

Update #1: DBaN is reporting errors on the (2) 160GB disks attached to the Promise FastTrak66 card, but not for the drive connected directly to the motherboard.  (Method: PRNG Stream, Verify: All Passes)
