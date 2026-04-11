---
layout: post
title: 'Auditing tools for Windows'
date: '2004-06-12T09:46:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
[fsum by SlavaSoft](http://www.slavasoft.com/fsum/) - (free) Creates md5 signature files compatible with the md5sum command line tool (found on most unix/linux distros), but has the additional feature of directory recursion.  The tool also supports other checksum/hash functions.

[DumpSec by SomarSoft](http://www.somarsoft.com/somarsoft_main.htm#DumpAcl) - (free) This tool used to be called DumpACL back in the days of Windows NT 4.0.  It has been re-released to report on the newer ACL information in an Active Directory Domain (Windows 2000), plus it has the option to dump out lists of users, groups, policies, shares, registry ACLs, and a few more goodies.  Output is either an interactive report viewer, a custom save file format, or various report file styles.

[rsync](http://rsync.samba.org/) - (free) While not strictly an auditing tool, rsync is useful for pushing/pulling log files off of a server onto a better protected server for long-term storage.  The primary advantage is that rsync will only send the portions of a file that have changed, reducing transfer traffic.  It also supports compression of the transfer and you can route the information through ssh for security.  The version I use is [cwRSync](http://www.itefix.no/), which is a streamlined version of the Microsoft Windows port that doesn't require the full [Cygwin](http://www.cygwin.com/) application to be installed.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>
		<div class="Byline">
			posted by Thomas at 
			[09:46](http://www.tgharold.com/techblog/2004/06/auditing-tools-for-windows.shtml)

		</div>