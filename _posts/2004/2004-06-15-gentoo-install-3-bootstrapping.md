---
layout: post
title: 'Gentoo Install 3 (Bootstrapping)'
date: '2004-06-15T20:28:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>([previous post](/techblog/2004/06/gentoo-install-2-via-epia-me6000.shtml))

Time to bootstrap the system (See [moving from stage 1 to stage 2](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=6)).  If you have multiple machines on the network, all with the same version of gcc, now is the when you'll want to [configure your distcc configuration](http://www.gentoo.org/doc/en/distcc.xml).
<pre># cd /usr/portage
# scripts/bootstrap.sh</pre>

This will take a while to run (update: took 8 hours to run).  If the bootstrap script fails, and you're re-using a portage tree (or possibly other files under /opt, /usr, /var, /home, /tmp or /var/tmp), then you may need to clean out the old files.  (Generally not an issue if you're doing a fresh install.)

Once that finishes, run the following command.
<pre># emerge system</pre>

Which will also take a while to run (last time it took around 5.5 hours).  Update: Took around 4.5 hours this time.

([next post](/techblog/2004/06/gentoo-install-4-installing-kernel.shtml))<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VIAEPIA.shtml">VIAEPIA</a>
		<div class="Byline">
			posted by Thomas at 
			[20:28](http://www.tgharold.com/techblog/2004/06/gentoo-install-3-bootstrapping.shtml)

		</div>