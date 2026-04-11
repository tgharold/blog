---
layout: post
title: 'Gentoo Samba (round 2)'
date: '2004-05-01T04:39:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


([Gentoo samba page](http://www.gentoo.org/doc/en/desktop.xml#doc_chap7), [attempt #1](/techblog/2004/05/gentoo-samba-with-ads.shtml))

Well, rebuilding the kernel didn't really do anything other then teach me how to rebuild the kernel...  I'm still getting the "net: command not found" error when trying to add the box the AD domain.  (And I'm not sure what I missed during the installation.)

I have noticed that "emerge samba" installed the 2.2.8a version of Samba instead of version 3... so now I need to find out how to install v3 on gentoo.  According to [the packages listing for samba](http://packages.gentoo.org/packages/?category=net-fs;name=samba), 3.0.2a-r2 is marked as stable as of Apr 29th.  (Also useful is the [graphical portage browser](http://www.gentoo-portage.com/browse-program.php?program=3323).)

# emerge sync
# emerge --pretend samba

Ah ha!  Now it indicates that it will install net-fs/samba-3.0.2a-r2, but first there's a message that I need to update portage to the latest version.  

# emerge search 'portage'

Shows me that I have 2.0.50-r1 and the latest is 2.0.50.r6 and that the size of the download is 219KB.

# emerge portage
# emerge samba
