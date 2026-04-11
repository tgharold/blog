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


Like I wrote about last time, I have a [failing drive in my triple active RAID mirror set on my firewall box](/blog/2007-12-05-failed-drive-slice-in-a-software-raid-after-resync/).  See also "[Failing hard drive in a Software RAID](/blog/2006-06-11-failing-hard-drive-in-a-software-raid/)".  I'm still trying to decide whether the disk has actually failed, or if it is just having issues.

```
# /sbin/badblocks -sv /dev/sdc2
```

Since I have unmounted this RAID slice, I'm going to test with a DESTRUCTIVE write/read verification.  (Which is also a good way to wipe the disk.)

```
# /sbin/badblocks -sv -w -t random /dev/sdc2
```

Well, after a few runs with that, the disk is no longer making "retry" noises.  So I'm going to re-add the slice to the RAID array and see what happens.

```
# /sbin/mdadm /dev/md1 -a /dev/sdc2
```

And force mdadm to verify the sync:

```
# echo check > /sys/block/md1/md/sync_action
```

It seems to be working.  I'm guessing that I finally convinced SMART to re-map the bad sector that was causing problems.
