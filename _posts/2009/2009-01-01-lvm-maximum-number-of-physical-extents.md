---
layout: post
title: 'LVM Maximum number of Physical Extents'
date: '2009-01-01T23:40:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Working on a 15-disk system (750GB SATA drives) so this issue came up again:

What is the maximum number of physical extents in LVM?

The answer is that there's no limit on the number of PEs within a Physical Volume (PV) or Volume Group (VG).  The limitation is, instead, the maximum number of PEs that can be formed into a Logical Volume (LV).  So a 32MB PE size allows for LVs up to 2TB in size.

Note: Older LVM implementations  may only allow a maximum of 65k PEs across the entire PV.  The VG can be composed of multiple PVs however.

So if you want to be safe, make your PE size large enough that you only end up with less then 65k PEs.  Just remember that <b>all PVs within a VG need to use the same PE size</b>.  So if you're planning for lots of expansion down the road, with very large PVs to be added later, you may wish to bump up your PE size by a factor of 4 or 8.

A good example of this is a Linux box using Software RAID across multiple 250GB disks.  The plan down the road is to replace those disks with larger models, create new Software RAID arrays across the extended areas on the larger disks, then extend VGs across new PVs.  At the start, you might only have a net space (let's say RAID6, 2 hot-spares, 15 total disks) of around 2.4TB.  That's small enough that a safe PE size might be 64MB (about 39,000 PEs).

Except that down the road, disks are getting much larger (1.5TB drives are now easily obtainable).  So if we had stuck with a 64MB PE size, our individual LVs could be no larger then 4TB.  If we were to put in 2TB disks (net space of about 20TB), the number of PEs would end up growing by about 8x (312,000).  We might even see 4TB drives in a 3.5" size, which would be closer to 40TB of net space.

A PE size of 256MB might have served us better when we setup that original PV area.  It would allow individual LVs sized up to 16TB.  The only downside is that you won't want to create LVs smaller then 256MB and you'll want to make sure all LVs are multiples of 256MB.

Bottom line, when setting up your PE sizes, plan for a 4x or 8x growth.

References:

[LVM Manpage](http://www.fifi.org/cgi-bin/man2html/usr/share/man/man8/lvm.8lvm-10.gz) - Talks about the limit in IA32.
[Maximum Size Of A Logical Volume In LVM](http://www.walkernews.net/2007/07/02/maximum-size-of-a-logical-volume-in-lvm/) - Walker News (blog entry)
[Manage Linux Storage with LVM and Smartctl](http://www.enterprisenetworkingplanet.com/nethub/article.php/3733141) - Enterprise Networking Planet
