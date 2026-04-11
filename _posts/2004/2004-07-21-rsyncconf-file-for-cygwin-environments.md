---
layout: post
title: 'rsync.conf file for Cygwin environments'
date: '2004-07-21T20:00:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>You should definitely refer to the [official rsync website](http://rsync.samba.org/) for the real documentation on [configuring the rsyncd.conf file](http://rsync.samba.org/ftp/rsync/rsyncd.conf.html).  

Locate your /etc folder under where you installed Cygwin.  Since I installed Cygwin to C:\bin\cygwin, my /etc folder is C:\bin\cygwin\etc.  For a fresh install, you'll need to create the "rsyncd.conf" file in that folder (C:\bin\cygwin\etc\rsyncd.conf).

(minimal rsyncd.conf file)
<pre>use chroot = false
strict modes = false
log file = rsyncd.log

[test]
path = /cygdrive/d/rsync/test
read only = false
transfer logging = yes</pre>
<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>
		<div class="Byline">
			posted by Thomas at 
			[20:00](http://www.tgharold.com/techblog/2004/07/rsyncconf-file-for-cygwin-environments.shtml)

		</div>