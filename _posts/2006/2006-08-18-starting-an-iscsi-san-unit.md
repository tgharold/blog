---
layout: post
title: 'Starting an iSCSI SAN unit'
date: '2006-08-18T23:17:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>So here's my first stab at a SAN unit that can hold 14 or 17 SATA drives.  All of the drives will be mounted in hot-swap trays which should make things much easier.  Some of the components are a bit overkill (such as the pair of dual-port server NICs) but I'm planning ahead to when we have two gigabit switches and we want to connect multiple gigabit ports together for speed.

For the case, motherboard and misc parts:

$0159 Thermaltake Armor VA8000BNS Black Chassis: 1.0mm SECC
$0190 Thermaltake ToughPower W0117RU ATX12V/ EPS12V 750W
$0035 DVD-RW (BLACK)
$0050 misc parts (fans, cables)
$0182 MB-BA22658 AMD Athlon64 X2 4200+ AM2 (WINDSOR)
$0200 XXXXXXXXXX Asus M2N32-SLI DLX
$0138 XXXXXXXXXX Mwave 2GB DDR2 533 (1GB x 2)
$0009 XXXXXXXXXX Assemble &amp; Test

The motherboard is a ASUS M2N32-SLI with multiple PCIe slots (2 x16, 1 x4, 1 x1), 2 PCI slots, 8 SATA-II ports, and dual-NICs on an nForce 590 chipset.  I plan on using the expansion slots as follows:

PCIe x16: Intel Pro/1000 PT Dual-Port PCIe x4
PCIe x4: HP RocketRAID 2320 8-port PCIe x4
PCIe x1: HP RocketRAID 2300 4-port PCIe x4
PCIe x16: Intel Pro/1000 PT Dual-Port PCIe x4
PCI:
PCI:  PCI video card

Note: I expect that you will need a fairly recent BIOS version in order to use the first x16 slot for something other then a video card.

Prices for the SATA controllers and NICs:

$0167 INTEL PRO/1000 PT DUAL PORT EXPI9402PT gigabit PCIe x4
$0140 HighPoint RocketRAID 2300 PCIe x1 (4-port SATA-II)
$0260 HighPoint RocketRAID 2320 PCIe x4 (8-port SATA-II)

Note: I'm not 100% sure that I'm going to use the RocketRAID 2320.  I still need to do some research to verify that it works properly in Linux without special binary drivers (I want it to work as a regular controller card).  Otherwise I may use either the PROMISE SuperTrak EX8350 PCIe x4 (8-port SATA-II) or the 3ware 9590SE-8ML PCIe x4 (8-port SATA-II).

Other components:

$0350 Seagate Barracuda 7200.10 750GB SATA-II
$0110 Athena Power 5:3 SATA-II Backplane SATA3051B (350SATA)

The 5:3 backplane should allow me to fit 15 drives into the front 5.25" expansion bays on the Thermaltake Armor case.  If I don't care for the design of the 5:3 backplane there are more conservative 4:3 backplanes that will allow me to fit 12 drives into the front bays.  

Or I could even use some 4:3 SCSI SCA hot-swap enclosures along with a PCIe x4 SCSI card.  That lets me have both SATA and SCSI drives in the same unit.  A pair of those would give me 6 SATA drives and 8 SCSI drives.

Estimated cost for the starter kit is $3200, including a pair of 750GB SATA drives.  Since I'll be building two of these, and then gradually expanding them:

$3200 02 - 700GB SAN (2 base disks per SAN) -- $4.57/GB
$3200 02 - redundancy for 700GB SAN (2 base disks per SAN) -- $9.14/GB
$1400 04 - expansion to 1.4TB (2 data disks per SAN added) -- $5.57/GB
$2800 08 - expansion to 2.8TB or reconfig to 3.5TB -- $3.78 to $3.03/GB
$2800 12 - expansion to 4.2TB or reconfig to 6.3TB -- $3.19 to $2.13/GB
$1400 14 - expansion to 4.9TB or reconfig to 7.7TB -- $3.02 to $1.92/GB

The 2nd column is the number of drives installed within a single SAN unit.  The first capacity is if I stick with my initial plan of RAID1 within the SAN unit and then RAID1 across the SAN fabric for redundancy.  The second capacity is if I RAID5 within the unit and then RAID1 across the SAN fabric for redundancy.

I may also expand the memory in the SAN boxes to 6GB or 8GB down the road to maximize any possible read-caching.

For home use, I wouldn't bother to build a 2nd SAN unit for redundancy.  Downtime in case of a blown power-supply would only be about 2 hours (assuming you have one on-hand) to a day or two.  I could also cut some costs by going with less expensive NICs or SATA controllers.  But that doesn't gain you much.

The other advantage of building out slowly is that you can take advantage of the 1TB and 2TB drives that might appear in 2007-2009.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/iSCSI.shtml">iSCSI</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SAN.shtml">SAN</a>
		<div class="Byline">
			posted by Thomas at 
			[23:17](http://www.tgharold.com/techblog/2006/08/starting-iscsi-san-unit.shtml)

		</div>