---
layout: post
title: 'Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 3)'
date: '2005-04-20T19:42:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

([previous step](/techblog/2005/04/gentoo-20043-on-gigabyte-ga-6va7-part_19.shtml))

Time to configure the timezone and setup the kernel, this is [chapter 7 in the Gentoo handbook](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7).

Timezone for me is EST5EDT, so here's how to set that up.

<code># ls /usr/share/zoneinfo
# ln -sf /usr/share/zoneinfo/EST5EDT /etc/localtime
# date
# zdump GMT
# zdump EST5EDT</code>

Last year, I went with development-sources for the kernel in order to get 2.6.  This is no longer necessary (and development-sources has been rolled into vanilla-sources).  So I'm going to go with the default gentoo-sources.

<code># emerge gentoo-sources
# ls -l /usr/src</code>

This takes a while to run (maybe an hour or two).

(next step)<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gigabyte-GA-6VA7%2B.shtml">Gigabyte-GA-6VA7+</a>
		<div class="Byline">
			posted by Thomas at 
			[19:42](http://www.tgharold.com/techblog/2005/04/gentoo-20043-on-gigabyte-ga-6va7-part_20.shtml)

		</div>