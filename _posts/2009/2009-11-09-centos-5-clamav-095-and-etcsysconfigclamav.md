---
layout: post
title: 'CentOS 5, ClamAV 0.95 and /etc/sysconfig/clamav'
date: '2009-11-09T09:36:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Trying to configure the new ClamAV 0.95 as a milter for our Postfix install this week.  So I've been doing some digging into the configuration files.  Here's what I've found so far.

In order to get the newer ClamAV for Red Hat Enterprise Linux 5 (RHEL5) and CentOS 5, I had to use the RPMForge repository in order to get the 0.95 version.  

The old clamav-milter package is outdated and should not be installed (use the newer clamav 0.95 or later package).

The /etc/rc.d/init.d/clamav script is still from 2008 and is very old.  It references /etc/sysconfig/clamav which has an outdated setting called "CLAMAV_MILTER=yes".  In ClamAV 0.95+, the milter was rewritten and now uses a configuration file (/etc/clamav-milter.conf) instead of command-line arguments.  The init.d script that manages the clamd daemon is still for the older milter.  It works fine for starting and stopping clamd, but you should not use the "CLAMAV_MILTER=yes" setting in the sysconfig file.

If you were using the /etc/sysconfig/clamav file to turn on the milter in RHEL5, then you will probably see the following error when you upgrade to ClamAV 0.95 or later:

<code>Starting clamav-milter: clamav-milter: unrecognized option `--max-children=10'
ERROR: Unknown option passed
ERROR: Can't parse command line options</code>

You'll need to convert your old command line options into configuration file options.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2009.shtml">2009</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/CentOS5.shtml">CentOS5</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/ClamAV.shtml">ClamAV</a>
		<div class="Byline">
			posted by Thomas at 
			[09:36](http://www.tgharold.com/techblog/2009/11/centos-5-clamav-095-and.shtml)

		</div>