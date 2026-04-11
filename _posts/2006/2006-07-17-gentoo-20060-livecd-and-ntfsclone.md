---
layout: post
title: 'Gentoo 2006.0 LiveCD and NTFSClone'
date: '2006-07-17T11:35:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>In the past, I've been using the [Knoppix LiveCD and NTFSClone](/techblog/2005/10/imaging-tecra-8200-windows-2000.shtml) to make snapshot images of Windows workstations.  However, since Knoppix 4.0.2 doesn't auto-detect the ethernet port on the Asus A8N-VM CSM motherboard, I tried out the Gentoo AMD64 2006.0 LiveCD instead.

The big trick with the newer LiveCDs is keeping them from booting into X.  At the <b>boot:</b> prompt you need to enter "<b>gentoo nox</b>" in order to prevent that from happening.  That gives you the normal command line that has root level access to the LiveCD and you can switch between sessions using [Alt-F1] and [Alt-F2].

After that, it's pretty easy to mount a drive and write the image file out to wherever you need it to go.  I typically create a hidden Linux partition at the end of the primary drive using ext3 and write a pair of images to it when I finish the initial build.  I'll also burn one of the images to DVD-R for use in cases where the user manages to wipe out the hidden partition (or the drive dies entirely).<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/NTFSClone.shtml">NTFSClone</a>
		<div class="Byline">
			posted by Thomas at 
			[11:35](http://www.tgharold.com/techblog/2006/07/gentoo-20060-livecd-and-ntfsclone.shtml)

		</div>