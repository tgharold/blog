---
layout: post
title: 'Resizing an ext3 partition in an LVM2 volume'
date: '2005-12-12T11:31:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
[Extending a Logical Volume](http://www.netadmintools.com/art366.html)

The basic (3) commands are:

lvextend
e2fsck 
resize2fs

For example, I have /home that is currently a 4GB partition mounted in my vgmirror volume group.  In order to turn /home into a 64GB partition, I need to use the following commands.

<code># pvscan
# lvscan
# umount /home
(if you can't unmount the volume, you may need to boot the LiveCD)
# lvextend -L+60G /dev/vgmirror/home
# e2fsck -f /dev/vgmirror/home
# resize2fs /dev/vgmirror/home
# mount /home</code>

Now, for /home, odds are high that you will have to boot a LiveCD due to the volume being in use.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/ext3.shtml">ext3</a>
		<div class="Byline">
			posted by Thomas at 
			[11:31](http://www.tgharold.com/techblog/2005/12/resizing-ext3-partition-in-lvm2-volume.shtml)

		</div>