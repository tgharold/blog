---
layout: post
title: 'Result code 0x57 when scheduling a backup'
date: '2006-07-28T20:44:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>This was a slightly odd one that did not show up on Google at all.  We had a bunch of backup jobs on our main Windows 2003 file server and had recently promoted the Win2003 server to a domain controller using DCPROMO.EXE.  In the process of doing that, some tasks refused to run and we also had to delete and re-add a lot of tasks.

In the Scheduled Tasks window, we saw a result code of "0x57" in the Last Result column.  In the schedule log (Scheduled Tasks, Advanced, View Log):

<code>"Backup-FileServer-DailyAppend-Week2.job" (ntbackup.exe)
    Finished 7/28/2006 8:30:48 PM
    Result: The task completed with an exit code of (57).</code>

We checked a few things and finally took a very close look at the "Run" field in the task.  Turns out that we were missing a double-quote in the middle of the NTBACKUP command line.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Backups.shtml">Backups</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Win2003.shtml">Win2003</a>
		<div class="Byline">
			posted by Thomas at 
			[20:44](http://www.tgharold.com/techblog/2006/07/result-code-0x57-when-scheduling.shtml)

		</div>