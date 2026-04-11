---
layout: post
title: 'Replacing a failed drive in a Software RAID mirror set'
date: '2007-12-21T07:25:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Like I wrote about last time, I have a [failing drive in my triple active RAID mirror set on my firewall box](/techblog/2007/12/failed-drive-slice-in-software-raid.shtml).  See also "[Failing hard drive in a Software RAID](/techblog/2006/06/failing-hard-drive-in-software-raid.shtml)".  I'm still trying to decide whether the disk has actually failed, or if it is just having issues.

<code># /sbin/badblocks -sv /dev/sdc2</code>

Since I have unmounted this RAID slice, I'm going to test with a DESTRUCTIVE write/read verification.  (Which is also a good way to wipe the disk.)

<code># /sbin/badblocks -sv -w -t random /dev/sdc2</code>

Well, after a few runs with that, the disk is no longer making "retry" noises.  So I'm going to re-add the slice to the RAID array and see what happens.

<code># /sbin/mdadm /dev/md1 -a /dev/sdc2</code>

And force mdadm to verify the sync:

<code># echo check &gt; /sys/block/md1/md/sync_action</code>

It seems to be working.  I'm guessing that I finally convinced SMART to re-map the bad sector that was causing problems.
