---
layout: post
title: 'Gentoo - dcfldd'
date: '2006-01-27T10:40:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
[dcfldd](http://dcfldd.sourceforge.net/)

A fancier version of the basic "dd" command.  The big advantage that I wanted was:

- Status information (useful when wiping large hard drives)

Here's my wipe command.

<code># dcfldd if=/dev/urandom of=/dev/sda conv=notrunc bs=128k</code>

If you're in more of a hurry, try:

<code># dcfldd if=/dev/zero of=/dev/sda conv=notrunc bs=128k</code>

Some slower CPUs can't generate PRNG numbers (/dev/urandom) fast enough to keep up with the disk wipe process.  If you're using "atop" you'll notice that the system is spending 100% of the time in the "sys" (and dcfldd is using up 100% CPU).  In addition, the hard drive lights will not be constantly lit.  Plus the "DSK" line for the drive being wiped will not be busy 100% of the time in "atop".<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>
		<div class="Byline">
			posted by Thomas at 
			[10:40](http://www.tgharold.com/techblog/2006/01/gentoo-dcfldd.shtml)

		</div>