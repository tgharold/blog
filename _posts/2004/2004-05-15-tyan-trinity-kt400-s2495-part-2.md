---
layout: post
title: 'Tyan Trinity KT400 S2495 (part 2)'
date: '2004-05-15T21:35:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>More fun with the Tyan Trinity KT400 S2495 board.  While attempting to add the Promise FastTrak TX2 PCI RAID card, everything is happy until I go and connect drives to it and define an array.  After that, if the Adaptec 2930CU PCI SCSI card is <b>also</b> installed, the system will not boot.  I have the HighPoint HPT372N IDE RAID ports disabled in the BIOS and the Silicon Image Sil3112 SATA ports enabled.

Symptom of the boot issue is that the Sil3112 BIOS splash will not appear during the boot process.  System will then hang before or at the ESCD/DMI update point (right before it boots from a device).

1. (neither TX2 or 2930CU) = boots
2. TX2 only = boots
3. 2930CU only = boots
4. 2930CU + TX2 = won't boot

Once I remove either of the TX2 or the 2930CU cards, things work fine.  I've stripped the 2930CU card, hooked the primary drives up to the TX2 RAID, left the scratch drive hooked to the Sil3112 SATA ports, swapped the SCSI CD-ROM / tape drive / zip drive for an IDE CD-RW and an IDE DVD-ROM/CD-RW drive.

During the install of Windows 2000, I hit F6 during the boot and install both the TX2 and the Sil3112 drivers.  This will avoid the issue where the boot order of the drives changes later when I add the Sil3112 driver post-install.

(I've lost count... this is something like my 6th attempt at getting Windows 2000 up and running on this motherboard.)

Update:  Everything looks fine so far, my first test copy of 2GB worth of data checked out okay with the MD5 tool (copying from the network to the TX2 RAID array as well as from the network to the Sil3112 SATA scratch drive).  Got everything patched and I'm now copying live data files onto the array.

Tyan Trinity KT400 (S2495)
3x512MB PC2100 RAM
AthlonXP 1800+ CPU
Promise FastTrak TX2 PCI IDE card
2x250GB 7200rpm drives, 8MB cache (o/s)
Silicon Image Sil3112 SATA ports (built-in)
200GB SATA 7200rpm drive (scratch)
IDE CD-RW
IDE DVD-ROM/CD-RW<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>
		<div class="Byline">
			posted by Thomas at 
			[21:35](http://www.tgharold.com/techblog/2004/05/tyan-trinity-kt400-s2495-part-2.shtml)

		</div>