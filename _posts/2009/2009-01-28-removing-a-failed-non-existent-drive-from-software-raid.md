---
layout: post
title: 'Removing a failed, non-existent drive from Software RAID'
date: '2009-01-28T13:04:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>So, you have a drive that has failed, you've replaced the drive on the fly (using hot-swap SATA) and now you need to remove the old RAID slice.

For example:

<pre>md0 : active raid1 sdi1[0] sdc1[2] sdb1[3](F) sda1[1]
      264960 blocks [3/3] [UUU]</pre>

In this case, sdb1 is marked as failed, and sdi1 was the slice from the newly added drive (via SATA hot-plug).  So we want to remove it with mdadm's remove command:

<pre># mdadm /dev/md0 --remove /dev/sdb1
mdadm: cannot find /dev/sdb1: No such file or directory</pre>

Oops, we can't do that because we already swapped out the failed drive (sdb).  

The answer is found in the mdadm man page for the remove feature:

<code>-r, --remove remove  listed devices.  They must not be active.  i.e. they should be failed or spare devices.  As well  as the name of a device file (e.g.  /dev/sda1) the words failed and detached can be given  to  --remove.  The  first causes all failed device to be removed.  The second causes any device which is no longer connected to the system (i.e an open returns ENXIO) to be removed.  This will only  succeed  for  devices that are spares or have already been marked as failed.</code>

So instead of specifying the name of the failed RAID slice we should instead us the following command:

<pre># mdadm /dev/md0 -r detached  
mdadm: hot removed 8:17</pre>

And there you have it, the failed raid slice that is no longer connected to the system has been removed.  It will not show up in "/proc/mdstat" any more.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2009.shtml">2009</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SoftwareRAID.shtml">SoftwareRAID</a>
		<div class="Byline">
			posted by Thomas at 
			[13:04](http://www.tgharold.com/techblog/2009/01/removing-failed-non-existent-drive-from.shtml)

		</div>