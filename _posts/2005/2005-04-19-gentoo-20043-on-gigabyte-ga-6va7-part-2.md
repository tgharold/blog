---
layout: post
title: 'Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 2)'
date: '2005-04-19T18:58:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>([Continuation of part 1](/techblog/2005/04/gentoo-20043-on-gigabyte-ga-6va7-part.shtml))

<code># ls -l /etc/make.profile</code>

As far as I can tell the 2004.3 already uses the 2.6 kernel, so there's nothing to do here.  I also configured my USE flags in my last post, so that's already done as well.

<code># cd /usr/portage
# scripts/bootstrap.sh</code>

This will take a while to run (I estimate a few hours, maybe even overnight).  Once that finishes, you move from stage2 to stage3.

<code># emerge --emptytree system</code>

Which will also take a few hours.

([next step](/techblog/2005/04/gentoo-20043-on-gigabyte-ga-6va7-part_20.shtml))<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gigabyte-GA-6VA7%2B.shtml">Gigabyte-GA-6VA7+</a>
		<div class="Byline">
			posted by Thomas at 
			[18:58](http://www.tgharold.com/techblog/2005/04/gentoo-20043-on-gigabyte-ga-6va7-part_19.shtml)

		</div>