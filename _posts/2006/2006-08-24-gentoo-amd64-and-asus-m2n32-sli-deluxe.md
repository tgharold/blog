---
layout: post
title: 'Gentoo AMD64 and Asus M2N32-SLI Deluxe'
date: '2006-08-24T14:24:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Finally got my Asus M2N32-SLI Deluxe motherboard setup and ready for installation.  Tossed the 2006.0 Gentoo AMD64 CD in and told it to use 80x25 for the old PCI video card that I have in it.  Unforunately, it hangs after a bit.

So my first plan of attack is to update the Asus BIOS from 0406 to 0603 (which is 2 revisions newer).  The 0603 revision was released on June 29, 2006.  The Asus BIOS includes an EZ-FLASH tool in the BIOS Setup (Tools menu), all I have to do is burn the BIOS file to a CD-ROM or diskette.

Update: It was actually easier to put the BIOS update on a USB flash drive and connect it one of the the USB ports.

Update #2: I had to boot the kernel using:

<code>boot: <b>gentoo noapic noacpi</b></code>

Which gets me past the hang at:

<code>io scheduler noop registered
io scheduler deadline registered</code>

I'm also using a very old PCI video card so I have to specify my video mode at the prompt (I usually pick 80x43).

Instead it now hangs at "Letting udev process events".  Could be time to try the "gentoo-nofb noapic" kernel option (no frame buffer). Hmm, that got me farther, but still no luck.  I'm reading that the nForce 590 chipsets aren't well supported by Linux yet.  Trying with the "noapic" option resulted in a hang entering kernel mode 3.

Time for plan B... seeing if the latest Ubuntu 6.06 CD works on this system.  That may give me some hints.  From what I'm reading I have to use the "apic=off" option on the Ubuntu 6.06 CD.  Hmm... that hung as well.

<code># gentoo-nofb noapic noacpi nolapic</code>

Hmm... still hangs.  Off to do some more research.

Update #3: Finally got a system that seems to be working.

Reverted the BIOS from the 0604 revision back to the 0503 revision.  Now I can boot the Gentoo AMD64 2006.0 minimal CD using the options <b>gentoo-nofb noapic</b>.  I still get the IRQ7 error that seems to be bugging other Gentoo users, but the system is stable enough to start the install.
