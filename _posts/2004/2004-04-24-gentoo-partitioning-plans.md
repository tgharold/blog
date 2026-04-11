---
layout: post
title: 'Gentoo Partitioning Plans'
date: '2004-04-24T02:49:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
[ [gentoo-user] Help with new system](http://groups.google.com/groups?hl=en&amp;lr=&amp;ie=UTF-8&amp;oe=UTF-8&amp;c2coff=1&amp;selm=16ucP-pC-7%40gated-at.bofh.it) (discusses partition sizes)

Possible partitions:

/boot ext2 64MB 
- [handbook](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=4) says 32MB
- [needs to be a primary partition](http://www.linuxforum.com/linux-partition/partition-4.html), type "linux native"
- can be mounted read-only

(swap)  512MB / 1GB / 2GB
- some places say 2x physical memory, others say twice what you think you use
- I'm probably going to go with 2GB and put it on the root of the 2nd drive

/ (root) ext3
- 1GB?, [should only hold selected trees](http://www.linuxquestions.org/questions/history/149602) such as /etc, /dev, /proc, /root, /bin, /sbin, /lib

(rootmirror)  ext3 
- a mirror of the root partition, typically not mounted, same size as /

Note: /home, /opt, /usr, and /var can be [handled with LVM](http://www.gentoo.org/doc/en/lvm2.xml).  The LVM doc suggests /usr (10GB), /home (5GB), /opt (5GB), /var (10GB), /tmp (2GB).

/home ext3
- user files, I'll probably go with a default of 5GB as any really large files (e.g. Samba shares or multi-media files) I'll stick in a seperate partition and symlink
- /home will probably end up in a seperate partition by itself, along with the multi-media storage so that I can handle that with regular backups

/opt ext3
- game servers store a bit of stuff here, I don't expect my /opt to use much, so 2GB in LVM

/tmp ext2
- same issues as /var/tmp (not sure if gentoo uses /tmp), probably

/usr ext3
- possibly mounted read-only?  suggestions indicate 2-3GB

/usr/portage
- source-code, 6-8GB

/var ext3
- mail servers store mail queues here (/var/mail?), print spools also end up under /var (/var/spool?)

/var/log ext3? 3GB
- log files, good to have in seperate partition so they don't fill the server

/var/tmp ext2 8GB
- temp files, can get away with less space if /var/tmp/portage is in a seperate location (maybe only 1-4GB)
- probably put this on the 2nd drive in the system

/var/tmp/portage ext2 or ext3 5GB
- this is where gentoo compiles, I've seen statements that 5GB is not unreasonable, good candidate for putting on the 2nd drive in the system

Decisions (probably how I'll allocate it):

DISK 1:
/boot ext2 64MB
/ (root) ext3 2GB
LVM #1 24GB
/opt 2GB
/usr 4GB
/var 4GB
LVM #2 (rest of disk)
/home

DISK 2:
(swap) 2GB
/tmp ext2 4GB
/var/tmp ext2 8GB
(root mirror) 2GB
(backup partition)<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>
		<div class="Byline">
			posted by Thomas at 
			[02:49](http://www.tgharold.com/techblog/2004/04/gentoo-partitioning-plans.shtml)

		</div>