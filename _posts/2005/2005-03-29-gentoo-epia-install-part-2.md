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



<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

First up, still using the 2004.0 Gentoo Boot CD and referring to my [old notes from last year](/blog/2004-04-27-gentoo-epia-install-part-1/).  Also note that I rebuilt it in [June 2004](http://www.tgharold.com/techblog/2004_06_01_archive.shtml), so it may be better to look at those notes.  Especially the "gentoo nohotplug" command during the boot process.

Going to use last June's installation notes for the most part, with a few notes here if I change anything.

Key commands (that don't do anything other then report status):

<b>/sbin/ifconfig</b> - verifies networking
<b>ls -l /dev/hd*</b> - shows hard drives
<b>hdparm -i /dev/hda</b> - display information about hda

Now to fire up fdisk and wipe any existing partitions.  Then I'm going to create the same partitions I did last year.  (Helps to refer to the Gentoo handbook for this step.)

Currently making my raid volumes, no changes from the June 2004 instructions.  Verifying progress using "<b>cat /proc/mdstat</b>".
