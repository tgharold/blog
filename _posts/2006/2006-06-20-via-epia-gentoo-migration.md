---
layout: post
title: 'VIA EPIA Gentoo Migration'
date: '2006-06-20T10:35:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Currently, I was using a VIA EPIA system as my music server, but now I'm thinking about turning it into a smart router for the home office.  This will entail adding a ethernet card to the unit in addition to migrating my hard drives from a pair of 300GB drives to a pair of notebook drives (for less power).  Since I'm using Software RAID, moving from one set of disks to another should be nearly seamless.

The hardware has changed a little bit since my [previous attempt at building the system back in March 2005](/techblog/2005/03/gentoo-epia-install-part-1.shtml), but the BIOS settings are identical.  The current hardware consists of:

(1) VIA EPIA ME6000 (EPIA M series), 600Mhz fanless CPU
(2) 300GB 5400rpm hard drives
(1) DVD-ROM 
(1) Morex Venus 668 Black Case
(1) 1GB PC2100 DIMM

I'm going to replace the two 300GB 3.5" drives with less power-hungry 60GB laptop drives.  The basic process is:
<ol>

<li>Detach the DVD-ROM (which happens to be the master drive on the 2nd cable) and connect the laptop drive.  That will allow me to work with the new drives one at a time while I migrate from the old to the new.

</li>
<li>Copy the boot sector from the old /dev/hda to the new laptop drive: <b>dd if=/dev/hda bs=512 count=1 of=/dev/hdc</b>

</li>
<li>Verify that the first (3) partitions on the new drive are identically sized as the original drive.

</li>
<li>Copy the filesystem from the old drive to the new drive: <b>dd if=/dev/hda1 of=/dev/hdc1</b>

</li>
<li>Install grub on the new disk.

</li>
<li>Shutdown

</li>
<li>Remove the old /dev/hda 300GB drive, move the new laptop drive into place

</li>
<li>Restart the system, verify the Software RAID.  I had to tell mdadm to add the /dev/hda partitions to the arrays: <b>mdadm /dev/md0 -a /dev/hda1</b>

</li>
</ol>

Note: I forgot to install grub on the new disk this last time.  So I need to boot from the LiveCD, chroot into the O/S and re-install grub on the new disks.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VIAEPIA.shtml">VIAEPIA</a>
		<div class="Byline">
			posted by Thomas at 
			[10:35](http://www.tgharold.com/techblog/2006/06/via-epia-gentoo-migration.shtml)

		</div>