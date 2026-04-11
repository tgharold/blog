---
layout: post
title: 'Second Copy 7 vs Samba v3'
date: '2009-08-03T11:26:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>One of the tools that we use on our desktop machines is [Second Copy 7](http://www.centered.com/), which is a very useful tool for doing file-level backups that are user friendly.  It has a mode where it mirrors the source directory tree to the remote location, along with putting older copies of the files in a second remote location.

However, if things are strange, you'll find that Second Copy will end up making repeated copies of files in the "older copies" location every time the profile runs.

The primary problem that causes this is if the Windows desktop's clock does not exactly match the server's clock.  You will see this problem frequently if you use "time.windows.com" as your clock source.  (In Windows XP; Control Panel -&gt; Date and Time -&gt; Internet Time tab.)  The "time.windows.com" clock source is generally horribly inaccurate compared to the time that your Linux boxes running Samba get their time from (usually from the pool.ntp.org servers).

So the solution is either to sync your Windows boxes to a better clock source (such as "us.pool.ntp.org" or an internal NTP time server), or to adjust Second Copy to be much more tolerant of time differences.  SC's default is a 2 sec time difference allowance.  You may wish to increase this to as much as 30 or 60 seconds.  This is a hidden option in the Second Copy profiles.dat file.  

Setting up a Linux box to poll the pool.ntp.org servers and provide time to the internal network is a much preferred solution.  You can also setup Samba to provide time to clients that belong to your domain.

References:

[Q10169 - INFO: How does Second Copy handle file time stamps when copying the files between different file systems?](http://www.secondcopy.com/kb/Article.aspx?id=10169)

Addendum:

- After a bit of playing around with Samba options, I finally gave up and increased the "IgnoreTimeDifference=N" value under [Options] in the "profiles.dat" file from 2 seconds to 15 seconds.  The Windows XP desktop machine, even though it was getting its time from the Linux Samba server, wasn't staying within 2 second variation.  But after loosening up the time to 15 seconds, things are working much better.

- If your Windows boxes are actually joined to the Samba Domain as client machines (only possible with Windows XP Pro, or the pro/business versions of Vista/Win7), then they might keep better synchronization with the Samba server's time.

- I'm pretty sure that the problem was not due to my referencing the backup location using UNC naming (i.e. \\servername\share\path).

- This issue mostly comes into play when you are backing up from one machine to another (such as a share location on another desktop or a server share).  This is not something that you'll normally run into if you're backing up to a drive hooked directly to the machine.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2009.shtml">2009</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/NTP.shtml">NTP</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Samba.shtml">Samba</a>
		<div class="Byline">
			posted by Thomas at 
			[11:26](http://www.tgharold.com/techblog/2009/08/second-copy-7-vs-samba-v3.shtml)

		</div>