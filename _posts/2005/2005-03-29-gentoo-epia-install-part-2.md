---
layout: post
title: 'Gentoo EPIA Install (part 2)'
date: '2005-03-29T13:16:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

First up, still using the 2004.0 Gentoo Boot CD and referring to my [old notes from last year](/techblog/2004/04/gentoo-epia-install-part-1.shtml).  Also note that I rebuilt it in [June 2004](http://www.tgharold.com/techblog/2004_06_01_archive.shtml), so it may be better to look at those notes.  Especially the "gentoo nohotplug" command during the boot process.

Going to use last June's installation notes for the most part, with a few notes here if I change anything.

Key commands (that don't do anything other then report status):

<b>/sbin/ifconfig</b> - verifies networking
<b>ls -l /dev/hd*</b> - shows hard drives
<b>hdparm -i /dev/hda</b> - display information about hda

Now to fire up fdisk and wipe any existing partitions.  Then I'm going to create the same partitions I did last year.  (Helps to refer to the Gentoo handbook for this step.)

Currently making my raid volumes, no changes from the June 2004 instructions.  Verifying progress using "<b>cat /proc/mdstat</b>".<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VIAEPIA.shtml">VIAEPIA</a>
		<div class="Byline">
			posted by Thomas at 
			[13:16](http://www.tgharold.com/techblog/2005/03/gentoo-epia-install-part-2.shtml)

		</div>