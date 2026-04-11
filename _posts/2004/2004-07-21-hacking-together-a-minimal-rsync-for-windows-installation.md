---
layout: post
title: 'Hacking together a minimal rsync for windows installation'
date: '2004-07-21T18:53:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Based on what I've read elsewhere (links in my [previous posting](/techblog/2004/06/rsync-and-windows.shtml)), I think I can pull the relevant pieces out of the [Cygwin package](http://cygwin.com/mirrors.html).  I'll try to keep good notes as to what worked and what didn't, but let me know if you find any errors.  [Rsync wrapper for Win32](http://footboot.net/rsync-win/) seems to be a good starting point for which DLLs and files I'll need to pull out of the standard Cygwin release.

You can download the files off of any of the [Cygwin public mirrors](http://cygwin.com/mirrors.html).  Grab the following  archives and extract them to a temporary directory on your machine.  

release/cygwin/cygwin-1.5.10-3.tar.bz2
- contains the DLL file (usr/bin/cygwin1.dll) and a lot of base utilities

release/popt/libpopt0/libpopt0-1.6.4-4.tar.bz2
- contains the usb/bin/cygpopt-0.dll file

release/rsync/rsync-2.6.2-1.tar.bz2
- RSync (rsync executable)

Create a folder where you're going to store the rsync files (I use C:\bin\rsync).

Copy the following files to your rsync folder:
<pre>cygwin1.dll
cygpopt-0.dll
rsync.exe</pre>

[Create your rsync.conf file](/techblog/2004/07/rsyncconf-file-for-cygwin-environments.shtml) and put it in your rsync folder.

Test out whether you've gotten rsync working (thanks to "[Aaron Johnson's page about rsync](http://www.cephas.net/blog/archives/000294.html)" for showing me what command line options to use).  To do this, type the following commands:
<pre>c:
cd \bin\rsync
rsync --config="c:\bin\rsync\rsyncd.conf" --daemon</pre>
If you have a log file, there should now be an entry indicating that rsync has started up and is listening on the default port (tcp/873).  Looking at the processes in Windows Task Manager, you should see the "rsync.exe" process.  You should also now test out some rsync transfers from another workstation to verify that your security settings and module settings are correct.

To do:
- create the user account to use for the rsync service
- setup rsync to run as a service (need the SRVANY.EXE file, I think)
- figure out how to get rsync talking through an SSHD server<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/RSync.shtml">RSync</a>
		<div class="Byline">
			posted by Thomas at 
			[18:53](http://www.tgharold.com/techblog/2004/07/hacking-together-minimal-rsync-for.shtml)

		</div>