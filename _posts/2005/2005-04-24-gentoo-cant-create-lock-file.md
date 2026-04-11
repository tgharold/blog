---
layout: post
title: "Gentoo: Can't create lock file"
date: '2005-04-24T00:10:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Well, first glitch. Looking at my boot screen with [Shift-PgUp] / [Shift-PgDn] to find the error. I see that the Software RAID is working fine (it built md0..md3 automatically).

<code>* Mounting proc at /proc [ ok ]
* Mounting sysfs at /sys [ !! ]
can't create lock file /etc/mtab~944: Read-only file system (use -n flag to override)
* Mounting ramfs at /dev... [ ok ]
* Configuring system to use udev... [ ok ]
*   Populating /dev with device nodes...
*   Using /sbin/hotplug for udev management...
* Mounting devpts at /dev/pts... [ ok ]
* Activating (possible) swap... [ ok ]
* Remounting root filesystem read-only (if necessary)... [ ok ]
* Checking root filesystem...
ext2fs_check_if_mount: No such file or directory while determining whether /dev/md2 is mounted.
fsck.ext3: No such file or directory while trying to open /dev/md2
/dev/md2: The superblock could not be read or does not describe a correct ext2 filesystem. If the device is valid and it really contains an ext2 filesystem (and not swap or ufs or something else), then the superblock is corrupt, and you might try running e2fsck -b 8193 &lt;device&gt;
* Filesystem couldn't be fixed :( [ !! ]

Give root password for maintenance
(or type Control-D for normal startup):</code>

So, according to a quick google, this indicates an issue with /etc/fstab.

I'll be digging into this in a few days when I get a chance.  (See [Troubleshooting 1](http://www.blogger.com/techblog/2005/04/gentoo-troubleshooting-1.shtml).)<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>
		<div class="Byline">
			posted by Thomas at 
			[00:10](http://www.tgharold.com/techblog/2005/04/gentoo-cant-create-lock-file.shtml)

		</div>