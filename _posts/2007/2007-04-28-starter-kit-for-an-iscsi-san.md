---
layout: post
title: 'Starter kit for an iSCSI SAN'
date: '2007-04-28T16:51:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Now that it's spring, it's time for us to start building out our preliminary iSCSI SAN unit.  Here's the hardware shopping list:

$0600 Super Micro 4U/TOWER RM EATX BLACK ( CSE-942I-R760B )
- triple-module redundant PSU w/ 760W
- 4U case for either rack or tower use
- (9) 5.25" bays

$0020 20-pin front panel connector to breakout cable
- Converts the 20-pin connector to something that can be attached to normal ATX motherboards
- CBL-0067 30cm 
- CBL-0085 15cm

$0050 Rackmount Rail Kit: CSE-PT26

$0320 (2) Spare PSU modules - PWS-0050(M)
- Spare PSU modules for the redundant PSU
- Useful to have a spare or two on-hand

$0600 (4) CSE-M35T1 (black) - SuperMicro SATA 5:3 backplanes
- These allow you to fit a total of (15) SATA drives into the (9) 5.25" bays
- There are other SATA 5:3 backplanes that you can use
- While we're only going to install (3) of these backplanes, I recommend buying a 4th for spare parts

$0167 3848163 (1) INTEL PRO/1000 PT DUAL PORT EXPI9402PT gigabit PCIe x4
- Used for SAN traffic
- Eventually, we'll upgrade to a quad-port PCIe or a 10GigE

$0167 1494573 (1) INTEL PRO/1000 PCI-X
- The PCI card is used to talk to the LAN and internet, no SAN traffic will flow over it
- You could use an inexpensive 10/100 PCI card, but with a dual-port NIC you can bond for high-availability

$0600 12-port Promise SATA-II PCIe x8 card EX12350
- CentOS5 automatically sees any drives attached to this card (when they are configured in JBOD mode)
- We're going the SoftwareRAID route

$0305 TYAN S2927G2NR dual-Opteron Socket F Thunder n3600B (S2927)
$0600 Opteron 2214 dual-core Socket F
$0200 (2) 1GB memory modules
$0100 (2) Socket F cooling fans (Cooljag CJC689C)
- (4) 1.8GHz cores should be plenty of horsepower to do use Software RAID instead of the Promise RAID software
- 2GB is probably minimal for RAM, 4GB would be better

$1800 (15) 500GB SATA-II drives
- 500GB is a good balance between price and capacity

Totals:

$3410 base system
$1800 drives

...

The drive plan for this unit is:

(3) 500GB drives in 3-way RAID1 (mirrored) for the operating system, log files, and other support software

Either:

(10) RAID10 + (2) hot-spares
(2) 5-disk RAID6 + (2) hot-spares

The pair of RAID6 arrays would give us about 20% more capacity (net of 6 disks vs 5 disks).  So the RAID10 setup results in around 2.27TB while the RAID6 setup would give 2.72TB.

With an overall cost of around $5500 for the entire unit, the price per gigabytes end up as:

$2.36/GB for (1) RAID10 array
$1.97/GB for (2) RAID6 arrays

Which is not terribly bad for a starter unit.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2007.shtml">2007</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/iSCSI.shtml">iSCSI</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SAN.shtml">SAN</a>
		<div class="Byline">
			posted by Thomas at 
			[16:51](http://www.tgharold.com/techblog/2007/04/starter-kit-for-iscsi-san.shtml)

		</div>