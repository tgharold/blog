---
layout: post
title: 'Gentoo 2005.1 on Athlon64 3200+ and Asus A8V Deluxe'
date: '2005-11-04T18:24:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>So, I was going to rebuild my 1Ghz Athlon machine with 640MB, but in the process of transplating hard drives and installing a new (quieter) CPU fan, I seem to have put it down for the count.  Moderate annoyance only as it's an older motherboard and was nearing the end of its lifespan.  (I may try and troubleshoot it next week.)

Instead, I replaced with an Asus A8V Deluxe (VIA chipset, BIOS version 08.00.09 05/19/05) motherboard with an Athlon64 3200+ and 2GB of RAM.  In addition, I have (8) 300GB hard drives hooked up to this unit.  The (2) RAID1 boot drives are 7200rpm (hooked to the primary IDE port and the 2nd one on the Promise FastTrak RAID port).  The other (6) drives are 5400rpm drives hooked up to a Promise SX6000 card.

Now, I'm not sure that I can have both the onboard FastTrak and the SX6000 running at the same time.  (If not, I have a 1-port ATA/133 PCI HighPoint card that I can use for the 2nd boot drive.)

Tossed the Gentoo 2005.1 boot CD in.  The graphical splash screen loads, and it starts counting through devices.  At "Booting the system (64%)", I get a kernel panic and it stops booting.  The screen now reads (approximately):

<code>kernel BUG at &lt;bad filename&gt;:55433!
Invalid operand: 0000 [#1]
PREEMPT SMP
Modules linked in: ...
(bunch of registers)
Process swapper (pid: 0 ...
(trace dump)
&lt;0&gt; Kernel panic - not syncing: Fatal exception in interrupt</code>

Pressing [F2] does nothing at this point.

Attempting to boot Knoppix 4.0.2 CD results in the boot CD hanging during device initialization.  But if I boot the Knoppix CD as "failsafe" it loads correctly.

<b>Attempted fix #1:</b>

Disable the onboard Promise FastTrak controller (since I have a Promise SX6000 installed in a PCI slot).  In past Windows systems (FastTrak66 and FastTrak100 cards), their documentation indicates that you should not have two FastTrak cards installed at the same time.  Whether this applies to a SuperTrak and FastTrak pairing, I'm unsure.

Still got the error.  It's probably not the Promise cards.

<b>Attempted fix #2:</b>

Re-enable the Promise FastTrak controller (setting it as "IDE mode"), and check boot options on the Gentoo Universal LiveCD.  Since this is a single-core Athlon64, I'm going to try the NOSMP flag.  This involves intervening in the boot process when the LiveCD reaches the "boot:" prompt.  You can then type "<b>gentoo nosmp</b>" to boot the kernel without SMP support.

No luck, system hangs when initializing the kernel (I'm wondering if NOSMP is even a boot option on the LiveCD).

<b>Attempted fix #3:</b>

Check for a newer version of the BIOS at [Asus Support](http://support.asus.com/default.aspx?SLanguage=en-us).  ([One person's experience with flashing an A8V](http://www.planetamd64.com/lofiversion/index.php/t11803.html).)

No luck.  System still bombs out with a kernel error.

<b>Attempted fix #4:</b>

Downloaded the AMD64 version of the 2005.1 Universal LiveCD.  This still gives me a kernel bug, but it bombs out with a more descriptive error (rather then saying "bad filename".)  The kernel is bombing on "include/linux/i2o.h:517".

One note indicates that it's a bug between the SX6000 card and the Linux kernel.  One suggestion indicates that you should go into the SX6000 BIOS (hitting Ctrl-F when prompted after it scans the arrays) and set the operating system type to "Other OS".  (Tried this, no luck.)

Currently, I'm using 1.10 build 15 version of the BIOS (B77 from June 2002), and I see that there is a newer 1.20.0.27 from April 2004 on the Promise.com website.  So I'll go ahead and try patching up the Promise BIOS.  (Tried this as well, the SX6000 refuses to flash in this system.  I'm getting an error message while trying to usethe flash tool.  I'll try the card in another system and see if that works better.)

<b>Attempted fix #5:</b>

Ripped the SX6000 out.  I replaced it with (1) FastTrak133 TX2 PCI card and (3) HighPoint Rocket133 PCI cards.  I also converted one of the drives over to SATA, using the on-board SATA port.  (Think of this as a poor-man's setup.)  I had a bunch of the Rocket133 cards laying around, and the system doesn't seem to care that I have multiple cards installed.

(My first attempt, used a pair of FastTrak133 TX2 PCI cards, but that caused the system to lockup when I went into the BIOS setup.)

I'm currently running DBaN at the moment to test the configuration (PRNG mode, multiple passes, verifying all passes).  It identified 7 of the 8 drives (the onboard Promise RAID chip is unknown to this version of DBaN) and is writing to all 7 at the same time with no errors.  I'm getting 10MB/s to each drive with a load average of around 8.0.  Once I let that run for another hour or two, I'll switch back to trying the AMD64 Gentoo CD.

Booted into the AMD64 Gentoo CD with zero issues.  My drives are:

<code>livecd ~ # cat /proc/partitions
major minor  #blocks  name

   7     0      49712 loop0
  33     0  292970160 hde
  34     0  292970160 hdg
  57     0  292970160 hdk
  89     0  292970160 hdo
  91     0  292970160 hds
   3     0  293057352 hda
   8     0  293057352 sda
   8    16  199148544 sdb
livecd ~ #</code>

Basically, hda &amp; sda are my (2) 7200rpm 300GB drives that I'm going to use as my primary RAID1.  The sdb drive is my 200GB 7200rpm SATA which I plan on using for a scratch drive.  The rest of the drives (all ending in "160" blocks) are 5400rpm 300GB IDEs hooked to the Highpoint / Promise PCI cards.

Now I can go ahead and build my system.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>
		<div class="Byline">
			posted by Thomas at 
			[18:24](http://www.tgharold.com/techblog/2005/11/gentoo-20051-on-athlon64-3200-and-asus.shtml)

		</div>