---
layout: post
title: 'How Much Is That Terabyte in the Window?'
date: '2003-05-19T14:41:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Storage
- Technology
---

We've been considering switching to using a huge array of IDE drives instead of backup tapes for the office (tape drives being notoriously fickled unless you baby them *every* day).  Anyway, I priced out a low-cost, secondary storage system to get a feel for pricing.

SuperMicro SC830 server case (pedastal style).  It has (9) externally accessible 5.25" drive bays, 2x400W power supply, (3) 3.5" bays and is only $750.  The case design looks very good, plus since the 5.25" drive bays are external, I can use the Promise SuperSwap 1000 drive bays ($80) to get hot-swap capability.  Add in the Promise SX6000 raid card ($300) and I can chain together (6) ATA/100 drives.  Figure about $750 for guts (CPU, RAM, MB) and $750 for the O/S.

$750 SuperMicro SC830 server case
$750 CPU, RAM, MB, etc.
$750 O/S
$300 Promise SX6000 raid card
$640 (8) SuperSwap 1000 bays
$160 (2) 80Gb HDs for the O/S and Apps
----------
~$3500 base cost

IBM 120Gb $140x6 = $840 - net 480Gb $9.04/Gb
IBM 180Gb $220x6 = $1320 - net 720Gb $6.67/Gb
WD 250Gb $320x6 = $1920 - net 1000Gb $5.50/Gb

So, for about $5500 you can setup a server that will house 1000Gb of secondary storage using plain old IDE drives.  Pricing using SCSI drives would be around 3x that as a rough guess.

There's also the alternative of using one of the Promise Tech external SCSI-IDE RAID units, which will house (8) IDE drives and connects to the SCSI port of the server.  Pricing for the Promise SX8000 unit is $2600, but all you need to add then is (8) IDE drives.  This is actually a lot cheaper as you're able to make the array 50% larger by just adding 2 more disks.  Personally, I like the idea of the external unit because you don't have to fiddle with setting up another server and the cost per Gb really drops.

IBM 120Gb $140x8 = $1120 - net 720Gb $5.17/Gb
IBM 180Gb $220x8 = $1760 - net 1080Gb $4.04/Gb
WD 250Gb $320x8 = $2560 - net 1500Gb $3.44/Gb