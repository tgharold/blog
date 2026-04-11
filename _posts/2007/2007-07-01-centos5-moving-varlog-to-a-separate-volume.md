---
layout: post
title: 'CentOS5: Moving /var/log to a separate volume'
date: '2007-07-01T20:21:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>One thing I like to do is put /var/log on its own volume.  That keeps the root volume from overflowing and also gets the log files out of the way.  However, in CentOS5 (and probably RHEL5), SELinux is probably going to complain unless we tell it to "fixup" the new filesystem.
<ol>

<li>Create the filesystem (I use ext3, so # /sbin/mke2fs -j /dev/mdX)

</li>
<li>Mount it at a temporary location: <b># mkdir /mnt/log ; mount /dev/mdX /mnt/log</b>

</li>
<li>Copy the contents: <b># cp -a /var/log/* /mnt/log/</b>

</li>
<li>It may be necessary to "fixup" the new volume: <b># cd /mnt/log ; /sbin/restorecon -R *</b>

</li>
<li>Edit the /etc/fstab file to mount the new volume at /var/log

</li>
<li>Reboot

</li>
</ol>

AFAIK, that's the extent of what's needed.  Looking at the directory listings using "ls -lZ" seems to show the correct SELinux flags on the files between the two different directories.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2007.shtml">2007</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/CentOS5.shtml">CentOS5</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SELinux.shtml">SELinux</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/ServerAdministration.shtml">ServerAdministration</a>
		<div class="Byline">
			posted by Thomas at 
			[20:21](http://www.tgharold.com/techblog/2007/07/centos5-moving-varlog-to-separate.shtml)

		</div>