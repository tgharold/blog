---
layout: post
title: 'SAN testing switch'
date: '2006-08-19T19:39:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


For testing out the SAN, it looks like I can make use of either a 
SMC SMCGS16-SMART or SMC SMCGS24-SMART switch.  These are 16/24 port gigabit switches that support link aggragation.  Price on the 16-port unit is only $260 or so and the 24-port switch sells for $320.

I'm still figuring out how I want to support bonding in the unit.  I have the (4) ports from the Intel Pro adapters plus the (2) ports on the motherboard.  My initial plan is to bond the Intel adapters together into a two pairs, then hook each pair to a different switch for fault-tolerance.  That would give me either 200MB/s of bandwidth or 400MB/s of bandwidth.

I'm still trying to find out what I would need to do on the switches to support this.  It's possible that the two switches would need to have some sort of interconnects.  Alternately, I may simply have (2) switches installed and bond all (4) Intel NICs together as a single adapter for 400MB/s of bandwidth.  In the remote case that the one switch fails, recovery would involve moving all of the cables to the 2nd switch.

On the disk drives, I would probably need a 12-drive RAID 1+0 array in order to drive those 4 bonded NICs.  Figure that I'm able to write 40MB/s to a single RAID1 array in the unit.  Putting 6 of those RAID1s together in a RAID0 set would give me around 240MB/s.

I could possibly go as high as a 16-drive RAID10 which would put me up around 320MB/s.  Again, it all depends on how good the performance is with a single RAID1 spindle pair.

Looking at my test results from Bonnie, I was only seeing around 15MB/s of performance from 300GB 5400RPM drives.  A naive estimate is that moving to 750GB 7200RPM drives would drive performance up by about 3.3x which would be around 50MB/s.  A more realistic estimate is around 33MB/s but probably as low as 20MB/s.

RAID10 (semi-random performance)
4-spindle: 40-66MB/s
8-spindle: 80-132MB/s
12-spindle: 120-198MB/s
16-spindle: 160-264MB/s

RAID10 (sequential reads/writes)
4-spindle: 120MB/s
8-spindle: 240MB/s
12-spindle: 360MB/s
16-spindle: 480MB/s

Those are big S.W.A.G. estimates.  In reality, performance will probably be closer to the semi-random performance numbers.  Which means that the first set of drives needs to be configured into an 8-spindle RAID10 in order to be viable.  A PCI motherboard would choke on this amount of bandwidth, but the newer PCIe motherboards should be able to handle it.
