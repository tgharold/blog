---
layout: post
title: 'Tyan KT400 Windows 2000 Boot Failure'
date: '2004-05-13T21:43:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>So after installing the 2nd round of patches (first round of patches was installing SP4 using WindowsUpdate), the system fails to start:

Windows 2000 could not start because the following file is missing or corrupt:
(something)\System32\Ntoskrnl.exe
Please re-install a copy of the above file.

Possibly, this is [error 319011 from Microsoft](http://support.microsoft.com/default.aspx?scid=kb;EN-US;319011), which indicates a corrupted BOOT.INI file.  Could be, since I just installed the driver for another disk in the system (hooked up a scratch drive to the SATA interface) in the previous WindowsUpdate.  This may have knocked my IDs around so that the BOOT.INI file is no longer correct.

Steps that they say to use, but which did NOT work for me:
1. Boot the Windows 2000 install CD
2. [F6] to load the device drivers for the boot array (in my case, HighPoint HPT372N IDE RAID).
3. Get to the point where you can pick [R]epair.
4. Choose [C]onsole, which should dump you at a command prompt (after you enter the local Administrator password).
5. Rename the existing BOOT.INI file in the root of C:, then copy a good BOOT.INI file off of a floppy.
6. Verify that [the correct NTBootDD.SYS file exists (troubleshooting)](http://support.microsoft.com/default.aspx?kbid=301680), and is in the correct place on the boot drive.  (Only if you have SCSI drives that you're attempting to boot from, the HighPoint RAID doesn't seem to use the NTBOOTDD.SYS file.)

Here's what my <b>broken</b> BOOT.INI file looks like (see [102873: BOOT.INI and ARC Path Naming Conventions and Usage](http://support.microsoft.com/default.aspx?scid=kb;EN-US;102873)):

[boot loader]
timeout=30
default=multi(0)disk(0)rdisk(0)partition(1)\WINNT
[operating systems]
multi(0)disk(0)rdisk(0)partition(1)\WINNT="Microsoft Windows 2000 Server" /fastdetect

Here's what my recovery BOOT.INI file looks like (note the change on the default= line, and the addition of a second multi(x) line under [operating systems], also note the long timeout value):

[boot loader]
timeout=120
default=multi(1)disk(0)rdisk(0)partition(1)\WINNT
[operating systems]
multi(0)disk(0)rdisk(0)partition(1)\WINNT="Microsoft Windows 2000 Server" /fastdetect
multi(1)disk(0)rdisk(0)partition(1)\WINNT="Microsoft Windows 2000 Server (HPT372N)" /fastdetect

Unfortunately, no matter what combination of scsi(x) or multi(x) I tried at the start of the line, or putting the driver file on the boot diskette (renamed as NTBootDD.SYS) would get me past the wonderful "Could not read from the selected boot disk" error.  At one point, I had a boot diskette with (8) different combinations of boot lines that I had tried.

Hint: The boot diskette is great for testing out BOOT.INI changes, it boots up quickly compared to waiting for the system to boot.

I'm going to try plan B, which is to reinstall... but during the Setup CD when I hit F6, I'm going to install both the HighPoint and the Silicon Image drivers.  That way, setup will see all of the disks in the system during the initial install and will hopefully write out a correct BOOT.INI file.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>
		<div class="Byline">
			posted by Thomas at 
			[21:43](http://www.tgharold.com/techblog/2004/05/tyan-kt400-windows-2000-boot-failure.shtml)

		</div>