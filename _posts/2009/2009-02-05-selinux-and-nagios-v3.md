---
layout: post
title: 'SELinux and Nagios v3'
date: '2009-02-05T08:10:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
<b>Note: This post was never finished... so it probably contains lots of errors and incorrect information, with one or two grains of useful information.</b>

Now that Nagios has upgraded to v3, I'm going to revisit my SELinux configuration for it.  Back when I first started I was somewhat clueless about SELinux (and still greatly so) and I created a lot of really bad policy modules.  They were a brute-force approach to fixing the issue using only audit2allow and ignoring labeling issues in the underlying filesystem.

(See my older piece "[SELinux - troubleshooting file labeling issues](/techblog/2009/02/selinux-troubleshooting-file-labeling.shtml)".)

First off, let's use <b>semodule</b> to take a look at what modules are loaded:

<code># semodule -l | grep "nagios"
nagios  1.1.0
nagios20080426  1.0
nagios20080522  1.0
nagios20080725  1.0</code>

What you see here is the base nagios module as provided by RedHat/CentOS (nagios 1.1.0) along with three modules that I created using audit2allow.  The contents of those modules are pretty immaterial, so I'm going to remove them and recreate the exceptions from scratch.

<code># semodule -r nagios20080426
# semodule -r nagios20080522
# semodule -r nagios20080725</code>

Now, if I were to startup Nagios right now, it would throw a lot of errors because I have SELinux set to Enforcing mode at the moment.  So what we're going to do is <i>temporarily</i> put SELinux in "permissive" mode instead of "enforcing" mode.  This will cause SELinux to log AVC denial messages to /var/log/audit/audit.log where we can look at them and use audit2allow to create a better exception policy.

<code># getenforce
Enforcing
# setenforce Permissive
# getenforce
Permissive</code>

Now we can startup Nagios, taking careful note of the time.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2009.shtml">2009</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Nagios.shtml">Nagios</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SELinux.shtml">SELinux</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SystemAdministration.shtml">SystemAdministration</a>
		<div class="Byline">
			posted by Thomas at 
			[08:10](http://www.tgharold.com/techblog/2009/02/selinux-and-nagios-v3.shtml)

		</div>