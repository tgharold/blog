---
layout: post
title: 'Securing cwRSync'
date: '2004-06-18T10:18:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>At the office we're working on setting up [cwRSync](http://www.itefix.no/) on the web server array to push the daily web/ftp/smtp log files back to a central point for archiving.  Right now, since all of the web servers are on the same LAN segment at the hosting facility, we're just sending the plain text data across the wire to the rsync port (tcp/873).  Since the previous solution was to use FTP to move the log files around, it's no worse then the old solution from a security standpoint.  (It is, however, much faster and more efficient.)  Security is handled solely thorugh the rsyncd.conf "hosts allow" setting (only the internal IP addresses are allowed to be used to transfer the data) with no passwords or shared keys.

However, since the next step is that we want to setup pulling those log files automatically back to the main office, we need to look into locking it down further and putting encryption in place (e.g. routing rsync traffic over an ssh tunnel). 

After digging around a bit here's what I've found:

The <b>cwRSync Service</b> [does not support SSH](http://www.itefix.no/phpws/index.php?module=faq&amp;FAQ_op=view&amp;FAQ_id=22), so there's no way to connect securely to a rsync server that is using cwRSync as its daemon.  Future releases are expected to add [ssh support for cwRSync servers](http://www.itefix.no/phpws/index.php?module=faq&amp;FAQ_op=view&amp;FAQ_id=26).  Locking down through IP address and username/password is the limit of what you can do for security, all traffic is in the clear (unless you have IPSec between the two machines).

However, you <b>can</b> use cwRSync in a client-configuration and route the traffic over SSH to a SSH-capable rsync server.

That being said, I'm going to explore some other packages.  All of which will either require that cygwin be installed, or at least that certain cygwin DLLs be installed.

Links:

[Rsync wrapper for Win32](http://footboot.net/rsync-win/) - Uses the cygwin DLLs, but doesn't require a full cygwin install, includes SSH.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/RSync.shtml">RSync</a>
		<div class="Byline">
			posted by Thomas at 
			[10:18](http://www.tgharold.com/techblog/2004/06/securing-cwrsync.shtml)

		</div>