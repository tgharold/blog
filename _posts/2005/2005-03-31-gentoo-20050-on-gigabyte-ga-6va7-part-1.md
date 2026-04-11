---
layout: post
title: 'Gentoo 2005.0 on Gigabyte GA-6VA7+ (part 1)'
date: '2005-03-31T09:32:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

While I swap around some memory modules in the old EPIA box, I'm also going to take a swipe at using the new 2005.0 Gentoo image and build a 2nd box.

This is an old Celeron 350Mhz or 400Mhz CPU with 384MB of RAM (Gigabyte GA-6VA7+).  About the same power as the VIA EPIA motherboard.  I've already gone into the BIOS and disabled all optional ports (serial, parallel, etc).  Drives are configured as:

Pri M: 72GB - /dev/hda
Pri S: (free)
Sec M: 72GB - /dev/hdc
Sec S: CD-ROM - /dev/hdd

I also have a 3rd hard drive (80GB, /dev/hde) hooked up to an old Promise FastTrak66 PCI RAID card.  It uses the PDC20262 chip and I'm really just using it as an IDE card rather then making use of its RAID functionality.

I plan on mirroring using the two 72GB master drives and using the 80GB as a backup/scratch disk.  Similar setup and goals as the EPIA box from [last June's install](/techblog/2004_06_01_archive.shtml).
