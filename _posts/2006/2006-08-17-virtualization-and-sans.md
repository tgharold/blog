---
layout: post
title: 'Virtualization and SANs'
date: '2006-08-17T21:43:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>One of my next projects at the office is to start migrating us from individual servers with direct attached storage (DAS) to a virtual server running on a storage area network (SAN).

<b>Individual servers with DAS</b>
+ Easy configuration
- A downed server takes services and data offline
+ Cheap
- Inflexible
- Wasted storage space
+ Higher utilization of raw storage capacity (50-90%)

<b>Virtual servers with SAN</b>
- Complexity
- Cost
+ Virtual servers can move from host to host on the fly
+ Data is accessible to a virtual server no matter which host
+ Fault-tolerant
+ Server redundancy
- Lower utilization of raw storage capacity (25%-40%)

For virtualization, you setup a hypervisor layer on the server hardware and all servers run on top of that layer as virtual servers.  With most virtualization setups, this means that a virtual guest server can be moved to other server hardware on-the-fly when needed.  So if you want to take down a host server for maintenance, you can simply move all of the guest O/Ss off to other servers temporarily.

Naturally, this works best if the data for your virtual servers is stored on a SAN rather then on local disks (DAS).  That way, when the server hardware is taken down, it doesn't affect the availability of data.  The downside is that you now have a central point of failure (the SAN) for multiple servers.  So you need to take care and design in redundancy / fault-tolerance / failover.

For the host servers, redundancy is as easy as having multiple host servers connected up to the SAN fabric (so they can talk to their data stores).

For the SAN fabric, redundancy can be done in various ways.  The easiest is to simply have two switches and two network paths between each host server and the SAN units.  There are also more complex topologies (core-edge, full-mesh, etc) but for the small business, a pair of switches will probably provide enough fault-tolerance.

The SAN storage units are the remaining weak link.  It should be possible to RAID together multiple SAN units to provide fault-tolerance.  But that's something that I'm still exploring with regards to iSCSI.  The other downside of RAID'ing multiple SAN units together is that it generally cuts the net storage amount in half.  So if you need N GB of data storage, you need N * 4 GB of raw storage (assuming RAID1 within the SAN and RAID1 across two SAN units).  The upside is that you would have to lose 3 of the 4 disks in a RAID 1+1 setup before you would lose data.

(If you construct your SAN as a 12-disk RAID6 with 83% net storage, a RAID1 of two SAN units would give you 42% net storage instead of only 25%.  Whether performance would be adequate is uncertain.)

...

Now, eventually, we may bring in the big guns such as EMC / IBM / Dell / Whoever.  But we estimate that we can get a multi-terabyte test SAN up and running for around $5000-$10000 using commodity hardware and SATA drives.

If things don't work out, then we will use the commodity hardware for other projects and call in the big guns.

Estimated costs for redundant SAN storage (these are very rough ballpark figures for fully-populated SANs):

$2.00/GB - homegrown
$4.50/GB - pre-built SATA iSCSI solutions
$13.33/GB - pre-built SCSI iSCSI solutions

Costs for half populated SANs are about double those $/GB values.  The SCSI SAN unit can only hold about 2/5 the capacity of the SATA SAN units.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>
		<div class="Byline">
			posted by Thomas at 
			[21:43](http://www.tgharold.com/techblog/2006/08/virtualization-and-sans.shtml)

		</div>