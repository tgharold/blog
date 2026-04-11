---
layout: post
title: 'Gentoo Install 4 (Installing the Kernel Sources)'
date: '2004-06-16T10:00:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>([previous post](/techblog/2004/06/gentoo-install-3-bootstrapping.shtml))

Picking up with [7. Configuring the Kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7).  If your system crashes after this point, I do have a few notes jotted down on [how to get back to here without rebuilding everything](/techblog/2004/04/gentoo-epia-install-part-4.shtml).  (Since this is where I screwed up last time and put the machine into an unusable state.)

Timezone for me is EST5EDT, so here's how to set that up.
<pre># ls /usr/share/zoneinfo
# ln -sf /usr/share/zoneinfo/EST5EDT /etc/localtime
# date 06161009
# zdump GMT
# zdump EST5EDT</pre>

Next, [pick your kernel](http://www.gentoo.org/doc/en/gentoo-kernel.xml).  For me, since gentoo-sources, gs-sources (gentoo stable) and vanilla-sources are all still on the 2.4 kernel, I'm going to go with development-sources which is at version 2.6.6 and regardless of the name is actually a rather stable tree.
<pre># emerge -s sources | less
# emerge development-sources</pre>

This will take a while to run.  Last time I think it took somewhere around 2 hours, this time it only took 30-40 minutes.  So my previous estimate was probably a bit off (or it took longer to download last time).

([next step](/techblog/2004/06/gentoo-install-5-manual-kernel.shtml))<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VIAEPIA.shtml">VIAEPIA</a>
		<div class="Byline">
			posted by Thomas at 
			[10:00](http://www.tgharold.com/techblog/2004/06/gentoo-install-4-installing-kernel.shtml)

		</div>