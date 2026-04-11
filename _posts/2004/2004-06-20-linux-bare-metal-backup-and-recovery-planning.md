---
layout: post
title: 'Linux Bare-Metal Backup and Recovery Planning'
date: '2004-06-20T01:06:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>The whole concept behind bare-metal restore is that it's the shortest point from pulling a replacement set of server hardware out of a box to having a working system to replace the one that's down.  Ideally, without having to go through re-installing the operating system (which, in the case of Gentoo, can take a few hours).  It also (generally) only works when you have exactly the same hardware in the replacement box as the box that's kaput.  So if you're using any exotic hardware (e.g. a fancy RAID card), you'd best buy (3).  That way when the first one dies, you can put in one of the (2) spare cards and still get at your data.

Some backup software makes the process as simple as dropping a boot CD in the drive and inserting the most recent bare-metal backup (sometimes called a "gold" tape?) tape.  It can also be a multi-step process, where the first step restores the operating system to a known state and the second step handles restoring the data and applications.

Since I'm not ready to tackle writing a guide, I'll settle for a few links:

[Linux Complete Backup and Recovery HOWTO](http://www.tldp.org/HOWTO/Linux-Complete-Backup-and-Recovery-HOWTO/) (by Charles Curley) - A very good starting point.

[Linux Journal: Bare Metal Recovery, Revisited](http://www.linuxjournal.com/article.php?sid=5484) (by Charles Curley, Aug 2002) - A good sidebar discussion of the HOWTO document that he wrote.

[About.com: Linux backup](http://linux.about.com/od/softbackup/) - A collection of links to backup software.

[Unix SysAdm Resources: Backup &amp; Archival Software for Unix](http://www.stokely.com/unix.sysadm.resources/backup.html) (Stokely Consulting) - Listing of backup software for unix.

[Linux Backups Mini-FAQ](http://kmself.home.netcom.com/Linux/FAQs/backups.html) (Karsten M. Self) - Good article on simply using "tar".<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/DisasterRecovery.shtml">DisasterRecovery</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Linux.shtml">Linux</a>
		<div class="Byline">
			posted by Thomas at 
			[01:06](http://www.tgharold.com/techblog/2004/06/linux-bare-metal-backup-and-recovery.shtml)

		</div>