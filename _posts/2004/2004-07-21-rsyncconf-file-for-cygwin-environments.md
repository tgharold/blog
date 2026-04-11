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


You should definitely refer to the [official rsync website](http://rsync.samba.org/) for the real documentation on [configuring the rsyncd.conf file](http://rsync.samba.org/ftp/rsync/rsyncd.conf.html).  

Locate your /etc folder under where you installed Cygwin.  Since I installed Cygwin to C:\bin\cygwin, my /etc folder is C:\bin\cygwin\etc.  For a fresh install, you'll need to create the "rsyncd.conf" file in that folder (C:\bin\cygwin\etc\rsyncd.conf).

(minimal rsyncd.conf file)
<pre>use chroot = false
strict modes = false
log file = rsyncd.log

[test]
path = /cygdrive/d/rsync/test
read only = false
transfer logging = yes</pre>
