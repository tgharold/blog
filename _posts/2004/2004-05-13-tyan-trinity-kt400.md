---
layout: post
title: 'Tyan Trinity KT400'
date: '2004-05-13T02:51:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


So I'm finally ditching the very troublesome Asus A7V266-E motherboard in my one file server.  I went with the [Tyan Trinity KT400](ftp://ftp.tyan.com/datasheets/d_s2495_105.pdf) because it was relatively inexpensive and I was able to simply move my AthlonXP 1800+ CPU and my 512MB PC2100 memory modules over to the new motherboard.

The old A7V266-E is a VIA-based chipset that was notorious for problems with the PCI bus ([search around for KT266 and PCI latency](http://www.google.com/search?hl=en&q=via+kt266+pci+bus+latency&btnG=Google+Search), or check the [PCI Latency Patch](http://adsl.cutw.net/dlink-dsl200-via.html) page).  (And that's on top of the issue that the A7V266-E Promise FastTrak100 Lite only supports 127GB and smaller drives.)  For me, it manifested itself as an incompatibility with my add-in Adaptec USB card.  Anytime I had activity on the USB bus, the entire machine would halt for a few seconds at a time.  Extremely annoying and the only way that I got around it was to not install the Adaptec 3100 USB PCI card.

So, getting a new motherboard should be easy right?  Ha ha ha ha ha ha!  (picks self back up off of the floor)

Well, before I start into the problems encountered... first I want to point you at what Tyan does correctly.  They make a very pretty manual.  When showing you the diagrams of various jumpers / pin-outs on the motherboard, they use very large text to draw your eye to the proper portion of the diagram.  It's rather well done, and makes it easy to flip through the book looking for, say, the FAN3 pin-out location.  Secondly, their motherboard includes the little 2-digit hexadecimal LED that shows you where the boot process is.  Usually, you have to buy an inexpensive add-in card (and I'm not even sure you can get them for PCI?).

Unfortunately, one of the things that they do poorly is the presentation of device drivers for their products.  Most motherboard manufacturers have a dedicated search engine, or a seperate page for each product.  And each page points to a local copy of all of the BIOS files, device drivers and manuals.  Tyan, OTOH, has a single page for BIOS, a single page for all their motherboards, a single page for RAID adapters (for all motherboards).   Worse, they rely on external websites to supply some of the drivers (e.g. their link to the VIA 4-in-1 driver set is useless since VIA has rearranged their site).  That's a real problem if you're not a grizzled vetran of DIY PC building.

So let's see... first issue is that the battery that came with the motherboard appears to be dead.  Removing power from the motherboard causes the BIOS clock to reset to the default of Jan 1 2003.  Replacing that was easy, I just stole the CR2032 battery from the old motherboard.

Next up, I plugged the (2) 250GB 7200rpm WD drives into the motherboard IDE RAID (HighPoint HPT372N), booted up on the SCSI CD-ROM and attempted to install Win2000 server.  Nada... tried 3x, with re-formatting the disk each time in case of read errors, but after you load the driver, Win2000 setup cannot see the HTP RAID that I had configured.

Okay, plan B, put a Promise FastTrak100 TX2 card in, hook the drives to that... spend another few hours setting up the drive array.  Now, the system refused to boot.  It gets to the ECSD/DMI portion (where it's setting up the PCI slots, figuring out what's where), but will not boot from the floppy or the CD-ROM.  Pull the Promise card back out, system boots up on the floppy or CD-ROM without a problem... put card back in, nada.  Updated the [Tyan Trinity KT400 motherboard BIOS from 1.02 to 1.05](http://www.tyan.com/support/html/bios_support.html), with no change in the situation.  The motherboard will not boot with the Promise card installed, regardless whether the onboard IDE RAID is enabled or disabled.

My next plan is now to try the HighPoint RAID again, possibly updating the HighPoint RAID BIOS (once I wait a few hours for the HighPoint array to finish duplicating itself again, my estimate is it takes 4-5 hours to create the 250GB array, roughly 45-60GB/hr).  Note, when trying to figure out which of the BIOS files to load into memory (e.g. my disk has BIOS\3xxv235.p4e, BIOS\3xxv235.p5e, and BIOS\3xxv235.p6e), refer to the README.TXT file on the root of the floppy.  Under section 2, there is a file listing that will tell you which BIOS file goes with which controller chip.  (e.g. I have a HPT372N, so I use the .P5E file)

Next error (loading the HPT BIOS).  I run the LOAD.EXE file, enter the BIOS file name (3XXV2351.P5E), it then errors out with:

    A:\BIOS&gt; <b>LOAD</b>
    Please input BIOS image file name: 3XXV2351.P5E
    Found adapter at bus 0, device 14
    No loadable EPROM found
    Try '-i' option

    A:\BIOS&gt; <b>LOAD /I 3XXV2351.P5E</b>
    Found adapter at bus 0, device 14
    No loadable EPROM found
    Found adapter at bus 0, device 14
    No loadable EPROM found

    Hmm... oh, wait... looks like the P4E file is <b>also</b> for the 372N chip.

    A:\BIOS&gt; <b>LOAD 3XXV2351.P4E</b>
    No supporting host adapter is found

Okay... (drums fingers on desk), eh, forget it for now.  I have v2.345 already, which is reasonably up-to-date.  And this time, the Win2k install seems to have found the partition correctly (only basic difference between now and when it didn't work last night is the motherboard BIOS revision update from 1.02 to 1.05).

Created my 16GB C: partition, and I'm off and installing.  Later, I get to test my recovery strategy (going to try to restore the system state through a non-authoritative restore).
