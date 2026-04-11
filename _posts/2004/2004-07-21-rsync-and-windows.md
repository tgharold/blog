---
layout: post
title: 'RSync and Windows'
date: '2004-07-21T17:59:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


This is a follow-up to my previous post about [Securing cwRSync](/techblog/2004/06/securing-cwrsync.shtml).  We were using the "[cwRSync package](http://www.itefix.no/)", but when running in server mode it doesn't know how to talk to clients over an SSH-encrypted connection. Which isn't a big deal if you're only talking to other servers on the local network, but is problematic in cases where you have to be wary of eavesdropping (across WiFi links or untrusted networks like the internet). So I've been looking off-and-on over the past month at figuring out how to get an rsync service running using SSH on a Windows server.

 One option is to install the full [Cygwin](http://cygwin.com/) package.  Which is a bit much for a server (or rather, I'm not comfortable installing Cygwin on a server... yet).

 Another option seems to be the [OpenSSH for Windows](http://sshwindows.sourceforge.net/) project at SourceForge.  That doesn't include rsync though, just scp.  So I might look at "[Installing ssh and rsync on a Windows machine: minimalist approach](http://optics.ph.unimelb.edu.au/help/rsync/rsync_pc1.html)" which requires an absolute bare minimum of files to be installed. However, the files at that location are from Jan 2002, which is a bit old and the [latest version as of July 2004 for the Cygwin DLL is cygwin-1.5.10-2](http://cygwin.com/ml/cygwin-announce/2004-05/).
