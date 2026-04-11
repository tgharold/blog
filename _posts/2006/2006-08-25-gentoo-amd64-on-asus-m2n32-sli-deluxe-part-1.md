---
layout: post
title: 'Gentoo AMD64 on Asus M2N32-SLI Deluxe (part 1)'
date: '2006-08-25T10:03:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Time to build the base Gentoo Linux O/S.  While I plan on switching over to a Xen hypervisor kernel in a few days, I still need to get a base Gentoo system up and running.  But first, let me document what sort of machine I'm building and the reasoning behind some of the decisions.

The unit is a custom-built system that will serve as a test unit for building out an iSCSI SAN (and eventually serve as part of that SAN if it tests well).  There will be multiple NICs so that I can bond NICs for bandwidth and so that I can connect NICs to multiple switches in the SAN mesh (for fault-tolerance).  Initially, it will have only (2) SATA drives installed, but the eventual loadout will have a total of (14) SATA drives.

Since I needed (2) SATA RAID cards and (2) Intel PRO/1000 dual-port server gigabit NICs, I needed a motherboard with multiple PCIe slots.  The Asus M2N32-SLI Deluxe meets that requirement with (2) x16, (1) x4, and (1) x1 slots.  Plus it has (2) PCI slots.  These slots will be populated as follows:

PCIe x16: Intel PRO/1000 dual-port PCIe x4
PCIe x4: 8-port SATA RAID card PCIe x4
PCIe x1: HighPoint RocketRAID 2300 SATA-II 4-port PCIe x1
PCIe x16: Intel PRO/1000 dual-port PCIe x4
PCI: 3com 3C905B NIC
PCI: old PCI video card

So I'm using the x16 slots for something other then a video card (which works on newer BIOS revisions).

Plus, the motherboard is an AM2 with the newer AMD Pacifica virtualization technology (AMD-V).  That will do a better job of running Xen then the current Opteron 940pin CPUs.  This motherboard also supports ECC, which I will be installing in a few weeks.  Other features include: (6) SATA-II ports, (2) gigabit Marvel NICs, (1) internal SATA-II port on a Silicon Image chip, (1) ESATA on the Silicon Image chip, (10) USB ports, (2) Firewire ports.

Not a cheap board ($200 retail) and has quite a bit of headroom.  The PCIe architecture should also perform better then the older PCI motherboards, which is important in a 14-disk SAN unit.

All of this is being installed in a ThermalTake Armor tower case (MODELNUMBER?).  The Armor case has (2) internal hard drive bays (actually 3, but I'm only using 2 for thermal reasons) and (11) 5.25" bays on the front.  One of those 5.25" bays is occupied by the floppy drive mount location, the power and reset switches and the power and HD LEDs.  That leaves me with (10) 5.25" bays.  

In those (10) 5.25" bays, I'm installing a DVD-RW in the top and then filling the rest of the (9) bays with 4:3 SATA hot-plug back planes.  These will hold (12) SATA-II hard drives and allow us to swap out hard drives easily (even if we don't hotplug we can still minimize downtime).  The two internal drives are not as easy to replace, but they are still fairly easy to get at and replace in under 30 minutes.

My initial configuration plan is a (2) drive RAID1 using the internal bays and the motherboard SATA-II connectors.  That will allow me to get the OS up and running and do some limited testing.  After that I will add (4) HDs to the first hotswap bay, connect them to the HighPoint 2300 card, and run them as RAID10 for twice the performance as a 2-drive RAID1 set.

Down the road we will add the 8-port SATA RAID card and fill the other 8 bays in the front.  These will be configured as a (6) drive RAID10 set (3x performance) with (2) hot spare drives.  That will fill out the unit.  If I'm pressed for space and capacity, I could add a 3rd drive to the internal drive bay for a hot-spare (risking more heat) and setup the last (8) drives up front as a (8) drive RAID10.

The current power-supply is a 750W ThermalTake ToughPower unit.  Ideally, I'd install a redundant PSU in this case, but I'll tackle that at a future date.  One thing that I do wish I had done was to have bought the "modular" 750W PSU.  That unit makes the component power cables connect to plugs on the PSU making it easier to swap out a failed PSU without re-wiring all of the components.  However, due to all of the room inside the Armor case, re-wiring is not that difficult or time-consuming.

I'm also not ready to spend $500-$600 on a redundant PSU until I know whether the 750W can handle (15) hard drives plus an Athlon64 X2 4200+ with multiple NICs and expansion cards.  I'm pretty sure that it will.  The base recommendation for an Athlon64 X2 with a simple setup is 300-350W.  Figure that each additional hard drive adds 20W to the load (overstatement) and 15x20W = 300W.  That puts us up around 600-650W not including the extra expansion cards.  So the 750W should perform very well.

...

For the install, I plan on a partition layout like so (both sda and sdb are configured identically and then mirrored together):

<pre>Disk /dev/sda: 750.1 GB, 750156374016 bytes
255 heads, 63 sectors/track, 91201 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1               1          17      136521   fd  Linux raid autodetect
/dev/sda2              18        1015     8016435   fd  Linux raid autodetect
/dev/sda3            1016        2013     8016435   fd  Linux raid autodetect
/dev/sda4            2014       91201   716402610    5  Extended
/dev/sda5            2014        2512     4008186   fd  Linux raid autodetect
/dev/sda6            2513       91201   712394361   fd  Linux raid autodetect</pre>

Partition #1 is the boot partition.  I generally go with 128MB as it allows me to have a dozen or so kernels setup in grub.

Partition #2 and #3 are 8GB install partitions.  I plan on installing once to the first 8GB partition, then cloning the install to the second 8GB partition.  That way, worst case, if the primary install gets hosed, we can boot to the second partition which is still functional.

Partition #4 is simply the extended (logical) partition place-holder.

Partition #5 will be used for the Linux swap area.  I always mirror my swap so that the machine keeps running even if one of the drives fails.

Partition #6 is for LVM2 and will be sub-divided up.  I estimate that I'll use about 50-100GB for the O/S which will leave 600GB or so for use by clients.

That's a fairly conservative partition layout and should provide me with enough flexibility to recover from most situations without having to toss an install CD into the unit.

...

Other sysadmin tricks that I plan on using are:

- Using SubVersion to store the contents of /boot, /etc, and other system configuration files.  That will give me a history of changes to the system.  That has been working very well on my other systems.

- Using Bacula or rdiff-snapshot or rsync or dd to create snapshots of the working root volumes.  In worst-case, we restore the root volumes from backups.

- Sharing the portage tree between the two root partitions.  This is low-risk and will save space and time.

- Sharing the /tmp and /var/tmp LVM partitions between the two root partitions.  Naturally, the swap partition is also shared between the two root partitions.

- Putting /home on its own LVM partition and sharing it between the two root partitions.  Moderately risky, but since this is a server-only headless setup with no users, it's not a big deal.

...

So it's a moderately complex setup, but provides me with multiple fall-back positions and restoration options.  Anything from reverting a configuration file to a newer version, to booting a known-good root partition, to restoring the system from backups.

And there's always the last resort of putting a Gentoo boot CD in the unit, starting networking and the SSH daemon, and attempting to fix the unit remotely.
