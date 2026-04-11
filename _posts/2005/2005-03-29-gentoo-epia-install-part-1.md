---
layout: post
title: 'Gentoo EPIA Install (part 1)'
date: '2005-03-29T12:55:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

So, I'm back to re-building my VIA EPIA linux box (it was scavanged for another project for a few months).  Once again, I'm digging out my Gentoo CDs and I'm going to simply build a box where I can house my music MP3s and do some Apache / PostGreSQL work.  Since this is an EPIA box, the [EPIAWiki.org](http://www.epiawiki.org/wiki/tiki-index.php) site comes in handy.  I'll also be referring back to my [April 2004 notes](2004_04_01_archive.shtml) to speed up my setup process.

Hardware:

(1) VIA EPIA ME6000 (EPIA M series), 600Mhz fanless CPU
(2) 160GB 5400rpm hard drives (primary master, secondary master)
(1) DVD-ROM (secondary slave)
(1) Morex Venus 668 Black Case
(1) 512MB PC2100 DIMM

First up is BIOS settings:

<b>Standard CMOS Features</b>
- Halt On: All, But Keyboard
- all other settings are automatic

<b>Advanced CMOS Features</b>
- Virus Warning: Disabled
- CPU L2 Cache ECC Checking: Enabled
- Quick Power On Self Test: Disabled
- First Boot Device: Floppy
- Second Boot Device: CDROM
- Third Boot Device: HDD-0
- Boot Other Device: Disabled
- Swap Floppy Drive: Disabled
- Boot Up Floopy Seek: Enabled
- Boot Up NumLock Status: Enabled
- Typematic Rate Setting: 30
- Typematic Delay: 250
- Security Option: Setup (not configured)
- Dispaly Full Screen Logo: Disabled
- Show Summary Information: Enabled
- Display Small Logo: Enabled

<b>Advanced Chipset Features</b>
- AP Aperture Size: 32M
- CPU to PCI POST Write: Enabled
- Select Display Device: CRT
- Panel Type: 1024x768
- TV Type: NTSC
- CPU Direct Access FB: Enabled

<b>Integrated Peripherals</b>
- Super IO Devices: All disabled except FDC Controller
- Onboard IDE Channel 1: Enabled
- Onboard IDE Channel 2: Enabled
- IDE Prefetch Mode: Enabled
- Display Card Priority: AGP
- Frame Buffer Size: 32MB (amount of RAM to use for video card)
- AC97 Audio: Disabled
- MC97 Modem: Disabled
- VIA OnChip LAN: Enabled
- USB Keyboard Support: Disabled
- Onboard LAN Boot ROM: Disabled
- Onboard Fast IR: Disabled

<b>Power Management Setup</b>
- ACPI Suspend Type: S1&amp;S3
- HDD Power Down: Disabled
- Power Management Timer: Disabled
- Video Off Option: Suspend -> Off
- Power Off by PWRBTN: Delay 4 Sec
- Run VGABIOS if S3 Resume: Auto
- AC Loss Auto Restart: On
- Peripherals Activities: (not important)
- IRQs Activities: (not important)

<b>PnP/PCI Configurations</b>
- PNP OS Installed: Yes
- (ignoring the rest of the options)

<b>PC Health Status</b>
- (information only)

<b>Frequency/Voltage Control</b>
- (left alone)
