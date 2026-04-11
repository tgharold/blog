---
layout: post
title: 'My new preferred disk layout for servers'
date: '2007-03-06T13:26:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>With age comes wisdom?  After working with SoftwareRAID and Linux servers for a while, I've changed my preferred disk system design and layout.

<b>RAID</b>

Under the old system, I was running a (2) disk RAID1 (mirror) with a hot-spare disk setup and ready for action.  But if you're going to have a hot-spare dedicated to the RAID1 array, why not use it as an active array member?  That way, if a disk fails, you still have two good disks.  Unfortunately, when a RAID element fails, the load from the rebuild process can often kill the one of the remaining disks in the array.

Is it a likely scenario?  Probably not.  But Linux's Software RAID handles a triple-active RAID1 mirror without any slowdown, so there's not much reason *not* to implement it that way.  Plus it's a useful trick to know for situations where you really *do* need to be that paranoid.

(I'm not sure whether any hardware RAID cards provide for a triple-active mirroring RAID1 configuration.)

<b>Partitions</b>

I've also simplified how many partitions I like to have on the disk.  My current disk layouts typically look like:

/dev/sdX1 - /dev/md0 - 250MB - /boot
/dev/sdX2 - /dev/md1 - 12GB - / (primary root)
/dev/sdX3 - /dev/md2 - 12GB - / (backup root)
/dev/sdX5 - /dev/md3 - 32GB - /var/log
/dev/sdX6 - /dev/md4 - 2GB - swap
/dev/sdX7 - /dev/md5 - 64GB - /backup/system
/dev/sdX8 - /dev/md6 - (remainder) - LVM area

During normal operations, we boot and run /dev/md1 as our / (root) partition.  The /dev/md2 partition is kept offline and is never mounted.  Periodically, after validating that the server is in good health, we will copy the contents of /dev/md1 to /dev/md2, make adjustments to /etc/fstab and the hostname.  This requires some server downtime (long enough to setup the 2nd root partition).

In the case where the primary OS is hosed, we can boot from the backup OS partition and get back up and running quickly.  That gives us the luxury to continue operations until we can schedule downtime to fix the primary OS partition.

Notice that I've broken /var/log out to its own partition.  I do this so that an overflowing set of logs won't take the server box down.  Plus, by putting the log files in their own physical partition, it's easy to use a boot CD or USB key to gain access to the logs in case of severe issues.

The other physical partition that I consider necessary is /backup/system.  This partition is used to hold images of the boot and root partitions, along with information about the partition layout and images of the MBRs.  Basically, it's used to store disaster recovery backups.  You should not have this partition mounted during normal operations.  Taking the contents of this partition offsite is also a good idea.  A basic text file of how the backups were created along with information for how to restore these backups is recommended.

<b>Summary</b>

This setup tries to walk the fine line between keeping it simple, but having enough flexibility to deal with a large set of potential failures.  Anything from a two-disk failure, to the primary OS being hosed, to both OS partitions having problems all the way up to boot records or the /boot partition being killed.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2007.shtml">2007</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/DisasterRecovery.shtml">DisasterRecovery</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Linux.shtml">Linux</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SoftwareRAID.shtml">SoftwareRAID</a>
		<div class="Byline">
			posted by Thomas at 
			[13:26](http://www.tgharold.com/techblog/2007/03/my-new-preferred-disk-layout-for.shtml)

		</div>