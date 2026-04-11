---
layout: post
title: 'Success at fixing sluggishness'
date: '2005-11-21T23:54:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Hah, I finally flipped the right bit on my AMD64 Gentoo server to eliminate the issue with sluggishness while mdadm is rebuilding a RAID array.  So, without further ado, here is my current .config file for a 2.6.13 kernel along with the diff between the last unsuccessful kernel and the kernel that worked.

[KernelConfig-1122-0030.txt](/techblog/Gentoo/AMD64/KernelConfig-1122-0030.txt)

[KernelConfig-1122-0030-diff.txt](/techblog/Gentoo/AMD64/KernelConfig-1122-0030-diff.txt)

I changed close to a dozen flags when I built the last kernel.  One (or more) of them was key in getting rid of the sluggishness.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>
		<div class="Byline">
			posted by Thomas at 
			[23:54](http://www.tgharold.com/techblog/2005/11/success-at-fixing-sluggishness.shtml)

		</div>