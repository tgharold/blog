---
layout: post
title: 'Gentoo EPIA Install (part 3)'
date: '2004-04-28T08:55:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>([Previous blog entry](/techblog/2004/04/gentoo-epia-install-part-2.shtml))

While I'm not exactly sure when the first phase finished overnight, it was probably around 8-12 hours.  I don't see any errors on the screen, so I'm assuming that I'm good to go for the [next step](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=6) in the handbook (chapter 6d).

One of the things I"m not sure about at this stage in the game is how to set the root password or what would happen if a reboot would occur.  Poking around on the hard drive failed to turn up the passwd command, although I can see that the root account has already been assigned a password in the shadow password file.   I'm guessing that I'd boot the LiveCD again, skip to the part where I chroot from the CD to the hard disk (after mounting all of my volumes by hand), then pickup whereever I left off.

Anyway, not much to this step, and it's another one that takes a while to run:

emerge system

Back in a few... ([next entry](/techblog/2004/04/gentoo-epia-install-part-4.shtml)).<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VIAEPIA.shtml">VIAEPIA</a>
		<div class="Byline">
			posted by Thomas at 
			[08:55](http://www.tgharold.com/techblog/2004/04/gentoo-epia-install-part-3.shtml)

		</div>