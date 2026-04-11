---
layout: post
title: 'More troubleshooting steps'
date: '2005-11-14T14:28:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>A) [AMD64 / Athlon X2 Opinions](http://forums.gentoo.org/viewtopic-t-385651-highlight-lost+ticks.html) - Recommends adding "clock=pmtmr notsc" to the kernel parameters in the grub.conf file.  It probably won't help with the sluggishness and lost ticks since those arguments are not being passed on the LiveCD boot.

The LiveCD boots with:

<code>livecd / # dmesg
Bootdata ok (command line is initrd=gentoo.igz root=/dev/ram0 init=/linuxrc looptype=squashfs loop=/livecd.squashfs udev nodevfs dokeymap cdroot vga=791 splash=silent,theme:livecd-2005.1 CONSOLE=/dev/tty1 quiet BOOT_IMAGE=gentoo )
Linux version 2.6.12-gentoo-r6 (root@poseidon) (gcc version 3.4.3 20041125 (Gentoo 3.4.3-r1, ssp-3.4.3-0, pie-8.7.7)) #1 SMP Mon Aug 1 14:22:17 UTC 2005
(snip)</code>

B) [Abit AN8 config file](http://home.earthlink.net/~paulsdead/config-vanilla) from [Help with kernel .config (amd64 3000+, s939 nforce4)](http://forums.gentoo.org/viewtopic-t-383692-highlight-lost+ticks.html).  The poster is also using "pci=biosirq pci=irqroute clock=pmtmr notsc" in their kernel config line.

(haven't tried yet)

C) Config file for an [Abit AN8-Ultra](http://people.clemson.edu/~rbjohns/linux/config-2.6.12-gentoo-r10).  No reported issues by the poster (same thread as #B above).

(haven't tried yet)

D) Turning off power management and CPU frequency options (in both the kernel and the BIOS).  A somewhat drastic step, but will allow me to hopefully rule this in/out.  This kernel will be my Nov 14th 1500 kernel.

I'm in the process of building this kernel.  But after booting and testing with it, no change in the issue.

E) Going to try flipping back to an earlier kernel.  I went back to my Nov 8th kernel and merely added in the driver support for sata_promise, the HPT302 chip and the TX2 card (even though the latter two are not installed at the moment).  I now have a slightly different "ticks" message:

Losing some ticks... checking if CPU frequency changed.
warning: many lost ticks.
Your time source seems to be instable or some driver is hogging interupts
rip scsi_dispatch_cmd+0x1f3/0x250

I had not seen "rip scsi_dispatch_cmd+0x1f3/0x250" yet.  The old message was "rip __do_softirq+0x48/0xb0".  Wow, no google hit for the scsi_dispatch_cmd line.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>
		<div class="Byline">
			posted by Thomas at 
			[14:28](http://www.tgharold.com/techblog/2005/11/more-troubleshooting-steps.shtml)

		</div>