---
layout: post
title: 'More trouble with the Tyan'
date: '2004-05-15T02:55:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>So... this is definitely a taxing of my patience when installing hardware.

The latest problem is that if I copy a file from the network to the HighPoint RAID 1 array... it gets corrupted.  (Using a MD5 tool to verify content.)  However, if I verify the file up on the network server, it's correct.  And copying it to the SATA scratch drive, it copies cleanly.

So I'm at a bit of a loss at the moment (and running MemTest86 while I ponder).  

Off-hand, plan B is to make sure I have the latest and greatest BIOS installed (if I can get the BIOS to install, unlike my last attempt).  I'm sure I have the latest drivers, but I'll double-check that again in the morning.

Plan C is to ditch the highpoint RAID and try the Promise IDE RAID card again.

Plan D would be to buy a 3Ware 2-port PATA RAID card.

Update: Well, I went with plan E.  In a few places on the web I read 2 things.

1) HighPoint BIOS, when included on the motherboard, is generally not user-updatable.  Instead, it's part of the mainboard's BIOS and thus updated when you update the motherboard's BIOS.  

2) The [driver version that you use should match that of the BIOS](http://www.highpoint-tech.com/372drivers_down.htm).  I have a HPT372N with 2.345 of the BIOS.  However, I was attempting to use 2.351 of the Windows 2000 device driver.  Updating the driver to 2.345 (yes, Windows will actually say the older version is a better match) seems to have fixed the issue.

So right now, it looks like the data corruption bug is fixed.  (It only affected files copied to the drive from another server, not the service packs that I installed from CD or from the web site.)  Needless to say, I'll be doing some more testing with wxChecksum (MD5 utility) to verify that stuff is copying down correctly.

Update #2: The system is still corrupting files that as they are written to the HighPoint RAID array.  Especially when the system is under load, copying files to both the HighPoint and the SATA drives at the same time.  Copying from the network to the SATA drive works properly, but copying from the network or the SATA to the IDE RAID causes data corruption.

I'm now going to remove the HPT from the BIOS, and put the drives back on the Promise FastTrak100 TX2 IDE RAID card.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>
		<div class="Byline">
			posted by Thomas at 
			[02:55](http://www.tgharold.com/techblog/2004/05/more-trouble-with-tyan.shtml)

		</div>