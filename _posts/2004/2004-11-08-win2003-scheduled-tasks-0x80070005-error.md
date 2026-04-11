---
layout: post
title: 'Win2003 Scheduled Tasks 0x80070005 Error'
date: '2004-11-08T10:49:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Trying to setup a backup job (kicked off by a .cmd file) on Windows 2003.  I have a special, limited rights, user account created (rather then running the backup job under the administrator account).  Everything seems fine until I go to test my scheduled task.

Looking at the log (Scheduled Tasks - Advanced - View Log) will show: 

<code>Unable to start task.
The specific error is:
0x80070005: Access is denied.</code>

["Access is denied" error message when you run a batch job on a Windows Server 2003-based computer](http://support.microsoft.com/?kbid=867466)

As expected, this is a permissions error.  Specifically, you need to grant permissions for batch processes to use "cmd.exe".<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>
		<div class="Byline">
			posted by Thomas at 
			[10:49](http://www.tgharold.com/techblog/2004/11/win2003-scheduled-tasks-0x80070005.shtml)

		</div>