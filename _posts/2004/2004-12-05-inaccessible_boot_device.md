---
layout: post
title: 'INACCESSIBLE_BOOT_DEVICE'
date: '2004-12-05T13:08:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Came home from my weekend trip to find that one of my Windows 2000 servers had crashed with the INACCESSIBLE_BOOT_DEVICE 0x0000007B error message.  Apparently, the power went out sometime this weekend because the 2nd server had turned itself off, and when the primary server booted back up it was BSOD'd with the 7B error.

The boot disks are mounted on a Promise FastTrak100 TX2 RAID card (which showed both disks as working).  So I wasn't too worried (I also have fairly fresh backups of everything on the RAID array.

[How to troubleshoot "Stop 0x0000007B" error messages in Windows 2000](http://support.microsoft.com/default.aspx?scid=kb;en-us;822052) wasn't all that useful.

[Troubleshooting Stop 0x0000007B or "0x4,0,0,0" Error](http://support.microsoft.com/default.aspx?scid=kb;en-us;122926) was a bit more useful.

The first thing tried was to remove any CDs/DVDs from the drives and reboot (no luck).  Then I tried rebooting into safe mode with the command prompt (no luck).  Then I tried rebooting to "last known good configuration" (again, no luck).  

Next, I booted up the Win2000 install CDs, loaded the RAID driver from floppy and went into (R)epair, (C)onsole mode (puts you at a command prompt in C:\WINNT).  A directory listing looked clean, so I did a "CHKDSK" from the C:\WINNT folder.  That found some errors, so I redid the command with the /R option ("CHKDSK /R").

Once it had finished checking the boot drive (C:), I rebooted the box and it came up fine.  It ran CHKDSK on all of the other drives during boot (finding some minor errors in the 2nd partition that is part of the Promise RAID).

My guess at this point is that when the UPS ran out of juice and the box crashed, it caused some issues with the NTFS file system.  One of these days I'll put each of my personal servers on their own UPSs and hookup the "shutdown on low battery" cable.
